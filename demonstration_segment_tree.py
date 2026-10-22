import pandas as pd
from segment_tree import SegmentTreeIndex

# 1. Исходные данные
df = pd.read_csv('online_learning_dataset.csv')
df_sorted = df.sort_values(by='timestamp').reset_index(drop=True)
scores = df_sorted['score'].to_list()

# 2. Построение Segment Tree
st_index = SegmentTreeIndex(scores)

# 3. Query (до изменений)
# Ищем максимальную оценку среди первых 1000 взаимодействий
max_score = st_index.query(0, 999)
print(f"Максимальная оценка до изменений среди первой 1000 записей: {max_score}")

## 4. Update (изменение данных)
# Представим, что студенту исправили оценку в 50-й строке на 100 баллов
row_id_to_update = 50
update_score = 101
st_index.update(row_id_to_update, update_score)

# 5. Query (после изменений)
# Проверяем, что дерево увидело изменение
max_score_after = st_index.query(0, 999)
print(f"Максимальная оценка после обновления: {max_score_after}")

if max_score_after == 101:
    print("УРОООО Дерево работает корректно")
else:
    print("Что то пошло не так...")