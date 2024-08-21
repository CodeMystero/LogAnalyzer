import csv
import os

# 로그 파일과 출력 CSV 파일 경로 설정
log_file_path = os.path.join('MeasurementDAQLog_20240730.log')
output_csv_path = os.path.join('extracted_times.csv')

def extract_time_from_line(line):
    """
    로그 파일의 한 줄에서 시간 정보를 추출합니다.
    시간 정보는 라인의 가장 앞에 00:00:00.000000 형식으로 위치한다고 가정합니다.
    """
    return line[:15]  # 처음 15글자까지가 시간 정보입니다.

def process_log_file(log_file_path, output_csv_path):
    """
    로그 파일을 읽어 시간 정보를 추출하고, 진행 상황을 출력합니다.
    추출된 시간 정보는 CSV 파일에 저장됩니다.
    """
    total_lines = sum(1 for _ in open(log_file_path, 'r', encoding='utf-8'))  # 전체 줄 수 계산
    print(f"총 {total_lines} 줄의 로그를 처리합니다.")

    with open(log_file_path, 'r', encoding='utf-8') as log_file, \
            open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time'])  # CSV 헤더 작성

        for i, line in enumerate(log_file, 1):
            time_info = extract_time_from_line(line)
            csv_writer.writerow([time_info])

            # 진행 상황 출력 (만 줄마다)
            if i % 10000 == 0 or i == total_lines:
                print(f"{i}/{total_lines} 줄 처리 완료 ({(i/total_lines)*100:.2f}%)")

if __name__ == "__main__":
    process_log_file(log_file_path, output_csv_path)
    print("시간 정보 추출 완료, 결과가 CSV 파일에 저장되었습니다.")
