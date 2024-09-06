import os
import pandas as pd
import numpy as np
import queue
from datetime import datetime
import matplotlib.pyplot as plt

class MovingAverage():
    def __init__(self):
        self.window_size = 30
        self.time_series = pd.Series(dtype=float)

    # 이상치 감지 함수
    def __detect_anomaly(self, user_time_seconds, moving_avg):
        residual = user_time_seconds - moving_avg.iloc[-1]
        
        # 이동 윈도우에 기반한 표준 편차 계산
        recent_data = self.time_series[-self.window_size:]  # 최근 데이터에 기반한 이동 윈도우
        self.time_series = self.time_series[1:] # 첫번째 데이터를 삭제하고 shift한다.
        threshold = 1.82 * np.std(recent_data.dropna())
        # 1.96 -> 95%
        # 2.576 -> 99%  2.17 -> 97% 
        # 1.645 -> 90%
        # 1.28 -> 80%
        # 1.04 -> 70%
        # 0.93 -> 65%
        # 0.84 -> 60%
        
        is_anomaly = abs(residual) > threshold
        
        # 최대값, 최소값 계산
        min_value = moving_avg.iloc[-1] - threshold
        max_value = moving_avg.iloc[-1] + threshold

        return is_anomaly, (min_value, max_value), residual, user_time_seconds
    
    def __calc(self,seconds):
        # 이동 평균 계산
        moving_average = self.time_series.rolling(window=self.window_size, min_periods=1).mean()
        
        return self.__detect_anomaly(seconds, moving_average)

    def __convert_time_to_second(self, buffer):
        h, m, s = buffer.split(':')
        s = float(s)  # 초와 밀리초를 포함한 float 형식
        return int(h) * 3600 + int(m) * 60 + s

    def addBuffer(self, buffer):
        # 새로운 데이터를 시계열에 추가
        seconds = self.__convert_time_to_second(buffer)
        self.time_series = pd.concat([self.time_series, pd.Series([seconds])], ignore_index=True)
        if len(self.time_series) -1 < self.window_size:
            return 0, (0, 0), 0, 0
        else:
            return self.__calc(seconds)
