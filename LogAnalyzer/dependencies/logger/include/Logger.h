#pragma once
#include <Windows.h>
#include <fstream>
#include "LogBuffer.h"
//ofstream을 열어놓고 write하다 보니, C++에서 이미 열었으면 C#에서 못 여는 상황이 발생.
class Logger
{
public :
	enum class SequenceStep
	{
		StepWait = 0,
		StepCheckQueueBufferCount,
		StepSave
	};
public:
	Logger();
	virtual ~Logger();

	void SetSavePath(const std::string path);
	void AddBuffer(const LogBuffer::Level level, const std::string message);
	void SetMinimumLevel(const LogBuffer::Level level);
	void Close();
	HANDLE GetHandleTerminate() const;
private:
	static void globalFunction(void* handle);
	void saveQueueBuffer();
	bool checkQueueBuffer();
	void writeToFile(const LogBuffer &buffer);
	HANDLE m_bufferHandle;
	HANDLE m_terminateHandle;
	std::string m_savePath;
	LogBuffer::Level m_minLevel;
	SequenceStep m_step;
	std::ofstream m_writer;
	std::string m_fileName;
};

