#include "Logger.h"

#include <filesystem>
//#include <fstream>
#include <thread>
#include <concurrent_queue.h>
#include <ctime>
#include <sstream>
#include <iostream>
namespace fs = std::filesystem;

std::thread* g_loggerThread = nullptr;
bool g_isRunLoggerThread = false;
Concurrency::concurrent_queue<LogBuffer> g_buffers;

Logger::Logger()
	: m_step(SequenceStep::StepWait)
{
	g_isRunLoggerThread = true;
	g_loggerThread = new std::thread(globalFunction, this);

	m_savePath = fs::current_path().generic_string();

	tm info;
	time_t m_time(NULL);
	time(&m_time);
	localtime_s(&info, &m_time);
	std::stringstream ss;
	ss << std::put_time(&info, "%F");
	m_fileName = ss.str() + ".txt";
	
	m_bufferHandle = CreateEvent(NULL, FALSE, FALSE, NULL);
	m_terminateHandle = CreateEvent(NULL, FALSE, FALSE, NULL);
	//m_writer.open(m_savePath + "\\" + m_fileName, std::ios_base::app);
}

Logger::~Logger()
{
	Close();
}

void Logger::Close()
{
	SetEvent(m_bufferHandle);

	g_isRunLoggerThread = false;
	if (g_loggerThread != nullptr)
	{
		g_loggerThread->join();
		g_loggerThread = nullptr;
	}

	//m_writer.close();

	g_buffers.clear();
}

void Logger::SetSavePath(const std::string path)
{
	if (fs::exists(path) == false)
		fs::create_directories(path);

	m_savePath = path;

	/*if (m_writer.is_open() == true)
		m_writer.close();
	
	m_writer.open(m_savePath + "\\" + m_fileName, std::ios_base::app);*/
}

void Logger::AddBuffer(const LogBuffer::Level level, const std::string message)
{
	LogBuffer buffer;
	buffer.SetData(level, message);
	g_buffers.push(buffer);

	SetEvent(m_bufferHandle);
}

void Logger::SetMinimumLevel(const LogBuffer::Level level)
{
	m_minLevel = level;
}

bool Logger::checkQueueBuffer()
{
	return g_buffers.unsafe_size() != 0;
}

void Logger::saveQueueBuffer()
{
	size_t counts = g_buffers.unsafe_size();
	for (size_t i = 0; i < counts; i++)
	{
		LogBuffer buffer;
		if (g_buffers.try_pop(buffer) == true)
		{
			auto level = buffer.GetLevel();
			if (level <= m_minLevel)
				writeToFile(buffer);
		}
	}
}

void Logger::writeToFile(const LogBuffer& buffer)
{
	//시간이 오래 걸림
	//std::string date =  buffer.GetDate();
	//std::string name = date + ".txt";
	//std::string fileName = m_savePath + "\\" + name;
	//std::ofstream writer(fileName, std::ios_base::app); //overwrite
	//if (writer.is_open() == true)
	//{
	//	writer.write(buffer.GetData().c_str(), buffer.GetData().length());
	//	writer.close();
	//}

	/// 
	//작업 중 다른 곳에서 같은 파일을 접근할 수 없음
	/*std::string date =  buffer.GetDate();
	std::string name = date + ".txt";
	if (m_fileName != name)
	{
		m_fileName = name;

		if (m_writer.is_open() == true)
			m_writer.close();

		m_writer.open(m_savePath + "\\" + m_fileName, std::ios_base::app);
	}

	m_writer.write(buffer.GetData().c_str(), buffer.GetData().length());*/

	///

	std::string date =  buffer.GetDate();
	std::string name = date + ".txt";
	std::string fileName = m_savePath + "\\" + name;
	HANDLE hFile = NULL;
	DWORD nWritten;
	hFile = ::CreateFileA(fileName.c_str(), GENERIC_WRITE, FILE_SHARE_READ, NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if (INVALID_HANDLE_VALUE != hFile)
	{
		::SetFilePointer(hFile, 0, NULL, FILE_END);
		::WriteFile(hFile, buffer.GetData().c_str(), buffer.GetData().length(), &nWritten, NULL);
		::CloseHandle(hFile);
	}
}

void Logger::globalFunction(void* handle)
{
	Logger* pApp = (Logger*)handle;

	while (g_isRunLoggerThread)
	{
		switch (pApp->m_step)
		{
			case SequenceStep::StepWait:
			{
				DWORD ret = WaitForSingleObject(pApp->m_bufferHandle, 100);
				if (ret == WAIT_OBJECT_0)
				{
					pApp->m_step = SequenceStep::StepCheckQueueBufferCount;
				}
				break;
			}
			case SequenceStep::StepCheckQueueBufferCount:
			{
				if (pApp->checkQueueBuffer() == true)
				{
					pApp->m_step = SequenceStep::StepSave;
				}
				else
				{
					pApp->m_step = SequenceStep::StepWait;
				}
				break;
			}

			case SequenceStep::StepSave:
			{
				pApp->saveQueueBuffer();
				
				pApp->m_step = SequenceStep::StepWait;
				break;
			}
		}
	}

	SetEvent(pApp->m_terminateHandle);
}

HANDLE Logger::GetHandleTerminate() const
{
	return m_terminateHandle;
}