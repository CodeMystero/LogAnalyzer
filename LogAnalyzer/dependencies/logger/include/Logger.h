#pragma once
#include <Windows.h>
#include <fstream>
#include "LogBuffer.h"
//ofstream�� ������� write�ϴ� ����, C++���� �̹� �������� C#���� �� ���� ��Ȳ�� �߻�.
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

