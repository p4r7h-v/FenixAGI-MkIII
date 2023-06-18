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

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

def calculate_hash(index, previous_hash, timestamp, data):
    block_string = f'{index}{previous_hash}{timestamp}{data}'.encode('utf-8')
    return hashlib.sha256(block_string).hexdigest()

# Initialize the blockchain with the genesis block
blockchain = [create_genesis_block()]

def add_transaction_data(data):
    previous_block = blockchain[-1]
    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)
    print(f'Block {new_block.index} has been added to the blockchain.')
    print(f'Hash: {new_block.hash}\n')

# Example usage: Adding transaction data to the blockchain
add_transaction_data('Alice sends 5 coins to Bob')
add_transaction_data('Bob sends 3 coins to Charlie')
add_transaction_data('Charlie sends 1 coin to Alice')