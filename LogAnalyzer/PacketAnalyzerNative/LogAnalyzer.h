#pragma once

#include <queue>
#include <sstream>
#include <iostream>
#include <string>
#include <mutex>
#include <thread>
#include <concurrent_queue.h>
#include <iomanip>
#include <filesystem>

#include "../dependencies/logger/include/Logger.h"
#include <pybind11/pybind11.h>
#include <pybind11/embed.h>  // pybind11::scoped_interpreter

namespace py = pybind11;

class LogAnalyzer
{
public:
	struct DeviceInfo
	{
		std::string name;
		std::string ipv4;
		int index;
	};

	struct DeviceStatistics
	{
		uint64_t packetsRecv;
		uint64_t packetsDrop;
		uint64_t packetsDropByInterface;
	};

	struct PacketData
	{
		std::vector<std::string> messages;
		std::string dateTime;
		std::string srcIPv4;
		std::string dstIPv4;
		std::string protocol;
		std::string payloadHex;
		std::string payloadASCII;
		std::string flag;
		std::vector<std::string> parsed;
		std::string srcPort;
		std::string dstPort;
		uint32_t frameNumber;
		uint32_t sequenceNumber;
		uint32_t acknowledgmentNumber;
		int capturedLength;
		int payloadLength;
		bool isValid; //concurrent_queue에서 try_pop 이후 유효성 확인 용도
		bool isTcpChecksumCorrect;
		bool isUdpChecksumCorrect;
		bool isKeepAlive;
		bool isKeepAliveAck;
	};

public:
	LogAnalyzer();
	virtual ~LogAnalyzer();
	
	bool fileLoad(const std::string filePath);
	bool IsRunning() const;


	void SetSaveLogPath(const std::string path);
	void SetLogLevel(const LogBuffer::Level level);

	void ClearParsedPacketData();
	int GetNumberOfParsedPacketData();
	PacketData GetParsedPacketData();
	static std::vector<DeviceInfo> GetDevices();

private :
	static void onDataArrives(void* instance, void* data);
	static void globalParsingFunction(void* handle);
	static void globalDumpingFunction(void* handle);

	void initializePythonModule();
	void dataArrives(void* data);
	bool checkParsingQueueBuffer();
	bool parsingQueueBuffer();

private:
	Concurrency::concurrent_queue<void*> m_rawDatas;
	Concurrency::concurrent_queue<LogAnalyzer::PacketData> m_parsedPackets;

	HANDLE m_packetArrived;
	HANDLE m_packetArrivedDumping;
	bool m_isRunning;
	Logger m_logger;
	std::string m_currentDate;
	void* m_rawData;
};