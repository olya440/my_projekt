class SegmentTreeIndex:
    def __init__(self, data):
        """
        1. ИСХОДНЫЕ ДАННЫЕ: Принимаем список оценок (score),
        уже отсортированный по времени (timestamp).
        """
        self.n = len(data)
        if self.n == 0:
            self.tree = []
            return

        self.tree = [float('-inf')] * (4*self.n)
        self.data = data[:]
        # 2. ПОСТРОЕНИЕ: Строим дерево из исходных данных
        self._build(0, 0, self.n - 1)

    def _build(self, v, tl, tr):
        """
        Рекурсивное построение дерева
        """
        if tl == tr:
            self.tree[v] = self.data[tl]
        else:
            tm = (tl + tr) // 2
            self._build(2 * v + 1, tl, tm)
            self._build(2 * v + 2, tm + 1, tr)
            self.tree[v] = max(self.tree[2 * v + 1], self.tree[2 * v + 2])

    def update(self, pos, value):
        """
        3. UPDATE: Изменяем значение по индексу pos на value
        Проверяем индекс
        """
        if pos < 0 or pos >= self.n:
          raise ValueError('Некорректная позиция для обнавления')
        self.data[pos] = value
        self._update(pos, value,0, 0, self.n - 1)

    def _update(self, pos, value, v=0, tl=0, tr=None):
        if tl == tr:
            self.tree[v] = value
            self.data[pos] = value
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self._update(pos, value, v * 2 + 1, tl, tm)
            else:
                self._update(pos, value, v * 2 + 2, tm + 1, tr)
            self.tree[v] = max(self.tree[v * 2 + 1], self.tree[v * 2 + 2])

    def query(self, l, r):
        """
        4. RANGE QUERY: Получаем максимум на отрезке [l, r]
        Проверяем корректность границ
        """
        if (l < 0) or (r > self.n) or (l > r):
            raise ValueError('Некорректные границы запроса')
        return self._query(l, r, 0, 0, self.n - 1)

    def _query(self, l, r, v=0, tl=0, tr=None):
        if r < tl or l > tr:
            return float('-inf')
        if l <= tl and r >= tr:
            return self.tree[v]
        tm = (tr + tl) // 2
        left_max = self._query(l, r, v * 2 + 1, tl, tm)
        right_max = self._query(l, r, v * 2 + 2, tm + 1, tr)
        return max(left_max, right_max)

