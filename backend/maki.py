# maki.py

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class MAKI:
    def __init__(self):
        self.keys = {}
        self.trust = {}  # Track trust levels

    def generate_key_pair(self, agent_id):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        self.keys[agent_id] = {
            'private_key': private_key,
            'public_key': public_key,
        }
        self.trust[agent_id] = 100  # Initial trust level
        pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return pem.decode('utf-8')

    def get_public_key(self, agent_id):
        public_key = self.keys[agent_id]['public_key']
        pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return pem.decode('utf-8')

    def encrypt_message(self, agent_id, message):
        public_key = self.keys[agent_id]['public_key']
        encrypted = public_key.encrypt(message.encode('utf-8'), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt_message(self, agent_id, encrypted_message):
        private_key = self.keys[agent_id]['private_key']
        encrypted_message_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
        decrypted = private_key.decrypt(encrypted_message_bytes, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return decrypted.decode('utf-8')

    def update_trust(self, agent_id, trust_value):
        if agent_id in self.trust:
            self.trust[agent_id] = trust_value
        return self.trust[agent_id]

    def get_all_agents(self):
        return [{'agent_id': agent_id, 'public_key': self.get_public_key(agent_id), 'trust_value': trust, 'role': 'agent'} for agent_id, trust in self.trust.items()]

# Agent class integrating MAKI and Blockchain
class Agent:
    def __init__(self, agent_id, blockchain, maki):
        self.agent_id = agent_id
        self.blockchain = blockchain
        self.maki = maki
        self.maki.generate_key_pair(agent_id)
        self.blockchain.state.balances[self.agent_id] = 100  # Assign initial balance

    def send_message(self, recipient_id, message):
        encrypted_message = self.maki.encrypt_message(recipient_id, message)
        return encrypted_message

    def receive_message(self, sender_id, encrypted_message):
        decrypted_message = self.maki.decrypt_message(self.agent_id, encrypted_message)
        return decrypted_message

    def start_transaction(self, recipient_id, amount):
        self.blockchain.add_transaction(self.agent_id, recipient_id, amount)

    def add_block(self):
        self.blockchain.mine_block()

    def broadcast_message(self, message):
        for agent in self.maki.get_all_agents():
            if agent['agent_id'] != self.agent_id:
                encrypted_message = self.send_message(agent['agent_id'], message)
                print(f"Broadcast message to {agent['agent_id']}: {encrypted_message}")
