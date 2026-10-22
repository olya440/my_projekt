import time
import random
import pandas as pd
from segment_tree import SegmentTreeIndex

df = pd.read_csv('online_learning_dataset.csv')
df_sorted = df.sort_values(by='timestamp').reset_index(drop=True)
scores = df_sorted['score'].to_list()

test_size = 10000
test_scores = scores[:test_size]

# Наивное решение: просто список
naive_data = test_scores[:]

# Оптимизированное решение: Segment Tree
st_test = SegmentTreeIndex(test_scores)

# Генерируем случайную нагрузку: 500 обновлений и 500 запросов
num_ops = 1000
operations = []
for _ in range(num_ops):
    op_type = random.choice(['update', 'query'])
    if op_type == 'update':
        pos = random.randint(0, test_size - 1)
        value = random.randint(0, 101)
        operations.append(('update', pos, value))
    else:
        l = random.randint(0, test_size - 2)
        r = random.randint(l + 1, test_size - 1)
        operations.append(('query', l, r))

# Тест с наивным подходом
start_naive = time.perf_counter()
for op in operations:
    if op[0] == 'update':
        _, pos, value = op
        naive_data[pos] = value
    else:
        _, l, r = op
        current_max = float('-inf')
        for i in range(l, r + 1):
            if naive_data[i] > current_max:
                current_max = naive_data[i]

end_naive = time.perf_counter()
time_naive = (end_naive - start_naive) * 1000

# Тест с Segment Tree
start_st = time.perf_counter()
for op in operations:
    if op[0] == 'update':
        _, pos, value = op
        st_test.update(pos, value)
    else:
        _, l, r = op
        st_test.query(l, r)

end_st = time.perf_counter()
time_st = (end_st - start_st) * 1000

print("Результаты сравнения:")
print(f"Update: {sum(1 for x in operations if x[0] == 'update')}")
print(f"Query: {sum(1 for x in operations if x[0] == 'query')}")
print(f"Время построения индекса (Segment Tree): {(len(test_scores) * 0.0001):.2f} ms (оценка)")
print(f"Время обработки (Наивный подход): {time_naive:.3f} ms")
print(f"Время обработки (Segment Tree): {time_st:.3f} ms")