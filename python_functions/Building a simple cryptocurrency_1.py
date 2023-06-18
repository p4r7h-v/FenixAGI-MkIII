import hashlib
import time

class SimpleBlock:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def create_genesis_block():
    return SimpleBlock(0, '0', time.time(), 'Genesis Block', calculate_hash(0, '0', time.time(), 'Genesis Block'))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_hash = previous_block.hash
    hash = calculate_hash(index, previous_hash, timestamp, data)
    return SimpleBlock(index, previous_hash, timestamp, data, hash)

def calculate_hash(index, previous_hash, timestamp, data):
    return hashlib.sha256(f'{index}{previous_hash}{timestamp}{data}'.encode('utf-8')).hexdigest()

blockchain = [create_genesis_block()]

def add_block(data):
    global blockchain
    new_block = create_new_block(blockchain[-1], data)
    blockchain.append(new_block)
    return new_block

def print_blockchain():
    for block in blockchain:
        print(f"Index: {block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}\n")

if __name__ == "__main__":
    add_block("Block 1")
    add_block("Block 2")
    add_block("Block 3")
    
    print_blockchain()