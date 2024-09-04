#pragma once

#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include "hex.h"
#include "IBlockType.h"

class IPacket
{
public:
    IPacket(unsigned char* ptr, unsigned int length)
    {
        this->ptr = ptr;
        this->length = length;
        this->isSuccess = false;
    }

    virtual std::vector<std::string> GetParsedString() = 0;

    bool IsParsingSuccess() { return this->isSuccess; }
protected:
    unsigned char* ptr;
    unsigned int length;
    bool isSuccess;

    std::string convertHexToString(std::string hexString)
    {
        std::string str = "";
        for (int i = 0; i < hexString.length(); i += 2)
        {
            std::string byte = hexString.substr(i, 2);
            char chr = (char)(int)strtol(byte.c_str(), nullptr, 16);
            str.push_back(chr);
        }

        return str;
    }

    std::string convertPointerToHexString()
    {
        std::stringstream ss;

        if (ptr != nullptr)
        {
            for (int i = 0; i < length; i++)
            {
                unsigned int byte = static_cast<unsigned int>(ptr[i]);
                ss << std::setw(2) << std::setfill('0') << std::hex << (byte & 0xff);
            }
        }

        return ss.str();
    }
};

class PLCPacket : public IPacket
{
public:
    PLCPacket(unsigned char* ptr, unsigned int length) : IPacket(ptr, length)
    {

    }

    std::vector<std::string> GetParsedString() override
    {
        std::vector<std::string> parsed;
        if (ptr == nullptr) return parsed;

        //\0 문자 때문에 hex string 변환 후 파싱 시작
        //std::string data = convertPointerToHexString();

        std::string data = "";
        data.resize(length * 2);
        encodeHex((uint8_t*)data.data(), (uint8_t*)ptr, length);
        
        std::string result = "";
        size_t pos = data.find("4c5f"); //4c5f: L_
        if (pos != -1)
        {
            if (data.length() >= 10)
            {
                std::string tmp = data.substr(pos + 4, 16);

                std::string decode = "";
                decode.resize(8);
                decodeHexLUT((uint8_t*)decode.data(), (uint8_t*)tmp.data(), decode.size());
                tmp = decode;
                //tmp = convertHexToString(tmp);
                pos = data.find("43454c4c"); //43454c4c: CELL
                if (pos != -1)
                {
                    if (this->length * 2 > pos + 8)
                    {
                        parsed.push_back("Date: " + tmp.substr(0, 4) + "-" + tmp.substr(4, 2) + "-" + tmp.substr(6, 2));
                        
                        tmp = data.substr(pos + 8, this->length - (pos + 8));
                        decode = "";
                        decode.reserve((this->length - (pos + 8)) / 2);
                        decodeHexLUT((uint8_t*)decode.data(), (uint8_t*)tmp.data(), decode.size());
                        tmp = decode;
                        //tmp = convertHexToString(tmp);
                        parsed.push_back("Cell: " + tmp);

                        this->isSuccess = true;
                    }
                }
            }
        }

        return parsed;
    }
};

class APIPacket : public IPacket
{
public:
    APIPacket(unsigned char* ptr, unsigned int length) : IPacket(ptr, length)
    {

    }

