import pandas as pd
from hash_map import MyHashMap


def main():
    df = pd.read_csv('online_learning_dataset.csv')

    UNIQUE_FIELD = 'interaction_id'
    keys = df[UNIQUE_FIELD].tolist()

    index = MyHashMap()
    for row_id, key in enumerate(keys):
        index.put(key, row_id)

    print(f"Индекс построен. Size: {len(index)}, Capacity: {index.capacity}")

    test_key = keys[0]
    found_row_id = index.get(test_key)

    print(f"\nПроверка поиска:")
    print(f"Ключ: {test_key}")
    print(f"Найденный Row ID: {found_row_id}")

    if found_row_id is not None:
        print("Данные строки:")
        print(df.iloc[found_row_id])
    else:
        print("Ключ не найден!")


if __name__ == "__main__":
    main()