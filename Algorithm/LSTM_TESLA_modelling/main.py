import collections
import threading
import time
import mmap

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
                    
                while len(self.log_buffer) >= self.log_buffer.maxlen:
                    time.sleep(0.1)
                    
                self.log_buffer.append(line)
                print(len(self.log_buffer))
                time.sleep(self.delay)
            mmap_obj.close()


class DataPreprocessor(threading.Thread):
    def __init__(self, raw_buffer, processed_buffer):
        super().__init__()
        self.raw_buffer = raw_buffer
        self.processed_buffer = processed_buffer
        self.daemon = True
        
    def run(self):
        while True:
            if self.raw_buffer:
                log_line = self.raw_buffer.popleft()
                processed_data = self.preprocess(log_line)
                self.processed_buffer.append(processed_data)
                
    def preprocess(self, log_line):
        
        return log_line

def main():
    
    file_path = 'MeasurementDAQLog_20240730.log'
    log_reading_delay = 1
    log_reader_buffer = collections.deque(maxlen = 10000)
    log_after_preprocessing_buffer = collections.deque(maxlen = 10000)
    
    log_reader = LogFileReader(file_path, log_reader_buffer, log_reading_delay)
    log_reader.start()
    
    
    

    
if __name__ == "__main__":
    main()