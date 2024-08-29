import numpy as np
import sys
from keras.models import load_model
import os
from collections import deque
import torch
import torch.nn as nn
import time

# 현재 파일의 디렉토리의 상위 디렉토리를 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from logPreprocessing import logClassifier

class LSTMInference_tf:
    def __init__(self, model_path="lstm_model.h5", n_steps=50):
        
        model_path = os.path.join(current_dir, model_path)
        
        # LSTM 모델 로드 (컴파일 생략)
        self.model = load_model(model_path, compile=False)
        print(f"Model loaded from {model_path}")

        # 모델을 다시 컴파일 (필요한 경우 손실 함수와 옵티마이저를 다시 지정)
        self.model.compile(optimizer='adam', loss='mse')
        
        # LogClassifier 초기화
        self.classifier = logClassifier.LogClassifier()
        
        # 시퀀스 길이 설정
        self.n_steps = n_steps
        
        # 고정된 크기의 큐 초기화 (최대 n_steps개까지 저장 가능)
        self.sequence_queue = deque(maxlen=self.n_steps)

        # 문장 버퍼 초기화 (최대 2개의 문장 저장)
        self.sentence_buffer = deque(maxlen=2)

    def sentence_to_group_number(self, sentence):
        """
        문장을 그룹 번호로 변환하는 함수.
        :param sentence: 입력 문장 (str)
        :return: 그룹 번호 (int)
        """
        # 그룹 이름을 고정된 숫자에 매핑
        group_to_number = {
            "group_1.txt": 1,
            "group_2.txt": 2,
            "group_3.txt": 3,
            "group_4.txt": 4,
            "group_5.txt": 5,
            "group_6.txt": 6,
            "group_7.txt": 7,
            "group_8.txt": 8,
            "group_9.txt": 9,
            "group_10.txt": 10,
            "group_11.txt": 11,
            "group_12.txt": 12,
            "group_13.txt": 13,
            "group_14.txt": 14,
            "group_15.txt": 15,
            "group_16.txt": 16,
            "group_17.txt": 17,
            "group_18.txt": 18,
            "group_19.txt": 19,
            "group_20.txt": 20,
            "group_21.txt": 21,
            "group_22.txt": 22,
            "group_23.txt": 23,
            "group_24.txt": 24,
            "group_25.txt": 25,
            "group_26.txt": 26,
            "group_27.txt": 27,
            "group_28.txt": 28,
            "group_29.txt": 29,
            "group_30.txt": 30,
            "group_31.txt": 31,
            "group_32.txt": 32,
            "group_33.txt": 33,
            "group_34.txt": 34,
            "group_35.txt": 35,
            "group_36.txt": 36,
            "group_37.txt": 37,
            "group_38.txt": 38,
            "group_39.txt": 39,
            "group_40.txt": 40,
            "group_41.txt": 41,
            "group_42.txt": 42,
            "group_43.txt": 43,
            "group_44.txt": 44,
            "group_45.txt": 45,
            "group_46.txt": 46,
            "group_47.txt": 47,
            "group_48.txt": 48,
            "group_49.txt": 49,
            "group_50.txt": 50,
        }

        # sentence가 group_to_number 딕셔너리에 있는지 확인하고 번호 리턴
        if sentence in group_to_number:
            return group_to_number[sentence]
        else:
            raise ValueError(f"Sentence '{sentence}' does not match any group.")

    def add_number_to_queue(self, number):
        """
        새로운 숫자를 큐에 추가. 큐가 가득 차면 가장 오래된 숫자를 제거.
        :param number: 추가할 숫자 (int)
        """
        self.sequence_queue.append(number)
        # print(f"Updated sequence queue: {list(self.sequence_queue)}")

    def predict_next_value(self):
        """
        현재 큐에 있는 그룹 번호 시퀀스를 입력으로 받아 다음 값을 예측하는 함수.
        :return: 예측된 다음 그룹 번호 (float)
        """
        # 시퀀스 길이가 부족한 경우 0으로 패딩
        padded_sequence = list(self.sequence_queue)
        if len(padded_sequence) < self.n_steps:
            padded_sequence = [0] * (self.n_steps - len(padded_sequence)) + padded_sequence
        
        sequence = np.array(padded_sequence).reshape((1, self.n_steps, 1))
        predicted_value = self.model.predict(sequence, verbose=0)
        return predicted_value[0][0]

