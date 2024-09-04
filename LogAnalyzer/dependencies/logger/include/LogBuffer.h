#pragma once
#define _CRT_SECURE_NO_WARNINGS
#include <string>

class LogBuffer
{
public:
	enum Level { Error, Warn, Debug, Info };

	LogBuffer();
	virtual ~LogBuffer();

	void SetData(const Level level, const std::string log);
	std::string GetData() const;
	std::string GetDate() const;
	Level GetLevel() const;
private:
	std::string m_log;
	std::string m_date;
	Level m_level;
	std::string toString(const Level level) const;
};

