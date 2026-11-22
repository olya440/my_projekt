import numpy as np

def bootstrap_diff(data_a, data_b, repeats=2000, statistic=np.mean, seed=42):
    """Bootstrap для оценки неопределенности разницы между двумя группами"""

    rng = np.random.default_rng(seed)
    results = []
    n_a, n_b = len(data_a), len(data_b)

    # Проверка на пустые массивы
    if n_a == 0 or n_b == 0:
        raise ValueError("Обе группы должны содержать хотя бы одно наблюдение")

    for _ in range(repeats):
        # ШАГ 1: Перевыборка КАЖДОЙ группы отдельно С ВОЗВРАЩЕНИЕМ
        sample_a = data_a[rng.integers(0, n_a, size=n_a)]
        sample_b = data_b[rng.integers(0, n_b, size=n_b)]

        # ШАГ 2: Вычисляем разницу статистик (B - A)
        diff = statistic(sample_b) - statistic(sample_a)
        results.append(diff)

    return np.array(results)