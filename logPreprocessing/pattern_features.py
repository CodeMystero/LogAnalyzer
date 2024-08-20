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

        time_match = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{6})", data)
        if time_match:
            time_str = time_match.group(1)
            features['Time'] = time_str
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

class Group3Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}

        time_match = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{6})", data)
        if time_match:
            features['Time'] = time_match.group(1)
        
        measurement_match = re.search(r"PC<-M#\d{2} : ([\d\.e\+\-]+),([\d\.e\+\-]+),([\d\.e\+\-]+)", data)
        if measurement_match:
            # float으로 변환하고 소수점 이하 16자리까지 유지
            features['Measurement1'] = str(float(measurement_match.group(1)))
            features['Measurement2'] = str(float(measurement_match.group(2)))
            features['Measurement3'] = str(float(measurement_match.group(3)))
        else:
            features['Measurement1'] = features['Measurement2'] = features['Measurement3'] = '0'
        
        return features

# 그룹 4의 피처 추출을 구현하는 클래스
class Group4Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}
        time_match = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{6})", data)
        if time_match:
            features['Time'] = time_match.group(1)

        features['MsgL'] = self.extract_value(data, "MsgL")
        features['PLC/PCReq'] = self.extract_value(data, "PLC/PCReq")
        features['DType'] = self.extract_value(data, "DType")
        features['ProVer'] = self.extract_value(data, "ProVer")
        features['MeasurementGroupNumber'] = self.extract_value(data, "MeasurementGroupNumber")
        features['PLCSendDelayTime'] = self.extract_value(data, "PLCSendDelayTime")
        features['CommonBitValue'] = self.extract_value(data, "CommonBitValue")
        features['Lot_ID'] = self.extract_value(data, "Lot_ID")
        features['Recipe_ID'] = self.extract_value(data, "Recipe_ID")
        features['M#00_ID'] = self.hash_id_to_numeric(self.extract_value(data, "M#00_ID"))
        features['M#00_BitValue#0'] = self.extract_value(data, "M#00_BitValue#0")
        features['M#00_BitValue#1'] = self.extract_value(data, "M#00_BitValue#1")
        features['M#00_BitValue#2'] = self.extract_value(data, "M#00_BitValue#2")
        features['M#00_BitValue#3'] = self.extract_value(data, "M#00_BitValue#3")
        features['M#00_Recipe_Number'] = self.extract_value(data, "M#00_Recipe_Number")
        features['M#00_PV_Number'] = self.extract_value(data, "M#00_PV_Number")
        features['M#00_RAW_Number'] = self.extract_value(data, "M#00_RAW_Number")
        features['M#00_Judge_Code'] = self.extract_value(data, "M#00_Judge_Code")
        features['M#00_TimeBlock_01'] = self.extract_value(data, "M#00_TimeBlock_01")
        features['M#00_TimeBlock_02'] = self.extract_value(data, "M#00_TimeBlock_02")
        features['M#00_TimeBlock_03'] = self.extract_value(data, "M#00_TimeBlock_03")
        features['M#00_TimeBlock_04'] = self.extract_value(data, "M#00_TimeBlock_04")
        features['M#00_CellCountNo'] = self.extract_value(data, "M#00_CellCountNo")
        features['M#01_ID'] = self.hash_id_to_numeric(self.extract_value(data, "M#01_ID"))
        features['M#01_BitValue#0'] = self.extract_value(data, "M#01_BitValue#0")
        features['M#01_BitValue#1'] = self.extract_value(data, "M#01_BitValue#1")
        features['M#01_BitValue#2'] = self.extract_value(data, "M#01_BitValue#2")
        features['M#01_BitValue#3'] = self.extract_value(data, "M#01_BitValue#3")
        features['M#01_Recipe_Number'] = self.extract_value(data, "M#01_Recipe_Number")
        features['M#01_PV_Number'] = self.extract_value(data, "M#01_PV_Number")
        features['M#01_RAW_Number'] = self.extract_value(data, "M#01_RAW_Number")
        features['M#01_Judge_Code'] = self.extract_value(data, "M#01_Judge_Code")
        features['M#01_TimeBlock_01'] = self.extract_value(data, "M#01_TimeBlock_01")
        features['M#01_TimeBlock_02'] = self.extract_value(data, "M#01_TimeBlock_02")
        features['M#01_TimeBlock_03'] = self.extract_value(data, "M#01_TimeBlock_03")
        features['M#01_TimeBlock_04'] = self.extract_value(data, "M#01_TimeBlock_04")
        features['M#01_CellCountNo'] = self.extract_value(data, "M#01_CellCountNo")
        features['BitModeValue'] = self.extract_value(data, "BitModeValue")
        return features

