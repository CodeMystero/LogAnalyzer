#pragma once
#include <vector>
#include <string>

class IBlockType
{
public:
    IBlockType(unsigned char* ptr)
    {
        this->ptr = ptr;
    }

    virtual std::vector<std::string> ToString() = 0;

protected:
    unsigned char* ptr;
};

class BlockType2 : public IBlockType
{
public:
    BlockType2(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare, 58));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare[58];
    };
};

class BlockType34 : public IBlockType
{
public:
    BlockType34(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;
        
        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("BCD: " + std::to_string(block->BCD));
            data.push_back("GrabCount: " + std::to_string(block->GrabCount));
            data.push_back("Encoder: " + std::to_string(block->Encoder));
            data.push_back("Spare: " + std::string((char*)block->spare, 46));
        }

        return data;
    }

private:
    struct BlockType 
    {
        long BCD;
        long GrabCount;
        long Encoder;
        unsigned char spare[46];
    };
};

class BlockType36 : public IBlockType
{
public:
    BlockType36(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare1, 8));
            data.push_back("Encoder: " + std::to_string(block->Encoder));
            data.push_back("Spare: " + std::string((char*)block->spare2, 46));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare1[8];
        long Encoder;
        unsigned char spare2[46];
    };
};

class BlockType1002 : public IBlockType
{
public:
    BlockType1002(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare, 58));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare[58];
    };
};

class BlockType1004 : public IBlockType
{
public:
    BlockType1004(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare, 58));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare[58];
    };
};

class BlockType1007 : public IBlockType
{
public:
    BlockType1007(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("BCD: " + std::to_string(block->BCD));
            data.push_back("Data1: " + std::to_string(block->Data1));
            data.push_back("Data1: " + std::to_string(block->Data2));
            data.push_back("Data1: " + std::to_string(block->Data3));
            data.push_back("Data1: " + std::to_string(block->Data4));
            data.push_back("Data1: " + std::to_string(block->Data5));
            data.push_back("Data1: " + std::to_string(block->Data6));
            data.push_back("Data1: " + std::to_string(block->Data7));
            data.push_back("Data1: " + std::to_string(block->Data8));
            data.push_back("Spare: " + std::string((char*)block->spare, 24));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned short BCD;
        unsigned long Data1;
        unsigned long Data2;
        unsigned long Data3;
        unsigned long Data4;
        unsigned long Data5;
        unsigned long Data6;
        unsigned long Data7;
        unsigned long Data8;
        unsigned char spare[24];
    };
};

class BlockType1008 : public IBlockType
{
public:
    BlockType1008(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell1 BCD: " + std::string((char*)block->Cell1BCD, 10));
            data.push_back("Cell1 Data1: " + std::to_string(block->Cell1Data1));
            data.push_back("Cell1 Data2: " + std::to_string(block->Cell1Data2));
            data.push_back("Cell1 Data3: " + std::to_string(block->Cell1Data3));
            data.push_back("Cell1 Data4: " + std::to_string(block->Cell1Data4));
            data.push_back("Cell2 BCD: " + std::string((char*)block->Cell2BCD, 10));
            data.push_back("Cell2 Data1: " + std::to_string(block->Cell2Data1));
            data.push_back("Cell2 Data2: " + std::to_string(block->Cell2Data2));
            data.push_back("Cell2 Data3: " + std::to_string(block->Cell2Data3));
            data.push_back("Cell2 Data4: " + std::to_string(block->Cell2Data4));
            data.push_back("spare: " + std::string((char*)block->spare, 6));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char Cell1BCD[10];
        unsigned long Cell1Data1;
        unsigned long Cell1Data2;
        unsigned long Cell1Data3;
        unsigned long Cell1Data4;
        unsigned char Cell2BCD[10];
        unsigned long Cell2Data1;
        unsigned long Cell2Data2;
        unsigned long Cell2Data3;
        unsigned long Cell2Data4;
        unsigned char spare[6];
    };
};

