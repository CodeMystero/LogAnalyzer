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
        "group_9.txt": 9,
        "group_10.txt": 10,
        "group_11.txt": 11,
        "group_12.txt": 12,
        "group_13.txt": 13,
        "group_14.txt": 14,
        "group_15.txt": 15,
        "group_16.txt": 16,
        "group_17.txt": 17,
        "group_18.txt": 18,
        "group_19.txt": 19,
        "group_20.txt": 20,
        "group_21.txt": 21,
        "group_22.txt": 22,
        "group_23.txt": 23,
        "group_24.txt": 24,
        "group_25.txt": 25,
        "group_26.txt": 26,
        "group_27.txt": 27,
        "group_28.txt": 28,
        "group_29.txt": 29,
        "group_30.txt": 30,
        "group_31.txt": 31,
        "group_32.txt": 32,
        "group_33.txt": 33,
        "group_34.txt": 34,
        "group_35.txt": 35,
        "group_36.txt": 36,
        "group_37.txt": 37,
        "group_38.txt": 38,
        "group_39.txt": 39,
        "group_40.txt": 40,
        "group_41.txt": 41,
        "group_42.txt": 42,
        "group_43.txt": 43,
        "group_44.txt": 44,
        "group_45.txt": 45,
        "group_46.txt": 46,
        "group_47.txt": 47,
        "group_48.txt": 48,
        "group_49.txt": 49,
        "group_50.txt": 50,
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
