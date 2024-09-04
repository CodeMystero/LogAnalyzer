using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using WrapperPacketAnalyzer;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Reflection;
using System.IO;
using WrapperLogger;

namespace CustomWireshark
{
    public partial class FormMain : Form
    {
       
        WorkerThreadStep _workerThreadStep = WorkerThreadStep.StepWait;

        delegate void updatePackeListDelegate();
        updatePackeListDelegate _delegateUpdatePacketList = null;

        static int MAX_BUFFERS = 1000;
        System.Collections.ArrayList _packetsForBackup = new System.Collections.ArrayList(MAX_BUFFERS);
        System.Collections.ArrayList _packetsForFiltered = new System.Collections.ArrayList(MAX_BUFFERS);
        System.Collections.ArrayList _packetsForDataGrid = new System.Collections.ArrayList(MAX_BUFFERS);
        BlockingCollection<PacketAnalyzerWrapper.PacketDataWrapper> _packetList =
            new BlockingCollection<PacketAnalyzerWrapper.PacketDataWrapper>(MAX_BUFFERS);

        int rowInEdit = -1;
        DataGridPacket customerInEdit = null;
        LoggerEx _logger = new LoggerEx();

        bool _isRunThread = false;
        bool _isPacketFiltered = false;
        Thread _thread = null;
        System.Timers.Timer _autoResetTimer = new System.Timers.Timer();
        EventWaitHandle _updateHandle = new EventWaitHandle(false, EventResetMode.AutoReset);

        PacketAnalyzerWrapper _capture = new PacketAnalyzerWrapper();

        string _filterSrcIPv4 = string.Empty;
        string _filterSrcPort = string.Empty;
        string _filterDstPort = string.Empty;

