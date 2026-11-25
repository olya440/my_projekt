# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from hash_map import MyHashMap
from segment_tree import SegmentTreeIndex
from page_rank import PageRank
from binary_heap import BinaryHeap
from bootstrap import bootstrap_diff
from minhash_lsh import prepare_data_and_build_index, find_similar_students

app = Flask(__name__)

# 1. ЗАГРУЗКА И ПОДГОТОВКА ДАННЫХ

df = pd.read_csv('online_learning_dataset.csv')
df_sorted = df.sort_values(by='timestamp').reset_index(drop=True)
scores = df_sorted['score'].tolist()
keys = df_sorted['interaction_id'].tolist()

# Агрегация до уровня пар (студент, курс) для Bootstrap
pair_stats = df.groupby(['student_id', 'course_id'])['score'].mean().reset_index()

# 2. ИНИЦИАЛИЗАЦИЯ СТРУКТУР ДАННЫХ

# Hash Map: индекс по interaction_id
hash_index = MyHashMap()
for row_id, key in enumerate(keys):
    hash_index.put(key, row_id)

# Segment Tree: для запросов на отрезке оценок
seg_tree = SegmentTreeIndex(scores)

# Binary Heap: для быстрого доступа к глобальному максимуму
score_heap = BinaryHeap()
for s in scores:
    score_heap.push(s)

# PageRank: графовый анализ значимости курсов
edges_data = []
for _, row in df.head(5000).iterrows():
    edges_data.append((str(row['student_id']), str(row['course_id']), row['score']))

pr_calculator = PageRank()
ranks = pr_calculator.calculate(edges_data)
course_ranks = {k: v for k, v in ranks.items() if k.startswith('COURSE_')}
top_courses = sorted(course_ranks.items(), key=lambda x: x[1], reverse=True)[:10]

# Нормализация рангов для CSS-визуализации (ширина полоски в %)
max_rank = top_courses[0][1] if top_courses else 1

# 3. РАСЧЕТ BOOTSTRAP (Сравнение топ-курса и среднего курса)

boot_result = None
course_a_name = None
course_b_name = None

if len(top_courses) > 1:
    course_b_name = top_courses[0][0]  # Топ-курс (Группа B)
    course_a_name = top_courses[len(top_courses) // 2][0]  # Средний курс (Группа A)

    scores_top = pair_stats[pair_stats['course_id'] == course_b_name]['score'].to_numpy(dtype=float)
    scores_mid = pair_stats[pair_stats['course_id'] == course_a_name]['score'].to_numpy(dtype=float)

    # Очищаем от NaN/Inf и проверяем размер выборки
    scores_top = scores_top[np.isfinite(scores_top)]
    scores_mid = scores_mid[np.isfinite(scores_mid)]

    if len(scores_top) >= 2 and len(scores_mid) >= 2:
        boot_diffs = bootstrap_diff(scores_mid, scores_top, repeats=1000)
        low, high = np.percentile(boot_diffs, [2.5, 97.5])

        boot_result = {
            'lower': round(float(low), 2),
            'upper': round(float(high), 2),
            'is_significant': not (low <= 0 <= high),
            'observed_diff': round(float(np.mean(scores_top) - np.mean(scores_mid)), 2)
        }

# 4. ИНИЦИАЛИЗАЦИЯ MINHASH / LSH

# num_hashes=128, lsh_width=4 (32 полосы), sample_size=500 студентов
signatures, lsh_index, students_sample, lsh_width = prepare_data_and_build_index(df)

# 5. МАРШРУТЫ

@app.route('/')
def home():
    top_score = score_heap.peek()
    return render_template(
        'index.html',
        top_courses=top_courses,
        max_rank=max_rank,
        top_score=top_score,
        total_records=len(df),
        boot_result=boot_result,
        course_a_name=course_a_name,
        course_b_name=course_b_name
    )


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    target_id = int(data.get('id'))
    row_id = hash_index.get(target_id)

    if row_id is not None:
        record = df_sorted.iloc[row_id].to_dict()
        record['timestamp'] = str(record['timestamp'])
        return jsonify({'found': True, 'data': record})
    else:
        return jsonify({'found': False})


@app.route('/analytics', methods=['POST'])
def analytics():
    data = request.json
    l = int(data.get('l'))
    r = int(data.get('r'))
    max_score = seg_tree.query(l, r)
    return jsonify({'max_score': max_score})


@app.route('/update', methods=['POST'])
def update_score():
    data = request.json
    idx = int(data.get('idx'))
    new_val = int(data.get('value'))

    # Обновляем дерево отрезков
    seg_tree.update(idx, new_val)
    # Добавляем новое значение в кучу (для простоты без удаления старого)
    score_heap.push(new_val)

    return jsonify({'status': 'ok'})


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    student_id = str(data.get('student_id'))

    similar = find_similar_students(student_id, signatures, lsh_index, students_sample, lsh_width)

    # Форматируем результат для фронтенда
    results = []
    for sid, jac in similar:
        results.append({'student_id': sid, 'jaccard': jac})

    return jsonify({'similar_students': results})


if __name__ == '__main__':
    app.run(debug=True)
