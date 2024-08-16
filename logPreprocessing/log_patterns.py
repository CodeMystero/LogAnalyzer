from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse
import numpy as np
import os

# ###################### 문장 길이 차이에 따른 가중치를 적용하는 함수 ######################
def adjusted_cosine_similarity_with_length(cosine_sim, log_data, length_tolerance=0.1):
    adjusted_sim = np.copy(cosine_sim)
    
    for i in range(len(cosine_sim)):
        for j in range(len(cosine_sim)):
            if i != j:
                # 문장 길이 차이 계산
                length_difference = abs(len(log_data[i]) - len(log_data[j])) / max(len(log_data[i]), len(log_data[j]))
                if length_difference > length_tolerance:
                    # 길이 차이가 클 경우 유사도에 패널티를 부여
                    adjusted_sim[i, j] *= (1 - length_difference)
    
    return adjusted_sim
# ###################### 문장 길이 차이에 따른 가중치를 적용하는 함수 끝 ######################


# 로그 파일에서 지정된 수만큼의 줄을 가져와서 처리하는 함수
def process_log_file(file_path, line_limit, threshold, max_groups=15):
    # 출력 디렉토리 생성
    output_dir = "log_groups"
    os.makedirs(output_dir, exist_ok=True)
    
    # 그룹별로 문장을 저장할 파일 이름 관리
    group_files = {}
    group_contents = []  # 각 그룹의 문장 리스트를 저장

    with open(file_path, "r") as file:
        # 지정된 줄 수만큼 파일에서 읽기
        lines = []
        for i in range(line_limit):
            line = file.readline()
            if not line:
                break
            lines.append(line.strip())
            
            # 진행 상황 출력 (퍼센트)
            progress = (i + 1) / line_limit * 100
            print(f"Reading lines... {progress:.2f}% complete", end='\r')
    
    if lines:
        print(f"\nProcessing {len(lines)} lines...")

        # TF-IDF 벡터화 및 코사인 유사도 계산
        vectorizer = TfidfVectorizer(ngram_range=(1, 3), min_df=2, max_df=0.8, max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(lines)
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # 문장 길이 차이에 따른 가중치 적용
        adjusted_sim = adjusted_cosine_similarity_with_length(cosine_sim, lines, length_tolerance=0.1)

        # 그룹화
        groups = group_similar_sentences(adjusted_sim, threshold)

        # 그룹별 텍스트 파일 작성 또는 이어쓰기
        for idx, group in enumerate(groups):
            group_signature = tuple(sorted([lines[g] for g in group]))  # 그룹 서명으로 문장 내용을 사용
            
            if len(group_files) < max_groups:
                if group_signature not in group_files:
                    group_filename = os.path.join(output_dir, f"group_{len(group_files)+1}.txt")
                    group_files[group_signature] = group_filename
                    group_contents.append([lines[g] for g in group])
            else:
                # 최대 그룹 수를 초과할 경우, 가장 유사한 기존 그룹에 포함
                best_match_idx = None
                best_match_score = -1
                new_group_text = ' '.join([lines[g] for g in group])
                
                for idx, existing_group in enumerate(group_contents):
                    existing_group_text = ' '.join(existing_group)
                    combined_text = [new_group_text, existing_group_text]
                    combined_vector = vectorizer.transform(combined_text)
                    similarity = cosine_similarity(combined_vector[0], combined_vector[1])[0][0]
                    
                    if similarity > best_match_score:
                        best_match_score = similarity
                        best_match_idx = idx
                
                # 가장 유사한 그룹에 포함
                best_group_signature = list(group_files.keys())[best_match_idx]
                group_filename = group_files[best_group_signature]
                group_contents[best_match_idx].extend([lines[g] for g in group])

            with open(group_filename, "a") as f:
                for sentence_index in group:
                    f.write(lines[sentence_index] + "\n")
            print(f"  - Group {len(group_files)} written to {group_filename}")

# 유사한 문장을 그룹화하는 함수
def group_similar_sentences(cosine_sim, threshold):
    grouped_indices = []
    visited = set()
    
    for i in range(len(cosine_sim)):
        if i not in visited:
            similar_indices = np.where(cosine_sim[i] > threshold)[0]
            visited.update(similar_indices)
            grouped_indices.append(similar_indices)
    
    return grouped_indices

# 메인 실행 함수
def main():
    parser = argparse.ArgumentParser(description="Process a limited number of log lines and group similar lines.")
    parser.add_argument('file_path', type=str, nargs='?', default="MeasurementDAQLog_20240724.log", help="Path to the log file")
    parser.add_argument('--line_limit', type=int, default=10000, help="Number of lines to process from the log file")
    parser.add_argument('--threshold', type=float, default=0.9, help="Threshold for cosine similarity grouping")
    parser.add_argument('--max_groups', type=int, default=15, help="Maximum number of groups to create")

    args = parser.parse_args()

    process_log_file(args.file_path, args.line_limit, args.threshold, args.max_groups)

if __name__ == "__main__":
    main()
