import hashlib
import random
import time

class Transaction:
    def __init__(self, sender, recipient, amount, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp if timestamp else int(time.time())
        self.tx_id = self.compute_tx_id()

    def compute_tx_id(self):
        tx_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}".encode()
        return hashlib.sha256(tx_string).hexdigest()

class Block:
    def __init__(self, previous_hash, transactions):
        self.timestamp = int(time.time())
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.block_hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.timestamp}{self.previous_hash}{[tx.tx_id for tx in self.transactions]}".encode()
        return hashlib.sha256(block_string).hexdigest()

class BinaryRadixTrieNode:
    def __init__(self):
        self.children = {}
        self.transactions = []

class BinaryRadixTrie:
    def __init__(self):
        self.root = BinaryRadixTrieNode()

    def insert(self, transaction):
        node = self.root
        tx_id_bin = bin(int(transaction.tx_id, 16))[2:].zfill(256)  # Binary representation of tx_id
        for bit in tx_id_bin:
            if bit not in node.children:
                node.children[bit] = BinaryRadixTrieNode()
            node = node.children[bit]
        node.transactions.append(transaction)

    def search(self, tx_id):
        node = self.root
        tx_id_bin = bin(int(tx_id, 16))[2:].zfill(256)  # Binary representation of tx_id
        for bit in tx_id_bin:
            if bit in node.children:
                node = node.children[bit]
            else:
                return None
        for transaction in node.transactions:
            if transaction.tx_id == tx_id:
                return transaction
        return None

class MiniBlockchain:
    def __init__(self, pruning_interval=10):
        self.chain = []
        self.current_transactions = []
        self.pruning_interval = pruning_interval
        self.trie = BinaryRadixTrie()
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("0", [])
        self.chain.append(genesis_block)

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)
        self.trie.insert(transaction)

    def mine_block(self):
        last_block_hash = self.chain[-1].block_hash if self.chain else "0"
        new_block = Block(last_block_hash, self.current_transactions)
        self.chain.append(new_block)
        self.current_transactions = []
        self.prune_old_transactions()

    def prune_old_transactions(self):
        if len(self.chain) > self.pruning_interval:
            blocks_to_prune = self.chain[:-self.pruning_interval]
            self.chain = self.chain[-self.pruning_interval:]
            for block in blocks_to_prune:
                for tx in block.transactions:
                    self.remove_transaction_from_trie(tx.tx_id)

    def remove_transaction_from_trie(self, tx_id):
        node = self.trie.root
        tx_id_bin = bin(int(tx_id, 16))[2:].zfill(256)
        nodes_stack = [node]
        for bit in tx_id_bin:
            if bit in node.children:
                node = node.children[bit]
                nodes_stack.append(node)
            else:
                return
        if nodes_stack[-1].transactions:
            nodes_stack[-1].transactions = [tx for tx in nodes_stack[-1].transactions if tx.tx_id != tx_id]
        while nodes_stack and not nodes_stack[-1].children and not nodes_stack[-1].transactions:
            nodes_stack.pop()
            if nodes_stack:
                del nodes_stack[-1].children[tx_id_bin[len(nodes_stack)]]

    def get_transaction(self, tx_id):
        return self.trie.search(tx_id)

# Example usage
blockchain = MiniBlockchain(pruning_interval=3)

# Adding some transactions
blockchain.add_transaction("Alice", "Bob", 50)
blockchain.add_transaction("Bob", "Charlie", 20)
blockchain.mine_block()

# Adding more transactions
blockchain.add_transaction("Alice", "Charlie", 15)
blockchain.add_transaction("Charlie", "Alice", 10)
blockchain.mine_block()

# Add more blocks to trigger pruning
blockchain.add_transaction("Alice", "Bob", 5)
blockchain.mine_block()
blockchain.add_transaction("Bob", "Charlie", 25)
blockchain.mine_block()
blockchain.add_transaction("Charlie", "Alice", 35)
blockchain.mine_block()

# Search for a transaction
tx_id_to_search = blockchain.chain[1].transactions[0].tx_id
found_tx = blockchain.get_transaction(tx_id_to_search)
print(f"Found Transaction: {vars(found_tx) if found_tx else 'Transaction not found'}")

# Print current blockchain state
print("\nCurrent Blockchain State:")
for block in blockchain.chain:
    print(vars(block))
