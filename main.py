import os
import time
import threading
from queue import Queue
from datetime import datetime
from collections import deque
from logPreprocessing import logClassifier, pattern_features, classifying_only_desired_log
from algorithmLog import movingAverage
from LSTMmodelling import LSTMinference

####### Condition 객체를 사용한 buffer 관리 추가 ########
buffer_lock = threading.Lock()
buffer_not_full = threading.Condition(buffer_lock)
buffer_not_empty = threading.Condition(buffer_lock)

# buffer max length
BUFFER_SIZE = 50000
####### Condition 객체를 사용한 buffer 관리 추가 끝 ########


########################################################################## 플라스크 web UI
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 공유 변수
shared_data = {
    "log": None, 
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

classifier = logClassifier.LogClassifier()
LSTMinfer = LSTMinference.LSTMInferenceTorch() 
desired_log_classifier = classifying_only_desired_log.desiredLogClassifier()

buffer_lock = threading.Lock()

detector = movingAverage.TimeSeriesAnomalyDetector(window_size=200)
directory = "log_groups/common_features"
file_name = "extracted_common_times.csv"
file_path = os.path.join(directory, file_name)
#############################################################################

def send_log_to_buffer_with_interval(file_path, buffer):
    
    if not os.path.exists(file_path):
        print(f"{file_path} 파일을 찾을 수 없습니다.")
        return
    
    with open(file_path, 'r') as file:
        file.seek(0)  # 파일 포인터를 처음으로 이동
        ####### 버퍼가 가득 찼을 때 대기하는 로직 추가 ########
        for line in file:
            with buffer_not_full:  # 버퍼에 여유 공간이 있을 때까지 대기
                while len(buffer) >= BUFFER_SIZE:
                    buffer_not_full.wait()

                with buffer_lock:  # 락을 사용하여 버퍼에 안전하게 접근
                    buffer.append(line.strip())
                    buffer_not_empty.notify()  # 버퍼가 비어 있지 않음을 알림

            time.sleep(0)  # 지정된 시간 간격 동안 대기
        ####### 버퍼가 가득 찼을 때 대기하는 로직 추가 끝 ########        
        
        # for line in file:
            # with buffer_lock:  # 락을 사용하여 버퍼에 안전하게 접근
                # buffer.append(line.strip())
                # #print(line)
            # #print(f"Line added to buffer: {line.strip()}")
            # time.sleep(0.0001)  # 지정된 시간 간격 동안 대기

def start_log_reader_with_interval(buffer): # 인터벌 여기
    buffer.clear()
    file_path = 'MeasurementDAQLog_20240730_B_1.log'
    log_thread = threading.Thread(target=send_log_to_buffer_with_interval, args=(file_path, buffer))
    log_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료
    log_thread.start()

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
        LSTM_result = 0  # 예측 값이 실제 값과 거의 같은 경우
    else:
        LSTM_result = 1  # 예측 값이 실제 값과 충분히 다른 경우
        
    LSTMinfer.add_number_to_queue(positive_pattern)   
    
    return LSTM_result, next_value
    
def write_log(log):
    log_file_path = 'anomaly_MeasurementDAQLog_20240730_B_1_2.log'
    with open(log_file_path, 'a') as log_file:
        log_file.write(log + "\n")    
    
def write_log_filtered(log):
    log_file_path = 'anomaly_MeasurementDAQLog_20240730_B_1_2.log'
    with open(log_file_path, 'a') as log_file:
        log_file.write("[PATTERN CHOSEN] " + log + "\n")
    
def addLSTMresultDelayAnomalyOnLog(LSTM_result, predicted_value, maxValue, userTime, example_log):
    log_file_path = 'anomaly_MeasurementDAQLog_20240730_B_1_2.log'
    
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
    
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write("\n")
        log_file.write(f"{anomaly_log_counter} 번째 이상치 검출 : 아래의 위치에는 다음과 같은 패턴이 예상됩니다. | {regex_patterns[predicted_value-1]}\n")
        log_file.write(f"                        동시에 해당 로그는 예측범위보다 {time_exceeded} us 지연되었습니다. \n")
        log_file.write("==================================================================================================================\n")
        log_file.write(str(example_log) + "\n")
        log_file.write("==================================================================================================================\n")
        log_file.write("\n")
    
    anomaly_log_counter +=1
    
    
anomaly_log_counter = 1
def addLSTMresultAnomalyOnLog(LSTM_result, example_log, predicted_value):
    global anomaly_log_counter
    log_file_path = 'anomaly_MeasurementDAQLog_20240730_B_1_2.log'
    
    
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
    log_file_path = 'anomaly_MeasurementDAQLog_20240730_B_1_2.log'
    global anomaly_log_counter
    
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
     
def main_for_classified_logs():
    buffer = deque(maxlen=BUFFER_SIZE)
    start_log_reader_with_interval(buffer)
    
    global desired_log_classifier
    global positive_pattern
    
    regex_patterns = [
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-M#\d{2}',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-API : .*MsgL=\d+,.*ProVer=10002.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC->API : .*MsgL=\d+,.*ProVer=10003.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*RawData.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*SpecNPara.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV'
    ]
    
    # flask_thread = threading.Thread(target=start_flask_app)
    # flask_thread.daemon = True
    # flask_thread.start()
    
    time.sleep(0.2)
    
    count = 0
    
    while(True):
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
        
        positive_pattern = desired_log_classifier.classify_single_log(example_log, regex_patterns)
       
        if positive_pattern == None:
            write_log(example_log)
            result = 0 
            
        elif positive_pattern in {1, 2, 3, 4, 5, 6}:
            
            pattern_features_(example_log, positive_pattern)
            #start_time = time.time()
            LSTM_result, predicted_value = LSTM_inference_()
            #end_time = time.time()  # 코드 실행 후 시간 기록

            #elapsed_time = end_time - start_time  # 실행 시간 계산
            #print(f"실행 시간: {elapsed_time}초")
            
           
            
            shared_data["LSTM_result"] = LSTM_result
            shared_data["log"] = example_log
            
            result, bounds, user_time_seconds = moving_average_()
            
            shared_data["result"] = result
            shared_data["bounds"] = bounds
            shared_data["user_time_seconds"] = user_time_seconds
            
            
            if count > 200:
                
                if LSTM_result == 1 and bounds[1] < user_time_seconds:
                    
                    addLSTMresultDelayAnomalyOnLog(LSTM_result, predicted_value, bounds[1], user_time_seconds, example_log)
             
                elif bounds[1] < user_time_seconds:
                    
                    addDelayAnomalyOnLog(bounds[1], user_time_seconds, example_log)
                    
                elif LSTM_result == 1:
                    
                    addLSTMresultAnomalyOnLog(LSTM_result,example_log, predicted_value)
                    
                else: 
                    
                    write_log_filtered(example_log)
                    
            else:
                
                write_log_filtered(example_log)
                count+=1
                
            result = 0 
            
        else:
            
            print("올바른 분류값이 나오지 않았습니다")
            result = 0 
            
if __name__ == "__main__":
    main_for_classified_logs()        
        
            
    