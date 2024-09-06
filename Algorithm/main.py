"""
LSTM, 이동평균 로깅 객체화 완료 실제 로그와 데이터 정합성 체크 완료 20240906

import 모듈 설명:

    - `logPreprocessing`: 로그를 전처리하는 함수 및 클래스
    - `logClassifier`: 로그를 정의된 기준에 따라 분류합니다.
    - `pattern_features`: 로그 패턴에서 특징을 추출합니다.
    - `classifying_only_desired_log`: 관심 있는 로그만 필터링하고 분류하여 처리
    - `ParsedData`: 타임스탬프와 로그 내용을 포함하는 파싱된 로그 데이터를 나타냄
    - `movingAverage`: 이동 평균 계산을 수행
    - `LSTMinference`: LSTM 기반의 추론 또는 모델링을 처리
    - `Log`: logging 스레드 제공, addLog메서드 통해서 데이터 입력 및 로그 파일 생성 및 입력
    - `file_lock`: 파일 무결성을 위한 lock 함수 파일을 열고 닫는 모듈 -> main, Log

"""
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

class LoadDataThread(threading.Thread):
    """
        로그(raw data)를 읽어와서 버퍼에 넣는 클래스 

        상속 : thread를 상속받아 thread처리 

        버퍼 : 전역으로 선언된 버퍼에 로그를 로딩

        arg :
            file_path : 로그 파일의 절대 경로를 입력받아 처리함
    """
    def __init__(self, file_path):
        """
            필드 : 
                self.file_path :    로그(raw data)가 존재하는 파일의 절대 경로
                self.daemon :   부모 프로세스 종료시 자식 프로세스, 즉 데이터 로깅 스레드 
                                강제 종료
        """
        super().__init__()
        self.file_path = file_path
        self.daemon = True

    def run(self):
        """
            arg :
                없음

            파일을 열어 한줄씩 버퍼에 입력, splitData 함수를 통해 로그를 timestamp, data
            로 분리 후 버퍼에 입력 type은 딕셔너리, line.strip()이유는 로그마다 개행문자가
            두개 붙어 있음, 버퍼가 비어있거나, 가득 찼을때의 상태는 .put메서드를 사용할때 
            기본적으로 그것을 체크하는 기능이 내재 되어 있음

        """
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
    """
        Process 버퍼에 데이터를 넣어 해당 버퍼의 데이터를 process함수에 넘기는 스레드 

        상속 : thread를 상속받아 병렬처리 
        
        필드 : 
            self._step_event : 중지 플래그를 위한 Event 객체 생성
            self.daemon : 부모 프로세스 종료시 자식 프로세스, 즉 데이터 로깅 스레드 
                        강제 종료

        arg:
            없음
    
    """
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()  
        self.daemon = True

    def run(self):
        """
            라인 해석:
                while not self._stop_event.is_set(): -> stop메서드 이벤트를 통해 
                                                    self._stop_event가 set이 되면 스레드 종료
                if process_buffer.qsize() >= 30: -> 로그가 30개 이상 쌓이면 이상치 판정 시작
        """

        print("Process buffer thread started")

        while not self._stop_event.is_set():
            with buffer_lock:
     
                data = buffer.get()
                process_buffer.put(data)
                

                if process_buffer.qsize() >= 30:
                    
                    process(process_buffer)

        print(f"AddRawDataThread finished.")

    def stop(self):
        self._stop_event.set()  # 중지 플래그를 설정하여 반복문 종료

            
# buffer 관련
buffer_size =                   2000000
buffer =                        queue.Queue(maxsize=buffer_size)
process_buffer =                queue.Queue(maxsize=200)

log_file =                      "MeasurementDAQLog_20240730.log"
main_dir =                      os.path.dirname(os.path.abspath(__file__))
log_dir =                       os.path.join(main_dir, '..', 'Input', 'Raw')
file_path =                     os.path.join(log_dir, log_file)

log_Thread =                    log.LogThread()
buffer_lock =                   threading.Lock()
load_Data_Thread =              LoadDataThread(file_path)
process_Thread =                ProcessThread()
moving_average =                movingAverage.MovingAverage()
parsing =                       ParsedData.ParsedData()
LSTMinfer =                     LSTMinference.LSTMInferenceTorch() 
desired_log_classifier =        classifying_only_desired_log.desiredLogClassifier()
anomaly_log_counter =           1
positive_pattern =              0
regex_patterns = [
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-M#\d{2}',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC<-API : .*MsgL=\d+,.*ProVer=10002.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} PC->API : .*MsgL=\d+,.*ProVer=10003.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*RawData.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV .*SpecNPara.*',
        r'\d{2}:\d{2}:\d{2}\.\d{6} M#\d{2} Save CSV'
    ]

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
    """
        splitData함수를 통해서 rawData (로그파일에서 한줄)을 받아 timestamp와 data로 나눠서
        딕셔너리로 값을 반환 (버퍼에 딕셔너리 형태로 데이터가 입력 및 출력)

        arg :
            rawData : 한줄의 로그 데이터
    """
    parts = rawData.split()
    if len(parts) < 2 :
        raise ValueError("입력 문자열이 올바른 형식이 아닙니다.")
    timestamp = parts[0]
    data = " ".join(parts[1:])
    parsing.update(timestamp, data)

    return parsing.to_dict()

