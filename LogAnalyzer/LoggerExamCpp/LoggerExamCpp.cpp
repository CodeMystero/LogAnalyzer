// ExamConsole.cpp : 이 파일에는 'main' 함수가 포함됩니다. 거기서 프로그램 실행이 시작되고 종료됩니다.
//
#include <iostream>
#include "../include/Logger.h"
#include <fstream>

#include <chrono>
#include <fcntl.h>
#include <iostream>
#include <sys/stat.h>
#include <stdio.h>
#include <utility>
#include <vector>


int main()
{
    try
    {
        Logger logger;

        logger.SetSavePath("F:\\test");
        logger.SetMinimumLevel(LogBuffer::Level::Warn);

        logger.AddBuffer(LogBuffer::Level::Error, "테스트");
        Sleep(10);
        logger.AddBuffer(LogBuffer::Level::Warn, "message");
        Sleep(10);
        logger.AddBuffer(LogBuffer::Level::Debug, "message");
        Sleep(10);
        logger.AddBuffer(LogBuffer::Level::Info, "message");
        Sleep(10);

        std::ofstream writer("F:\\test.txt", std::ios_base::binary | std::ios_base::app);

        std::string msg = "테스트 TEST!!!!!\n";
        
        writer.write(msg.c_str(), msg.length());

        writer.close();

        const int file = open("out.dat", O_CREAT | O_WRONLY | O_DIRECT, 0600);

    }
    catch (const std::exception& exc)
    {
        std::cout << exc.what() << std::endl;
    }
}