import numpy as np
import sys
from keras.models import load_model
import os
from collections import deque

# 현재 파일의 디렉토리의 상위 디렉토리를 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from logPreprocessing import logClassifier

class LSTMInference:
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