def LSTM_inference_():
    """
        LSTM모델을 사용하여 예측패턴을 추론하는 함수. 해당 함수를 통해 로그에서 불러온 패턴을 
        LSTM추론 모듈에 전달하여 해당 모듈의 버퍼를 채우고 다음 예상 패턴을 불러옴 

        arg : 
            tolerance : 예측값과 실제값의 차이를 설정할 수 있음. 해당 값이 높아지면 느슨하게 
                        판정하고 (이상치가 적어짐), 작아질 수록 타이트하게 판정함 (이상치가 많아짐)

            LSTM_result : 이상판정일때 1, 정상판정일때 0을 리턴함  
    """
    global positive_pattern
    next_value = LSTMinfer.predict_next_value()

    tolerance = 1

    if abs(next_value - positive_pattern) <= tolerance:
    
        LSTM_result = 0  

    else:

        LSTM_result = 1 
        
    LSTMinfer.add_number_to_queue(positive_pattern)   
    
    return LSTM_result, next_value
        
def write_log(log):
    """
        로그를 남기는 함수. 해당 함수는 이상치 검사에 해당하지 않는 로그의 라인들을 그대로 
        파일에 입력하는 함수. 

        arg :
            file_lock : 이상치 로그를 남기는 함수도 같은 파일을 열기 때문에, 데이터의
                        무결성을 위해서 양쪽에 file_lock을 걸어 파일을 동시에 열지 못하
                        도록 함 
            file_mode : 파일이 존재 하지 않다면 'w'모드로 파일을 생성 후 입력하고 
                        파일이 존재 한다면 'a'모드로 로그를 append함
    """
    now = datetime.now()
    log_file_path = 'D:/9999.Code/AnalyticsLog/Output/Log/anomaly_MeasurementDAQLog_' + now.strftime("%Y%m%d") + '.log'

    with file_lock:
        file_mode = 'a' if os.path.exists(log_file_path) else 'w'

        with open(log_file_path, file_mode) as log_file:
            log_file.write(log + "\n")    
    
def log_message(anomaly_log_counter, predicted_value,maxValue, userTime, example_log, regex_patterns, flag):
    """
        검사 결과를 data(딕셔너리) 메시지에 담아서 한번에 보내면 이상치 로그를 파일에 입력하기
        전에 해당 메시지를 받아 처리

        arg :
            time_exceeded : 시계열 검사 결과 max값과 실제 값의 차이를 통해 얼마의 시간이 초과
                            됐는지 계산
            value : 예측된 패턴 값, 시계열 검사 max값, 실제 로그에 기록된 시간, 초과된 시간 
                    (time_exceeded)를 기록 
            msg : 실제 로그
            regex_patters : 패턴을 찾기 위한 정규화 문장을 담은 리스트 
            flag : 해당 플래그를 통해 어떤 이상치를 가진 로그인지 판단 
    """
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
    """
        정규식을 통해 선별된 패턴의 로그를 파일에 입력하는 함수. data 메시지를 작성하고 
        해당 메시지를 이상치 로그 입력 스레드로 addLog함 

        arg :
            anomaly_log_counter : 현재까지 이상치 로그 발견 개수 
    """
    global anomaly_log_counter

    predicted_value = round(predicted_value)
    predicted_value = int(predicted_value)

    if predicted_value > 6:
        predicted_value = 6

    if predicted_value < 1:
        predicted_value = 1

    data = log_message(
        anomaly_log_counter,
        predicted_value,
        maxValue,
        userTime,
        example_log,
        regex_patterns,
        flag)
    
    log_Thread.addLog(data)

    if flag in {1, 2, 3}:
        anomaly_log_counter +=1
    
def main():
    """
        메인이 되는 함수. 로그 로딩, 로그 프로세스, 이상치 로그 파일 입력, 이 3가지 스레드를 
        작동 시키고 while을 통해 부모 프로세스를 작동시킴
    """
    loadRawData(file_path)

    while True: 
        pass

def process(process_buffer):
    """
    주어진 버퍼에서 로그 항목을 처리하고, 로그를 분류하며, LSTM 추론을 수행하고,
    이상 여부를 처리합니다.

    이 함수는 주어진 버퍼에서 로그 항목을 가져와 타임스탬프와 데이터를 추출한 후,
    로그 문자열을 생성합니다. 로그를 분류하여 positive_pattern 값을 결정하고,
    LSTM 추론을 수행하여 결과와 예측값을 얻습니다. 이동 평균을 업데이트하여 이상을 감지합니다.
    분류 패턴에 따라 로그를 작성하거나 추가 처리를 통해 이상을 처리하고,
    필요한 경우 관련 세부 정보를 기록합니다.

    Args:
        process_buffer (Queue): 처리할 로그 항목을 포함하는 큐입니다.

    Returns:
        None
    """
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
        
            
    