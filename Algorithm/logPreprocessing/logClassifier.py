from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import numpy as np

class LogClassifier:
    def __init__(self, group_dir=None, lines_per_group=1000, ngram_range=(1, 3), min_df=2, max_df=0.8, max_features=5000):
        if group_dir is None:
            # 현재 파일의 경로를 기준으로 상위 디렉토리로 이동하여 log_groups 폴더 설정
            group_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log_groups")

        self.group_dir = group_dir
        self.lines_per_group = lines_per_group  # 그룹 파일에서 읽어올 줄 수 설정
        self.vectorizer = TfidfVectorizer(ngram_range=ngram_range, min_df=min_df, max_df=max_df, max_features=max_features)
        self.group_vectors = []
        self.group_names = []

        self._initialize_groups()

    def _initialize_groups(self):
        """
        그룹 디렉토리에서 그룹 파일을 읽어와 수치화합니다.
        각 그룹 파일에서 지정된 수만큼의 문장을 읽어옵니다.
        """
        group_texts = []
        for file_name in os.listdir(self.group_dir):
            if file_name.startswith("group_") and file_name.endswith(".txt"):
                group_path = os.path.join(self.group_dir, file_name)
                with open(group_path, 'r') as file:
                    lines = []
                    for i in range(self.lines_per_group):
                        line = file.readline()
                        if not line:
                            break
                        lines.append(line.strip())
                    if lines:  # 내용이 있으면 벡터화 대상에 추가
                        group_text = ' '.join(lines)
                        self.group_names.append(file_name)
                        group_texts.append(group_text)

        if group_texts:
            self.group_vectors = self.vectorizer.fit_transform(group_texts)
        else:
            raise ValueError("No valid group files found or files are empty. Please check the group directory.")


    def classify_log(self, log_line):
        """
        버퍼에서 들어온 문장을 그룹 파일과 비교하여 해당 그룹을 리턴합니다.
        """
        
        if not isinstance(log_line, str):
            log_line = ' '.join(log_line)  # deque나 리스트일 경우 문자열로 변환

        if self.group_vectors is None or self.group_vectors.shape[0] == 0:
            raise ValueError("The TF-IDF vectorizer has not been fitted. Ensure the group files are correctly loaded and processed.")
    
        log_vector = self.vectorizer.transform([log_line])

        # 각 그룹과 문장의 코사인 유사도 계산
        similarities = cosine_similarity(log_vector, self.group_vectors)
        
        # 가장 유사한 그룹 선택
        best_match_index = np.argmax(similarities)
        best_match_group = self.group_names[best_match_index]
        best_match_score = similarities[0, best_match_index]

        return best_match_group, best_match_score

if __name__ == "__main__":
    # 예제 실행
    classifier = LogClassifier()

    # 버퍼에서 읽어온 문장을 분류 (예제 문장)
    example_log = "Example log line to classify."
    group, score = classifier.classify_log(example_log)

    print(f"Log line classified as {group} with a similarity score of {score:.4f}")
