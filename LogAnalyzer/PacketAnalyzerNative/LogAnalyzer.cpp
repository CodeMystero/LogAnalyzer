#include "pch.h"
#include "LogAnalyzer.h"


std::thread* g_parsingThread = nullptr;
bool g_isRunParsingThread = false;

std::thread* g_dumpingThread = nullptr;
bool g_isRunDumpingThread = false;

enum class SequenceStepParsing
{
	StepWait = 0,
	StepCheckParsingQueueBufferCount,
	StepParsing
};

enum class SequenceStepDumping
{
	StepWait = 0,
	StepCheckDumpingQueueBufferCount,
	StepDumping
};

SequenceStepParsing g_stepParsing = SequenceStepParsing::StepWait;
SequenceStepDumping g_stepDumping = SequenceStepDumping::StepWait;

std::vector<LogAnalyzer::DeviceInfo> LogAnalyzer::GetDevices()
{
	std::vector<LogAnalyzer::DeviceInfo> list;
	/*int index = 0;
	for (const auto &dev : pcpp::PcapLiveDeviceList::getInstance().getPcapLiveDevicesList())
	{
		LogAnalyzer::DeviceInfo info;
		info.name = dev->getDesc();
		info.ipv4 = dev->getIPv4Address().toString();
		info.index = index++;

		list.push_back(info);
	}*/

	return list;
}
LogAnalyzer::LogAnalyzer()
{
	initializePythonModule();

	/*g_isRunParsingThread = true;
	g_parsingThread = new std::thread(globalParsingFunction, this);

	g_isRunDumpingThread = true;
	g_dumpingThread = new std::thread(globalDumpingFunction, this);

	m_packetArrived = CreateEvent(NULL, FALSE, FALSE, NULL);
	m_packetArrivedDumping = CreateEvent(NULL, FALSE, FALSE, NULL);*/
}

LogAnalyzer::~LogAnalyzer()
{
	SetEvent(m_packetArrived);

	g_isRunParsingThread = false;
	if (g_parsingThread != nullptr)
	{
		g_parsingThread->join();
		g_parsingThread = nullptr;
	}

	SetEvent(m_packetArrivedDumping);

	g_isRunDumpingThread = false;
	if (g_dumpingThread != nullptr)
	{
		g_dumpingThread->join();
		g_dumpingThread = nullptr;
	}
}

void LogAnalyzer::initializePythonModule()
{
	// Python 인터프리터 초기화
	py::scoped_interpreter guard{};

	// 현재 작업 디렉토리 얻기
	std::filesystem::path current_path = std::filesystem::current_path();
	// 상위 폴더로 경로 설정
	std::filesystem::path parent_path = current_path.parent_path().parent_path();

	// Python 모듈이 위치한 폴더 경로 지정
	std::filesystem::path module_path = parent_path; // main.py가 위치한 디렉토리

	// Python 모듈 경로에 추가
	//py::module sys = py::module::import("sys");
	//py::object path = sys.attr("path");
	//path.attr("append")(module_path.string());  // 모듈이 위치한 상위 폴더 경로를 추가


	// Python 모듈 임포트
	try {
		py::module::import("sys").attr("path").attr("append")(module_path.string());

		py::module mymodule = py::module::import("main");  // main.py의 모듈 이름
		// Python 함수 호출
		py::object result = mymodule.attr("myfunction")(10);

		// Python 함수 호출
		result = mymodule.attr("main_for_classified_logs")();

		// 결과 출력
		std::cout << "Result: " << result.cast<int>() << std::endl;
	}
	catch (const py::error_already_set& e) {
		std::cerr << "Error importing Python module or calling function: " << e.what() << std::endl;
	}
}

bool LogAnalyzer::fileLoad(const std::string filePath)
{
	//1. 현재 날짜 확인
	tm info;
	time_t m_time(NULL);
	time(&m_time);
	localtime_s(&info, &m_time);
	std::stringstream ss;
	ss << std::put_time(&info, "%F");
	m_currentDate = ss.str();



	m_logger.AddBuffer(LogBuffer::Level::Debug, "File Load : " + filePath);

	return false;
}

