from itertools import chain
from tqdm import tqdm
from collections import defaultdict

def read_sequences_from_file(filename, sequence_length):
    sequences = []
    current_sequence = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in tqdm(lines, desc="Reading sequences", unit=" lines"):
            number = int(line.strip())
            current_sequence.append(number)

            if len(current_sequence) == sequence_length:
                sequences.append(current_sequence)
                current_sequence = []

    return sequences

def is_subsequence(sequence, subsequence):
    iter_seq = iter(sequence)
    return all(item in iter_seq for item in subsequence)

def count_support(candidates, sequences):
    support_count = defaultdict(int)
    for candidate in candidates:
        for sequence in sequences:
            if is_subsequence(sequence, candidate):
                support_count[candidate] += 1
    return support_count

def filter_candidates(support_count, min_support):
    return {candidate: count for candidate, count in support_count.items() if count >= min_support}

def generate_candidates(prev_frequent, length):
    candidates = set()
    prev_frequent_list = list(prev_frequent)
    for i in range(len(prev_frequent_list)):
        for j in range(i + 1, len(prev_frequent_list)):
            candidate = tuple(sorted(set(prev_frequent_list[i]) | set(prev_frequent_list[j])))
            if len(candidate) == length:
                candidates.add(candidate)
    return candidates

def gsp(sequences, min_support, start_k=2, max_k=None):
    items = set(chain.from_iterable(sequences))
    
    # Generate frequent k-itemsets starting from start_k
    if start_k == 1:
        candidates = {(item,) for item in items}
        support_count = count_support(candidates, sequences)
        frequent = filter_candidates(support_count, min_support)
    else:
        candidates = {(item,) for item in items}
        frequent = filter_candidates(count_support(candidates, sequences), min_support)

    all_frequent = frequent.copy()
    k = start_k

    with tqdm(total=(max_k - start_k + 1) if max_k else len(items), desc="Generating frequent sequences", unit=" step") as pbar:
        while frequent and (max_k is None or k <= max_k):
            if max_k is not None and k > max_k:
                break
            
            candidates = generate_candidates(frequent.keys(), k)
            support_count = count_support(candidates, sequences)
            frequent = filter_candidates(support_count, min_support)
            all_frequent.update(frequent)
            k += 1
            pbar.update(1)

    return all_frequent

# 사용 예시
filename = 'group_sequence.txt'
sequence_length = 100
min_support = 1
start_k = 2  # 시작 k값
max_k = 5  # 최대 k값

# 파일에서 시퀀스를 읽어옴
sequences = read_sequences_from_file(filename, sequence_length)

# GSP 알고리즘 실행
frequent_patterns = gsp(sequences, min_support, start_k, max_k)

# 결과 출력
print(f"Total frequent patterns found: {len(frequent_patterns)}")
for pattern, frequency in sorted(frequent_patterns.items(), key=lambda x: (len(x[0]), x)):
    print(f"Pattern: {pattern}, Frequency: {frequency}")
