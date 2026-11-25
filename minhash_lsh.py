import numpy as np
import pandas as pd
from collections import defaultdict


def prepare_data_and_build_index(df, num_hashes=128, lsh_width=4, sample_size=500):
    """
    Подготавливает данные, строит MinHash-подписи и LSH-индекс.
    Возвращает словарь signatures, индекс index и маппинг student->courses для точного расчета.
    """
    # 1. Маппинг курсов в ID
    unique_courses = sorted(df['course_id'].unique())
    course_to_id = {c: i for i, c in enumerate(unique_courses)}

    # 2. Агрегация до уровня студента (список ID курсов)
    student_courses = df.groupby('student_id')['course_id'].apply(
        lambda x: [course_to_id[c] for c in x]
    ).to_dict()

    # Берем выборку для скорости
    students_sample = dict(list(student_courses.items())[:sample_size])

    # 3. Генерация хеш-функций
    max_id = len(unique_courses) - 1
    p = max_id + 100003
    rng = np.random.RandomState(42)
    hash_funcs = [(rng.randint(1, p), rng.randint(0, p)) for _ in range(num_hashes)]

    # 4. Вычисление подписей
    def compute_sig(ids):
        sig = []
        for a, b in hash_funcs:
            min_h = float('inf')
            for cid in ids:
                h = (a * cid + b) % p
                if h < min_h: min_h = h
            sig.append(min_h)
        return tuple(sig)

    signatures = {sid: compute_sig(courses) for sid, courses in students_sample.items()}

    # 5. Построение LSH индекса
    index = {}
    num_bands = num_hashes // lsh_width
    for sid, sig in signatures.items():
        for band_idx in range(num_bands):
            start = band_idx * lsh_width
            band_key = (band_idx, tuple(sig[start:start + lsh_width]))
            if band_key not in index:
                index[band_key] = set()
            index[band_key].add(sid)

    return signatures, index, students_sample, lsh_width


def find_similar_students(target_id, signatures, index, students_sample, width):
    """Находит топ-5 похожих студентов через LSH + точный Jaccard."""
    if target_id not in signatures:
        return []

    candidates = set()
    sig = signatures[target_id]
    num_bands = len(sig) // width

    # Сбор кандидатов из бакетов
    for band_idx in range(num_bands):
        start = band_idx * width
        band_key = (band_idx, tuple(sig[start:start + width]))
        if band_key in index:
            candidates.update(index[band_key])

    candidates.discard(target_id)

    # Точный расчет Jaccard
    target_set = set(students_sample[target_id])
    results = []
    for cand in candidates:
        cand_set = set(students_sample[cand])
        union = len(target_set | cand_set)
        if union == 0: continue
        jaccard = len(target_set & cand_set) / union
        results.append((cand, round(jaccard, 4)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]