bool LogAnalyzer::IsRunning() const
{
	return m_isRunning;
}

void LogAnalyzer::SetSaveLogPath(const std::string path)
{
	m_logger.SetSavePath(path);
}

void LogAnalyzer::SetLogLevel(const LogBuffer::Level level)
{
	m_logger.SetMinimumLevel(level);
}



int LogAnalyzer::GetNumberOfParsedPacketData()
{
	size_t counts = m_parsedPackets.unsafe_size();
	return counts;
}

LogAnalyzer::PacketData LogAnalyzer::GetParsedPacketData()
{
	PacketData packet;
	packet.isValid = m_parsedPackets.try_pop(packet);
	return packet;
}

void LogAnalyzer::onDataArrives(void* instance, void* data)
{
	LogAnalyzer* pApp = (LogAnalyzer*)instance;
	pApp->dataArrives(data);
}



void LogAnalyzer::dataArrives(void* data)
{
	if (data == nullptr)
		return;

	/*pcpp::Packet parsedPacket(packet);
	m_rawPackets.push(parsedPacket);

	if (m_isDumped == true)
	{
		m_dumpPackets.push(parsedPacket);
		SetEvent(m_packetArrivedDumping);
	}*/

	SetEvent(m_packetArrived);
}

void LogAnalyzer::globalParsingFunction(void* handle)
{
	LogAnalyzer* pApp = (LogAnalyzer*)handle;

	while (g_isRunParsingThread)
	{
		switch (g_stepParsing)
		{
			case SequenceStepParsing::StepWait:
			{
				DWORD ret = WaitForSingleObject(pApp->m_packetArrived, 100);
				if (ret == WAIT_OBJECT_0)
				{
					g_stepParsing = SequenceStepParsing::StepCheckParsingQueueBufferCount;
				}
				break;
			}
			case SequenceStepParsing::StepCheckParsingQueueBufferCount:
			{
				if (pApp->checkParsingQueueBuffer() == true)
				{
					g_stepParsing = SequenceStepParsing::StepParsing;
				}
				else
				{
					g_stepParsing = SequenceStepParsing::StepWait;
				}
				break;
			}

			case SequenceStepParsing::StepParsing:
			{
				if (pApp->parsingQueueBuffer() == true)
				{
					g_stepParsing = SequenceStepParsing::StepWait;
				}
				else
				{
					g_stepParsing = SequenceStepParsing::StepCheckParsingQueueBufferCount;
				}
				break;
			}
		}
	}
}

bool LogAnalyzer::checkParsingQueueBuffer()
{
	bool ret = m_rawDatas.try_pop(m_rawData);
	return ret;
}

void LogAnalyzer::ClearParsedPacketData()
{
	m_parsedPackets.clear();
}

