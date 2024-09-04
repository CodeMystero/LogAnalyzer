#include "LogBuffer.h"
#include <chrono>
#include <sstream>
#include <iomanip>
#include <ctime>

LogBuffer::LogBuffer()
	: m_log("")
    , m_date("")
    , m_level(LogBuffer::Level::Debug)
{

}

LogBuffer::~LogBuffer()
{

}

void LogBuffer::SetData(const Level level, const std::string log)
{
    const auto now = std::chrono::system_clock::now();
    const auto nowAsTimeT = std::chrono::system_clock::to_time_t(now);
    const auto nowMs = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

    std::stringstream ss;
    ss << std::put_time(std::localtime(&nowAsTimeT), "%F");
    m_date = ss.str();
    ss.str("");

    m_level = level;
    std::string strLevel = toString(m_level);

    ss << std::put_time(std::localtime(&nowAsTimeT), "%F %T")
        << '.' << std::setfill('0') << std::setw(3) << nowMs.count() << " " << strLevel << " " << log;

    m_log = ss.str() + "\n";
}

std::string LogBuffer::GetData() const
{
    return m_log;
}

std::string LogBuffer::GetDate() const
{
    return m_date;
}

LogBuffer::Level LogBuffer::GetLevel() const
{
    return m_level;
}

std::string LogBuffer::toString(const LogBuffer::Level level) const
{
    std::string strLevel = "";
    switch (level)
    {
        case LogBuffer::Level::Error: strLevel = "ERROR"; break;
        case LogBuffer::Level::Warn: strLevel = "WARN"; break;
        case LogBuffer::Level::Debug: strLevel = "DEBUG"; break;
        case LogBuffer::Level::Info: strLevel = "INFO"; break;
    }

    return strLevel;
}