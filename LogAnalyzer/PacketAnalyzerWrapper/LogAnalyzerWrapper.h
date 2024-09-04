#pragma once
#include "../PacketAnalyzerNative/LogAnalyzer.h"
#ifdef _DEBUG
#pragma comment(lib, "../x64/Debug/PacketAnalyzerNative_d.lib")
#else
#pragma comment(lib, "../x64/Release/PacketAnalyzerNative.lib")
#endif
#include <msclr/marshal_cppstd.h>

using namespace msclr::interop;
using namespace System;
using namespace System::Collections;
using namespace System::Collections::Concurrent;

namespace WrapperPacketAnalyzer {
	public ref class PacketAnalyzerWrapper
	{
	public:
		ref struct DeviceInfoWrapper
		{
			System::String^ name;
			System::String^ ipv4;
			int index;
		};

		ref struct DeviceStatisticsWrapper
		{
			uint64_t packetsRecv;
			uint64_t packetsDrop;
			uint64_t packetsDropByInterface;
		};

		ref struct PacketDataWrapper
		{
			System::Collections::Generic::List<System::String^>^ messages;
			System::String^ dateTime;
			System::String^ srcIPv4;
			System::String^ dstIPv4;
			System::String^ protocol;
			System::String^ flag;
			System::String^ payloadHex;
			System::String^ payloadASCII;
			System::Collections::Generic::List<System::String^>^ parsed;
			System::String^ srcPort;
			System::String^ dstPort;
			UINT32 frameNumber;
			UINT32 sequenceNumber;
			UINT32 acknowledgmentNumber;
			int capturedLength;
			int payloadLength;
			bool isValid;
			bool isTcpChecksumCorrect;
			bool isUdpChecksumCorrect;
			bool isKeepAlive;
			bool isKeepAliveAck;
		};

		enum class LevelWrapper { Error, Warn, Debug, Info };

	public:
		PacketAnalyzerWrapper();
		virtual ~PacketAnalyzerWrapper();

		bool Open(System::String^ ipv4, bool promiscuousMode);
		bool Open(int index, bool promiscuousMode);
		bool Close();
		bool StartDump(System::String^ path);
		void StopDump();
		bool StartCapture();
		void StopCapture();
		bool SetFilterIPv4(System::String^ ipv4);
		void SetSaveLogPath(System::String^ path);
		void SetLogLevel(LevelWrapper level);
		void ClearParsedPacketData();
		property int GetNumberOfParsedPacketData { int get(); }
		property bool IsOpened { bool get(); }
		property bool IsCaptured { bool get(); }
		PacketDataWrapper^ GetParsedPacketData();
		DeviceStatisticsWrapper^ GetDeviceStatistics();
		BlockingCollection<PacketDataWrapper^>^ GetParsedPacketDatas();
		static System::Collections::Generic::List<DeviceInfoWrapper^>^ GetDevices();

	private:
		LogAnalyzer* m_device;
	};
}