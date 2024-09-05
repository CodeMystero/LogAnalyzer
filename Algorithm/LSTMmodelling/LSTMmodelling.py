import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset
import os

# GPU 사용 가능 여부 확인
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

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

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.dropout = nn.Dropout(0.1)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        h_0 = torch.zeros(num_layers, x.size(0), hidden_size).to(device)
        c_0 = torch.zeros(num_layers, x.size(0), hidden_size).to(device)

        out, _ = self.lstm(x, (h_0, c_0))
        out = self.bn1(out[:, -1, :])
        out = self.dropout(out)
        out = self.fc(out)
        return out

if __name__ == "__main__":
    # 데이터 준비
    sequence_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logPreprocessing/classified_number_sequence.txt")
    sequence = load_sequence(sequence_file)

    # LSTM 입력 데이터 준비
    n_steps = 4  # 입력 시퀀스의 길이
    X, y = create_dataset(sequence, n_steps)
    
    # 데이터 스케일링 (0과 1 사이로 정규화)
    scaler = MinMaxScaler(feature_range=(0, 1))
    X = scaler.fit_transform(X)
    y = scaler.fit_transform(y.reshape(-1, 1))

    X = X.reshape((X.shape[0], X.shape[1], 1))  # LSTM 입력 형태로 변환 (samples, timesteps, features)

    # 데이터 분할: 70% 트레이닝, 15% 밸리데이션, 15% 테스트
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # NumPy 데이터를 PyTorch 텐서로 변환
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)
    X_val = torch.tensor(X_val, dtype=torch.float32)
    y_val = torch.tensor(y_val, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32)

    # 배치 크기 설정
    batch_size = 128  # 원하는 배치 크기로 설정 (예: 32)

    # DataLoader를 사용하여 데이터를 배치로 묶음
    train_dataset = TensorDataset(X_train, y_train)
    val_dataset = TensorDataset(X_val, y_val)
    test_dataset = TensorDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    # 모델 정의
    input_size = 1
    hidden_size = 512
    num_layers = 4
    model = LSTMModel(input_size, hidden_size, num_layers).to(device)

    # Adam 옵티마이저에 학습률 설정
    learning_rate = 0.001
    
    ############# L2 정규화 및 학습률 스케줄링 추가 #############
    # L2 정규화는 optimizer의 weight_decay 파라미터로 설정됩니다.
    # weight_decay 값을 0.001로 설정하면, L2 정규화가 추가된 옵티마이저를 생성할 수 있습니다.
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=0)

    # StepLR 스케줄러 추가: 50 에포크마다 학습률을 0.1배로 줄입니다.
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.1)
    ############# L2 정규화 및 학습률 스케줄링 추가 끝 #############
    

    # 손실 함수 정의
    criterion = nn.MSELoss()

    # 학습
    num_epochs = 500
    best_val_loss = float('inf')
    patience = 20
    patience_counter = 0

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            output = model(X_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # Gradient Clipping
            optimizer.step()
            running_loss += loss.item()

        avg_train_loss = running_loss / len(train_loader)

        # 검증 데이터로 평가
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                val_output = model(X_batch)
                loss = criterion(val_output, y_batch)
                val_loss += loss.item()
        avg_val_loss = val_loss / len(val_loader)

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_train_loss}, Val Loss: {avg_val_loss}")

        # 모델 저장 및 Early Stopping
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), "best_lstm_model.pth")
            patience_counter = 0
            print(f"Model saved with Validation Loss: {best_val_loss}")
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print("Early stopping triggered")
            break

    # 테스트 데이터로 평가
    model.load_state_dict(torch.load("best_lstm_model.pth"))
    model.eval()
    test_loss = 0.0
    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            test_output = model(X_batch)
            loss = criterion(test_output, y_batch)
            test_loss += loss.item()
    avg_test_loss = test_loss / len(test_loader)
    print(f"Test loss: {avg_test_loss}")

    # 예측 테스트
    recent_sequence = np.array(sequence[-n_steps:]).reshape((1, n_steps, 1))
    recent_sequence = scaler.transform(recent_sequence.reshape(-1, 1)).reshape(1, n_steps, 1)  # 시퀀스도 스케일링 적용
    recent_sequence = torch.tensor(recent_sequence, dtype=torch.float32).to(device)
    with torch.no_grad():
        predicted_value = model(recent_sequence)
    predicted_value = scaler.inverse_transform(predicted_value.cpu().numpy())  # 예측 결과 역스케일링
    print(f"Predicted next value: {predicted_value[0][0]}")
