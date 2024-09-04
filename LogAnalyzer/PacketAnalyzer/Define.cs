using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CustomWireshark
{
    class Define
    {
    }

    public enum WorkerThreadStep
    {
        StepWait = 0,
        StepCheckQueueBufferCount,
        StepUpdatePacketList,
        StepDisplay
    }

    public struct SystemSettings
    {
        public bool enableSaveLog;
        public string savePathLog;
        public string logLevel;
        public string savePathDump;
        public string fileNameDump;
    }
}
