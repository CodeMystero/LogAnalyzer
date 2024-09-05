import os
import re

class desiredLogClassifier:
    def __init__(self, log_file_path=None, max_lines=None):
        self.log_file_path = log_file_path
        self.max_lines = max_lines
    
    def classify_logs(self, regex_patterns):
        """
        주어진 정규 표현식 패턴에 맞는 로그를 필터링하고 그룹 번호로 매핑합니다.
        """
        if not os.path.exists(self.log_file_path):
            print(f"Error: Log file '{self.log_file_path}' not found.")
            return []
        
        classified_logs = []
        classified_numbers = []  # 숫자만 저장할 리스트
        line_count = 0
        
        with open(self.log_file_path, 'r') as file:
            for line in file:
                line_count += 1
                if self.max_lines and line_count > self.max_lines:
                    break  # 최대 줄 수를 초과하면 중지
                
                for idx, pattern in enumerate(regex_patterns, start=1):
                    if re.search(pattern, line):
                        classified_logs.append(f"{idx}: {line}")
                        classified_numbers.append(f"{idx}\n")
                        # break  # 패턴이 매칭되면 다음 패턴을 확인하지 않고 다음 로그로 넘어감
        
        return classified_logs, classified_numbers
    
    def save_classified_logs(self, classified_logs, classified_numbers, output_file, number_file):
        """
        그룹화된 로그와 숫자를 파일로 저장합니다.
        """
        # 파일이 없으면 생성
        if not os.path.exists(output_file):
            print(f"Output file '{output_file}' does not exist. Creating a new file.")
        
        with open(output_file, 'w') as file:
            file.writelines(classified_logs)
        
        print(f"Classified logs saved to '{output_file}'")

        # 숫자만 저장할 파일도 생성
        if not os.path.exists(number_file):
            print(f"Number sequence file '{number_file}' does not exist. Creating a new file.")
        
        with open(number_file, 'w') as file:
            file.writelines(classified_numbers)
        
        print(f"Classified numbers saved to '{number_file}'")

    def classify_single_log(self, log_line, regex_patterns):
        """
        단일 로그 라인을 받아서 정규 표현식 패턴에 따라 매칭되는 번호를 반환합니다.
        """
        for idx, pattern in enumerate(regex_patterns, start=1):
            if re.search(pattern, log_line):
                return idx
        return None  # 어떤 패턴에도 매칭되지 않으면 None을 반환

if __name__ == "__main__":
    log_file_path = 'MeasurementDAQLog_20240730.log'
    output_file_path = 'classified_group_sequence.txt'
    number_file_path = 'classified_number_sequence.txt'
    
    # 원하는 정규 표현식 패턴을 정의
    regex_patterns = [
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-M#\d{2}',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-API : .*MsgL=\d+,.*ProVer=10002.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC->API : .*MsgL=\d+,.*ProVer=10003.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*RawData.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*SpecNPara.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV'
    ]
    
    log_classifier = LogClassifier(log_file_path, max_lines=60000)
    classified_logs, classified_numbers = log_classifier.classify_logs(regex_patterns)
    
    if classified_logs:
        log_classifier.save_classified_logs(classified_logs, classified_numbers, output_file_path, number_file_path)
    else:
        print("No matching logs found.")