# 그룹 5의 피처 추출을 구현하는 클래스
class Group5Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}
        path_match = re.search(r"Buffer\[([^\]]+)\]", data)
        if path_match:
            features['FilePath'] = path_match.group(1)
        else:
            features['FilePath'] = 'N/A'
        return features

# 그룹 6의 피처 추출을 구현하는 클래스
class Group6Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}
        path_match = re.search(r"Save CSV \[([^\]]+)\]", data)
        if path_match:
            features['FilePath'] = path_match.group(1)

        fields_match = re.search(r"\[([^\]]+)\]$", data)
        if fields_match:
            features_list = fields_match.group(1).split(',')
            for i, field in enumerate(features_list):
                features[f'Field_{i+1}'] = field.strip()
        return features

# 그룹 7의 피처 추출을 구현하는 클래스
class Group7Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}
        # This group seems to have a simpler log format, perhaps just track the event
        features['Event'] = "Added to Send Queue"
        return features

# 그룹 8의 피처 추출을 구현하는 클래스
class Group8Extractor(FeatureExtractor):
    def extract_features(self, data):
        features = {}
        path_match = re.search(r"Save CSV \[([^\]]+)\]", data)
        if path_match:
            features['FilePath'] = path_match.group(1)

        fields_match = re.search(r"\[([^\]]+)\]$", data)
        if fields_match:
            features_list = fields_match.group(1).split(',')
            for i, field in enumerate(features_list):
                features[f'Field_{i+1}'] = field.strip()
        return features

def process_all_groups():
    log_groups_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../log_groups')
    output_dir = os.path.join(log_groups_dir, 'pattern_features')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(1, 9):
        file_path = os.path.join(log_groups_dir, f'group_{i}.txt')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = file.readlines()

            # 각 그룹에 맞는 Extractor 인스턴스 생성
            if i == 1:
                extractor = Group1Extractor(group_number=i, output_dir=output_dir)
            elif i == 2:
                extractor = Group2Extractor(group_number=i, output_dir=output_dir)
            elif i == 3:
                extractor = Group3Extractor(group_number=i, output_dir=output_dir)
            elif i == 4:
                extractor = Group4Extractor(group_number=i, output_dir=output_dir)
            elif i == 5:
                extractor = Group5Extractor(group_number=i, output_dir=output_dir)
            elif i == 6:
                extractor = Group6Extractor(group_number=i, output_dir=output_dir)
            elif i == 7:
                extractor = Group7Extractor(group_number=i, output_dir=output_dir)
            elif i == 8:
                extractor = Group8Extractor(group_number=i, output_dir=output_dir)

            all_features = []
            # 데이터를 추가하여 피처를 추출하고 리스트에 추가
            for line in data:
                line = line.strip()
                if line:  # 빈 줄은 무시
                    features = extractor.extract_features(line)
                    all_features.append(features)

            # 추출된 모든 피처를 한 번에 DataFrame으로 변환하여 CSV 파일에 저장
            if all_features:
                df = pd.DataFrame(all_features)
                if not os.path.exists(extractor.output_file_path):
                    df.to_csv(extractor.output_file_path, index=False)
                    print(f"File created and first entry saved to {extractor.output_file_path}")
                else:
                    df.to_csv(extractor.output_file_path, mode='a', header=False, index=False)
                    print(f"Appended new features to {extractor.output_file_path}")

        else:
            print(f"File {file_path} does not exist.")



if __name__ == "__main__":
    process_all_groups()
