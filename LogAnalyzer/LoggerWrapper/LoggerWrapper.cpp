#include "pch.h"

#include "LoggerWrapper.h"
using namespace WrapperLogger;

LoggerEx::LoggerEx()
{
	m_logger = new Logger();
}

LoggerEx::~LoggerEx()
{
	delete m_logger;
	m_logger = nullptr;
}

void LoggerEx::SetSavePath(System::String^ path)
{
	try
	{
		m_logger->SetSavePath(msclr::interop::marshal_as<std::string>(path));
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void LoggerEx::AddBuffer(const Level level, System::String^ message)
{
	try
	{
		m_logger->AddBuffer(static_cast<LogBuffer::Level>(level), msclr::interop::marshal_as<std::string>(message));
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void LoggerEx::SetMinimumLevel(const Level level)
{
	try
	{
		m_logger->SetMinimumLevel(static_cast<LogBuffer::Level>(level));
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

void LoggerEx::Close()
{
	try
	{
		m_logger->Close();
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}

System::IntPtr LoggerEx::handleTerminate::get()
{
	try
	{
		return (System::IntPtr)(void*)m_logger->GetHandleTerminate();
	}
	catch (const std::exception& err)
	{
		throw gcnew System::Exception(msclr::interop::marshal_as<System::String^>(err.what()));
	}
}