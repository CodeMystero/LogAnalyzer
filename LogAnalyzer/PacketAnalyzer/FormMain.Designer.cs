namespace CustomWireshark
{
    partial class FormMain
    {
        /// <summary>
        /// 필수 디자이너 변수입니다.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 사용 중인 모든 리소스를 정리합니다.
        /// </summary>
        /// <param name="disposing">관리되는 리소스를 삭제해야 하면 true이고, 그렇지 않으면 false입니다.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 디자이너에서 생성한 코드

        /// <summary>
        /// 디자이너 지원에 필요한 메서드입니다. 
        /// 이 메서드의 내용을 코드 편집기로 수정하지 마세요.
        /// </summary>
        private void InitializeComponent()
        {
            this.ltbDeviceList = new System.Windows.Forms.ListBox();
            this.btnCaptureStart = new System.Windows.Forms.Button();
            this.btnCaptureStop = new System.Windows.Forms.Button();
            this.btnOpen = new System.Windows.Forms.Button();
            this.btnClose = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.chkPromiscuousMode = new System.Windows.Forms.CheckBox();
            this.tbxFilterSrcIPv4 = new System.Windows.Forms.TextBox();
            this.btnFilterApply = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.chkAutoScroll = new System.Windows.Forms.CheckBox();
            this.label3 = new System.Windows.Forms.Label();
            this.tbxFilterDstPort = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.tbxFilterSrcPort = new System.Windows.Forms.TextBox();
            this.btnFilterClear = new System.Windows.Forms.Button();
            this.btnDumpStart = new System.Windows.Forms.Button();
            this.btnDumpStop = new System.Windows.Forms.Button();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.groupBox5 = new System.Windows.Forms.GroupBox();
            this.panel1 = new System.Windows.Forms.Panel();
            this.ltbParsedInfo = new System.Windows.Forms.ListBox();
            this.panel2 = new System.Windows.Forms.Panel();
            this.panel4 = new System.Windows.Forms.Panel();
            this.panel6 = new System.Windows.Forms.Panel();
            this.panel5 = new System.Windows.Forms.Panel();
            this.ltbPacketInfo = new System.Windows.Forms.ListBox();
            this.panel3 = new System.Windows.Forms.Panel();
            this.gridPacket = new System.Windows.Forms.DataGridView();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.menuExit = new System.Windows.Forms.ToolStripMenuItem();
            this.helpToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.menuSettings = new System.Windows.Forms.ToolStripMenuItem();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.groupBox4.SuspendLayout();
            this.groupBox5.SuspendLayout();
            this.panel1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.panel4.SuspendLayout();
            this.panel6.SuspendLayout();
            this.panel5.SuspendLayout();
            this.panel3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.gridPacket)).BeginInit();
            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // ltbDeviceList
            // 
            this.ltbDeviceList.FormattingEnabled = true;
            this.ltbDeviceList.ItemHeight = 12;
            this.ltbDeviceList.Location = new System.Drawing.Point(12, 12);
            this.ltbDeviceList.Name = "ltbDeviceList";
            this.ltbDeviceList.Size = new System.Drawing.Size(398, 208);
            this.ltbDeviceList.TabIndex = 0;
            // 
            // btnCaptureStart
            // 
            this.btnCaptureStart.Enabled = false;
            this.btnCaptureStart.Location = new System.Drawing.Point(8, 19);
            this.btnCaptureStart.Name = "btnCaptureStart";
            this.btnCaptureStart.Size = new System.Drawing.Size(88, 36);
            this.btnCaptureStart.TabIndex = 1;
            this.btnCaptureStart.Text = "Start";
            this.btnCaptureStart.UseVisualStyleBackColor = true;
            this.btnCaptureStart.Click += new System.EventHandler(this.btnCaptureStart_Click);
            // 
            // btnCaptureStop
            // 
            this.btnCaptureStop.Enabled = false;
            this.btnCaptureStop.Location = new System.Drawing.Point(102, 19);
            this.btnCaptureStop.Name = "btnCaptureStop";
            this.btnCaptureStop.Size = new System.Drawing.Size(88, 36);
            this.btnCaptureStop.TabIndex = 2;
            this.btnCaptureStop.Text = "Stop";
            this.btnCaptureStop.UseVisualStyleBackColor = true;
            this.btnCaptureStop.Click += new System.EventHandler(this.btnCaptureStop_Click);
            // 
            // btnOpen
            // 
            this.btnOpen.Location = new System.Drawing.Point(8, 20);
            this.btnOpen.Name = "btnOpen";
            this.btnOpen.Size = new System.Drawing.Size(88, 36);
            this.btnOpen.TabIndex = 4;
            this.btnOpen.Text = "Open";
            this.btnOpen.UseVisualStyleBackColor = true;
            this.btnOpen.Click += new System.EventHandler(this.btnOpen_Click);
            // 
            // btnClose
            // 
            this.btnClose.Enabled = false;
            this.btnClose.Location = new System.Drawing.Point(102, 20);
            this.btnClose.Name = "btnClose";
            this.btnClose.Size = new System.Drawing.Size(88, 36);
            this.btnClose.TabIndex = 5;
            this.btnClose.Text = "Close";
            this.btnClose.UseVisualStyleBackColor = true;
            this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.chkPromiscuousMode);
            this.groupBox1.Location = new System.Drawing.Point(12, 230);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(196, 64);
            this.groupBox1.TabIndex = 13;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Option";
            // 
            // chkPromiscuousMode
            // 
            this.chkPromiscuousMode.AutoSize = true;
            this.chkPromiscuousMode.Checked = true;
            this.chkPromiscuousMode.CheckState = System.Windows.Forms.CheckState.Checked;
            this.chkPromiscuousMode.Location = new System.Drawing.Point(9, 29);
            this.chkPromiscuousMode.Name = "chkPromiscuousMode";
            this.chkPromiscuousMode.Size = new System.Drawing.Size(178, 16);
            this.chkPromiscuousMode.TabIndex = 2;
            this.chkPromiscuousMode.Text = "Enable Promiscuous Mode";
            this.chkPromiscuousMode.UseVisualStyleBackColor = true;
            // 
            // tbxFilterSrcIPv4
            // 
            this.tbxFilterSrcIPv4.Location = new System.Drawing.Point(62, 18);
            this.tbxFilterSrcIPv4.Name = "tbxFilterSrcIPv4";
            this.tbxFilterSrcIPv4.Size = new System.Drawing.Size(114, 21);
            this.tbxFilterSrcIPv4.TabIndex = 14;
            // 
            // btnFilterApply
            // 
            this.btnFilterApply.Location = new System.Drawing.Point(184, 17);
            this.btnFilterApply.Name = "btnFilterApply";
            this.btnFilterApply.Size = new System.Drawing.Size(75, 23);
            this.btnFilterApply.TabIndex = 17;
            this.btnFilterApply.Text = "Apply";
            this.btnFilterApply.UseVisualStyleBackColor = true;
            this.btnFilterApply.Click += new System.EventHandler(this.btnFilterIPv4_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(9, 22);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(47, 12);
            this.label2.TabIndex = 16;
            this.label2.Text = "SrcIPv4";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.chkAutoScroll);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.tbxFilterDstPort);
            this.groupBox2.Controls.Add(this.label1);
            this.groupBox2.Controls.Add(this.tbxFilterSrcPort);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.btnFilterClear);
            this.groupBox2.Controls.Add(this.btnFilterApply);
            this.groupBox2.Controls.Add(this.tbxFilterSrcIPv4);
            this.groupBox2.Location = new System.Drawing.Point(145, 370);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(265, 118);
            this.groupBox2.TabIndex = 17;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Display Filter";
            // 
            // chkAutoScroll
            // 
            this.chkAutoScroll.AutoSize = true;
            this.chkAutoScroll.Checked = true;
            this.chkAutoScroll.CheckState = System.Windows.Forms.CheckState.Checked;
            this.chkAutoScroll.Location = new System.Drawing.Point(171, 93);
            this.chkAutoScroll.Name = "chkAutoScroll";
            this.chkAutoScroll.Size = new System.Drawing.Size(85, 16);
            this.chkAutoScroll.TabIndex = 22;
            this.chkAutoScroll.Text = "Auto Scroll";
            this.chkAutoScroll.UseVisualStyleBackColor = true;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(9, 70);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(45, 12);
            this.label3.TabIndex = 20;
            this.label3.Text = "DstPort";
            // 
            // tbxFilterDstPort
            // 
            this.tbxFilterDstPort.Location = new System.Drawing.Point(62, 66);
            this.tbxFilterDstPort.Name = "tbxFilterDstPort";
            this.tbxFilterDstPort.Size = new System.Drawing.Size(114, 21);
            this.tbxFilterDstPort.TabIndex = 16;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(9, 46);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(46, 12);
            this.label1.TabIndex = 18;
            this.label1.Text = "SrcPort";
            // 
            // tbxFilterSrcPort
            // 
            this.tbxFilterSrcPort.Location = new System.Drawing.Point(62, 42);
            this.tbxFilterSrcPort.Name = "tbxFilterSrcPort";
            this.tbxFilterSrcPort.Size = new System.Drawing.Size(114, 21);
            this.tbxFilterSrcPort.TabIndex = 15;
            // 
            // btnFilterClear
            // 
            this.btnFilterClear.Location = new System.Drawing.Point(184, 64);
            this.btnFilterClear.Name = "btnFilterClear";
            this.btnFilterClear.Size = new System.Drawing.Size(75, 23);
            this.btnFilterClear.TabIndex = 18;
            this.btnFilterClear.Text = "Clear";
            this.btnFilterClear.UseVisualStyleBackColor = true;
            this.btnFilterClear.Click += new System.EventHandler(this.btnFilterClear_Click);
            // 
            // btnDumpStart
            // 
            this.btnDumpStart.Enabled = false;
            this.btnDumpStart.Location = new System.Drawing.Point(7, 20);
            this.btnDumpStart.Name = "btnDumpStart";
            this.btnDumpStart.Size = new System.Drawing.Size(88, 36);
            this.btnDumpStart.TabIndex = 1;
            this.btnDumpStart.Text = "Start";
            this.btnDumpStart.UseVisualStyleBackColor = true;
            this.btnDumpStart.Click += new System.EventHandler(this.btnDumpStart_Click);
            // 
            // btnDumpStop
            // 
            this.btnDumpStop.Enabled = false;
            this.btnDumpStop.Location = new System.Drawing.Point(101, 20);
            this.btnDumpStop.Name = "btnDumpStop";
            this.btnDumpStop.Size = new System.Drawing.Size(88, 36);
            this.btnDumpStop.TabIndex = 2;
            this.btnDumpStop.Text = "Stop";
            this.btnDumpStop.UseVisualStyleBackColor = true;
            this.btnDumpStop.Click += new System.EventHandler(this.btnDumpStop_Click);
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.btnDumpStop);
            this.groupBox3.Controls.Add(this.btnDumpStart);
            this.groupBox3.Location = new System.Drawing.Point(12, 300);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(196, 64);
            this.groupBox3.TabIndex = 19;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Dump";
            // 
            // groupBox4
            // 
            this.groupBox4.Controls.Add(this.btnCaptureStop);
            this.groupBox4.Controls.Add(this.btnCaptureStart);
            this.groupBox4.Location = new System.Drawing.Point(214, 300);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(196, 64);
            this.groupBox4.TabIndex = 20;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "Capture";
            // 
            // groupBox5
            // 
            this.groupBox5.Controls.Add(this.btnClose);
            this.groupBox5.Controls.Add(this.btnOpen);
            this.groupBox5.Location = new System.Drawing.Point(214, 230);
            this.groupBox5.Name = "groupBox5";
            this.groupBox5.Size = new System.Drawing.Size(196, 64);
            this.groupBox5.TabIndex = 21;
            this.groupBox5.TabStop = false;
            this.groupBox5.Text = "Connection";
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.ltbDeviceList);
            this.panel1.Controls.Add(this.groupBox5);
            this.panel1.Controls.Add(this.groupBox1);
            this.panel1.Controls.Add(this.groupBox4);
            this.panel1.Controls.Add(this.groupBox2);
            this.panel1.Controls.Add(this.groupBox3);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Left;
            this.panel1.Location = new System.Drawing.Point(0, 24);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(417, 650);
            this.panel1.TabIndex = 22;
            // 
            // ltbParsedInfo
            // 
            this.ltbParsedInfo.Dock = System.Windows.Forms.DockStyle.Fill;
            this.ltbParsedInfo.FormattingEnabled = true;
            this.ltbParsedInfo.HorizontalScrollbar = true;
            this.ltbParsedInfo.ItemHeight = 12;
            this.ltbParsedInfo.Location = new System.Drawing.Point(0, 0);
            this.ltbParsedInfo.Name = "ltbParsedInfo";
            this.ltbParsedInfo.Size = new System.Drawing.Size(934, 150);
            this.ltbParsedInfo.TabIndex = 22;
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.panel4);
            this.panel2.Controls.Add(this.panel3);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel2.Location = new System.Drawing.Point(417, 24);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(934, 650);
            this.panel2.TabIndex = 23;
            // 
            // panel4
            // 
            this.panel4.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panel4.Controls.Add(this.panel6);
            this.panel4.Controls.Add(this.panel5);
            this.panel4.Location = new System.Drawing.Point(0, 350);
            this.panel4.Name = "panel4";
            this.panel4.Size = new System.Drawing.Size(934, 300);
            this.panel4.TabIndex = 22;
            // 
            // panel6
            // 
            this.panel6.Controls.Add(this.ltbParsedInfo);
            this.panel6.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel6.Location = new System.Drawing.Point(0, 150);
            this.panel6.Name = "panel6";
            this.panel6.Size = new System.Drawing.Size(934, 150);
            this.panel6.TabIndex = 1;
            // 
            // panel5
            // 
            this.panel5.Controls.Add(this.ltbPacketInfo);
            this.panel5.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel5.Location = new System.Drawing.Point(0, 0);
            this.panel5.Name = "panel5";
            this.panel5.Size = new System.Drawing.Size(934, 150);
            this.panel5.TabIndex = 0;
            // 
            // ltbPacketInfo
            // 
            this.ltbPacketInfo.Dock = System.Windows.Forms.DockStyle.Fill;
            this.ltbPacketInfo.FormattingEnabled = true;
            this.ltbPacketInfo.HorizontalScrollbar = true;
            this.ltbPacketInfo.ItemHeight = 12;
            this.ltbPacketInfo.Location = new System.Drawing.Point(0, 0);
            this.ltbPacketInfo.Name = "ltbPacketInfo";
            this.ltbPacketInfo.Size = new System.Drawing.Size(934, 150);
            this.ltbPacketInfo.TabIndex = 20;
            // 
            // panel3
            // 
            this.panel3.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panel3.Controls.Add(this.gridPacket);
            this.panel3.Location = new System.Drawing.Point(0, 0);
            this.panel3.Name = "panel3";
            this.panel3.Size = new System.Drawing.Size(934, 350);
            this.panel3.TabIndex = 21;
            // 
            // gridPacket
            // 
            this.gridPacket.AllowUserToAddRows = false;
            this.gridPacket.AllowUserToDeleteRows = false;
            this.gridPacket.AllowUserToResizeColumns = false;
            this.gridPacket.AllowUserToResizeRows = false;
            this.gridPacket.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.gridPacket.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridPacket.Location = new System.Drawing.Point(0, 0);
            this.gridPacket.Name = "gridPacket";
            this.gridPacket.RowHeadersVisible = false;
            this.gridPacket.RowTemplate.Height = 23;
            this.gridPacket.Size = new System.Drawing.Size(934, 350);
            this.gridPacket.TabIndex = 21;
            this.gridPacket.VirtualMode = true;
            this.gridPacket.CellClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.gridPacket_CellClick);
            this.gridPacket.CellValueNeeded += new System.Windows.Forms.DataGridViewCellValueEventHandler(this.gridPacket_CellValueNeeded);
            this.gridPacket.Scroll += new System.Windows.Forms.ScrollEventHandler(this.gridPacket_Scroll);
            this.gridPacket.KeyUp += new System.Windows.Forms.KeyEventHandler(this.gridPacket_KeyUp);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem,
            this.helpToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1351, 24);
            this.menuStrip1.TabIndex = 23;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.menuExit});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "&File";
            // 
            // menuExit
            // 
            this.menuExit.Name = "menuExit";
            this.menuExit.Size = new System.Drawing.Size(93, 22);
            this.menuExit.Text = "E&xit";
            this.menuExit.Click += new System.EventHandler(this.menuExit_Click);
            // 
            // helpToolStripMenuItem
            // 
            this.helpToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.menuSettings});
            this.helpToolStripMenuItem.Name = "helpToolStripMenuItem";
            this.helpToolStripMenuItem.Size = new System.Drawing.Size(44, 20);
            this.helpToolStripMenuItem.Text = "&Help";
            // 
            // menuSettings
            // 
            this.menuSettings.Name = "menuSettings";
            this.menuSettings.Size = new System.Drawing.Size(126, 22);
            this.menuSettings.Text = "&Settings...";
            this.menuSettings.Click += new System.EventHandler(this.menuSettings_Click);
            // 
            // FormMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1351, 674);
            this.Controls.Add(this.panel2);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.menuStrip1);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "FormMain";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Packet Analyzer v1.3";
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.FormMain_FormClosed);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox4.ResumeLayout(false);
            this.groupBox5.ResumeLayout(false);
            this.panel1.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.panel4.ResumeLayout(false);
            this.panel6.ResumeLayout(false);
            this.panel5.ResumeLayout(false);
            this.panel3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.gridPacket)).EndInit();
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox ltbDeviceList;
        private System.Windows.Forms.Button btnCaptureStart;
        private System.Windows.Forms.Button btnCaptureStop;
        private System.Windows.Forms.Button btnOpen;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.TextBox tbxFilterSrcIPv4;
        private System.Windows.Forms.Button btnFilterApply;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Button btnDumpStart;
        private System.Windows.Forms.Button btnDumpStop;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.GroupBox groupBox5;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Panel panel4;
        private System.Windows.Forms.ListBox ltbPacketInfo;
        private System.Windows.Forms.Panel panel3;
        private System.Windows.Forms.DataGridView gridPacket;
        private System.Windows.Forms.ListBox ltbParsedInfo;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox tbxFilterDstPort;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox tbxFilterSrcPort;
        private System.Windows.Forms.Button btnFilterClear;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem menuExit;
        private System.Windows.Forms.ToolStripMenuItem helpToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem menuSettings;
        private System.Windows.Forms.Panel panel6;
        private System.Windows.Forms.Panel panel5;
        private System.Windows.Forms.CheckBox chkAutoScroll;
        private System.Windows.Forms.CheckBox chkPromiscuousMode;
    }
}

