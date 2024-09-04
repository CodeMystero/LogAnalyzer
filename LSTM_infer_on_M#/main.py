import threading
import queue
import mmap
import time
import re
import os
import shutil

from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim

class LogFileReader(threading.Thread):
    def __init__(self, file_path, log_buffer, delay):
        super().__init__()
        self.file_path = file_path
        self.log_buffer = log_buffer
        self.delay = delay
        self.daemon = True

    def run(self):
        with open(self.file_path, 'r') as file:
            mmap_obj = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            while True:
                line = mmap_obj.readline().decode('utf-8').strip()+'\n'
                
                if not line:
                    break
                    
                while self.log_buffer.is_full():
                    time.sleep(0.1)
                    
                self.log_buffer.add_log_line(line)
                time.sleep(self.delay)
            mmap_obj.close()


class LogBuffer:
    def __init__(self, max_size):
        self.buffer = queue.Queue(maxsize = max_size)
        self.lock = threading.Lock()
        
    def add_log_line(self, log_line):
        with self.lock:
            if not self.buffer.full():
                self.buffer.put(log_line)
            else:
                pass
                
    def get_log_line(self):
        with self.lock:  
            if not self.buffer.empty():
                return self.buffer.get()
            return None

    def is_empty(self):
        with self.lock:
            return self.buffer.empty()

    def is_full(self):
        with self.lock:
            return self.buffer.full()

    def get_size(self):
        with self.lock:
            return self.buffer.qsize()        

    def get_all_logs_as_list(self):
        with self.lock:
            return list(self.buffer.queue)


    def __str__(self):
        with self.lock:
            return f'LogBuffer({list(self.buffer.queue)})'
   
    def __repr__(self):
        return self.__str__()
   
class LogClassifierOnMeasurer:
    def __init__(self, output_dir='classified_logs'):
        self.meter_count = 0
        self.meters = set()
        self.output_dir = output_dir
        self.buffers = {}
        self.lstm_trainers = {}

        
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        
        os.makedirs(self.output_dir)
            
    def add_log_line(self, log_line):
        
        pattern = r'M#\d{2}'
        meters_in_line = re.findall(pattern, log_line)
        
        unique_meters = set(meters_in_line)

        print(self.buffers)
        
        for meter in unique_meters:
            if meter not in self.meters:
                
                self.meters.add(meter) 
                self.meter_count += 1
                
                self.buffers[meter] = LogBuffer(max_size = 100)
                self.lstm_trainers[meter] = LSTMTrainer(input_size=1, hidden_size=10, output_size=1, sequence_length=100, device='cuda')
            
            pattern_number = self.assign_pattern_number(meter, log_line)
            labeled_log_line = f'{pattern_number}: {log_line}'
            
            predicted_value = self.lstm_trainers[meter].predict()
            
            self.lstm_trainers[meter].add_data_and_train(pattern_number)
            self.buffers[meter].add_log_line(pattern_number)
            #print(self.buffers)
            self._write_log_to_file(meter, labeled_log_line)
            
            
            
            return log_line, meter, pattern_number, predicted_value

    def assign_pattern_number(self,meter,log_line):
        
        bitvalue_pattern = f'{meter}_BitValue#0='

        if                                  re.search(rf'PC<-\s*{meter}', log_line):
            return 1
            
        if                                  re.search(r'ProVer=10002', log_line):
            if                                  re.search(f'{bitvalue_pattern}0', log_line):
                return 2  
            elif                                re.search(f'{bitvalue_pattern}67', log_line):
                return 3  
            elif                                re.search(f'{bitvalue_pattern}69', log_line):
                return 4 
            else:
                return -1
                
        if                                  re.search(rf'{meter}\s+Skip by PLC Order', log_line):
            return 5
            
        if                                  re.search(rf'{meter}\s+API Received', log_line):
            return 6  

        if                                  re.search(rf'{meter}\s+API Checked', log_line):
            return 7  

        if                                  re.search(rf'{meter}\s+API Merge Start', log_line):
            return 8 

        if                                  re.search(rf'{meter}\s+API Merge End, Clear Receved Message', log_line):
            return 9  

        if                                  re.search(rf'{meter}\s+API Merge End', log_line):
            return 10  

        if                                  re.search(rf'{meter}\s+Add To Send Queue Buffer', log_line):
            return 11  

        if                                  re.search(rf'{meter}\s+Add To SAVE CSV Qeueu Buffer', log_line):
            if                                  re.search(r'\\Measure\\', log_line):
                return 13  
            elif                                re.search(r'\\SpecNPara\\', log_line):
                return 14  
            elif                                re.search(r'\\Status\\', log_line):
                return 15

        if                                  re.search(r'ProVer=10003', log_line):
            if                                  re.search(f'{bitvalue_pattern}0', log_line):
                return 16  
            elif                                re.search(f'{bitvalue_pattern}67', log_line):
                return 17  
            elif                                re.search(f'{bitvalue_pattern}69', log_line):
                return 18  
            else:
                return -2

        if                                  re.search(rf'{meter}\s+Clear Measure Receive Buffer', log_line):
            return 19 

        if                                  re.search(rf'{meter}\s+Request Answer form PLC', log_line):
            return 20
            
        if                                  re.search(rf'{meter}\s+Save CSV', log_line):
            if                                  re.search(r'\\Measure\\', log_line):
                return 21  
            elif                                re.search(r'\\SpecNPara\\', log_line):
                return 22  

        return 0

    def _write_log_to_file(self, meter, log_line):
        file_path = os.path.join(self.output_dir, f'{meter}.log')
        with open(file_path, 'a') as log_file:
            log_file.write(log_line)

    def get_meter_count(self):
        return self.meter_count

    def get_all_meter_names(self):
        return list(self.meters)
        
    def get_buffer_for_meter(self, meter):
        """지정된 meter에 대한 LogBuffer를 반환합니다."""
        return self.buffers.get(meter, None)
    