class LSTMInferenceTorch:
    def __init__(self, model_path="best_lstm_model_2_4.pth", n_steps=4, device=None):
        # 모델 경로
        model_path = os.path.join(os.getcwd(), model_path)

        # 디바이스 설정 (GPU 사용 여부)
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # LSTM 모델 로드
        self.model = self.load_model(model_path)
        
        # 시퀀스 길이 설정
        self.n_steps = n_steps
        
        # 고정된 크기의 큐 초기화 (최대 n_steps개까지 저장 가능)
        self.sequence_queue = deque(maxlen=self.n_steps)

        # 정규화 범위 설정
        self.min_value = 1
        self.max_value = 6

    def load_model(self, model_path):
        """
        모델을 로드하고 평가 모드로 설정합니다.
        """
        model = LSTMModel(input_size=1, hidden_size=512, num_layers=4)  # 모델 구조는 학습에 사용된 구조와 동일해야 함
        model.load_state_dict(torch.load(model_path))
        model.to(self.device)
        model.eval()
        return model
        
    def normalize_value(self, value):
        """
        입력 값을 0~1 범위로 정규화하는 함수.
        :param value: 원래 값 (int)
        :return: 정규화된 값 (float)
        """
        return (value - self.min_value) / (self.max_value - self.min_value)

    def denormalize_value(self, value):
        """
        예측된 값을 원래 스케일로 되돌리는 함수.
        :param value: 정규화된 값 (float)
        :return: 원래 값 (float)
        """
        return value * (self.max_value - self.min_value) + self.min_value


    

    def add_number_to_queue(self, number):
        """
        새로운 숫자를 큐에 추가. 큐가 가득 차면 가장 오래된 숫자를 제거.
        :param number: 추가할 숫자 (int)
        """
        normalized_number = self.normalize_value(number)
        self.sequence_queue.append(normalized_number)
        # print(self.sequence_queue)
            
    def predict_next_value(self):
        """
        현재 큐에 있는 그룹 번호 시퀀스를 입력으로 받아 다음 값을 예측하는 함수.
        :return: 예측된 다음 그룹 번호 (float)
        """
        # 시퀀스 길이가 부족한 경우 0으로 패딩
        padded_sequence = list(self.sequence_queue)
        if len(padded_sequence) < self.n_steps:
            padded_sequence = [0] * (self.n_steps - len(padded_sequence)) + padded_sequence
        
        sequence = np.array(padded_sequence).reshape((1, self.n_steps, 1))
        sequence = torch.tensor(sequence, dtype=torch.float32).to(self.device)
        
        start_time = time.time()
        # 예측 수행
        with torch.no_grad():
            predicted_value = self.model(sequence)
        end_time = time.time()  # 코드 실행 후 시간 기록

        elapsed_time = end_time - start_time  # 실행 시간 계산
        #print(f"실행 시간: {elapsed_time}초")
        
        return self.denormalize_value(predicted_value.item())

# LSTM 모델 정의 (PyTorch)
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.dropout = nn.Dropout(0)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        h_0 = torch.zeros(self.lstm.num_layers, x.size(0), self.lstm.hidden_size).to(x.device)
        c_0 = torch.zeros(self.lstm.num_layers, x.size(0), self.lstm.hidden_size).to(x.device)

        out, _ = self.lstm(x, (h_0, c_0))
        out = self.bn1(out[:, -1, :])
        out = self.dropout(out)
        out = self.fc(out)
        return out

# 사용 예제
if __name__ == "__main__":
    # LSTMInference 클래스 초기화
    inference = LSTMInference()

    # 예제 문장
    example_sentence = "Example log line to classify."

    # 문장을 그룹 번호로 변환 후 큐에 추가
    group_number = inference.sentence_to_group_number(example_sentence)
    inference.add_number_to_queue(group_number)

    # 예제 시퀀스 추가 및 예측
    example_sequence = [1, 2, 3, 4, 5]
    for num in example_sequence:
        inference.add_number_to_queue(num)
    
    # 예측 시도 (패딩 처리됨)
    next_value = inference.predict_next_value()
    print(f"Predicted next value: {next_value}")
