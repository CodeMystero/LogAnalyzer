import os
import time
import threading
import queue

from datetime import datetime
from collections import deque
from logPreprocessing import logClassifier, pattern_features, classifying_only_desired_log, ParsedData
from algorithmLog import movingAverage
from LSTMmodelling import LSTMinference
from datetime import datetime
from Log import log
from file_lock import file_lock


####### LoadDataThread ########
class LoadDataThread(threading.Thread):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.daemon = True

    def run(self):

        print("LoadDataThread Started")

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    file.seek(0)  # 파일 포인터를 처음으로 이동
                    for line in file:                      
                        with buffer_lock:  # 락을 사용하여 버퍼에 안전하게 접근
                            parsed_data = splitData(line.strip())
                            buffer.put(parsed_data)
                            
                            
            except PermissionError:

                print(f"No authorization to access file")

            except IOError as e:

                print(f"Cannot open the file: {e}")  

        else:

            print(f"file doesn't exist.")

        print(f"LoadDataThread finished.")

####### ProcessThread ########
class ProcessThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()  # 중지 플래그를 위한 Event 객체 생성
        self.daemon = True

    def run(self):

        print("Process buffer thread started")

        while not self._stop_event.is_set():
            with buffer_lock:
     
                data = buffer.get()
                process_buffer.put(data)
                

                if process_buffer.qsize() >= 10:
                    
                    process(process_buffer)

        print(f"AddRawDataThread finished.")

    def stop(self):
        self._stop_event.set()  # 중지 플래그를 설정하여 반복문 종료

            
# buffer 관련
buffer_size = 2000000
buffer = queue.Queue(maxsize=buffer_size)
process_buffer = queue.Queue(maxsize=200)

log_file = "MeasurementDAQLog_20240730.log"
main_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(main_dir, '..', 'Input', 'Raw')
file_path = os.path.join(log_dir, log_file)

log_Thread = log.LogThread()

buffer_lock = threading.Lock()

load_Data_Thread = LoadDataThread(file_path)
process_Thread = ProcessThread()

moving_average = movingAverage.MovingAverage()
parsing = ParsedData.ParsedData()


LSTMinfer = LSTMinference.LSTMInferenceTorch() 
desired_log_classifier = classifying_only_desired_log.desiredLogClassifier()



regex_patterns = [
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-M#\d{2}',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-API : .*MsgL=\d+,.*ProVer=10002.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC->API : .*MsgL=\d+,.*ProVer=10003.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*RawData.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*SpecNPara.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV'
    ]

anomaly_log_counter =1

def setBufferSize(bufferSize):

    buffer_size = bufferSize

def loadRawData(filePath):
    
    if not os.path.exists(file_path):
        print(f"{file_path} 파일을 찾을 수 없습니다.")
        return False
    
    try:

        load_Data_Thread.start()
        pass
    except Exception as e:
        print(f"Exception in thread: {e}")

    try:

        process_Thread.start()
        pass

    except Exception as e:
        print(f"Exception in thread: {e}")

    try:

        log_Thread.start()
        pass

    except Exception as e:
        print(f"Exception in thread: {e}")
    
    return True

def splitData(rawData):
    parts = rawData.split()
    if len(parts) < 2 :
        raise ValueError("입력 문자열이 올바른 형식이 아닙니다.")
    timestamp = parts[0]
    data = " ".join(parts[1:])
    parsing.update(timestamp, data)

    return parsing.to_dict()


positive_pattern = 0

def LSTM_inference_():
    global positive_pattern
    next_value = LSTMinfer.predict_next_value()

    tolerance = 1

    if abs(next_value - positive_pattern) <= tolerance:
    
        LSTM_result = 0  # 예측 값이 실제 값과 거의 같은 경우

    else:

        LSTM_result = 1  # 예측 값이 실제 값과 충분히 다른 경우
        
    LSTMinfer.add_number_to_queue(positive_pattern)   
    
    return LSTM_result, next_value
        
def write_log(log):

    now = datetime.now()
    log_file_path = 'D:/9999.Code/AnalyticsLog/Output/Log/anomaly_MeasurementDAQLog_' + now.strftime("%Y%m%d") + '.log'

    with file_lock:
        file_mode = 'a' if os.path.exists(log_file_path) else 'w'

        with open(log_file_path, file_mode) as log_file:
            log_file.write(log + "\n")    
    
def log_message(anomaly_log_counter, predicted_value,maxValue, userTime, example_log, regex_patterns, flag):
    
    time_exceeded = userTime - maxValue

    data = {
        "index" : anomaly_log_counter,
        "value" : {
            "predicted_value" : predicted_value,
            "maxValue" : maxValue, 
            "userTime" : userTime,
            "time_exceeded" : time_exceeded,
        },
        "msg" : example_log,
        "regex_patterns" : regex_patterns,
        "flag" : flag
        }
    
    return data


def anormaly_write_log(flag, predicted_value, maxValue, userTime, example_log ):
    global anomaly_log_counter

    predicted_value = round(predicted_value)
    predicted_value = int(predicted_value)

    if predicted_value > 6:
        predicted_value = 6

    if predicted_value < 1:
        predicted_value = 1


    data = log_message(anomaly_log_counter, predicted_value,maxValue, userTime, example_log, regex_patterns, flag)



    log_Thread.addLog(data)

    anomaly_log_counter +=1
    
def main():

    loadRawData(file_path)

    while True: 
        pass

def process(process_buffer):

    global positive_pattern

    process_line = process_buffer.get()

    timestamp = process_line["timestamp"]
    data = process_line["data"]

    log = f"{timestamp} {data}"


    positive_pattern = desired_log_classifier.classify_single_log(log, regex_patterns)
    LSTM_result, predicted_value = LSTM_inference_()
    is_anomaly, bounds, residual, userTime = moving_average.addBuffer(timestamp)


    if positive_pattern == 0:
        
        write_log(log)

    elif positive_pattern in {1, 2, 3, 4, 5, 6}:

        LSTM_result, predicted_value = LSTM_inference_()
        is_anomaly, bounds, residual, userTime = moving_average.addBuffer(timestamp)

        if is_anomaly == 0 and LSTM_result == 0:

            flag = 0

        elif LSTM_result == 1 and is_anomaly == 0:

            flag = 1

        elif LSTM_result == 0 and is_anomaly == 1:

            flag = 2

        elif LSTM_result == 1 and is_anomaly == 1:

            flag = 3

        anormaly_write_log(flag, predicted_value, bounds[1], userTime, log)

    else: 

        pass



    return positive_pattern

            
if __name__ == "__main__":
    main()     
        
            
    