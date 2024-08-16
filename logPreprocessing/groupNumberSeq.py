import logClassifier
import os

def generate_group_sequence(log_file_path, classifier, output_file="group_sequence.txt", max_lines=50000):
    group_sequence = []
    total_lines = 0

    # 그룹 이름을 고정된 숫자에 매핑
    group_to_number = {
        "group_1.txt": 1,
        "group_2.txt": 2,
        "group_3.txt": 3,
        "group_4.txt": 4,
        "group_5.txt": 5,
        "group_6.txt": 6,
        "group_7.txt": 7,
        "group_8.txt": 8,
        # 필요한 만큼 추가
    }

    with open(log_file_path, 'r') as log_file:
        with open(output_file, 'w') as out_file:
            for i, line in enumerate(log_file):
                if i >= max_lines:  # 최대 줄 수를 넘으면 중단
                    break
                line = line.strip()  # 공백 제거
                if line:  # 공백 줄은 무시
                    group, _ = classifier.classify_log(line)
                    group_sequence.append(group)
                
                # 몇 번째 줄 처리 중인지 출력
                if (i + 1) % 100 == 0 or i == 0:  # 100줄마다 또는 처음에 한 번 출력
                    print(f"Processing line {i + 1}/{max_lines}...")
                
                total_lines += 1

            # 숫자 시퀀스를 파일에 저장
            for group in group_sequence:
                if group in group_to_number:
                    number = group_to_number[group]
                    out_file.write(f"{number}\n")
                else:
                    print(f"Warning: {group} not found in predefined group mappings.")

    print(f"Group sequence saved to {output_file}")
    print(f"Total lines processed: {total_lines}")
    return group_sequence

if __name__ == "__main__":
    # LogClassifier 초기화
    classifier = logClassifier.LogClassifier()

    # 로그 파일 경로
    log_file_path = os.path.join(os.path.dirname(__file__), "..", "MeasurementDAQLog_20240730.log")
    group_sequence_file = os.path.join(os.path.dirname(__file__), "group_sequence.txt")

    # 로그를 시퀀스 그룹 숫자로 변환하여 파일에 저장 (최대 10,000줄만 읽음)
    if os.path.exists(log_file_path):
        generate_group_sequence(log_file_path, classifier, output_file=group_sequence_file, max_lines=20000)
    else:
        print(f"Log file {log_file_path} does not exist.")
