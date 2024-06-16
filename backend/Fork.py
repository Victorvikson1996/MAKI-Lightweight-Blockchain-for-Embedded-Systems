import hashlib
import random
from collections import defaultdict

class AlgorandNode:
    def __init__(self, account_id, stake):
        self.account_id = account_id
        self.stake = stake
        self.online = True
        self.participation_key = self.generate_participation_key()
    
    def generate_participation_key(self):
        # Simulate generation of a participation key
        return hashlib.sha256(f"{self.account_id}{random.random()}".encode()).hexdigest()

    def vrf(self, value):
        # Simulate the VRF process
        key = self.participation_key
        hash_value = hashlib.sha256(f"{key}{value}".encode()).hexdigest()
        proof = hashlib.sha256(f"{hash_value}{key}".encode()).hexdigest()
        return hash_value, proof

class AlgorandBlockchain:
    def __init__(self, nodes):
        self.nodes = nodes
        self.blockchain = []
        self.round = 0
        self.recovery_mode = False
    
    def select_proposer(self):
        # Select a block proposer using VRF
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
        # Soft vote to filter down to one proposal
        soft_vote_results = defaultdict(int)
        for node in self.nodes:
            if node.online:
                vrf_value, _ = node.vrf(self.round)
                soft_vote_results[proposals[0]] += node.stake  # Simplified soft vote
        return max(soft_vote_results, key=soft_vote_results.get)
    
    def certify_vote(self, proposal):
        # Certify vote to finalize the block
        certify_vote_results = defaultdict(int)
        for node in self.nodes:
            if node.online:
                vrf_value, _ = node.vrf(self.round)
                certify_vote_results[proposal] += node.stake  # Simplified certify vote
        if certify_vote_results[proposal] > sum(node.stake for node in self.nodes) // 2:
            self.blockchain.append(proposal)
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
                proposals = [proposal]  # In a real scenario, there would be multiple proposals
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
        # Simplified recovery process
        self.recovery_mode = False
        self.run_round()

# Example usage
nodes = [AlgorandNode(f"Account_{i}", random.randint(1, 10)) for i in range(10)]
blockchain = AlgorandBlockchain(nodes)

for _ in range(5):
    blockchain.run_round()
