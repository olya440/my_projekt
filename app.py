from flask import Flask, render_template, request, jsonify
import pandas as pd
from hash_map import MyHashMap
from segment_tree import SegmentTreeIndex

app = Flask(__name__)

# Загружаем данные один раз при запуске сайта
df = pd.read_csv('online_learning_dataset.csv')
df_sorted = df.sort_values(by='timestamp').reset_index(drop=True)
scores = df_sorted['score'].tolist()
keys = df_sorted['interaction_id'].tolist()

# Строим индексы
hash_index = MyHashMap()
for row_id, key in enumerate(keys):
    hash_index.put(key, row_id)

seg_tree = SegmentTreeIndex(scores)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    target_id = int(data.get('id'))

    row_id = hash_index.get(target_id)

    if row_id is not None:
        record = df_sorted.iloc[row_id].to_dict()
        # Преобразуем timestamp в строку для удобства
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
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)