class BlockType1010 : public IBlockType
{
public:
    BlockType1010(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell1 BCD: " + std::string((char*)block->Cell1BCD, 10));
            data.push_back("Cell1 Data1: " + std::to_string(block->Cell1Data1));
            data.push_back("Cell1 Data2: " + std::to_string(block->Cell1Data2));
            data.push_back("Cell1 Data3: " + std::to_string(block->Cell1Data3));
            data.push_back("Cell1 Data4: " + std::to_string(block->Cell1Data4));
            data.push_back("Cell1 Data5: " + std::to_string(block->Cell1Data5));
            data.push_back("Cell1 Data6: " + std::to_string(block->Cell1Data6));
            data.push_back("Cell1 Data7: " + std::to_string(block->Cell1Data7));
            data.push_back("Cell1 Data8: " + std::to_string(block->Cell1Data8));
            data.push_back("Cell2 BCD: " + std::string((char*)block->Cell2BCD, 10));
            data.push_back("Cell2 Data1: " + std::to_string(block->Cell2Data1));
            data.push_back("Cell2 Data2: " + std::to_string(block->Cell2Data2));
            data.push_back("Cell2 Data3: " + std::to_string(block->Cell2Data3));
            data.push_back("Cell2 Data4: " + std::to_string(block->Cell2Data4));
            data.push_back("Cell2 Data5: " + std::to_string(block->Cell2Data5));
            data.push_back("Cell2 Data6: " + std::to_string(block->Cell2Data6));
            data.push_back("Cell2 Data7: " + std::to_string(block->Cell2Data7));
            data.push_back("Cell2 Data8: " + std::to_string(block->Cell2Data8));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char Cell1BCD[10];
        unsigned long Cell1Data1;
        unsigned long Cell1Data2;
        unsigned long Cell1Data3;
        unsigned long Cell1Data4;
        unsigned long Cell1Data5;
        unsigned long Cell1Data6;
        unsigned long Cell1Data7;
        unsigned long Cell1Data8;
        unsigned char Cell2BCD[10];
        unsigned long Cell2Data1;
        unsigned long Cell2Data2;
        unsigned long Cell2Data3;
        unsigned long Cell2Data4;
        unsigned long Cell2Data5;
        unsigned long Cell2Data6;
        unsigned long Cell2Data7;
        unsigned long Cell2Data8;
    };
};

class BlockType1012 : public IBlockType
{
public:
    BlockType1012(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell1 BCD: " + std::string((char*)block->Cell1BCD, 10));
            data.push_back("Cell1 Data1: " + std::to_string(block->Cell1Data1));
            data.push_back("Cell1 Data2: " + std::to_string(block->Cell1Data2));
            data.push_back("Cell1 Data3: " + std::to_string(block->Cell1Data3));
            data.push_back("Cell1 Data4: " + std::to_string(block->Cell1Data4));
            data.push_back("Cell1 Data5: " + std::to_string(block->Cell1Data5));
            data.push_back("Cell1 Data6: " + std::to_string(block->Cell1Data6));
            data.push_back("Cell1 Data7: " + std::to_string(block->Cell1Data7));
            data.push_back("Cell1 Data8: " + std::to_string(block->Cell1Data8));
            data.push_back("Cell2 BCD: " + std::string((char*)block->Cell2BCD, 10));
            data.push_back("Cell2 Data1: " + std::to_string(block->Cell2Data1));
            data.push_back("Cell2 Data2: " + std::to_string(block->Cell2Data2));
            data.push_back("Cell2 Data3: " + std::to_string(block->Cell2Data3));
            data.push_back("Cell2 Data4: " + std::to_string(block->Cell2Data4));
            data.push_back("Cell2 Data5: " + std::to_string(block->Cell2Data5));
            data.push_back("Cell2 Data6: " + std::to_string(block->Cell2Data6));
            data.push_back("Cell2 Data7: " + std::to_string(block->Cell2Data7));
            data.push_back("Cell2 Data8: " + std::to_string(block->Cell2Data8));
            data.push_back("Vision Cell1 BCD: " + std::string((char*)block->VisionCell1BCD, 10));
            data.push_back("Vision Cell2 BCD: " + std::string((char*)block->VisionCell2BCD, 10));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char Cell1BCD[10];
        unsigned long Cell1Data1;
        unsigned long Cell1Data2;
        unsigned long Cell1Data3;
        unsigned long Cell1Data4;
        unsigned long Cell1Data5;
        unsigned long Cell1Data6;
        unsigned long Cell1Data7;
        unsigned long Cell1Data8;
        unsigned char Cell2BCD[10];
        unsigned long Cell2Data1;
        unsigned long Cell2Data2;
        unsigned long Cell2Data3;
        unsigned long Cell2Data4;
        unsigned long Cell2Data5;
        unsigned long Cell2Data6;
        unsigned long Cell2Data7;
        unsigned long Cell2Data8;
        unsigned char VisionCell1BCD[10];
        unsigned char VisionCell2BCD[10];
    };
};

