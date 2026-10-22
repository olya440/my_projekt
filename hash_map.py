class MyHashMap:
    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _index(self, key):
        return hash(key) % self.capacity

    def load_factor(self):
        if self.capacity == 0:
            return 0
        return self.size / self.capacity

    def _resize(self):
        old_buckets = self.buckets
        self.capacity = self.capacity * 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
          for key, value in bucket:
            idx = self._index(key)
            self.buckets[idx].append((key, value))
            self.size += 1


    def put(self, key, value):
        if not self.contains(key):
            if (self.size + 1) / self.capacity > self.MAX_LOAD_FACTOR:
                self._resize()
            self.size += 1

        idx = self._index(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
          if k == key:
            bucket[i] = (key, value)
            return

        bucket.append((key, value))


    def get(self, key):
        idx = self._index(key)
        for k, v in self.buckets[idx]:
          if k == key:
            return v
        return None

    def contains(self, key):
        idx = self._index(key)
        for k, v in self.buckets[idx]:
          if k == key:
            return True
        return False


    def remove(self, key):
        idx = self._index(key)
        bucket = self.buckets[idx]

        for i, (k,v) in enumerate(bucket):
          if k == key:
            del bucket[i]
            self.size -= 1
            return True

        return False

    def __len__(self):
        return self.size