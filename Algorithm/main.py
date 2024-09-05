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

####### LoadDataThread ########
class LoadDataThread(threading.Thread):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.daemon = True

    def run(self):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    file.seek(0)  # 파일 포인터를 처음으로 이동
                    for line in file:
                        while len(buffer) >= buffer_size:
                            with buffer_lock:  # 락을 사용하여 버퍼에 안전하게 접근
                                parsed_data = splitData(line.strip())
                                buffer.put(parsed_data)
                                buffer_condition.notify()
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
        while not self._stop_event.is_set():
            if buffer.empty():
                self._stop_event.set()
            else:
                with buffer_condition:
                    buffer_condition.wait()
                    with buffer_lock:  # 락을 사용하여 버퍼에 안전하게 접근
                            data = buffer.get()
                            process_buffer.put(data)
                            if process_buffer == 200:
                                process(process_buffer)
        print(f"AddRawDataThread finished.")

    def stop(self):
        self._stop_event.set()  # 중지 플래그를 설정하여 반복문 종료

                
class ResultData():
    def __init__(self, log, result, time, bounds, lstm_result):
        
        self.log = log
        self.result = result
        self.time = time
        self.bounds = bounds
        self.lstm_result = lstm_result



# buffer 관련
buffer_size = 2000000
buffer = queue.Queue(maxlen=buffer_size)
process_buffer = queue.Queue(maxlen=200)

log_Thread = log.LogThread()

buffer_lock = threading.Lock()
buffer_condition = threading.Condition()
load_Data_Thread = LoadDataThread()
process_Thread = ProcessThread()
result_data = ResultData()
moving_average = movingAverage.MovingAverage

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

from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(result_data)

def start_flask_app():
    app.run(debug=True, use_reloader=False)

#############################################################################

def setBufferSize(bufferSize):
    buffer_size = bufferSize

def loadRawData(filePath):
    
    if not os.path.exists(file_path):
        print(f"{file_path} 파일을 찾을 수 없습니다.")
        return False
    
    log_Thread.start()
    load_Data_Thread.start(file_name)
    process_Thread.start()
    
    return True

def splitData(rawData):
    parts = rawData.split()
    if len(parts) < 2 :
        raise ValueError("입력 문자열이 올바른 형식이 아닙니다.")
    timestamp = parts[0]
    data = " ".join(parts[1:])
    return ParsedData(timestamp, data)

def log_classifier_():
    
    global classifier
    global positive_pattern
    
    ####### 버퍼가 비었을 때 대기하는 로직 추가 ########
    while True:
        with buffer_not_empty:
            while not buffer:
                buffer_not_empty.wait()

            with buffer_lock:
                example_log = buffer.popleft()  # 버퍼에서 가장 오래된 로그를 가져옴
                buffer_not_full.notify()  # 버퍼에 여유 공간이 생겼음을 알림
                break
        
        time.sleep(0.001)  # 버퍼가 비어 있으면 0.1초 대기 후 다시 시도
    ####### 버퍼가 비었을 때 대기하는 로직 추가 끝 ########
    
    # # 버퍼가 비어 있으면 대기
    # while True:
        # with buffer_lock:
            # if buffer:
                # example_log = buffer.popleft()  # 버퍼에서 가장 오래된 로그를 가져옴
                # break  # while 루프를 빠져나옴
        
        # # 버퍼가 비어 있으면 0.1초 대기 후 다시 시도
        # time.sleep(0.1)
    
    group, score = classifier.classify_log(example_log)
    group_num = LSTMinfer.sentence_to_group_number(group)
    positive_pattern = group_num
    
    return example_log, group_num

def pattern_features_(log, group_num):
    
    new_log_line = log
    
    common_time_extractor = pattern_features.CommonTimeExtractor()
    common_time_extractor.add_feature(new_log_line)
    
def moving_average_():
    global detector 
    global directory 
    global file_name 
    global file_path 
    
    result, bounds, user_time_seconds = detector.process_last_line_from_file(file_path)

    return result, bounds, user_time_seconds

values = {
        "previous": None,
        "current": 0
        }

def update_infered_result(new_value):
    values["previous"] = values["current"]
    values["current"] = new_value 


positive_pattern = 0

def LSTM_inference_():
    global positive_pattern
    next_value = LSTMinfer.predict_next_value()
    #update_infered_result(next_value)
    # LSTM 예측 값과 positive_pattern 비교
    tolerance = 2.6  # 허용 오차 설정
    
    
    # print(f'previous value : {values["previous"]}')
    # print(f'positive_pattern : {positive_pattern}')

    if abs(next_value - positive_pattern) <= tolerance:
        addLSTMresultAnomalyOnLog(LSTM_result, data, positive_patterne)
        LSTM_result = 0  # 예측 값이 실제 값과 거의 같은 경우
    else:
        LSTM_result = 1  # 예측 값이 실제 값과 충분히 다른 경우
        
    LSTMinfer.add_number_to_queue(positive_pattern)   
    
    

    return LSTM_result, next_value
        
def write_log(log):
    now = datetime.now()
    log_file_path = 'D:/9999.Code/AnalyticsLog/Output/anomaly_MeasurementDAQLog_' + now.strftime("%Y%m%d") + '.log'
    with open(log_file_path, 'a') as log_file:
        log_file.write(log + "\n")    
    
