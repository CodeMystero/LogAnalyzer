import re
import pandas as pd
import os

class FeatureExtractor:
    def __init__(self, group_number, output_dir="log_groups/pattern_features"):
        self.group_number = group_number
        self.output_dir = output_dir
        self.output_file_path = os.path.join(self.output_dir, f"extracted_features_group_{group_number}.csv")

    def extract_value(self, data, key):
        match = re.search(rf"{key}=(\d+|[A-Za-z0-9_]+)", data)
        return match.group(1) if match else '0'

    def hash_id_to_numeric(self, id_str):
        if id_str:
            numeric_value = sum(ord(char) for char in id_str) % 1000
            return numeric_value
        return None

    def extract_features(self, data):
        raise NotImplementedError("This method should be overridden by subclasses")

    def save_features_to_csv(self):
        df = self.process_group()

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        df.to_csv(self.output_file_path, index=False)
        print(f"Extracted features saved to {self.output_file_path}")

    def add_feature(self, new_data):
        # 피처를 추출
        new_features = self.extract_features(new_data)

        # 새로 추출한 피처를 DataFrame으로 변환
        new_features_df = pd.DataFrame([new_features])

        # CSV 파일에 추가 (파일이 없으면 생성)
        if not os.path.exists(self.output_file_path):
            new_features_df.to_csv(self.output_file_path, index=False)
            print(f"File created and first entry saved to {self.output_file_path}")
        else:
            new_features_df.to_csv(self.output_file_path, mode='a', header=False, index=False)
            #print(f"New features appended to {self.output_file_path}")


# 그룹 1의 피처 추출을 구현하는 클래스
class Group1Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}
        # 그룹 1만의 피처 추출 로직 작성
        # 예시: features['example_key'] = self.extract_value(data, "ExampleKey")
        return features


# 그룹 2의 피처 추출을 구현하는 클래스
class Group2Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}

        time_match = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{6})", data)
        if time_match:
            time_str = time_match.group(1)
            features['Time'] = time_str

        features['MsgL'] = self.extract_value(data, "MsgL")
        features['PLC/PCReq'] = self.extract_value(data, "PLC/PCReq")
        features['DType'] = self.extract_value(data, "DType")
        features['ProVer'] = self.extract_value(data, "ProVer")
        features['PVGroupNumber'] = self.extract_value(data, "PVGroupNumber")
        features['PLCSendDelayTime'] = self.extract_value(data, "PLCSendDelayTime")
        features['CommonBitValue'] = self.extract_value(data, "CommonBitValue")
        features['BitModeValue'] = self.extract_value(data, "BitModeValue")

        m00_id = self.extract_value(data, "M#00_ID")
        features['M#00'] = (
            self.hash_id_to_numeric(m00_id),
            self.extract_value(data, "M#00_BitValue#0"),
            self.extract_value(data, "M#00_BitValue#1"),
            self.extract_value(data, "M#00_BitValue#2"),
            self.extract_value(data, "M#00_BitValue#3"),
            self.extract_value(data, "M#00_Recipe_Number")
        )

        m01_id = self.extract_value(data, "M#01_ID")
        features['M#01'] = (
            self.hash_id_to_numeric(m01_id),
            self.extract_value(data, "M#01_BitValue#0"),
            self.extract_value(data, "M#01_BitValue#1"),
            self.extract_value(data, "M#01_BitValue#2"),
            self.extract_value(data, "M#01_BitValue#3"),
            self.extract_value(data, "M#01_Recipe_Number")
        )

        return features


if __name__ == "__main__":
    # Group 2 처리 예제
    group2_extractor = Group2Extractor(group_number=2)

    # 새로운 문장을 받아서 CSV 파일에 추가
    new_log_line = "00:12:42.039496 MsgL=263,PLC/PCReq=0,DType=0,ProVer=10003,PVGroupNumber=2,PLCSendDelayTime=50,CommonBitValue=0,M#00_ID=Y47Pnb00Yz,M#00_BitValue#0=69,M#00_BitValue#1=128,M#00_BitValue#2=0,M#00_BitValue#3=0,M#00_Recipe_Number=0,M#01_ID=Y47Nnb1CGC,M#01_BitValue#0=69,M#01_BitValue#1=128,M#01_BitValue#2=0,M#01_BitValue#3=0,M#01_Recipe_Number=0,BitModeValue=0"
    group2_extractor.add_feature(new_log_line)
