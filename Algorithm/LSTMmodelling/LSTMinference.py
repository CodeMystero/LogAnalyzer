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

class LSTMInferenceTorch:
    def __init__(self, model_path="D:/9999.Code/AnalyticsLog/Model/best_lstm_model_2_4.pth", n_steps=4, device=None):
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
