import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def create_genesis_block():
    return Block(0, '0', time.time(), 'Genesis Block', calculate_hash(0, '0', time.time(), 'Genesis Block'))

def create_new_block(prev_block, data):
    index = prev_block.index + 1
    timestamp = time.time()
    block_hash = calculate_hash(index, prev_block.hash, timestamp, data)
    return Block(index, prev_block.hash, timestamp, data, block_hash)

def calculate_hash(index, previous_hash, timestamp, data):
    block_info = f'{index}{previous_hash}{timestamp}{data}'.encode('utf-8')
    return hashlib.sha256(block_info).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]

    def add_block(self, data):
        self.chain.append(create_new_block(self.chain[-1], data))

# Test the blockchain
def test_blockchain():
    blockchain = Blockchain()

    for i in range(1, 11):
        blockchain.add_block(f'Block {i}')
        print(f'Block {i} has been added')
        print(f'Hash: {blockchain.chain[i].hash}\n')

if __name__ == '__main__':
    test_blockchain()