from flask import Flask, render_template, request, jsonify
import pandas as pd
from hash_map import MyHashMap
from segment_tree import SegmentTreeIndex
from page_rank import PageRank
from binary_heap import BinaryHeap  # Импортируем нашу кучу

app = Flask(__name__)

# Загрузка данных
df = pd.read_csv('online_learning_dataset.csv')
df_sorted = df.sort_values(by='timestamp').reset_index(drop=True)
scores = df_sorted['score'].tolist()
keys = df_sorted['interaction_id'].tolist()

# --- Инициализация структур ---
hash_index = MyHashMap()
for row_id, key in enumerate(keys):
    hash_index.put(key, row_id)

seg_tree = SegmentTreeIndex(scores)

# PageRank
edges_data = []
for _, row in df.head(5000).iterrows():
    edges_data.append((str(row['student_id']), str(row['course_id']), row['score']))
pr_calculator = PageRank()
ranks = pr_calculator.calculate(edges_data)
course_ranks = {k: v for k, v in ranks.items() if k.startswith('COURSE_')}
top_courses = sorted(course_ranks.items(), key=lambda x: x[1], reverse=True)[:10]

# Binary Heap: Заполняем кучу оценками для быстрого доступа к топу
score_heap = BinaryHeap()
for s in scores:
    score_heap.push(s)


@app.route('/')
def home():
    # Берем топ-5 оценок из кучи (не удаляя их, просто смотрим)
    # Для демонстрации мы можем просто показать вершину
    top_score = score_heap.peak()
    return render_template('index.html', top_courses=top_courses, top_score=top_score)


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

    seg_tree.update(idx, new_val)
    score_heap.push(new_val)

    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