bool LogAnalyzer::parsingQueueBuffer()
{
	//PacketData data;

	////Capture된 패킷의 길이. Live 장치에서는 FrameLength를 얻을 수 없음.
	////https://github.com/seladb/PcapPlusPlus/issues/954
	//int rawlength = m_packet.getRawPacket()->getRawDataLen();
	//data.capturedLength = rawlength;

	//data.frameNumber = m_frameNumber++;
	////m_packet.toStringList(data.messages, true);
	//data.dateTime = m_packet.toString(true);
	//
	//std::string pattern = "Arrival time: ";
	//size_t pos = data.dateTime.find(pattern);
	//if (pos != -1)
	//{
	//	size_t pos2 = data.dateTime.find("\n");
	//	//Arrival time 중 마지막 3자리는 000을 의미해서 제거
	//	std::string time = data.dateTime.substr(pos + pattern.length(), pos2 - pattern.length() - pos - 3);
	//	data.dateTime = time;
	//}
	////if (data.messages.size() != 0)
	////{
	////	std::string pattern = "Arrival time: ";
	////	size_t pos = data.messages[0].find(pattern);
	////	if (pos != -1)
	////	{
	////		//Arrival time 중 마지막 3자리는 000을 의미해서 제거
	////		std::string time = data.messages[0].substr(pos + pattern.length(), data.messages[0].length() - pattern.length() - pos - 3);
	////		data.dateTime = time;
	////	}
	////}

	//pcpp::Layer* firstLayer = nullptr;
	//firstLayer = m_packet.getFirstLayer();

	//if (firstLayer != nullptr)
	//{
	//	data.protocol = getProtocolTypeAsString(firstLayer->getProtocol());
	//}

	//if (m_packet.isPacketOfType(pcpp::IPv4) == true)
	//{
	//	pcpp::IPv4Layer* ipv4Layer = nullptr;
	//	ipv4Layer = m_packet.getLayerOfType<pcpp::IPv4Layer>();
	//	if (ipv4Layer != nullptr)
	//	{
	//		pcpp::IPv4Address srcIP = ipv4Layer->getSrcIPv4Address();
	//		pcpp::IPv4Address dstIP = ipv4Layer->getDstIPv4Address();

	//		data.srcIPv4 = srcIP.toString();
	//		data.dstIPv4 = dstIP.toString();
	//	}
	//}

	////전송 메시지 확인
	//pcpp::PayloadLayer* payloadLayer = nullptr;
	//payloadLayer = m_packet.getLayerOfType<pcpp::PayloadLayer>();
	//if (payloadLayer != nullptr)
	//{
	//	int lenSize = payloadLayer->getDataLen();
	//	data.payloadLength = lenSize;

	//	uint8_t* ptr = nullptr;
	//	ptr = payloadLayer->getData();
	//	int length = payloadLayer->getDataLen();
	//	if (ptr != nullptr)
	//	{
	//		IPacket* packet = nullptr;

	//		if (m_isLoopback == true)
	//		{
	//			packet = new APIPacket((unsigned char*)ptr, length);
	//		}
	//		else
	//		{
	//			//2022-12-01
	//			//Hex <-> String 함수 대체 후 테스트 못 함.
	//			packet = new PLCPacket((unsigned char*)ptr, length);
	//		}

	//		//파싱된 데이터
	//		data.parsed = packet->GetParsedString();
	//		if (packet->IsParsingSuccess() == true)
	//		{
	//			//m_logger.AddBuffer(LogBuffer::Level::Debug, "패킷 파싱 성공");
	//		}
	//		else
	//		{
	//			//m_logger.AddBuffer(LogBuffer::Level::Debug, "패킷 파싱 실패");
	//		}

	//		if (packet != nullptr)
	//		{
	//			delete packet;
	//			packet = nullptr;
	//		}
	//		

	//		//byte to HexString 변환 함수
	//		/*std::stringstream ss;
	//		for (int i = 0; i < lenSize; i++)
	//		{
	//			unsigned int byte = static_cast<unsigned int>(ptr[i]);
	//			ss << std::setw(2) << std::setfill('0') << std::hex << (byte & 0xff) << "  ";
	//		}
	//		data.payload = ss.str();*/

	//		std::string temp = "";
	//		temp.resize(lenSize * 2);
	//		encodeHex((uint8_t*)temp.data(), (uint8_t*)ptr, lenSize);
	//		data.payloadHex = temp;

	//		std::string decode = "";
	//		decode.resize(temp.size() / 2);
	//		decodeHexLUT((uint8_t*)decode.data(), (uint8_t*)temp.data(), decode.size());
	//		data.payloadASCII = decode;
	//	}
	//}

	//pcpp::TcpLayer* tcpLayer = nullptr;
	//tcpLayer = m_packet.getLayerOfType<pcpp::TcpLayer>();
	//if (tcpLayer != nullptr)
	//{
	//	uint16_t should_be_checksum = tcpLayer->calculateChecksum(false);
	//	uint16_t captured_header_checksum = tcpLayer->getTcpHeader()->headerChecksum;
	//	uint16_t converted_header_checksum = _byteswap_ushort(captured_header_checksum);

	//	if (should_be_checksum == converted_header_checksum)
	//	{
	//		data.isTcpChecksumCorrect = true;
	//	}
	//	else
	//	{
	//		data.isTcpChecksumCorrect = false;
	//	}

	//	data.srcPort = std::to_string(tcpLayer->getSrcPort());
	//	data.dstPort = std::to_string(tcpLayer->getDstPort());

	//	data.flag = getTcpFlags(tcpLayer);

	//	data.sequenceNumber = _byteswap_ulong(tcpLayer->getTcpHeader()->sequenceNumber);
	//	data.acknowledgmentNumber = _byteswap_ulong(tcpLayer->getTcpHeader()->ackNumber);
	//}
	//else
	//{
	//	data.srcPort = "";
	//	data.dstPort = "";
	//}

	////udp 체크섬 확인하기
	//pcpp::UdpLayer* udpLayer = nullptr;
	//udpLayer = m_packet.getLayerOfType<pcpp::UdpLayer>();
	//if (udpLayer != nullptr)
	//{
	//	uint16_t should_be_checksum = udpLayer->calculateChecksum(false);
	//	uint16_t captured_header_checksum = udpLayer->getUdpHeader()->headerChecksum;
	//	uint16_t converted_header_checksum = _byteswap_ushort(captured_header_checksum);

	//	if (should_be_checksum == converted_header_checksum)
	//	{
	//		data.isUdpChecksumCorrect = true;
	//	}
	//	else
	//	{
	//		data.isUdpChecksumCorrect = false;
	//	}

	//	if (data.srcPort == "")
	//	{
	//		data.srcPort = std::to_string(udpLayer->getSrcPort());
	//	}
	//	if (data.dstPort == "")
	//	{
	//		data.dstPort = std::to_string(udpLayer->getDstPort());
	//	}
	//}

	//data.isKeepAlive = isKeepAlive();
	//data.isKeepAliveAck = isKeepAliveAck();

	//m_parsedPackets.push(data);

	//m_isLastPacketKeepAlive = data.isKeepAlive;
	//m_lastPacketPayloadLength = data.payloadLength;
	//if (tcpLayer != nullptr)
	//{
	//	m_lastPacketSequenceNumber = _byteswap_ulong(tcpLayer->getTcpHeader()->sequenceNumber);
	//}
	//else
	//	m_lastPacketSequenceNumber = 0;

	//bool ret = m_rawDatas.unsafe_size() == 0;

	//m_logger.AddBuffer(LogBuffer::Level::Debug, 
	//	"[패킷] SrcIP: " + data.srcIPv4 + ", SrcPort: " + data.srcPort + 
	//	", DstIP: " + data.dstIPv4 + ", DstPort: " + data.dstPort +
	//	", Payload Size: " + std::to_string(data.payloadLength) + 
	//	", Payload Hex Data: " + data.payloadHex + 
	//	", TCP Checksum: " + std::to_string(data.isTcpChecksumCorrect) +
	//	", UDP Checksum: " + std::to_string(data.isUdpChecksumCorrect));
	//return ret;

	return false;
}

