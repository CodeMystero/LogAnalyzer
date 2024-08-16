import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import re

# 시간 문자열을 인티저로 변환하는 함수 (HH:MM:SS.SSSSSS -> HHMMSSSSS)
def convert_time_to_integer(time_str):
    return int(time_str.replace(":", "").replace(".", "")[:9])

# CSV 파일 경로 설정
file_path = "log_groups/pattern_features/extracted_features_group_2.csv"

# CSV 파일에서 데이터 읽기
df = pd.read_csv(file_path)

# Time 피처를 인티저 형식으로 변환 (HH:MM:SS.SSSSSS -> HHMMSSSSS)
df['Time'] = df['Time'].apply(lambda x: convert_time_to_integer(x))

# 현재 시간을 기준으로 24시간 이내의 데이터만 유지하는 함수
def filter_last_24_hours(data, time_col, reference_time):
    # 24시간 차이는 24 * 3600 * 1000000 = 24000000 (HHMMSSSSS)
    last_24_hours = reference_time - 24000000  # 24000000은 24시간을 나타냄
    return data[data[time_col] >= last_24_hours]

# 24시간 이내의 데이터만 사용
reference_time = df['Time'].max()  # 가장 최근 시간
df_filtered = filter_last_24_hours(df, 'Time', reference_time)

# 시계열 데이터로 변환 (인티저 형식의 시간을 그대로 사용)
time_series = df_filtered['Time']

# SARIMA 모델 학습
model = SARIMAX(time_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
model_fit = model.fit()

# 예측 및 잔차 계산
df_filtered['Prediction'] = model_fit.predict(start=1, end=len(df_filtered))
df_filtered['Residual'] = time_series - df_filtered['Prediction']

# 이상치 탐지 (잔차의 절대값이 특정 임계값을 초과하는 경우)
threshold = 1.96 * np.std(df_filtered['Residual'])  # 통계적 임계값 설정
df_filtered['Anomaly'] = df_filtered['Residual'].abs() > threshold

# 정상 범위 정의
lower_bound = df_filtered['Prediction'] - threshold
upper_bound = df_filtered['Prediction'] + threshold

# 결과 출력
print("Initial Anomalies Detected:")
print(df_filtered[df_filtered['Anomaly'] == True][['Time', 'Prediction', 'Residual', 'Anomaly']])

# 커맨드라인에서 사용자 입력을 받아서 이상치 감지 및 재학습
while True:
    user_input = input("Enter a time value (in HH:MM:SS.SSSSSS format) or 'exit' to quit: ")
    
    if user_input.lower() == 'exit':
        break
    
    try:
        # 입력된 시간을 인티저로 변환
        user_time = convert_time_to_integer(user_input)
    except ValueError:
        print("Please enter a valid time in HH:MM:SS.SSSSSS format.")
        continue
    
    # 새로운 데이터를 사용하여 예측
    new_prediction = model_fit.get_forecast(steps=1).predicted_mean.values[0]
    residual = user_time - new_prediction
    
    # 이상치 감지
    is_anomaly = abs(residual) > threshold
    
    if is_anomaly:
        print(f"Time {user_input} is detected as an anomaly.")
        print(f"Normal range is between {new_prediction - threshold:.2f} and {new_prediction + threshold:.2f}.")
    else:
        print(f"Time {user_input} is not an anomaly.")
        print(f"Normal range is between {new_prediction - threshold:.2f} and {new_prediction + threshold:.2f}.")
    
    # 새로운 데이터를 시계열에 추가
    time_series = pd.concat([time_series, pd.Series([user_time])], ignore_index=True)

    # 현재 시간을 기준으로 다시 24시간 이내 데이터 필터링
    reference_time = time_series.max()
    df_filtered = filter_last_24_hours(time_series.to_frame(name='Time'), 'Time', reference_time)
    time_series = df_filtered['Time']

    # 모델을 다시 학습
    model = SARIMAX(time_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
    model_fit = model.fit()
