import hashlib
import random
import time
from collections import defaultdict

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

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "tx_id": self.tx_id
        }

class Block:
    def __init__(self, previous_hash, transactions):
        self.timestamp = int(time.time())
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.block_hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.timestamp}{self.previous_hash}{[tx.tx_id for tx in self.transactions]}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "block_hash": self.block_hash
        }

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

class State:
    def __init__(self):
        self.balances = {
            "agent_a": 1000000,  # Initial balance for Agent A
            "agent_b": 1000000 
        }

    def apply_transaction(self, transaction):
        # Bypassing balance check for testing purposes
        if transaction.sender != "SYSTEM":
            if self.balances.get(transaction.sender, 0) < transaction.amount:
                print(f"Warning: {transaction.sender} has insufficient balance.")
                # Raise error or skip, depending on requirement
                return
            self.balances[transaction.sender] -= transaction.amount
        if transaction.recipient not in self.balances:
            self.balances[transaction.recipient] = 0
        self.balances[transaction.recipient] += transaction.amount

    def get_balance(self, account):
        return self.balances.get(account, 0)

class AlgorandNode:
    def __init__(self, account_id, stake):
        self.account_id = account_id
        self.stake = stake
        self.online = True
        self.participation_key = self.generate_participation_key()

    def generate_participation_key(self):
        return hashlib.sha256(f"{self.account_id}{random.random()}".encode()).hexdigest()

    def vrf(self, value):
        key = self.participation_key
        hash_value = hashlib.sha256(f"{key}{value}".encode()).hexdigest()
        proof = hashlib.sha256(f"{hash_value}{key}".encode()).hexdigest()
        return hash_value, proof

# class MiniBlockchain:
#     def __init__(self, nodes, pruning_interval=10):
#         self.chain = []
#         self.current_transactions = []
#         self.state = State()
#         self.trie = BinaryRadixTrie()
#         self.nodes = nodes
#         self.round = 0
#         self.recovery_mode = False
#         self.pruning_interval = pruning_interval
#         self.deprecated_blocks = []
#         self.create_genesis_block()

#     def create_genesis_block(self):
#         genesis_block = Block("0", [])
#         self.chain.append(genesis_block)

#     def add_transaction(self, sender, recipient, amount):
#         transaction = Transaction(sender, recipient, amount)
#         self.current_transactions.append(transaction)
#         self.trie.insert(transaction)
#         self.state.apply_transaction(transaction)

#     def mine_block(self):
#         last_block_hash = self.chain[-1].block_hash if self.chain else "0"
#         new_block = Block(last_block_hash, self.current_transactions)
#         self.chain.append(new_block)
#         self.current_transactions = []
#         self.prune_old_blocks()

#     def prune_old_blocks(self):
#         if len(self.chain) > self.pruning_interval:
#             deprecated_block = self.chain.pop(0)
#             self.deprecated_blocks.append(deprecated_block)
#             if len(self.deprecated_blocks) > 10:
#                 self.deprecated_blocks.pop(0)

#     def remove_transaction_from_trie(self, tx_id):
#         node = self.trie.root
#         tx_id_bin = bin(int(tx_id, 16))[2:].zfill(256)
#         nodes_stack = [node]
#         for bit in tx_id_bin:
#             if bit in node.children:
#                 node = node.children[bit]
#                 nodes_stack.append(node)
#             else:
#                 return
#         if nodes_stack[-1].transactions:
#             nodes_stack[-1].transactions = [tx for tx in nodes_stack[-1].transactions if tx.tx_id != tx_id]
#         while nodes_stack and not nodes_stack[-1].children and not nodes_stack[-1].transactions:
#             nodes_stack.pop()
#             if nodes_stack:
#                 del nodes_stack[-1].children[tx_id_bin[len(nodes_stack)]]

#     def select_proposer(self):
#         proposer = None
#         lowest_vrf = None
#         for node in self.nodes:
#             if node.online:
#                 vrf_value, _ = node.vrf(self.round)
#                 if lowest_vrf is None or vrf_value < lowest_vrf:
#                     lowest_vrf = vrf_value
#                     proposer = node
#         return proposer

#     def soft_vote(self, proposals):
#         soft_vote_results = defaultdict(int)
#         for node in self.nodes:
#             if node.online:
#                 vrf_value, _ = node.vrf(self.round)
#                 soft_vote_results[proposals[0]] += node.stake
#         return max(soft_vote_results, key=soft_vote_results.get)

#     def certify_vote(self, proposal):
#         certify_vote_results = defaultdict(int)
#         for node in self.nodes:
#             if node.online:
#                 vrf_value, _ = node.vrf(self.round)
#                 certify_vote_results[proposal] += node.stake
#         if certify_vote_results[proposal] > sum(node.stake for node in self.nodes) // 2:
#             self.chain.append(proposal)
#             return True
#         return False

#     def propose_block(self):
#         proposer = self.select_proposer()
#         if proposer:
#             return f"Block proposed by {proposer.account_id} in round {self.round}"
#         return None

