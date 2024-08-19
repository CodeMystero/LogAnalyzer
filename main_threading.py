import os
import time
import threading
from queue import Queue
from datetime import datetime
from collections import deque
from logPreprocessing import logClassifier, pattern_features
from algorithmLog import movingAverage
from LSTMmodelling import LSTMinference
##########################################################################
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 공유 변수
shared_data = {
    "result": None,
    "user_time_seconds": None,
    "bounds": (None, None),
    "LSTM_result": None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(shared_data)

def start_flask_app():
    app.run(debug=True, use_reloader=False)

#############################################################################


def get_log_file_path(date=None):
 
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    return f"MeasurementDAQLog_{date}.log"

def monitor_log_file(file_path, buffer):
   
    current_date = datetime.now().strftime('%Y%m%d')
    last_position = 0
    
    # 기존 로그 내용을 처음부터 읽어와 버퍼에 저장
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                buffer.append(line.strip())
                #print(f"Initial load to buffer: {line.strip()}")
            last_position = file.tell()  # 마지막 위치 저장
    
    # 이후 로그 파일을 실시간으로 감시
    while True:
        new_date = datetime.now().strftime('%Y%m%d')
        
        # 자정이 지나면 새로운 로그 파일로 변경
        if new_date != current_date:
            current_date = new_date
            file_path = get_log_file_path(current_date)
            last_position = 0  # 새로운 파일의 시작 위치로 초기화
            #print(f"Switching to new log file: {file_path}")
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                file.seek(last_position)  # 마지막 읽은 위치로 이동
                for line in file:
                    buffer.append(line.strip())
                    #print(f"New line added to buffer: {line.strip()}")
                last_position = file.tell()  # 파일의 마지막 위치 저장

        time.sleep(0)  # 1초 간격으로 파일 감시


def start_log_monitor(buffer):
    """
    로그 감시를 스레드로 시작합니다.
    """
    file_path = get_log_file_path()
    log_thread = threading.Thread(target=monitor_log_file, args=(file_path, buffer))
    log_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료
    log_thread.start()
    
    
def send_log_to_buffer_with_interval(file_path, buffer, interval=0.1):
    
    """
    로그 파일의 내용을 처음부터 한 줄씩 읽어 지정된 시간 간격마다 버퍼로 보냅니다.
    
    :param file_path: 로그 파일 경로
    :param buffer: 데이터를 저장할 버퍼
    :param interval: 한 줄씩 버퍼로 보내는 시간 간격(초)
    """
    
    if not os.path.exists(file_path):
        print(f"{file_path} 파일을 찾을 수 없습니다.")
        return
    
    with open(file_path, 'r') as file:
        for line in file:
            buffer.append(line.strip())
            #print(f"Line added to buffer: {line.strip()}")
            time.sleep(interval)  # 지정된 시간 간격 동안 대기

def start_log_reader_with_interval(buffer, interval=0): # 인터벌 여기
    
    """
    로그 파일을 지정된 시간 간격으로 읽어 버퍼로 보내는 작업을 스레드로 시작합니다.
    
    :param file_path: 로그 파일 경로
    :param buffer: 데이터를 저장할 버퍼
    :param interval: 한 줄씩 버퍼로 보내는 시간 간격(초)
    """
    
    file_path = 'MeasurementDAQLog_20240724.log'
    log_thread = threading.Thread(target=send_log_to_buffer_with_interval, args=(file_path, buffer, interval))
    log_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료
    log_thread.start()
 
 
log_queue = Queue()
group_event = threading.Event()
 
def log_classifier_():
    classifier = logClassifier.LogClassifier()
    
    while(True):
        if buffer:
            example_log = buffer.popleft()
            #print(example_log)
            group, score = classifier.classify_log(example_log)
            
            #print(f"Log line classified as {group} with a similarity score of {score:.4f}")
            #print("\n")
            
            log_queue.put((example_log, group, score))
            group_event.set()
            
           

        
def start_log_classifier_():
    classifier_thread = threading.Thread(target=log_classifier_, args=())
    classifier_thread.daemon = True  
    classifier_thread.start()
 
 
inference = LSTMinference.LSTMInference() 
is_added = 0 # 0 not added 1 added
positive_pattern = 0

feature_event = threading.Event()
def pattern_features_():
    global is_added
    global positive_pattern
    while(True):
        
        group_event.wait()
        example_log, group, score = log_queue.get()
        group_event.clear()
        
        
        group_num = inference.sentence_to_group_number(group)
        positive_pattern = group_num
        is_added = 1
        
        if group == "group_1.txt":
            pass
            
        elif group == "group_2.txt":
            group2_extractor = pattern_features.Group2Extractor(group_number=2)
            new_log_line = example_log
            group2_extractor.add_feature(new_log_line)
            feature_event.set()
            
        elif group == "group_3.txt":
            pass
            
        elif group == "group_4.txt":
            pass
        
        elif group == "group_5.txt":
            pass
            
        elif group == "group_6.txt":
            pass
            
        elif group == "group_7.txt":
            pass
            
        elif group == "group_8.txt":
            pass

def start_pattern_features_():
    features_thread = threading.Thread(target=pattern_features_, args=())
    features_thread.daemon = True
    features_thread.start()
 

 
def moving_average_():
    detector = movingAverage.TimeSeriesAnomalyDetector(window_size=60)
    directory = "log_groups/pattern_features"
    file_name = "extracted_features_group_2.csv"
    file_path = os.path.join(directory, file_name)
    
    ################
    global shared_data
    ################
    
    while(True):
        feature_event.wait()
        result, bounds, user_time_seconds = detector.process_last_line_from_file(file_path)
        print(bounds)
        ######################
        shared_data["result"] = result
        shared_data["bounds"] = bounds
        shared_data["user_time_seconds"] = user_time_seconds
        ##########################
        feature_event.clear()
        
def start_moving_average_():

    maverage_thread = threading.Thread(target=moving_average_, args=())
    maverage_thread.daemon = True
    maverage_thread.start()

values = {
        "previous": None,
        "current": 0
        }

def update_infered_result(new_value):
    values["previous"] = values["current"]
    values["current"] = new_value 
    
def LSTM_inference_():
    LSTM_result = 0 #이 값이 0이면 정상 1이면 문제 있음 
    global is_added
    
    ###########
    global shared_data
    ############
    
    while(True):
        feature_event.wait()
        if is_added:
            next_value = inference.predict_next_value()
            update_infered_result(next_value)
            
            print(f'previous value : {values["previous"]}')
            print(f'positive_pattern : {positive_pattern}')
            
            # LSTM 예측 값과 positive_pattern 비교
            tolerance = 1  # 허용 오차 설정

            if abs(values["previous"] - positive_pattern) <= tolerance:
                LSTM_result = 0  # 예측 값이 실제 값과 거의 같은 경우
            else:
                LSTM_result = 1  # 예측 값이 실제 값과 충분히 다른 경우
                
            inference.add_number_to_queue(positive_pattern)   
            shared_data["LSTM_result"] = LSTM_result            
            print(f'LSTM_result: {LSTM_result}')
            is_added = 0

def start_LSTM_inference_():

    LSTM_thread = threading.Thread(target=LSTM_inference_, args=())
    LSTM_thread.daemon = True
    LSTM_thread.start()  
 


 
if __name__ == "__main__":
    buffer = deque(maxlen=10000)
    start_log_reader_with_interval(buffer)    
    start_log_classifier_()
    start_pattern_features_();
    start_moving_average_()
    start_LSTM_inference_()

    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    while(True):
        pass
            
            
        