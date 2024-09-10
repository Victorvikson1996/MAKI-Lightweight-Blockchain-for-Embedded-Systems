# # agent_b.py

# import time
# import random
# import json
# import psutil
# import paho.mqtt.client as mqtt
# from prometheus_client import start_http_server, Summary, Gauge
# from maki import MAKI, Agent
# from blockchain import MiniBlockchain, AlgorandNode
# from cryptography.hazmat.primitives import serialization

# # Initialize Prometheus metrics
# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
# CPU_USAGE = Gauge('agent_cpu_usage', 'CPU usage of the agent')
# MEMORY_USAGE = Gauge('agent_memory_usage', 'Memory usage of the agent')
# BLOCKCHAIN_SIZE = Gauge('blockchain_size', 'Size of the blockchain')
# NUM_TRANSACTIONS = Gauge('num_transactions', 'Number of transactions in the blockchain')

# # Initialize nodes for Algorand consensus
# nodes = [AlgorandNode(f"Account_{i}", random.randint(1, 10)) for i in range(10)]
# blockchain = MiniBlockchain(nodes, pruning_interval=3)
# maki = MAKI()

# # Initialize Agent B
# agent_b = Agent("Agent_B", blockchain, maki)

# # MQTT setup
# broker = 'localhost'
# port = 1883
# topic = "agent/communication"
# agent_a_key_received = False

# metrics = []

# def track_metrics(operation, details=""):
#     process = psutil.Process()
#     cpu_usage = process.cpu_percent(interval=1)
#     memory_info = process.memory_info()
#     memory_used = memory_info.rss
#     memory_total = psutil.virtual_memory().total
#     memory_percent = psutil.virtual_memory().percent
#     data_size = len(blockchain.chain)
#     num_transactions = sum(len(block.transactions) for block in blockchain.chain)
#     timestamp = time.time()
#     pid = process.pid
    
#     # Update Prometheus metrics
#     CPU_USAGE.set(cpu_usage)
#     MEMORY_USAGE.set(memory_used)
#     BLOCKCHAIN_SIZE.set(data_size)
#     NUM_TRANSACTIONS.set(num_transactions)

#     metric = {
#         "operation": operation,
#         "details": details,
#         "cpu_usage": cpu_usage,
#         "memory_used": memory_used,
#         "memory_total": memory_total,
#         "memory_percent": memory_percent,
#         "data_size": data_size,
#         "num_transactions": num_transactions,
#         "timestamp": timestamp,
#         "pid": pid
#     }
    
#     metrics.append(metric)

# def save_metrics():
#     with open('metrics_agent_b.json', 'w') as json_file:
#         json.dump(metrics, json_file, indent=4)

# def on_connect(client, userdata, flags, rc):
#     print("Connected to MQTT Broker!")
#     client.subscribe(topic)
#     print("Agent B: Requesting keys...")
#     client.publish(topic, "Request Key")

# def on_message(client, userdata, msg):
#     global agent_a_key_received
#     message = msg.payload.decode()
#     print(f"Agent B received message: {message}")
#     if message.startswith("Agent_A to Agent_B: "):
#         encrypted_message = message.split(": ")[1]
#         decrypted_message = agent_b.receive_message("Agent_A", encrypted_message)
#         print(f"Agent B decrypted message: {decrypted_message}")
#         if decrypted_message == "Hello Agent B":
#             client.publish(topic, f"Agent_B to Agent_A: {agent_b.send_message('Agent_A', 'Request Transaction')}")
#             track_metrics("Message Sending", "Agent_B sent 'Request Transaction' to Agent_A")
#             save_metrics()
#         elif decrypted_message == "Request Transaction":
#             agent_b.blockchain.add_transaction("Agent_B", "Agent_A", 50)
#             track_metrics("Transaction", "Transaction from Agent_B to Agent_A")
#             client.publish(topic, f"Agent_B to Agent_A: {agent_b.send_message('Agent_A', 'Transaction Completed')}")
#         elif decrypted_message == "Transaction Completed":
#             agent_b.blockchain.mine_block()
#             track_metrics("Block Addition", "Block added by Agent_B after transaction with Agent_A")
#             save_metrics()
#     elif message.startswith("Agent_A Key: "):
#         agent_a_public_key = message.split(": ")[1]
#         agent_b.maki.keys['Agent_A'] = {
#             'private_key': None,
#             'public_key': serialization.load_pem_public_key(agent_a_public_key.encode())
#         }
#         agent_a_key_received = True
#         print("Agent B: Received Agent A's key")
#     elif message == "Request Key":
#         client.publish(topic, f"Agent_B Key: {agent_b.maki.get_public_key('Agent_B')}")
#         print("Agent B: Sent my key to Agent A")
#         track_metrics("Key Exchange", "Agent_B sent its key to Agent_A")
#         save_metrics()

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(broker, port, 60)
# client.loop_start()

# # Start Prometheus server
# start_http_server(8001)

# # Wait until Agent A's key is received
# while not agent_a_key_received:
#     time.sleep(1)

# # Perform random transactions and block additions
# while True:
#     if random.random() < 0.5:
#         client.publish(topic, f"Agent_B to Agent_A: {agent_b.send_message('Agent_A', 'Request Transaction')}")
#         track_metrics("Request Transaction", "Agent_B requested a transaction from Agent_A")
#         save_metrics()
#     time.sleep(random.randint(5, 10))


from agent import AgentClient, blockchain, maki

# Configuration for Agent B
agent_b = AgentClient(
    agent_name="Agent_B",
    other_agent_name="Agent_A",
    broker="localhost",  # Replace with the actual IP address of your MQTT broker
    port=1883,
    topic="agent/communication",
    blockchain=blockchain,
    maki=maki
)

# Start Agent B
agent_b.start(prometheus_port=8001)