#     def run_round(self):
#         if self.recovery_mode:
#             self.recovery()
#         else:
#             self.round += 1
#             proposal = self.propose_block()
#             if proposal:
#                 proposals = [proposal]
#                 soft_vote_winner = self.soft_vote(proposals)
#                 if self.certify_vote(soft_vote_winner):
#                     print(f"Round {self.round}: Block certified and added to the blockchain")
#                     self.recovery_mode = False
#                 else:
#                     print(f"Round {self.round}: Failed to certify the block")
#                     self.recovery_mode = True
#             else:
#                 print(f"Round {self.round}: No block proposal")
#                 self.recovery_mode = True

#     def recovery(self):
#         print(f"Round {self.round}: Entering recovery mode")
#         self.recovery_mode = False
#         self.run_round()

#     def derive_state(self, target_block_index):
#         derived_state = State()
#         for block in self.chain[:target_block_index+1]:
#             for tx in block.transactions:
#                 derived_state.apply_transaction(tx)
#         return derived_state

#     def get_balance(self, account):
#         return self.state.get_balance(account)

#     def get_historical_balance(self, account, block_index):
#         derived_state = self.derive_state(block_index)
#         return derived_state.get_balance(account)

#     def get_transaction(self, tx_id):
#         return self.trie.search(tx_id)

#     def remove_deprecated_blocks(self):
#         while len(self.deprecated_blocks) > 10:
#             self.deprecated_blocks.pop(0)
#         return self.deprecated_blocks

class MiniBlockchain:
    def __init__(self, nodes, pruning_interval=10):
        self.chain = []
        self.current_transactions = []
        self.state = State()
        self.trie = BinaryRadixTrie()
        self.nodes = nodes
        self.round = 0
        self.recovery_mode = False
        self.pruning_interval = pruning_interval
        self.deprecated_blocks = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("0", [])
        self.chain.append(genesis_block)

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)
        self.trie.insert(transaction)
        self.state.apply_transaction(transaction)

    def mine_block(self):
        last_block_hash = self.chain[-1].block_hash if self.chain else "0"
        new_block = Block(last_block_hash, self.current_transactions)
        self.chain.append(new_block)
        self.current_transactions = []

    def prune_old_blocks(self):
        if self.deprecated_blocks:
            deprecated_block = self.deprecated_blocks.pop(0)
            return deprecated_block
        return None

    def remove_deprecated_blocks(self):
        removed_blocks = []
        while self.deprecated_blocks:
            removed_blocks.append(self.prune_old_blocks())
        return removed_blocks

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

    def select_proposer(self):
        proposer = None
        lowest_vrf = None
        for node in self.nodes:
            if node.online:
                vrf_value, _ = node.vrf(self.round)
                if lowest_vrf is None or vrf_value < lowest_vrf:
                    lowest_vrf = vrf_value
                    proposer = node
        return proposer

    def soft_vote(self, proposals):
        soft_vote_results = defaultdict(int)
        for node in self.nodes:
            if node.online:
                vrf_value, _ = node.vrf(self.round)
                soft_vote_results[proposals[0]] += node.stake
        return max(soft_vote_results, key=soft_vote_results.get)

    def certify_vote(self, proposal):
        certify_vote_results = defaultdict(int)
        for node in self.nodes:
            if node.online:
                vrf_value, _ = node.vrf(self.round)
                certify_vote_results[proposal] += node.stake
        if certify_vote_results[proposal] > sum(node.stake for node in self.nodes) // 2:
            self.chain.append(proposal)
            return True
        return False

    def propose_block(self):
        proposer = self.select_proposer()
        if proposer:
            return f"Block proposed by {proposer.account_id} in round {self.round}"
        return None

    def run_round(self):
        if self.recovery_mode:
            self.recovery()
        else:
            self.round += 1
            proposal = self.propose_block()
            if proposal:
                proposals = [proposal]
                soft_vote_winner = self.soft_vote(proposals)
                if self.certify_vote(soft_vote_winner):
                    print(f"Round {self.round}: Block certified and added to the blockchain")
                    self.recovery_mode = False
                else:
                    print(f"Round {self.round}: Failed to certify the block")
                    self.recovery_mode = True
            else:
                print(f"Round {self.round}: No block proposal")
                self.recovery_mode = True

    def recovery(self):
        print(f"Round {self.round}: Entering recovery mode")
        self.recovery_mode = False
        self.run_round()

    def derive_state(self, target_block_index):
        derived_state = State()
        for block in self.chain[:target_block_index+1]:
            for tx in block.transactions:
                derived_state.apply_transaction(tx)
        return derived_state

    def get_balance(self, account):
        return self.state.get_balance(account)

    def get_historical_balance(self, account, block_index):
        derived_state = self.derive_state(block_index)
        return derived_state.get_balance(account)

    def get_transaction(self, tx_id):
        return self.trie.search(tx_id)