        SystemSettings _systemSetting = new SystemSettings();
        public FormMain()
        {
            InitializeComponent();

            try
            {
                var dateTime = Get_BuildDateTime(System.Reflection.Assembly.GetExecutingAssembly().GetName().Version);
                this.Text = $"Packet Analyzer {dateTime.Year}.{dateTime.Month}.{dateTime.Day}.{System.Reflection.Assembly.GetExecutingAssembly().GetName().Version.Revision}";

                updateDeviceList();

                initializeDataGrid();

                initializeSystemFile();

                initializeLogger();

                _delegateUpdatePacketList = new updatePackeListDelegate(updateDataGridView);

                updateCaptureLogInfo();

                _logger.AddBuffer(LoggerEx.Level.Debug, "[프로그램] 실행");

                _autoResetTimer.Interval = 100;
                _autoResetTimer.Elapsed += new System.Timers.ElapsedEventHandler(OnTick_AutoReset);
                _autoResetTimer.Start();

                beginThread();
            }
            catch (Exception exc)
            {
                MessageBox.Show(exc.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
            }
        }

        public System.DateTime Get_BuildDateTime(System.Version version = null)
        {
            // 주.부.빌드.수정
            // 주 버전    Major Number
            // 부 버전    Minor Number
            // 빌드 번호  Build Number
            // 수정 버전  Revision NUmber

            //매개 변수가 존재할 경우
            if (version == null)
                version = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version;

            //세번째 값(Build Number)은 2000년 1월 1일부터
            //Build된 날짜까지의 총 일(Days) 수 이다.
            int day = version.Build;
            System.DateTime dtBuild = (new System.DateTime(2000, 1, 1)).AddDays(day);

            //네번째 값(Revision NUmber)은 자정으로부터 Build된
            //시간까지의 지나간 초(Second) 값 이다.
            int intSeconds = version.Revision;
            intSeconds = intSeconds * 2;
            dtBuild = dtBuild.AddSeconds(intSeconds);


            //시차 보정
            System.Globalization.DaylightTime daylingTime = System.TimeZone.CurrentTimeZone
                    .GetDaylightChanges(dtBuild.Year);
            if (System.TimeZone.IsDaylightSavingTime(dtBuild, daylingTime))
                dtBuild = dtBuild.Add(daylingTime.Delta);

            return dtBuild;
        }

        private void initializeDataGrid()
        {
            DataGridViewTextBoxColumn column1 = new DataGridViewTextBoxColumn();
            column1.HeaderText = "No.";
            column1.Name = "No.";
            column1.Width = 70;

            DataGridViewTextBoxColumn column2 = new DataGridViewTextBoxColumn();
            column2.HeaderText = "Time";
            column2.Name = "Time";
            column2.Width = 170;

            DataGridViewTextBoxColumn column3 = new DataGridViewTextBoxColumn();
            column3.HeaderText = "SrcIPv4";
            column3.Name = "SrcIPv4";
            column3.Width = 80;

            DataGridViewTextBoxColumn column4 = new DataGridViewTextBoxColumn();
            column4.HeaderText = "DstIPv4";
            column4.Name = "DstIPv4";
            column4.Width = 80;

            DataGridViewTextBoxColumn column5 = new DataGridViewTextBoxColumn();
            column5.HeaderText = "Protocol";
            column5.Name = "Protocol";

            DataGridViewTextBoxColumn column6 = new DataGridViewTextBoxColumn();
            column6.HeaderText = "TCP";
            column6.Name = "TCP";
            column6.Width = 50;

            DataGridViewTextBoxColumn column7 = new DataGridViewTextBoxColumn();
            column7.HeaderText = "UDP";
            column7.Name = "UDP";
            column7.Width = 50;

            DataGridViewTextBoxColumn column8 = new DataGridViewTextBoxColumn();
            column8.HeaderText = "Length";
            column8.Name = "Length";
            column8.Width = 50;

            DataGridViewTextBoxColumn column9 = new DataGridViewTextBoxColumn();
            column9.HeaderText = "Message";
            column9.Name = "Message";
            column9.Width = 480;

            gridPacket.Columns.Add(column1);
            gridPacket.Columns.Add(column2);
            gridPacket.Columns.Add(column3);
            gridPacket.Columns.Add(column4);
            gridPacket.Columns.Add(column5);
            gridPacket.Columns.Add(column6);
            gridPacket.Columns.Add(column7);
            gridPacket.Columns.Add(column8);
            gridPacket.Columns.Add(column9);

            gridPacket.VirtualMode = true;
            gridPacket.RowCount = MAX_BUFFERS;
            gridPacket.ReadOnly = true;
            gridPacket.AllowUserToAddRows = false;
            gridPacket.AllowUserToDeleteRows = false;
            gridPacket.AllowUserToOrderColumns = false;
            gridPacket.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.None;
            gridPacket.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.None;
            gridPacket.MultiSelect = false;
            gridPacket.SelectionMode = DataGridViewSelectionMode.FullRowSelect;

            typeof(DataGridView).InvokeMember("DoubleBuffered", BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.SetProperty, null, gridPacket, new object[] { true });
        }

        private void initializeSystemFile()
        {
            string filePath = System.Windows.Forms.Application.StartupPath + @"\system.xml";
            FileInfo fi = new FileInfo(filePath);
            XmlEx xml = new XmlEx();
            if (fi.Exists == false)
            {
                xml.Create(filePath, "system");
                xml.CreateNode("system", "settings", null);
                xml.CreateNode(@"/system/settings", "enableSaveLog", "true");
                xml.CreateNode(@"/system/settings", "savePathLog", Environment.GetFolderPath(Environment.SpecialFolder.Desktop));
                xml.CreateNode(@"/system/settings", "logLevel", "Debug");
                xml.CreateNode(@"/system/settings", "savePathDump", Environment.GetFolderPath(Environment.SpecialFolder.Desktop));
                xml.CreateNode(@"/system/settings", "fileNameDump", "dump");
                xml.Save();
            }
            
            xml.Open(filePath);
            string value = "";
            xml.GetNodeValue(@"/system/settings", "enableSaveLog", out value);

            bool enable = false;
            Boolean.TryParse(value, out enable);
            _systemSetting.enableSaveLog = enable;

            xml.GetNodeValue(@"/system/settings", "savePathLog", out value);
            DirectoryInfo di = new DirectoryInfo(value);
            if (di.Exists == false)
                value = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);

            _systemSetting.savePathLog = value;

            xml.GetNodeValue(@"/system/settings", "logLevel", out value);
            _systemSetting.logLevel = value;

            xml.GetNodeValue(@"/system/settings", "savePathDump", out value);
            di = new DirectoryInfo(value);
            if (di.Exists == false)
                value = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);

