using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WrapperPacketAnalyzer;

namespace CustomWireshark
{
    class DataGridPacket
    {
        private uint _frameNumber;
        private int _length;
        private string _dateTime;
        private string _srcIPv4;
        private string _srcPort;
        private string _dstIPv4;
        private string _dstPort;
        private string _message;
        private string _flag;
        private string _protocol;
        private PacketAnalyzerWrapper.PacketDataWrapper _packet;
        private bool _isTcpChecksumCorrect;
        private bool _isUdpChecksumCorrect;
        private bool _isKeepAlive;
        private bool _isKeepAliveAck;

        public DataGridPacket()
        {
        }

        public DataGridPacket(uint frameNumber, int length, string dateTime, string srcIPv4, string srcPort, string dstIPv4, string dstPort, string flag, string protocol, bool tcpChecksumCorrect, bool udpChecksumCorrect, bool isKeepAlive, bool isKeepAliveAck, string message, PacketAnalyzerWrapper.PacketDataWrapper packet)
        {
            _frameNumber = frameNumber;
            _length = length;
            _dateTime = dateTime;
            _srcIPv4 = srcIPv4;
            _srcPort = srcPort;
            _dstIPv4 = dstIPv4;
            _dstPort = dstPort;
            _flag = flag;
            _protocol = protocol;
            _message = message;
            _isTcpChecksumCorrect = tcpChecksumCorrect;
            _isUdpChecksumCorrect = udpChecksumCorrect;
            _isKeepAlive = isKeepAlive;
            _isKeepAliveAck = isKeepAliveAck;
            _packet = packet;
        }

        public uint frameNumber
        {
            get { return _frameNumber; }
            set { _frameNumber = value; }
        }

        public int length
        {
            get { return _length; }
            set { _length = value; }
        }

        public string dateTime
        {
            get { return _dateTime; }
            set { _dateTime = value; }
        }

        public string srcIPv4
        {
            get { return _srcIPv4; }
            set { _srcIPv4 = value; }
        }

        public string srcPort
        {
            get { return _srcPort; }
            set { _srcPort = value; }
        }

        public string dstIPv4
        {
            get { return _dstIPv4; }
            set { _dstIPv4 = value; }
        }

        public string dstPort
        {
            get { return _dstPort; }
            set { _dstPort = value; }
        }

        public string flag
        {
            get { return _flag; }
            set { _flag = value; }
        }
        public string protocol
        {
            get { return _protocol; }
            set { _protocol = value; }
        }

        public bool tcpChecksumCorrect
        {
            get { return _isTcpChecksumCorrect; }
            set { _isTcpChecksumCorrect = value; }
        }

        public bool udpChecksumCorrect
        {
            get { return _isUdpChecksumCorrect; }
            set { _isUdpChecksumCorrect = value; }
        }

        public bool isKeepAlive
        {
            get { return _isKeepAlive; }
            set { _isKeepAlive = value; }
        }

        public bool isKeepAliveAck
        {
            get { return _isKeepAliveAck; }
            set { _isKeepAliveAck = value; }
        }

        public string message
        {
            get { return _message; }
            set { _message = value; }
        }

        public WrapperPacketAnalyzer.PacketAnalyzerWrapper.PacketDataWrapper packet
        {
            get { return _packet; }
            set { _packet = value; }
        }

        public override bool Equals(object o)
        {
            if (o == null || o.GetType() != typeof(DataGridPacket))
                return false;
            DataGridPacket ca = (DataGridPacket)o;
            return ca.frameNumber.Equals(this.frameNumber);
        }
    }
}
