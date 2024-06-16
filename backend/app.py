# app.py

from maki import MAKI, Agent
from blockchain import MiniBlockchain, AlgorandNode
import random

# Initialize nodes for Algorand consensus
nodes = [AlgorandNode(f"Account_{i}", random.randint(1, 10)) for i in range(10)]
blockchain = MiniBlockchain(nodes, pruning_interval=3)
maki = MAKI()

# Initialize agents
agent_a = Agent("Agent_A", blockchain, maki)
agent_b = Agent("Agent_B", blockchain, maki)

# Agent A sends an encrypted message to Agent B
encrypted_message = agent_a.send_message("Agent_B", "Hello Agent B")
print(f"Agent A to Agent B: {encrypted_message}")

# Agent B receives and decrypts the message
decrypted_message = agent_b.receive_message("Agent_A", encrypted_message)
print(f"Agent B received: {decrypted_message}")

# Agents start transactions and add blocks
agent_a.start_transaction("Agent_B", 50)
agent_b.start_transaction("Agent_A", 30)
agent_a.add_block()
agent_b.add_block()

# Broadcast a message from Agent A
agent_a.broadcast_message("This is a broadcast message from Agent A")

# Broadcast a message from Agent B
agent_b.broadcast_message("This is a broadcast message from Agent B")

# Get current balances
print("Current Balances:")
print("Agent_A:", blockchain.get_balance("Agent_A"))
print("Agent_B:", blockchain.get_balance("Agent_B"))