            _systemSetting.savePathDump = value;

            xml.GetNodeValue(@"/system/settings", "fileNameDump", out value);
            _systemSetting.fileNameDump = value;
        }

        private void initializeLogger()
        {
            _logger.SetSavePath(_systemSetting.savePathLog);

            if (_systemSetting.logLevel == "Error")
            {
                _logger.SetMinimumLevel(LoggerEx.Level.Error);
            }
            else if (_systemSetting.logLevel == "Warn")
            {
                _logger.SetMinimumLevel(LoggerEx.Level.Warn);
            }
            else if (_systemSetting.logLevel == "Debug")
            {
                _logger.SetMinimumLevel(LoggerEx.Level.Debug);
            }
            else if (_systemSetting.logLevel == "Info")
            {
                _logger.SetMinimumLevel(LoggerEx.Level.Info);
            }
        }

        private void updateCaptureLogInfo()
        {
            _capture.SetSaveLogPath(_systemSetting.savePathLog);
            if (_systemSetting.logLevel == "Error")
            {
                _capture.SetLogLevel(PacketAnalyzerWrapper.LevelWrapper.Error);
            }
            else if (_systemSetting.logLevel == "Warn")
            {
                _capture.SetLogLevel(PacketAnalyzerWrapper.LevelWrapper.Warn);
            }
            else if (_systemSetting.logLevel == "Debug")
            {
                _capture.SetLogLevel(PacketAnalyzerWrapper.LevelWrapper.Debug);
            }
            else if (_systemSetting.logLevel == "Info")
            {
                _capture.SetLogLevel(PacketAnalyzerWrapper.LevelWrapper.Info);
            }
        }

        private void FormMain_FormClosed(object sender, FormClosedEventArgs e)
        {

            _logger.AddBuffer(LoggerEx.Level.Debug, "[프로그램] 종료");
            
            _autoResetTimer.Stop();

            if (_capture != null)
            {
                if (_capture.IsOpened == true && _capture.IsCaptured == true)
                    _capture.StopCapture();
            }
                
            terminateThread();

            if (_capture != null)
            {
                if (_capture.IsOpened == true)
                    _capture.Close();  
                //GLogger(0, "Capture 객체 해제");
            }

            //_logger.Close();
            //EventWaitHandle handle = new EventWaitHandle(false, EventResetMode.AutoReset);
            //handle.SafeWaitHandle = new Microsoft.Win32.SafeHandles.SafeWaitHandle(_logger.handleTerminate, true);
            //handle.WaitOne();
        }

        private void updateDeviceList()
        {
            var list = PacketAnalyzerWrapper.GetDevices();
            foreach (var dev in list)
            {
                string name = $"[{dev.index}] ({dev.ipv4}) {dev.name}";
                ltbDeviceList.Items.Add(name);
            }
        }