class BlockType1034 : public IBlockType
{
public:
    BlockType1034(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cutter Counter: " + std::to_string(block->counter));
            data.push_back("Spare: " + std::string((char*)block->spare, 54));
        }

        return data;
    }

private:
    struct BlockType
    {
        long counter;
        unsigned char spare[54];
    };
};

class BlockType2001 : public IBlockType
{
public:
    BlockType2001(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Result: " + std::to_string(block->result));
            data.push_back("Vision AA: " + std::string((char*)block->VisionAA, 2));
            data.push_back("Vision BB: " + std::string((char*)block->VisionBB, 2));
            data.push_back("Vision CC: " + std::string((char*)block->VisionCC, 2));
            data.push_back("Vision DD: " + std::string((char*)block->VisionDD, 2));
            data.push_back("Vision EE: " + std::string((char*)block->VisionEE, 2));
            data.push_back("Vision FF: " + std::string((char*)block->VisionFF, 2));
            data.push_back("Vision GG: " + std::string((char*)block->VisionGG, 2));
            data.push_back("Spare: " + std::string((char*)block->spare, 42));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned short result;
        unsigned char VisionAA[2];
        unsigned char VisionBB[2];
        unsigned char VisionCC[2];
        unsigned char VisionDD[2];
        unsigned char VisionEE[2];
        unsigned char VisionFF[2];
        unsigned char VisionGG[2];
        unsigned char spare[42];
    };
};

class BlockType2002 : public IBlockType
{
public:
    BlockType2002(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Result: " + std::to_string(block->result));
            data.push_back("Vision AA: " + std::string((char*)block->VisionAA, 2));
            data.push_back("Vision BB: " + std::string((char*)block->VisionBB, 2));
            data.push_back("Vision CC: " + std::string((char*)block->VisionCC, 2));
            data.push_back("Vision DD: " + std::string((char*)block->VisionDD, 2));
            data.push_back("Vision EE: " + std::string((char*)block->VisionEE, 2));
            data.push_back("Vision FF: " + std::string((char*)block->VisionFF, 2));
            data.push_back("Vision GG: " + std::string((char*)block->VisionGG, 2));
            data.push_back("Model AA: " + std::string((char*)block->ModelAA, 2));
            data.push_back("Model BB: " + std::string((char*)block->ModelBB, 2));
            data.push_back("Model CC: " + std::string((char*)block->ModelCC, 2));
            data.push_back("Model DD: " + std::string((char*)block->ModelDD, 2));
            data.push_back("Model EE: " + std::string((char*)block->ModelEE, 2));
            data.push_back("Model FF: " + std::string((char*)block->ModelFF, 2));
            data.push_back("Model GG: " + std::string((char*)block->ModelGG, 2));
            data.push_back("Temp1: " + std::string((char*)block->Temp1, 2));
            data.push_back("Temp2: " + std::string((char*)block->Temp2, 2));
            data.push_back("Temp3: " + std::string((char*)block->Temp3, 2));
            data.push_back("Spare: " + std::string((char*)block->spare, 22));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned short result;
        unsigned char VisionAA[2];
        unsigned char VisionBB[2];
        unsigned char VisionCC[2];
        unsigned char VisionDD[2];
        unsigned char VisionEE[2];
        unsigned char VisionFF[2];
        unsigned char VisionGG[2];
        unsigned char ModelAA[2];
        unsigned char ModelBB[2];
        unsigned char ModelCC[2];
        unsigned char ModelDD[2];
        unsigned char ModelEE[2];
        unsigned char ModelFF[2];
        unsigned char ModelGG[2];
        unsigned char Temp1[2];
        unsigned char Temp2[2];
        unsigned char Temp3[2];
        unsigned char spare[22];
    };
};