    std::vector<std::string> GetParsedString() override
    {
        std::vector<std::string> parsed;
        Header* header = nullptr;
        Cell* cell = nullptr;

        if (ptr == nullptr) return parsed;
        if (length <= (sizeof(Header) + sizeof(Cell)))
        {
            std::string temp = "";
            temp.resize(length * 2);
            encodeHex((uint8_t*)temp.data(), (uint8_t*)ptr, length);
            parsed.push_back("Payload: " + temp);
            //parsed.push_back("Payload: " + convertPointerToHexString());
            parsed.push_back("Length: " + std::to_string(length));
            return parsed;
        }

        header = (Header*)ptr;
        if (header == nullptr)
        {
            std::string temp = "";
            temp.resize(length * 2);
            encodeHex((uint8_t*)temp.data(), (uint8_t*)ptr, length);
            parsed.push_back("Payload: " + temp);
            //parsed.push_back("Payload: " + convertPointerToHexString());
            parsed.push_back("Length: " + std::to_string(length));
            return parsed;
        }

        int totalLength = getTotalLength(header->H4);
        if (totalLength == 0)
        {
            std::string temp = "";
            temp.resize(length * 2);
            encodeHex((uint8_t*)temp.data(), (uint8_t*)ptr, length);
            parsed.push_back("Payload: " + temp);
            //parsed.push_back("Payload: " + convertPointerToHexString());
            parsed.push_back("Length: " + std::to_string(length));
            return parsed;
        }

        //totalLength와 length가 맞지 않는 경우가 있음...
        /*if (length != totalLength)
        {
            parsed.push_back("Payload: " + convertPointerToHexString());
            parsed.push_back("Length: " + std::to_string(length));
            return parsed;
        }*/

        cell = (Cell*)(ptr + sizeof(Header));
        if (cell == nullptr)
        {
            std::string temp = "";
            temp.resize(length * 2);
            encodeHex((uint8_t*)temp.data(), (uint8_t*)ptr, length);
            parsed.push_back("Payload: " + temp);
            //parsed.push_back("Payload: " + convertPointerToHexString());
            parsed.push_back("Length: " + std::to_string(length));
            return parsed;
        }

        //H1~H4
        parsed.push_back("H1: " + std::to_string(header->H1));
        parsed.push_back("H2: " + std::to_string(header->H2));
        parsed.push_back("H3: " + std::to_string(header->H3));
        parsed.push_back("H4: " + std::to_string(header->H4));
        //C1~C5
        parsed.push_back("C1: " + std::to_string(cell->C1));
        parsed.push_back("C2: " + std::to_string(cell->C2));
        parsed.push_back("C3: " + std::string((char*)cell->C3));
        parsed.push_back("C4: " + std::string((char*)cell->C4));
        parsed.push_back("C5: " + std::string((char*)cell->C5));
        //Variable Data
        std::vector<std::string> datas = getParsedVariableData(header->H4, header->H1); //H1의 의미를 모르겠음
        for (auto& data : datas)
        {
            parsed.push_back(data);
        }

        this->isSuccess = true;

        return parsed;
    }

private:
    std::vector<std::string> getParsedVariableData(unsigned int type, unsigned int length)
    {
        std::vector<std::string> data;
        if (length <= 0) return data;

        IBlockType* blockType = nullptr;
        switch (type)
        {
            case 2:
                blockType = new BlockType2(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 34:
                blockType = new BlockType34(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 36:
                blockType = new BlockType36(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 1002:
                blockType = new BlockType1002(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 1004:
                blockType = new BlockType1004(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 1007:
                blockType = new BlockType1007(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 1008:
                blockType = new BlockType1008(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 1010:
                blockType = new BlockType1010(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 1012:
                blockType = new BlockType1012(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 1034:
                blockType = new BlockType1034(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 2001:
                blockType = new BlockType2001(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 2002:
                blockType = new BlockType2002(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 2004:
                blockType = new BlockType2004(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 3002:
                blockType = new BlockType3002(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 3004:
                blockType = new BlockType3004(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 4002:
                blockType = new BlockType4002(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 4004:
                blockType = new BlockType4004(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65002:
                blockType = new BlockType65002(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65004:
                blockType = new BlockType65004(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65006:
                blockType = new BlockType65006(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65008:
                blockType = new BlockType65008(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65010:
                blockType = new BlockType65010(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65012:
                blockType = new BlockType65012(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65014:
                blockType = new BlockType65014(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65016:
                blockType = new BlockType65016(ptr + sizeof(Header) + sizeof(Cell));
                break;

            case 65534:
                blockType = new BlockType65534(ptr + sizeof(Header) + sizeof(Cell));
                break;

            default:
                break;
        }

        if (blockType != nullptr)
        {
            data = blockType->ToString();
            
            delete blockType;
            blockType = nullptr;
        }

        return data;
    }

    int getTotalLength(unsigned int type)
    {
        int length = 0;
        switch (type)
        {
            case 2: length = 100; break;
            case 34: length = 100; break;
            case 36: length = 100; break;
            case 1002: length = 100; break;
            case 1004: length = 100; break;
            case 1007: length = 100; break;
            case 1008: length = 100; break;
            case 1010: length = 140; break;
            case 1012: length = 146; break;
            case 1034: length = 100; break;
            case 2001: length = 100; break;
            case 2002: length = 100; break;
            case 3002: length = 100; break;
            case 3004: length = 100; break;
            case 4002: length = 872; break;
            case 4004: length = 100; break;
            case 65002: length = 100; break;
            case 65004: length = 162; break;
            case 65006: length = 826; break;
            case 65008: length = 100; break;
            case 65010: length = 100; break;
            case 65012: length = 100; break;
            case 65014: length = 128; break;
            case 65016: length = 954; break;
            case 65534: length = 100; break;
            default: length = 0; break;
        }

        return length;
    }

private:
    struct Header
    {
        unsigned short H1;
        unsigned short H2;
        unsigned short H3;
        unsigned short H4;
    };

    struct Cell
    {
        unsigned short C1;
        unsigned short C2;
        unsigned char C3[10];
        unsigned char C4[10];
        unsigned char C5[10];
    };
};