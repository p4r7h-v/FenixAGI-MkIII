import hashlib
import math

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        for index in self.get_hash_indices(item):
            self.bit_array[index] = 1

    def check(self, item):
        return all(self.bit_array[index] for index in self.get_hash_indices(item))

    def get_hash_indices(self, item):
        hash_one = int(hashlib.sha1(item.encode('utf-8')).hexdigest(), 16) % self.size
        hash_two = int(hashlib.sha256(item.encode('utf-8')).hexdigest(), 16) % self.size

        return [(hash_one + i * hash_two) % self.size for i in range(self.num_hashes)]

def optimal_filter_params(n, p):
    # Calculate optimal size and number of hashes for a bloom filter
    # n: expected number of elements to be stored
    # p: desired false positive probability

    size = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2))
    num_hashes = math.ceil((size / n) * math.log(2))

    return size, num_hashes