class BlockType2004 : public IBlockType
{
public:
    BlockType2004(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare, 58));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare[58];
    };
};

class BlockType3002 : public IBlockType
{
public:
    BlockType3002(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare, 58));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare[58];
    };
};

class BlockType3004 : public IBlockType
{
public:
    BlockType3004(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell ID3: " + std::string((char*)block->CellID3, 10));
            data.push_back("Cell ID4: " + std::string((char*)block->CellID4, 10));
            data.push_back("Spare: " + std::string((char*)block->spare, 38));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID3[10];
        unsigned char CellID4[10];
        unsigned char spare[38];
    };
};

//4002 PLC->PC or API에 따라 다르게 구현?? 확인 필요
class BlockType4002 : public IBlockType
{
public:
    BlockType4002(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell ID3: " + std::string((char*)block->CellID3, 10));
            data.push_back("Cell ID4: " + std::string((char*)block->CellID4, 10));
            data.push_back("Spare: " + std::string((char*)block->spare, 38));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID3[10];
        unsigned char CellID4[10];
        unsigned char spare[38];
    };
};

class BlockType4004 : public IBlockType
{
public:
    BlockType4004(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare, 58));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare[58];
    };
};

class BlockType65002 : public IBlockType
{
public:
    BlockType65002(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell ID3: " + std::string((char*)block->CellID3, 10));
            data.push_back("Cell ID4: " + std::string((char*)block->CellID4, 10));
            data.push_back("Cell ID5: " + std::string((char*)block->CellID5, 10));
            data.push_back("Cell ID6: " + std::string((char*)block->CellID6, 10));
            data.push_back("Spare: " + std::string((char*)block->spare, 18));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID3[10];
        unsigned char CellID4[10];
        unsigned char CellID5[10];
        unsigned char CellID6[10];
        unsigned char spare[18];
    };
};

class BlockType65004 : public IBlockType
{
public:
    BlockType65004(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell ID3: " + std::string((char*)block->CellID3, 10));
            data.push_back("Cell ID4: " + std::string((char*)block->CellID4, 10));
            data.push_back("Cell ID5: " + std::string((char*)block->CellID5, 10));
            data.push_back("Cell ID6: " + std::string((char*)block->CellID6, 10));
            data.push_back("Cell ID7: " + std::string((char*)block->CellID7, 10));
            data.push_back("Cell ID8: " + std::string((char*)block->CellID8, 10));
            data.push_back("Cell ID9: " + std::string((char*)block->CellID9, 10));
            data.push_back("Cell ID10: " + std::string((char*)block->CellID10, 10));
            data.push_back("LD Tray ID: " + std::string((char*)block->LDTrayID, 20));
            data.push_back("UD Tray ID: " + std::string((char*)block->UDTrayID, 20));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID3[10];
        unsigned char CellID4[10];
        unsigned char CellID5[10];
        unsigned char CellID6[10];
        unsigned char CellID7[10];
        unsigned char CellID8[10];
        unsigned char CellID9[10];
        unsigned char CellID10[10];
        unsigned char LDTrayID[20];
        unsigned char UDTrayID[20];
    };
};

class BlockType65006 : public IBlockType
{
public:
    BlockType65006(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            for (int i = 0; i < 64; i++)
            {
                data.push_back("Cell ID" + std::to_string(i + 1) + ": " + std::string((char*)block->CellID[i], 12));
            }
            
            data.push_back("Lot ID: " + std::string((char*)block->LotID, 16));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID[64][12];
        unsigned char LotID[16];
    };
};

class BlockType65008 : public IBlockType
{
public:
    BlockType65008(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell ID1: " + std::string((char*)block->CellID1, 12));
            data.push_back("Lot ID: " + std::string((char*)block->LotID, 16));
            data.push_back("Spare: " + std::string((char*)block->spare, 30));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID1[12];
        unsigned char LotID[16];
        unsigned char spare[30];
    };
};

class BlockType65010 : public IBlockType
{
public:
    BlockType65010(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Spare: " + std::string((char*)block->spare, 58));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char spare[58];
    };
};

