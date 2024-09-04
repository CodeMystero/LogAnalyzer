using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WrapperLogger;

namespace ExamCSConsole
{
    class Program
    {
        static void Main(string[] args)
        {
            LoggerEx logger = new LoggerEx();

            logger.SetSavePath(@"F:\test");
            logger.SetMinimumLevel(LoggerEx.Level.Info);

            logger.AddBuffer(LoggerEx.Level.Debug, "CS message");
            logger.AddBuffer(LoggerEx.Level.Info, "CS message");
            logger.AddBuffer(LoggerEx.Level.Error, "CS message");
        }
    }
}