class LSTMTrainer:
    def __init__(self, input_size, hidden_size, output_size, sequence_length, device='cpu'):
        self.device = device
        print(f"Using device: {self.device}")
        self.sequence_length = sequence_length
        self.model = nn.LSTM(input_size, hidden_size, batch_first=True).to(self.device)
        self.fc = nn.Linear(hidden_size, output_size).to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.1)
        self.sequence = deque(maxlen=sequence_length)
        self.hidden = None
        self.initial_training_flag = False

    def add_data_and_train(self, data_point):
        self.sequence.append([data_point])
        if len(self.sequence) == self.sequence_length:
            if not self.initial_training_flag:
                start_time = time.time()
                self.train_on_sequence()
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Elapsed time: {elapsed_time} seconds")
                self.initial_training_flag = True


    def train_on_sequence(self):
        inputs = torch.tensor(self.sequence, dtype=torch.float32).unsqueeze(0).to(self.device)
        targets = torch.tensor([self.sequence[-1]], dtype=torch.float32).to(self.device)  # 예측하려는 다음 값
        self.optimizer.zero_grad()
        
        output, self.hidden = self.model(inputs, self.hidden)
        output = self.fc(output[:, -1])  # 마지막 타임스텝의 출력을 사용
        
        loss = self.criterion(output, targets)
        loss.backward()
        self.optimizer.step()

        self.hidden = None

    def predict(self):
        if len(self.sequence) == self.sequence_length:
            inputs = torch.tensor(list(self.sequence), dtype=torch.float32).unsqueeze(0).to(self.device)
            with torch.no_grad():
                output, _ = self.model(inputs)
                output = self.fc(output[:, -1])  # 마지막 타임스텝의 출력을 사용
            return output.cpu().numpy()
        else:
            return None

    def refresh_model(self):
        self.model = nn.LSTM(self.model.input_size, self.model.hidden_size, batch_first=True).to(self.device)
        self.fc = nn.Linear(self.model.hidden_size, self.fc.out_features).to(self.device)
        self.hidden = None
   
def main():
    file_path = 'MeasurementDAQLog_20240730.log'
    max_size = 10000
    log_buffer = LogBuffer(max_size)
    log_classifier = LogClassifierOnMeasurer()
    
    log_reader = LogFileReader(file_path, log_buffer, delay = 1)
    log_reader.start()
    
    while log_reader.is_alive() or not log_buffer.is_empty():
        log_line = log_buffer.get_log_line()
        if log_line:
            result =  log_classifier.add_log_line(log_line)
            if result:
                log, meter, real_value, predicted_value = result
                print("================================================")
                print(f"Log: {log}")
                print(f"Meter: {meter}")
                print(f"Real Value: {real_value}")
                print(f"Predicted Value: {predicted_value}")
                print("================================================") 
    
    log_reader.join()

    
if __name__ == "__main__":
    main()