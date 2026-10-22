import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Настройки
NUM_RECORDS = 100_000
np.random.seed(42)

# Генерируем данные
data = {
    # Уникальный идентификатор записи
    'interaction_id': range(1, NUM_RECORDS + 1),

    # Связь между объектами: студент → курс
    'student_id': np.random.randint(1000, 9999, NUM_RECORDS),
    'course_id': np.random.choice([f'COURSE_{i}' for i in range(1, 51)], NUM_RECORDS),

    # Числовая характеристика связи
    'watch_time_minutes': np.random.exponential(30, NUM_RECORDS).astype(int),
    'score': np.random.randint(0, 101, NUM_RECORDS),

    # Категориальное поле
    'category': np.random.choice(['Programming', 'Data Science', 'Design', 'Business', 'Languages'], NUM_RECORDS),

    # Поле для упорядочивания (дата/время)
    'timestamp': [datetime(2024, 1, 1) + timedelta(minutes=int(x))
                  for x in np.random.randint(0, 525600, NUM_RECORDS)]  # год в минутах
}

df = pd.DataFrame(data)

# Сохраняем
df.to_csv('online_learning_dataset.csv', index=False)

print(f"Размер датасета: {df.shape}")
print(f"\nПервые 5 строк:")
print(df.head())
print(f"\nТипы данных:")
print(df.dtypes)
print(f"\nПроверка уникальности interaction_id: {df['interaction_id'].is_unique}")
print(f"Пропусков в interaction_id: {df['interaction_id'].isna().sum()}")