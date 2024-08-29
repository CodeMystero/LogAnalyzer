import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

class TimeSeriesAnomalyDetector:
    def __init__(self, window_size=200):
        self.time_series = pd.Series(dtype=float)
        self.window_size = window_size
    
    # 시간 문자열을 초 단위로 변환하는 함수 (HH:MM:SS.SSSSSS -> 초 단위로 변환)
    def convert_time_to_seconds(self, time_str):
        h, m, s = time_str.split(':')
        s = float(s)  # 초와 밀리초를 포함한 float 형식
        return int(h) * 3600 + int(m) * 60 + s

    # 함수로 현재 시간을 확인하여 자정인지 판단
    def is_midnight(self):
        current_time = datetime.now().time()
        return current_time.hour == 0 and current_time.minute == 0

    # 시계열 데이터 초기화 및 이동 평균 계산 함수
    def update_time_series(self, user_time_seconds):
        # 시계열 데이터 초기화 조건 확인
        if self.is_midnight():
            print("Resetting time series and model as it is now midnight.")
            self.time_series = pd.Series(dtype=float)  # 윈도우 초기화
        
        # 새로운 데이터를 시계열에 추가
        self.time_series = pd.concat([self.time_series, pd.Series([user_time_seconds])], ignore_index=True)
        
        # 이동 평균 계산
        window_size = min(len(self.time_series), self.window_size)  # 윈도우 크기를 현재 데이터 크기와 비교해 결정
        moving_avg = self.time_series.rolling(window=window_size, min_periods=1).mean()
        
        return moving_avg

    # 이상치 감지 함수
    def detect_anomaly(self, user_time_seconds, moving_avg):
        residual = user_time_seconds - moving_avg.iloc[-1]
        
        if len(self.time_series) > 1:
            # 이동 윈도우에 기반한 표준 편차 계산
            recent_data = self.time_series[-self.window_size:]  # 최근 데이터에 기반한 이동 윈도우
            threshold = 1.82 * np.std(recent_data.dropna())
            # 1.96 -> 95%
            # 2.576 -> 99%  2.17 -> 97% 
            # 1.645 -> 90%
            # 1.28 -> 80%
            # 1.04 -> 70%
            # 0.93 -> 65%
            # 0.84 -> 60%
        else:
            threshold = np.inf  # 데이터가 충분하지 않으면 임계값을 무한대로 설정
        
        is_anomaly = abs(residual) > threshold
        
        return is_anomaly, threshold, residual

    # 파일에서 마지막 줄을 읽어와 처리하는 메서드
    def process_last_line_from_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist.")
            return

        # 파일의 마지막 줄만 읽기
        with open(file_path, 'rb') as file:
            # 파일의 끝에서부터 역순으로 읽기
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
            last_line = file.readline().decode()

        last_line = last_line.strip()
        
        # Time을 제외한 나머지 데이터를 처리하지 않도록 수정
        try:
            time_str = last_line.split(',')[0]  # 첫 번째 요소만 사용하여 시간 문자열 추출
            user_time_seconds = self.convert_time_to_seconds(time_str)
        except ValueError:
            print(f"Invalid time format in line: {last_line}")
            return

        # 업데이트된 시계열 데이터 및 이동 평균 계산
        moving_avg = self.update_time_series(user_time_seconds)

        # 이상치 감지
        is_anomaly, threshold, residual = self.detect_anomaly(user_time_seconds, moving_avg)

        # 최대값, 최소값 계산
        min_value = moving_avg.iloc[-1] - threshold
        max_value = moving_avg.iloc[-1] + threshold

        if is_anomaly:
            #print(f"Time {time_str} (in seconds: {user_time_seconds}) is detected as an anomaly.")
            return 1, (min_value, max_value), user_time_seconds
            #if np.isfinite(threshold):
                #print(f"Normal range is between {moving_avg.iloc[-1] - threshold:.2f} and {moving_avg.iloc[-1] + threshold:.2f} seconds.")
        else:
            return 0, (min_value, max_value), user_time_seconds
            #print(f"Time {time_str} (in seconds: {user_time_seconds}) is not an anomaly.")
            #if np.isfinite(threshold):
                #print(f"Normal range is between {moving_avg.iloc[-1] - threshold:.2f} and {moving_avg.iloc[-1] + threshold:.2f} seconds.")


if __name__ == "__main__":
    detector = TimeSeriesAnomalyDetector(window_size=60)
    
    # 고정된 경로 사용
    directory = "log_groups/pattern_features"
    file_name = "extracted_features_group_2.csv"
    file_path = os.path.join(directory, file_name)
    
    detector.process_last_line_from_file(file_path)
