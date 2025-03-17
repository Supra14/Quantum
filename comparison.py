import random
import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Network, Host
from qunetsim.objects import Qubit

def bb84(sender, receiver, num_bits):
    key = []
    for _ in range(num_bits):
        qubit = Qubit(sender)
        basis = random.choice(['Z', 'X'])
        bit = random.choice([0, 1])
        if bit == 1:
            qubit.X()
        if basis == 'X':
            qubit.H()
        sender.send_qubit(receiver.host_id, qubit, await_ack=True)
        
        recv_qubit = receiver.get_qubit(sender.host_id, wait=10)
        recv_basis = random.choice(['Z', 'X'])
        if recv_basis == 'X':
            recv_qubit.H()
        
        measured_bit = recv_qubit.measure()
        if basis == recv_basis:
            key.append(measured_bit)
    return key

def b92(sender, receiver, num_bits):
    key = []
    for _ in range(num_bits):
        qubit = Qubit(sender)
        bit = random.choice([0, 1])
        if bit == 1:
            qubit.X()
        qubit.H()
        sender.send_qubit(receiver.host_id, qubit, await_ack=True)
        
        recv_qubit = receiver.get_qubit(sender.host_id, wait=10)
        recv_basis = random.choice(['Z', 'X'])
        if recv_basis == 'X':
            recv_qubit.H()
        measured_bit = recv_qubit.measure()
        if measured_bit == 1:
            key.append(bit)
    return key

def e91(sender, receiver, num_bits):
    key = []
    for _ in range(num_bits):
        qubit1 = Qubit(sender)
        qubit2 = Qubit(sender)
        qubit1.H()
        qubit2.cnot(qubit1)
        sender.send_qubit(receiver.host_id, qubit2, await_ack=True)
        recv_qubit = receiver.get_qubit(sender.host_id, wait=10)
        basis = random.choice(['Z', 'X'])
        if basis == 'X':
            recv_qubit.H()
        measured_bit = recv_qubit.measure()
        key.append(measured_bit)
    return key

def simulate_qkd():
    network = Network.get_instance()
    network.start()
    sender = Host('A')
    receiver = Host('B')
    sender.add_connection('B')
    receiver.add_connection('A')
    network.add_hosts([sender, receiver])
    sender.start()
    receiver.start()
    
    num_bits_list = np.linspace(10, 500, 50)
    key_lengths = { 'BB84': [], 'B92': [], 'E91': [] }
    complexities = { 'BB84': [], 'B92': [], 'E91': [] }
    
    for num_bits in num_bits_list:
        bb84_key = bb84(sender, receiver, int(num_bits))
        b92_key = b92(sender, receiver, int(num_bits))
        e91_key = e91(sender, receiver, int(num_bits))
        
        key_lengths['BB84'].append(len(bb84_key))
        key_lengths['B92'].append(len(b92_key))
        key_lengths['E91'].append(len(e91_key))
        
        complexities['BB84'].append(num_bits * 2)  # Approximate operations count
        complexities['B92'].append(num_bits * 1.5)
        complexities['E91'].append(num_bits * 3)
    
    network.stop(True)
    
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(num_bits_list, key_lengths['BB84'], label='BB84', linestyle='-', marker='')
    plt.plot(num_bits_list, key_lengths['B92'], label='B92', linestyle='-', marker='')
    plt.plot(num_bits_list, key_lengths['E91'], label='E91', linestyle='-', marker='')
    plt.xlabel('Number of Bits Sent')
    plt.ylabel('Key Length Generated')
    plt.title('Key Length Comparison')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(num_bits_list, complexities['BB84'], label='BB84 Complexity', linestyle='-', marker='')
    plt.plot(num_bits_list, complexities['B92'], label='B92 Complexity', linestyle='-', marker='')
    plt.plot(num_bits_list, complexities['E91'], label='E91 Complexity', linestyle='-', marker='')
    plt.xlabel('Number of Bits Sent')
    plt.ylabel('Complexity (Approximate Operations)')
    plt.title('Complexity Analysis of QKD Protocols')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    simulate_qkd()