#include "pch.h"

#include "PacketAnalyzerWrapper.h"

using namespace WrapperPacketAnalyzer;
using namespace System;
using namespace System::Collections::Generic;

List<PacketAnalyzerWrapper::DeviceInfoWrapper^>^ PacketAnalyzerWrapper::GetDevices()
{
	try
	{
		std::vector<LogAnalyzer::DeviceInfo> native_devices = LogAnalyzer::GetDevices();
		List<PacketAnalyzerWrapper::DeviceInfoWrapper^>^ wrapper_devices = gcnew List<PacketAnalyzerWrapper::DeviceInfoWrapper^>();

		for (const auto &native_device : native_devices)
		{
			PacketAnalyzerWrapper::DeviceInfoWrapper^ wrapper_data = gcnew PacketAnalyzerWrapper::DeviceInfoWrapper();
			wrapper_data->index = native_device.index;
			wrapper_data->ipv4 = msclr::interop::marshal_as<System::String^>(native_device.ipv4);
			wrapper_data->name = msclr::interop::marshal_as<System::String^>(native_device.name);

			wrapper_devices->Add(wrapper_data);
		}

		return wrapper_devices;
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

PacketAnalyzerWrapper::PacketAnalyzerWrapper()
{
	m_device = new LogAnalyzer();
}

PacketAnalyzerWrapper::~PacketAnalyzerWrapper()
{
	delete m_device;
	m_device = nullptr;
}

bool PacketAnalyzerWrapper::Open(System::String^ ipv4, bool promiscuousMode)
{
	try
	{
		std::string temp = msclr::interop::marshal_as<std::string>(ipv4);
		return m_device->Open(temp, promiscuousMode);
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

bool PacketAnalyzerWrapper::Open(int index, bool promiscuousMode)
{
	try
	{
		return m_device->Open(index, promiscuousMode);
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

bool PacketAnalyzerWrapper::Close()
{
	try
	{
		return m_device->Close();
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

bool PacketAnalyzerWrapper::StartDump(System::String^ path)
{
	try
	{
		return m_device->StartDump(msclr::interop::marshal_as<std::string>(path));
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void PacketAnalyzerWrapper::StopDump()
{
	try
	{
		return m_device->StopDump();
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

bool PacketAnalyzerWrapper::StartCapture()
{
	try
	{
		return m_device->StartCapture();
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void PacketAnalyzerWrapper::StopCapture()
{
	try
	{
		m_device->StopCapture();
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

bool PacketAnalyzerWrapper::SetFilterIPv4(System::String^ ipv4)
{
	try
	{
		return m_device->SetFilterIPv4(msclr::interop::marshal_as<std::string>(ipv4));
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void PacketAnalyzerWrapper::SetSaveLogPath(System::String^ path)
{
	try
	{
		return m_device->SetSaveLogPath(msclr::interop::marshal_as<std::string>(path));
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void PacketAnalyzerWrapper::SetLogLevel(LevelWrapper level)
{
	try
	{
		return m_device->SetLogLevel(static_cast<LogBuffer::Level>(level));
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void PacketAnalyzerWrapper::ClearParsedPacketData()
{
	try
	{
		return m_device->ClearParsedPacketData();
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

int PacketAnalyzerWrapper::GetNumberOfParsedPacketData::get()
{
	try
	{
		return m_device->GetNumberOfParsedPacketData();
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

bool PacketAnalyzerWrapper::IsOpened::get()
{
	try
	{
		return m_device->IsOpened();
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

bool PacketAnalyzerWrapper::IsCaptured::get()
{
	try
	{
		return m_device->IsCaptured();
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

PacketAnalyzerWrapper::PacketDataWrapper^ PacketAnalyzerWrapper::GetParsedPacketData()
{
	try
	{
		PacketAnalyzerWrapper::PacketDataWrapper^ wrapper_data = gcnew PacketAnalyzerWrapper::PacketDataWrapper();

		LogAnalyzer::PacketData native_data = m_device->GetParsedPacketData();

		wrapper_data->payloadLength = native_data.payloadLength;
		wrapper_data->dstIPv4 = msclr::interop::marshal_as<System::String^>(native_data.dstIPv4);
		wrapper_data->capturedLength = native_data.capturedLength;
		wrapper_data->frameNumber = native_data.frameNumber;
		wrapper_data->sequenceNumber = native_data.sequenceNumber;
		wrapper_data->acknowledgmentNumber = native_data.acknowledgmentNumber;
		wrapper_data->dateTime = msclr::interop::marshal_as<System::String^>(native_data.dateTime);
		wrapper_data->srcPort = msclr::interop::marshal_as<System::String^>(native_data.srcPort);
		wrapper_data->dstPort = msclr::interop::marshal_as<System::String^>(native_data.dstPort);
		wrapper_data->flag = msclr::interop::marshal_as<System::String^>(native_data.flag);
		wrapper_data->payloadHex = msclr::interop::marshal_as<System::String^>(native_data.payloadHex);
		wrapper_data->payloadASCII = msclr::interop::marshal_as<System::String^>(native_data.payloadASCII);
		wrapper_data->protocol = msclr::interop::marshal_as<System::String^>(native_data.protocol);
		wrapper_data->srcIPv4 = msclr::interop::marshal_as<System::String^>(native_data.srcIPv4);
		wrapper_data->isValid = native_data.isValid;
		wrapper_data->isTcpChecksumCorrect = native_data.isTcpChecksumCorrect;
		wrapper_data->isUdpChecksumCorrect = native_data.isUdpChecksumCorrect;
		wrapper_data->isKeepAlive = native_data.isKeepAlive;
		wrapper_data->isKeepAliveAck = native_data.isKeepAliveAck;
		
		List<String^>^ wrapper_messages = gcnew List<String^>();
		for (const auto &native_message : native_data.messages)
			wrapper_messages->Add(msclr::interop::marshal_as<System::String^>(native_message));

		wrapper_data->messages = wrapper_messages;

		List<String^>^ wrapper_parsed = gcnew List<String^>();
		for (const auto& native_parsed : native_data.parsed)
			wrapper_parsed->Add(msclr::interop::marshal_as<System::String^>(native_parsed));
		
		wrapper_data->parsed = wrapper_parsed;

		return wrapper_data;
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

BlockingCollection<PacketAnalyzerWrapper::PacketDataWrapper^>^ PacketAnalyzerWrapper::GetParsedPacketDatas()
{
	try
	{
		BlockingCollection<PacketAnalyzerWrapper::PacketDataWrapper^>^ wrapper_datas = gcnew BlockingCollection<PacketAnalyzerWrapper::PacketDataWrapper^>();

		int size = m_device->GetNumberOfParsedPacketData();
		for (int i = 0; i < size; i++)
		{
			LogAnalyzer::PacketData native_data = m_device->GetParsedPacketData();

			PacketAnalyzerWrapper::PacketDataWrapper^ wrapper_data = gcnew PacketAnalyzerWrapper::PacketDataWrapper();
			wrapper_data->payloadLength = native_data.payloadLength;
			wrapper_data->dstIPv4 = msclr::interop::marshal_as<System::String^>(native_data.dstIPv4);
			wrapper_data->payloadLength = native_data.capturedLength;
			wrapper_data->sequenceNumber = native_data.sequenceNumber;
			wrapper_data->acknowledgmentNumber = native_data.acknowledgmentNumber;
			wrapper_data->frameNumber = native_data.frameNumber;
			wrapper_data->dateTime = msclr::interop::marshal_as<System::String^>(native_data.dateTime);
			wrapper_data->srcPort = msclr::interop::marshal_as<System::String^>(native_data.srcPort);
			wrapper_data->dstPort = msclr::interop::marshal_as<System::String^>(native_data.dstPort);
			wrapper_data->payloadHex = msclr::interop::marshal_as<System::String^>(native_data.payloadHex);
			wrapper_data->payloadASCII = msclr::interop::marshal_as<System::String^>(native_data.payloadASCII);
			wrapper_data->flag = msclr::interop::marshal_as<System::String^>(native_data.flag);
			wrapper_data->protocol = msclr::interop::marshal_as<System::String^>(native_data.protocol);
			wrapper_data->srcIPv4 = msclr::interop::marshal_as<System::String^>(native_data.srcIPv4);
			wrapper_data->isValid = native_data.isValid;
			wrapper_data->isTcpChecksumCorrect = native_data.isTcpChecksumCorrect;
			wrapper_data->isUdpChecksumCorrect = native_data.isUdpChecksumCorrect;
			wrapper_data->isKeepAlive = native_data.isKeepAlive;
			wrapper_data->isKeepAliveAck = native_data.isKeepAliveAck;

			List<String^>^ wrapper_messages = gcnew List<String^>();
			for (const auto &native_message : native_data.messages)
				wrapper_messages->Add(msclr::interop::marshal_as<System::String^>(native_message));

			wrapper_data->messages = wrapper_messages;

			List<String^>^ wrapper_parsed = gcnew List<String^>();
			for (const auto& native_parsed : native_data.parsed)
				wrapper_parsed->Add(msclr::interop::marshal_as<System::String^>(native_parsed));
			
			wrapper_data->parsed = wrapper_parsed;

			wrapper_datas->Add(wrapper_data);
		}
		
		return wrapper_datas;
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

PacketAnalyzerWrapper::DeviceStatisticsWrapper^ PacketAnalyzerWrapper::GetDeviceStatistics()
{
	try
	{
		PacketAnalyzerWrapper::DeviceStatisticsWrapper^ wrapper_data = gcnew PacketAnalyzerWrapper::DeviceStatisticsWrapper();

		LogAnalyzer::DeviceStatistics native_data = m_device->GetDeviceStatistics();

		wrapper_data->packetsRecv = native_data.packetsRecv;
		wrapper_data->packetsDrop = native_data.packetsDrop;
		wrapper_data->packetsDropByInterface = native_data.packetsDropByInterface;

		return wrapper_data;
	}
	catch (const std::exception &err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}