#pragma once

#include "../dependencies/logger/include/Logger.h"

#ifdef _DEBUG
#pragma comment(lib, "../x64/Debug/LoggerNative.lib")
#else
#pragma comment(lib, "../x64/Release/LoggerNative.lib")
#endif
using namespace System;

#include <msclr/marshal_cppstd.h>

using namespace msclr::interop;
using namespace System;

namespace WrapperLogger {
	public ref class LoggerEx
	{
	public:
		enum class Level { Error, Warn, Debug, Info };
		LoggerEx();
		~LoggerEx();

		void SetSavePath(System::String^ path);
		void AddBuffer(const Level level, System::String^ message);
		void SetMinimumLevel(const Level level);
		void Close();
		property System::IntPtr handleTerminate { System::IntPtr get(); }
	private:
		Logger* m_logger;
	};
}
