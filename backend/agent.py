import time
import random
import json
import psutil
import paho.mqtt.client as mqtt
from prometheus_client import start_http_server, Summary, Gauge
from maki import MAKI, Agent
from blockchain import MiniBlockchain, AlgorandNode
from cryptography.hazmat.primitives import serialization

# Initialize Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
CPU_USAGE = Gauge('agent_cpu_usage', 'CPU usage of the agent')
MEMORY_USAGE = Gauge('agent_memory_usage', 'Memory usage of the agent')
BLOCKCHAIN_SIZE = Gauge('blockchain_size', 'Size of the blockchain')
NUM_TRANSACTIONS = Gauge('num_transactions', 'Number of transactions in the blockchain')

# Initialize nodes for Algorand consensus
nodes = [AlgorandNode(f"Account_{i}", random.randint(1, 10)) for i in range(10)]
blockchain = MiniBlockchain(nodes, pruning_interval=3)
maki = MAKI()

# Metrics storage
metrics = []

def track_metrics(agent, operation, details=""):
    process = psutil.Process()
    cpu_usage = process.cpu_percent(interval=1)
    memory_info = process.memory_info()
    memory_used = memory_info.rss
    memory_total = psutil.virtual_memory().total
    memory_percent = psutil.virtual_memory().percent
    data_size = len(blockchain.chain)
    num_transactions = sum(len(block.transactions) for block in blockchain.chain)
    timestamp = time.time()
    pid = process.pid
    
    # Update Prometheus metrics
    CPU_USAGE.set(cpu_usage)
    MEMORY_USAGE.set(memory_used)
    BLOCKCHAIN_SIZE.set(data_size)
    NUM_TRANSACTIONS.set(num_transactions)

    metric = {
        "agent": agent,
        "operation": operation,
        "details": details,
        "cpu_usage": cpu_usage,
        "memory_used": memory_used,
        "memory_total": memory_total,
        "memory_percent": memory_percent,
        "data_size": data_size,
        "num_transactions": num_transactions,
        "timestamp": timestamp,
        "pid": pid
    }
    
    metrics.append(metric)

def save_metrics(agent):
    with open(f'metrics_{agent}.json', 'w') as json_file:
        json.dump(metrics, json_file, indent=4)

class AgentClient:
    def __init__(self, agent_name, other_agent_name, broker, port, topic, blockchain, maki):
        self.agent_name = agent_name
        self.other_agent_name = other_agent_name
        self.agent = Agent(agent_name, blockchain, maki)
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.agent_key_received = False

    def start(self, prometheus_port):
        print(f"Connecting to MQTT broker at {self.broker}:{self.port}")
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        start_http_server(prometheus_port)

        while not self.agent_key_received:
            time.sleep(1)

        print(f"{self.agent_name}: Sending message to {self.other_agent_name}")
        self.client.publish(self.topic, f"{self.agent_name} to {self.other_agent_name}: {self.agent.send_message(self.other_agent_name, 'Hello ' + self.other_agent_name)}")
        track_metrics(self.agent_name, "Message Sending", f"{self.agent_name} sent 'Hello {self.other_agent_name}' to {self.other_agent_name}")
        save_metrics(self.agent_name)

        while True:
            if random.random() < 0.5:
                self.client.publish(self.topic, f"{self.agent_name} to {self.other_agent_name}: {self.agent.send_message(self.other_agent_name, 'Request Transaction')}")
                track_metrics(self.agent_name, "Request Transaction", f"{self.agent_name} requested a transaction from {self.other_agent_name}")
                save_metrics(self.agent_name)
            time.sleep(random.randint(5, 10))

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT Broker with result code {rc}")
        client.subscribe(self.topic)
        print(f"{self.agent_name}: Requesting keys...")
        client.publish(self.topic, "Request Key")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"{self.agent_name} received message: {message}")
        if message.startswith(f"{self.other_agent_name} to {self.agent_name}: "):
            encrypted_message = message.split(": ")[1]
            decrypted_message = self.agent.receive_message(self.other_agent_name, encrypted_message)
            print(f"{self.agent_name} decrypted message: {decrypted_message}")
            if decrypted_message == "Request Transaction":
                self.agent.blockchain.add_transaction(self.agent_name, self.other_agent_name, 50)
                track_metrics(self.agent_name, "Transaction", f"Transaction from {self.agent_name} to {self.other_agent_name}")
                client.publish(self.topic, f"{self.agent_name} to {self.other_agent_name}: {self.agent.send_message(self.other_agent_name, 'Transaction Completed')}")
            elif decrypted_message == "Transaction Completed":
                self.agent.blockchain.mine_block()
                track_metrics(self.agent_name, "Block Addition", f"Block added by {self.agent_name} after transaction with {self.other_agent_name}")
                save_metrics(self.agent_name)
        elif message.startswith(f"{self.other_agent_name} Key: "):
            other_agent_public_key = message.split(": ")[1]
            self.agent.maki.keys[self.other_agent_name] = {
                'private_key': None,
                'public_key': serialization.load_pem_public_key(other_agent_public_key.encode())
            }
            self.agent_key_received = True
            print(f"{self.agent_name}: Received {self.other_agent_name}'s key")
        elif message == "Request Key":
            client.publish(self.topic, f"{self.agent_name} Key: {self.agent.maki.get_public_key(self.agent_name)}")
            print(f"{self.agent_name}: Sent my key to {self.other_agent_name}")
            track_metrics(self.agent_name, "Key Exchange", f"{self.agent_name} sent its key to {self.other_agent_name}")
            save_metrics(self.agent_name)