class BlockType65012 : public IBlockType
{
public:
    BlockType65012(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("Cell ID1: " + std::string((char*)block->CellID1, 36));
            data.push_back("Lot ID: " + std::string((char*)block->LotID, 16));
            data.push_back("Spare: " + std::string((char*)block->spare, 6));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID1[36];
        unsigned char LotID[16];
        unsigned char spare[6];
    };
};

class BlockType65014 : public IBlockType
{
public:
    BlockType65014(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("LD TrayID: " + std::string((char*)block->LDTrayID, 20));
            data.push_back("UD TrayID: " + std::string((char*)block->UDTrayID, 20));
            data.push_back("Result: " + std::to_string(block->RV[0]));
            data.push_back("OverHang: " + std::to_string(block->RV[1]));
            data.push_back("Shoulder: " + std::to_string(block->RV[2]));
            data.push_back("Electrode: " + std::to_string(block->RV[3]));
            data.push_back("AC Gap: " + std::to_string(block->RV[4]));
            data.push_back("Positive X AC: " + std::to_string(block->RV[5]));
            data.push_back("Positive Y AC: " + std::to_string(block->RV[6]));
            data.push_back("Negative X AC: " + std::to_string(block->RV[7]));
            data.push_back("Negative Y AC: " + std::to_string(block->RV[8]));
            data.push_back("Positive X AC Gap Min: " + std::to_string(block->RV[9]));
            data.push_back("Positive X AC Gap Max: " + std::to_string(block->RV[10]));
            data.push_back("Positive Y AC Gap Min: " + std::to_string(block->RV[11]));
            data.push_back("Positive Y AC Gap Max: " + std::to_string(block->RV[12]));
            data.push_back("Shoulder Y AC Gap Min: " + std::to_string(block->RV[13]));
            data.push_back("Shoulder Y AC Gap Max: " + std::to_string(block->RV[14]));
            data.push_back("Negative X AC Gap Min: " + std::to_string(block->RV[15]));
            data.push_back("Negative X AC Gap Max: " + std::to_string(block->RV[16]));
            data.push_back("Negative Y AC Gap Min: " + std::to_string(block->RV[17]));
            data.push_back("Negative Y AC Gap Max: " + std::to_string(block->RV[18]));
            data.push_back("Positive Count: " + std::to_string(block->RV[19]));
            data.push_back("Negative Count: " + std::to_string(block->RV[20]));
            data.push_back("Positive X Diff Max: " + std::to_string(block->RV[21]));
            data.push_back("Positive Y Diff Max: " + std::to_string(block->RV[22]));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char LDTrayID[20];
        unsigned char UDTrayID[20];
        short RV[23];
    };
};

class BlockType65016 : public IBlockType
{
public:
    BlockType65016(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            for (int i = 0; i < 64; i++)
            {
                data.push_back("Cell ID" + std::to_string(i + 1) + ": " + std::string((char*)block->CellID[i], 14));
            }

            data.push_back("Lot ID: " + std::string((char*)block->LotID, 16));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned char CellID[64][14];
        unsigned char LotID[16];
    };
};

class BlockType65534 : public IBlockType
{
public:
    BlockType65534(unsigned char* ptr) : IBlockType(ptr)
    {

    }

    virtual std::vector<std::string> ToString() override
    {
        std::vector<std::string> data;

        BlockType* block = (BlockType*)ptr;
        if (block != nullptr)
        {
            data.push_back("YYYY: " + std::to_string(block->Year));
            data.push_back("MM: " + std::to_string(block->Month));
            data.push_back("DD: " + std::to_string(block->Day));
            data.push_back("HH: " + std::to_string(block->Hour));
            data.push_back("mm: " + std::to_string(block->Minute));
            data.push_back("SS: " + std::to_string(block->Second));
            data.push_back("Spare: " + std::string((char*)block->spare, 46));
        }

        return data;
    }

private:
    struct BlockType
    {
        unsigned short Year;
        unsigned short Month;
        unsigned short Day;
        unsigned short Hour;
        unsigned short Minute;
        unsigned short Second;
        unsigned char spare[46];
    };
};