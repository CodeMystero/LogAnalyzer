import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import os

def load_sequence(file_path):
    with open(file_path, 'r') as file:
        sequence = [int(line.strip()) for line in file if line.strip()]
    return sequence

def create_dataset(sequence, n_steps):
    X, y = [], []
    for i in range(len(sequence) - n_steps):
        X.append(sequence[i:i + n_steps])
        y.append(sequence[i + n_steps])
    return np.array(X), np.array(y)

if __name__ == "__main__":
    # 데이터 준비
    sequence_file = os.path.join(os.path.dirname(__file__), "logPreprocessing/group_sequence.txt")
    sequence = load_sequence(sequence_file)

    # LSTM 입력 데이터 준비
    n_steps = 50  # 입력 시퀀스의 길이
    X, y = create_dataset(sequence, n_steps)
    X = X.reshape((X.shape[0], X.shape[1], 1))  # LSTM 입력 형태로 변환 (samples, timesteps, features)

    # 데이터 분할: 70% 트레이닝, 15% 밸리데이션, 15% 테스트
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # LSTM 모델 정의
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(n_steps, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # 모델 학습
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=200, verbose=1)

    # 모델 저장
    model_save_path = os.path.join(os.path.dirname(__file__), "lstm_model.h5")
    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    # 테스트 데이터로 예측 평가
    loss = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test loss: {loss}")

    # 예측 테스트
    recent_sequence = np.array(sequence[-n_steps:]).reshape((1, n_steps, 1))
    predicted_value = model.predict(recent_sequence, verbose=0)
    print(f"Predicted next value: {predicted_value[0][0]}")
