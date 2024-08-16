import numpy as np
from sklearn.ensemble import IsolationForest
from collections import deque
from datetime import datetime

# 각 문자열을 숫자로 변환하는 함수
def convert_to_numeric(values):
    return [sum(ord(char) for char in value) if not value.isdigit() else int(value) for value in values]

# M#01 피처의 이상치를 검출하는 함수
def is_outlier(input_data, model):
    # 입력된 데이터를 숫자로 변환
    input_data = convert_to_numeric(input_data)
    input_data = np.array(input_data).reshape(1, -1)
    
    print(f"Converted input data for prediction: {input_data}")  # 데이터 변환 결과 출력
    
    # 예측 수행
    prediction = model.predict(input_data)
    print(f"Prediction result: {prediction}")  # 예측 결과 출력
    
    # -1이면 이상치, 1이면 정상
    return prediction[0] == -1

# 모델을 업데이트하고 데이터를 추가하는 함수
def update_model(new_data, model, existing_data, max_size):
    # 새로운 데이터를 기존 데이터에 추가
    if len(existing_data) >= max_size:
        existing_data.popleft()  # 가장 오래된 데이터를 제거
    existing_data.append(new_data)
    
    # 모델 재학습
    model.fit(np.array(existing_data))
    print(f"Updated dataset length: {len(existing_data)}")  # 데이터셋 크기 출력
    
    return model, existing_data

# 함수로 현재 시간을 확인하여 자정인지 판단
def is_midnight():
    current_time = datetime.now().time()
    return current_time.hour == 0 and current_time.minute == 0

# 초기화 함수: 초기 데이터를 받아 모델을 초기화하는 함수
def initialize_model(initial_data, max_size=1500):
    # 데이터를 숫자로 변환
    numeric_data = [convert_to_numeric(data) for data in initial_data]

    # numpy 배열로 변환하여 deque에 저장
    data_deque = deque(numeric_data, maxlen=max_size)

    # Isolation Forest 모델 초기화 및 학습
    iso_forest = IsolationForest(
        n_estimators=                                                   100,  # 트리 수를 늘려 복잡성을 증가시킵니다.
        max_samples=                                                    0.5,    # 트리를 구성할 때 사용하는 샘플의 수를 줄여 오버피팅을 유도합니다.
        max_features=                                                   0.5,  # 전체 피처를 사용하도록 설정합니다.
        contamination=                                                  0.1, # 이상치 비율 설정
        random_state=                                                   42,    # 재현 가능성을 위한 랜덤 시드
        bootstrap=                                                      True,         # 부트스트랩 샘플링을 사용하여 샘플에 더욱 민감하게 반응하도록 합니다.
    )
    
    # 모델 학습
    iso_forest.fit(np.array(data_deque))
    
    return iso_forest, data_deque

# 단일 입력을 처리하는 함수
def process_input(user_input, model, existing_data, max_size=1500):
    user_data = user_input.split()  # 공백을 기준으로 문자열을 나누어 리스트로 변환
    print(f"User input data: {user_data}")  # 사용자 입력 데이터 출력
    
    # 입력된 데이터로 이상치 판단
    outlier = is_outlier(user_data, model)

    if outlier:
        print("입력된 데이터는 이상치입니다.")
    else:
        print("입력된 데이터는 정상입니다.")
        new_numeric_data = np.array(convert_to_numeric(user_data)).reshape(1, -1)
        print(f"New data added to model: {new_numeric_data}")  # 모델에 추가된 데이터 출력
        model, existing_data = update_model(new_numeric_data[0], model, existing_data, max_size)
    
    return model, existing_data

# 전체 로직을 관리하는 함수
def run_anomaly_detection(initial_data, max_size=1500):
    # 모델 초기화
    model, existing_data = initialize_model(initial_data, max_size)
    last_reset_day = datetime.now().day
    
    while True:
        user_input = input("Enter a time value (in format like '1 2 3 2 1 2') or 'exit' to quit: ")
        
        if user_input.lower() == 'exit':
            break

        # 자정 확인 및 초기화
        if is_midnight() or datetime.now().day != last_reset_day:
            print("Resetting time series and model as it is now midnight or a new day.")
            model, existing_data = initialize_model([], max_size)
            last_reset_day = datetime.now().day
        
        # 입력 데이터를 처리하고 모델 업데이트
        model, existing_data = process_input(user_input, model, existing_data, max_size)

if __name__ == "__main__":
    # 초기 데이터를 직접 전달 (예: M#01 형태의 데이터)
    initial_data = [
        "1 2 3 2 1 2",
        "2 3 4 3 2 1",
        "1 1 1 1 1 1",
        "3 3 3 3 3 3"
    ]

    run_anomaly_detection(initial_data)