//void LogAnalyzer::globalDumpingFunction(void* handle)
//{
//	LogAnalyzer* pApp = (LogAnalyzer*)handle;
//
//	while (g_isRunDumpingThread)
//	{
//		switch (g_stepDumping)
//		{
//			case SequenceStepDumping::StepWait:
//			{
//				DWORD ret = WaitForSingleObject(pApp->m_packetArrivedDumping, 1000);
//				if (ret == WAIT_OBJECT_0)
//				{
//					g_stepDumping = SequenceStepDumping::StepCheckDumpingQueueBufferCount;
//				}
//				break;
//			}
//			case SequenceStepDumping::StepCheckDumpingQueueBufferCount:
//			{
//				if (pApp->checkDumpingQueueBuffer() == true)
//				{
//					g_stepDumping = SequenceStepDumping::StepDumping;
//				}
//				else
//				{
//					g_stepDumping = SequenceStepDumping::StepWait;
//				}
//				break;
//			}
//
//			case SequenceStepDumping::StepDumping:
//			{
//				if (pApp->dumpingQueueBuffer() == true)
//				{
//					g_stepDumping = SequenceStepDumping::StepWait;
//				}
//				else
//				{
//					g_stepDumping = SequenceStepDumping::StepCheckDumpingQueueBufferCount;
//				}
//				break;
//			}
//		}
//	}
//}