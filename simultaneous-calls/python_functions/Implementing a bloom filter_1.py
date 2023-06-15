import hashlib
import math
import ctypes

class BloomFilter:
    def __init__(self, num_items, false_positive_rate):
        self.array_size = self._get_array_size(num_items, false_positive_rate)
        self.num_hashes = self._get_num_hashes(num_items, self.array_size)
        self.bit_array = (ctypes.c_bool * self.array_size)()

    def _get_array_size(self, num_items, false_positive_rate):
        m = -(num_items * math.log(false_positive_rate)) / (math.log(2) ** 2)
        return math.ceil(m)

    def _get_num_hashes(self, num_items, m):
        k = (m / num_items) * math.log(2)
        return math.ceil(k)

    def _hash_functions(self, item):
        h1 = int(hashlib.sha1(item.encode()).hexdigest(), 16)
        h2 = int(hashlib.sha256(item.encode()).hexdigest(), 16)
        return h1, h2

    def add_item(self, item):
        h1, h2 = self._hash_functions(item)
        for i in range(self.num_hashes):
            index = (h1 + i * h2) % self.array_size
            self.bit_array[index] = True

    def check_item(self, item):
        h1, h2 = self._hash_functions(item)
        for i in range(self.num_hashes):
            index = (h1 + i * h2) % self.array_size
            if not self.bit_array[index]:
                return False
        return True