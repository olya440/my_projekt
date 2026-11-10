class BinaryHeap:
    def __init__(self):
        self.heap = [None]

    def push(self, value):
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, index):
        parent = index // 2
        while index > 1 and self.heap[index] > self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = index // 2

    def pop_max(self):
        if len(self.heap) <= 1:
            return None
        max_val = self.heap[1]
        last_val = self.heap.pop()
        if len(self.heap) > 1:
            self.heap[1] = last_val
            self._sift_down(1)
        return max_val

    def _sift_down(self, index):
        size = len(self.heap)
        while True:
            left = 2 * index
            right = 2 * index + 1
            largest = index
            if left < size and self.heap[left] > self.heap[largest]:
                largest = left
            if right < size and self.heap[right] > self.heap[largest]:
                largest = right
            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break

    def peak(self):
        if len(self.heap) <= 1:
            return None
        return self.heap[1]

    def __len__(self):
        return len(self.heap) - 1