        #region Button 이벤트
        private void btnOpen_Click(object sender, EventArgs e)
        {
            try
            {
                int pos = ltbDeviceList.SelectedIndex;
                if (pos == -1) return;

                bool ret = false;
                ret = _capture.Open(pos, chkPromiscuousMode.Checked);

                if (ret == false)
                    MessageBox.Show("Failed to open device.", "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);

                _packetsForBackup.Clear();

                btnOpen.Enabled = false;
                btnClose.Enabled = true;
                btnCaptureStart.Enabled = true;
                btnCaptureStop.Enabled = false;
                ltbDeviceList.Enabled = false;
                btnDumpStart.Enabled = true;
                chkPromiscuousMode.Enabled = false;
            }
            catch (Exception exc)
            {
                MessageBox.Show(exc.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
            }
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            try
            {
                if (_capture.Close() == false)
                    MessageBox.Show("Failed to close device.", "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);

                btnOpen.Enabled = true;
                btnClose.Enabled = false;
                btnCaptureStart.Enabled = false;
                btnCaptureStop.Enabled = false;
                ltbDeviceList.Enabled = true;
                btnDumpStart.Enabled = false;
                chkPromiscuousMode.Enabled = true;
            }
            catch (Exception exc)
            {
                MessageBox.Show(exc.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
            }
        }

        private void btnCaptureStart_Click(object sender, EventArgs e)
        {
            try
            {
                _packetsForBackup.Clear();
                _packetsForDataGrid.Clear();

                _capture.StartCapture();

                btnOpen.Enabled = false;
                btnClose.Enabled = false;
                btnCaptureStart.Enabled = false;
                btnCaptureStop.Enabled = true;
            }
            catch (Exception exc)
            {
                MessageBox.Show(exc.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
            }
        }

        private void btnCaptureStop_Click(object sender, EventArgs e)
        {
            try
            {
                _capture.StopCapture();

                btnOpen.Enabled = false;
                btnClose.Enabled = true;
                btnCaptureStart.Enabled = true;
                btnCaptureStop.Enabled = false;
            }
            catch (Exception exc)
            {
                MessageBox.Show(exc.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
            }
        }

        private void btnDumpStart_Click(object sender, EventArgs e)
        {
            try
            {
                _capture.StartDump(_systemSetting.savePathDump + $@"\{_systemSetting.fileNameDump}.pcapng");

                btnDumpStart.Enabled = false;
                btnDumpStop.Enabled = true;
            }
            catch (Exception exc)
            {
                MessageBox.Show(exc.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
            }
        }

        private void btnDumpStop_Click(object sender, EventArgs e)
        {
            try
            {
                _capture.StopDump();
                btnDumpStart.Enabled = true;
                btnDumpStop.Enabled = false;
            }
            catch (Exception exc)
            {
                MessageBox.Show(exc.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
            }
        }

        private void btnFilterClear_Click(object sender, EventArgs e)
        {
            tbxFilterSrcIPv4.Text = "";
            tbxFilterSrcPort.Text = "";
            tbxFilterDstPort.Text = "";

            btnFilterApply.PerformClick();
        }

        private void btnFilterIPv4_Click(object sender, EventArgs e)
        {
            _filterSrcIPv4 = tbxFilterSrcIPv4.Text;
            _filterSrcPort = tbxFilterSrcPort.Text;
            _filterDstPort = tbxFilterDstPort.Text;

            _packetsForDataGrid.Clear();
            if (_filterSrcIPv4 == "" && _filterSrcPort == "" && _filterDstPort == "")
                _isPacketFiltered = false;
            else
                _isPacketFiltered = true;
        }
        #endregion

        #region Thread 함수
        private void beginThread()
        {
            //GLogger(0, "ENTER beginThread()");

            object[] lParameters = new object[] { this };
            _isRunThread = true;
            _thread = new Thread(new ParameterizedThreadStart(WorkerThread));
            _thread.Start(lParameters);
        }
        private void terminateThread()
        {
            _isRunThread = false;

            if (_thread != null)
            {
                _thread.Join();
                _thread = null;
            }
            
            //GLogger(0, "LEAVE terminateThread()");
        }

        private static void WorkerThread(object aParameters)
        {
            object[] lParameters = (object[])aParameters;
            FormMain lThis = (FormMain)lParameters[0];

            //GLogger(0, "WorkerThread 시작");
            try
            {
                while (lThis._isRunThread)
                {
                    switch (lThis._workerThreadStep)
                    {
                        case WorkerThreadStep.StepWait:
                            //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "WorkerThreadStep.StepWait");
                            Thread.Sleep(100); //일단 냅두기. 방법이 있는듯.
                            //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._workerThreadStep = WorkerThreadStep.StepCheckQueueBufferCount;");
                            lThis._workerThreadStep = WorkerThreadStep.StepCheckQueueBufferCount;
                            break;

                        case WorkerThreadStep.StepCheckQueueBufferCount:
                            //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "WorkerThreadStep.StepCheckQueueBufferCount");
                            if (lThis.checkQueueBuffer() == true)
                            {
                                //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis.checkQueueBuffer() == true");
                                //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._workerThreadStep = WorkerThreadStep.StepUpdatePacketList;");
                                lThis._workerThreadStep = WorkerThreadStep.StepUpdatePacketList;
                            }
                            else
                            {
                                //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis.checkQueueBuffer() == false");
                                if (lThis._isPacketFiltered == true)
                                {
                                    //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._isPacketFiltered == true");
                                    //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._workerThreadStep = WorkerThreadStep.StepDisplay;");
                                    lThis._workerThreadStep = WorkerThreadStep.StepDisplay;
                                }
                                else
                                {
                                    //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._isPacketFiltered == false");
                                    //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._workerThreadStep = WorkerThreadStep.StepWait;");
                                    lThis._workerThreadStep = WorkerThreadStep.StepWait;
                                }
                            }
                            break;

                        case WorkerThreadStep.StepUpdatePacketList:
                            //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "WorkerThreadStep.StepUpdatePacketList");
                            if (lThis.updateRawPacketList() == true)
                            {
                                //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._workerThreadStep = WorkerThreadStep.StepDisplay;");
                                lThis._workerThreadStep = WorkerThreadStep.StepDisplay;
                            }
                            else
                            {
                                //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis._workerThreadStep = WorkerThreadStep.StepWait");
                                lThis._workerThreadStep = WorkerThreadStep.StepWait;
                            }

                            break;

                        case WorkerThreadStep.StepDisplay:
                            //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "WorkerThreadStep.StepDisplay");
                            //lThis._logger.AddBuffer(LoggerEx.Level.Debug, "lThis.BeginInvoke(new updatePackeListDelegate(lThis.updateDataGridView));");
                            lThis.updateDataGridView();
                            //lThis.BeginInvoke(new updatePackeListDelegate(lThis.updateDataGridView));
                            //Delegate를 변수로 만들고 프로그램 생성 시 생성. 그리고 호출만.
                            //Invoke Require이면 BeginInvoke 호출하는 형태로 변경하기.
                            //lThis.Invoke(new updatePackeListDelegate(lThis.updateDataGridView));
                            //lThis.updateDataGridView();
                            lThis._workerThreadStep = WorkerThreadStep.StepWait;
                            break;
                    }
                }
            }
            catch (Exception exc)
            {
                MessageBox.Show("Worker Thread 예외!!");
            }
            finally
            {
                lThis._logger.AddBuffer(LoggerEx.Level.Debug, "WorkerThread 종료");
            }
        }
        #endregion

        private bool checkQueueBuffer()
        {
            try
            {
                return _capture.GetNumberOfParsedPacketData != 0;
            }
            catch
            {
                return false;
            }
            finally
            {
            }
        }

        private bool updateRawPacketList()
        {
            try
            {
                var packets = _capture.GetParsedPacketDatas();
                bool requireUpdate = packets.Count != 0;

                PacketAnalyzerWrapper.PacketDataWrapper packet;
                while (packets.TryTake(out packet) == true)
                {
                    if (_packetList.TryAdd(packet) == true)
                    {

                    }
                    else
                    {

                    }
                        
                    if (_packetList.Count >= MAX_BUFFERS)
                    {
                        if (_packetList.TryTake(out packet) == true)
                        {

                        }
                        else
                        {

                        }
                    }
                }

                return requireUpdate;
            }
            finally
            {
            }
        }

        private void updateDataGridView()
        {
            if (gridPacket.InvokeRequired == true)
            {
                BeginInvoke(_delegateUpdatePacketList);
            }
            else
            {
                PacketAnalyzerWrapper.PacketDataWrapper packet;
                while (_packetList.TryTake(out packet) == true)
                {
                    //string payload = packet.payload.Replace("  ", "");
                    //var tmp = FromHex(payload);
                    //string converted = System.Text.Encoding.UTF8.GetString(tmp);
                    //var removeNull = converted.Replace('\0', ' ');
                    string removeNull = packet.payloadHex;

                    this._packetsForBackup.Add(new DataGridPacket(packet.frameNumber, packet.payloadLength, packet.dateTime,
                        packet.srcIPv4, packet.srcPort, packet.dstIPv4, packet.dstPort, packet.flag,  packet.protocol, 
                        packet.isTcpChecksumCorrect, packet.isUdpChecksumCorrect, packet.isKeepAlive, packet.isKeepAliveAck, removeNull, packet));

                    if (_packetsForBackup.Count >= MAX_BUFFERS)
                    {
                        _packetsForBackup.RemoveAt(0);
                    }
                }

                foreach (DataGridPacket tmp in _packetsForBackup)
                {
                    if ((_filterSrcIPv4 == "" && _filterSrcPort == "" && _filterDstPort == "") || 
                        (tmp.srcIPv4 == _filterSrcIPv4 || tmp.srcPort == _filterSrcPort || tmp.dstPort == _filterDstPort)
                        )
                    {
                        if (_packetsForDataGrid.Contains(tmp) == false)
                        {
                            this._packetsForDataGrid.Add(tmp);
                        }
                    }

                    if (_packetsForDataGrid.Count >= MAX_BUFFERS)
                    {
                        _packetsForDataGrid.RemoveAt(0);
                    }
                }

                if (chkAutoScroll.Checked == true)
                {
                    int firstRow = _packetsForDataGrid.Count - gridPacket.DisplayedRowCount(false);
                    if (firstRow < 0)
                        firstRow = 0;

                    gridPacket.FirstDisplayedScrollingRowIndex = firstRow;
                }

                //gridPacket.Update();
                gridPacket.Refresh();
            }
        }

        private byte[] FromHex(string hex)
        {
            byte[] raw = new byte[hex.Length / 2];
            for (int i = 0; i < raw.Length; i++)
            {
                raw[i] = Convert.ToByte(hex.Substring(i * 2, 2), 16);
            }
            return raw;
        }

        #region DataGrid 이벤트
        private void gridPacket_CellValueNeeded(object sender, DataGridViewCellValueEventArgs e)
        {
            // If this is the row for new records, no values are needed.
            if (e.RowIndex == gridPacket.RowCount - 1) return;

            DataGridPacket customerTmp = null;

            // Store a reference to the Customer object for the row being painted.
            if (e.RowIndex == rowInEdit)
            {
                customerTmp = this.customerInEdit;
            }
            else
            {
                if (this._packetsForDataGrid.Count != 0)
                {
                    int index = e.RowIndex;
                    if (index < 0)
                        return;

                    if (index >= _packetsForDataGrid.Count)
                        return;

                    customerTmp = (DataGridPacket)this._packetsForDataGrid[index];
                }
            }

            if (customerTmp != null)
            {
                if (gridPacket.Columns[e.ColumnIndex] != null)
                {
                    switch (gridPacket.Columns[e.ColumnIndex].Name)
                    {
                        case "No.":
                            e.Value = customerTmp.frameNumber;
                            break;

                        case "Time":
                            e.Value = customerTmp.dateTime;
                            break;

                        case "SrcIPv4":
                            e.Value = customerTmp.srcIPv4;
                            break;

                        case "DstIPv4":
                            e.Value = customerTmp.dstIPv4;
                            break;

                        case "Protocol":
                            e.Value = customerTmp.protocol;
                            break;

                        case "TCP":
                            e.Value = customerTmp.tcpChecksumCorrect;
                            break;

                        case "UDP":
                            e.Value = customerTmp.udpChecksumCorrect;
                            break;

                        case "Length":
                            e.Value = customerTmp.length;
                            break;

                        case "Message":
                            if (customerTmp.isKeepAlive == true)
                            {
                                e.Value = $"[Keep Alive] {customerTmp.flag} {customerTmp.srcPort}->{customerTmp.dstPort} {customerTmp.message}";
                            }
                            else if (customerTmp.isKeepAliveAck == true)
                            {
                                e.Value = $"[Keep-Alive Ack] {customerTmp.flag} {customerTmp.srcPort}->{customerTmp.dstPort} {customerTmp.message}";
                            }
                            else
                            {
                                e.Value = $"{customerTmp.flag} {customerTmp.srcPort}->{customerTmp.dstPort} {customerTmp.message}";
                            }
                            break;
                    }
                }
            }
        }
           
        private void updatePacketInfo(PacketAnalyzerWrapper.PacketDataWrapper packet)
        {
            ltbPacketInfo.Items.Clear();

            ltbPacketInfo.Items.Add("Frame No: " + packet.frameNumber);

            foreach (var messeage in packet.messages)
                ltbPacketInfo.Items.Add(messeage);

            ltbPacketInfo.Items.Add("Source: " + packet.srcIPv4);
            ltbPacketInfo.Items.Add("Destination: " + packet.dstIPv4);
            ltbPacketInfo.Items.Add("Protocol: " + packet.protocol);
            ltbPacketInfo.Items.Add("Sequence Number: " + packet.sequenceNumber.ToString());
            ltbPacketInfo.Items.Add("Acknowledgment Number: " + packet.acknowledgmentNumber.ToString());
            ltbPacketInfo.Items.Add("Payload Size: " + packet.payloadLength);
            string payload = packet.payloadHex;
            ltbPacketInfo.Items.Add("Payload(HEX): " + payload);

            //payload = payload.Replace("  ", "");
            //var tmp = FromHex(payload);
            //string converted = System.Text.Encoding.UTF8.GetString(tmp);
            //var removeNull = converted.Replace('\0', ' ');
            var removeNull = payload;
            ltbPacketInfo.Items.Add("Payload(ASCII): " + packet.payloadASCII);

            ltbPacketInfo.Items.Add($"TCP Checksum: {packet.isTcpChecksumCorrect}");
            ltbPacketInfo.Items.Add($"UDP Checksum: {packet.isUdpChecksumCorrect}");
        }

        private void updateParsedInfo(PacketAnalyzerWrapper.PacketDataWrapper packet)
        {
            ltbParsedInfo.Items.Clear();

            foreach(var data in packet.parsed)
            {
                ltbParsedInfo.Items.Add(data);
            }
        }

        private void gridPacket_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (_packetsForDataGrid.Count == 0) return;

            DataGridPacket customerTmp = null;

            int selected = e.RowIndex;//this._packetsForDataGrid.Count - e.RowIndex - 1;
            if (selected >= _packetsForDataGrid.Count)
                return;

            if (selected < 0)
                selected = 0;

            customerTmp = (DataGridPacket)this._packetsForDataGrid[selected];
            if (customerTmp != null)
            {
                updatePacketInfo(customerTmp.packet);
                updateParsedInfo(customerTmp.packet);
            }
        }

        private void gridPacket_KeyUp(object sender, KeyEventArgs e)
        {
            if (_packetsForDataGrid.Count == 0) return;
            var cell = gridPacket.SelectedCells[0];
            if (cell == null) return;

            if (cell.RowIndex == -1) return;

            if (e.KeyCode == Keys.Up || e.KeyCode == Keys.Down || e.KeyCode == Keys.PageUp || e.KeyCode == Keys.PageDown)
            {
                DataGridPacket customerTmp = null;

                int selected = cell.RowIndex;//this._packetsForDataGrid.Count - cell.RowIndex - 1;
                if (selected >= _packetsForDataGrid.Count)
                    return;

                if (selected < 0)
                    selected = 0;

                customerTmp = (DataGridPacket)this._packetsForDataGrid[selected];
                if (customerTmp != null)
                {
                    updatePacketInfo(customerTmp.packet);
                    updateParsedInfo(customerTmp.packet);
                }
            }
            else if (e.KeyCode == Keys.Home)
            {
                DataGridPacket customerTmp = null;
                customerTmp = (DataGridPacket)this._packetsForDataGrid[0];
                if (customerTmp != null)
                {
                    updatePacketInfo(customerTmp.packet);
                    updateParsedInfo(customerTmp.packet);
                }

                gridPacket.CurrentCell = gridPacket.Rows[0].Cells[0];
            }
            else if (e.KeyCode == Keys.End)
            {
                DataGridPacket customerTmp = null;
                customerTmp = (DataGridPacket)this._packetsForDataGrid[_packetsForDataGrid.Count - 1];
                if (customerTmp != null)
                {
                    updatePacketInfo(customerTmp.packet);
                    updateParsedInfo(customerTmp.packet);
                }

                gridPacket.CurrentCell = gridPacket.Rows[_packetsForDataGrid.Count - 1].Cells[0];
            }
        }

        private void gridPacket_Scroll(object sender, ScrollEventArgs e)
        {
            if (e.Type == ScrollEventType.SmallDecrement || e.Type == ScrollEventType.SmallIncrement)
                chkAutoScroll.Checked = false;
        }
        #endregion

        #region Menu 이벤트
        private void menuSettings_Click(object sender, EventArgs e)
        {
            try
            {
                FormSettings dlg = new FormSettings();
                dlg.settings = _systemSetting;
                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    _systemSetting = dlg.settings;
                    saveSystemFile(_systemSetting);

                    updateCaptureLogInfo();
                }
            }
            catch (Exception exc)
            {
                
            }
            finally
            {

            }
        }

        private void saveSystemFile(SystemSettings settings)
        {
            string filePath = System.Windows.Forms.Application.StartupPath + @"\system.xml";
            FileInfo fi = new FileInfo(filePath);
            XmlEx xml = new XmlEx();
            if (fi.Exists == false)
            {
                xml.Create(filePath, "system");
                xml.CreateNode("system", "settings", null);
                xml.CreateNode(@"/system/settings", "enableSaveLog", settings.enableSaveLog.ToString());
                xml.CreateNode(@"/system/settings", "savePathLog", settings.savePathLog);
                xml.CreateNode(@"/system/settings", "logLevel", settings.logLevel);
                xml.CreateNode(@"/system/settings", "savePathDump", settings.savePathDump);
                xml.CreateNode(@"/system/settings", "fileNameDump", settings.fileNameDump);
                xml.Save();
            }
            else
            {
                xml.Open(filePath);
                xml.EditNodeValue(@"/system/settings", "enableSaveLog", settings.enableSaveLog.ToString());
                xml.EditNodeValue(@"/system/settings", "savePathLog", settings.savePathLog);
                xml.EditNodeValue(@"/system/settings", "logLevel", settings.logLevel);
                xml.EditNodeValue(@"/system/settings", "savePathDump", settings.savePathDump);
                xml.EditNodeValue(@"/system/settings", "fileNameDump", settings.fileNameDump);
                xml.Save();
            }
        }

        private void menuExit_Click(object sender, EventArgs e)
        {
            Close();
        }
        #endregion

        private void OnTick_AutoReset(object sender, System.Timers.ElapsedEventArgs e)
        {
            _autoResetTimer.Stop();
            _autoResetTimer.Elapsed -= OnTick_AutoReset;
            //처리

            _updateHandle.Set();

            ///~처리
            _autoResetTimer.Elapsed += OnTick_AutoReset;
            _autoResetTimer.Start();

        }
    }
}