def addLSTMresultDelayAnomalyOnLog(LSTM_result, predicted_value, maxValue, userTime, example_log):
    global anomaly_log_counter
    
    # 원하는 정규 표현식 패턴을 정의
    regex_patterns = [
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-M#\d{2}',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-API : .*MsgL=\d+,.*ProVer=10002.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC->API : .*MsgL=\d+,.*ProVer=10003.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*RawData.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*SpecNPara.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV'
    ]
    
    # predicted_value를 반올림하고 정수로 변환
    predicted_value = round(predicted_value)
    predicted_value = int(predicted_value)
    
    
    if predicted_value > 6:
        predicted_value = 6
    
    if predicted_value < 1:
        predicted_value = 1
    
    time_exceeded = userTime - maxValue

    flag = 3

    data = {
        "index" : anomaly_log_counter,
        "value" : {
            "LSTM_result" : LSTM_result,
            "predicted_value" : predicted_value,
            "maxValue" : maxValue, 
            "userTime" : userTime,
        },
        "msg" : example_log,
        "regex_patterns" : regex_patterns,
        "flag" : flag
    }

    log_Thread.addLog(data)
    
def addLSTMresultAnomalyOnLog(LSTM_result, example_log, predicted_value):

    # 원하는 정규 표현식 패턴을 정의
    regex_patterns = [
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-M#\d{2}',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-API : .*MsgL=\d+,.*ProVer=10002.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC->API : .*MsgL=\d+,.*ProVer=10003.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*RawData.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*SpecNPara.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV'
    ]
    
    # predicted_value를 반올림하고 정수로 변환
    predicted_value = round(predicted_value)
    predicted_value = int(predicted_value)
    
    
    if predicted_value > 6:
        predicted_value = 6
    
    if predicted_value < 1:
        predicted_value = 1
    
    
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write("\n")
        log_file.write(f"{anomaly_log_counter} 번째 이상치 검출 : 아래의 위치에는 다음과 같은 패턴이 예상됩니다.| {regex_patterns[predicted_value-1]}\n")
        log_file.write("==================================================================================================================\n")
        log_file.write(str(example_log) + "\n")
        log_file.write("==================================================================================================================\n")
        log_file.write("\n")
    
    anomaly_log_counter +=1
      
      

def addDelayAnomalyOnLog(maxValue, userTime, example_log):
    global anomaly_log_counter
    now = datetime.now()
    log_file_path = 'D:/9999.Code/AnalyticsLog/Output/anomaly_MeasurementDAQLog_' + now.strftime("%Y%m%d") + '.log'
    
    time_exceeded = userTime - maxValue
    
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write("\n")
        log_file.write(f"{anomaly_log_counter} 번째 이상치 검출 : 아래의 로그는 {time_exceeded} us 지연되었습니다. \n")
        log_file.write("==================================================================================================================\n")
        log_file.write(str(example_log) + "\n")
        log_file.write("==================================================================================================================\n")
        log_file.write("\n")
      
    anomaly_log_counter +=1
    
def main_for_all_logs():
    buffer = deque(maxlen=BUFFER_SIZE)
    start_log_reader_with_interval(buffer)
    
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    time.sleep(1)
    while(True):
          
        log, group_num = log_classifier_()    
        pattern_features_(log, group_num)
        LSTM_result = LSTM_inference_()
        shared_data["LSTM_result"] = LSTM_result
        shared_data["log"] = log
        
        result, bounds, user_time_seconds = moving_average_()

        shared_data["result"] = result
        shared_data["bounds"] = bounds
        shared_data["user_time_seconds"] = user_time_seconds
            
        log_anomaly(log, LSTM_result, result)
            
        result = 0 

def process(buffer):
    global positive_pattern
    positive_pattern = desired_log_classifier.classify_single_log(process_buffer, regex_patterns)
    if positive_pattern == 0:
        write_log(process_buffer)
    elif positive_pattern in {1, 2, 3, 4, 5, 6}:
        pattern_features_(data, positive_pattern)
        #start_time = time.time()
        #end_time = time.time()  # 코드 실행 후 시간 기록
        #elapsed_time = end_time - start_time  # 실행 시간 계산
        #print(f"실행 시간: {elapsed_time}초")
        
        LSTM_result, predicted_value = LSTM_inference_()
        is_anomaly, bounds, residual = moving_average.addBuffer(buffer)

        if is_anomaly == 1:
            addDelayAnomalyOnLog(bounds[1], user_time_seconds, data)

        result, min_max_value, user_time_seconds = moving_average_()
        result_data = ResultData(data, result, user_time_seconds, bounds, LSTM_result)

        if LSTM_result == 1 and bounds[1] < user_time_seconds:
            addLSTMresultDelayAnomalyOnLog(LSTM_result, predicted_value, bounds[1], user_time_seconds, data)
        elif bounds[1] < user_time_seconds:
            addDelayAnomalyOnLog(bounds[1], user_time_seconds, data)
        elif LSTM_result == 1:
            addLSTMresultAnomalyOnLog(LSTM_result,data, predicted_value)
        else: 
            write_log("[PATTERN CHOSEN]" + data)
    else: 
        print("Unexpected classified number returned.")

    return positive_pattern


def process_moving_average(buffer):
    global desired_log_classifier
    global positive_pattern
    global result_data



    return positive_pattern
            
#if __name__ == "__main__":
main_for_classified_logs()        
        
            
    