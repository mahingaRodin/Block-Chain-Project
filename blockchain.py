import hashlib
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()


def create_genesis_block():
    """Creates the first block in the blockchain."""
    return Block(0, time.time(), "Genesis Block", "0")


class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]
        self.difficulty = 4

    def get_latest_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]

    def add_block(self, new_block):
        """Adds a new block to the chain after mining."""
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Checks the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the blocks are properly linked
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def proof_of_work(self, block):
        """Implements Proof of Work by finding a valid hash."""
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.hash


if __name__ == "__main__":
    # Initialize blockchain
    blockchain = Blockchain()

    # Mining block 1
    print("Mining block 1...")
    block1 = Block(1, time.time(), {"amount": 4}, blockchain.get_latest_block().hash)
    blockchain.add_block(block1)

    # Mining block 2
    print("Mining block 2...")
    block2 = Block(2, time.time(), {"amount": 8}, blockchain.get_latest_block().hash)
    blockchain.add_block(block2)

    # Display the blockchain
    for block in blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("-" * 30)
