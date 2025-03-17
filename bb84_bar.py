import random
import numpy as np
import matplotlib.pyplot as plt
import psutil
import time
from qunetsim.components import Network, Host
from qunetsim.objects import Qubit

def measure_resource_usage():
    return {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'network': psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    }

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

def simulate_bb84():
    network = Network.get_instance()
    network.start()
    sender = Host('A')
    receiver = Host('B')
    sender.add_connection('B')
    receiver.add_connection('A')
    network.add_hosts([sender, receiver])
    sender.start()
    receiver.start()
    
    num_bits = 100
    resource_usage = { 'CPU': 0, 'Memory': 0, 'Disk': 0, 'Network': 0 }
    
    usage_before = measure_resource_usage()
    time.sleep(1)
    
    bb84(sender, receiver, num_bits)
    
    time.sleep(1)
    usage_after = measure_resource_usage()
    
    resource_usage['CPU'] = abs(usage_after['cpu'] - usage_before['cpu'])
    resource_usage['Memory'] = abs(usage_after['memory'] - usage_before['memory'])
    resource_usage['Disk'] = abs(usage_after['disk'] - usage_before['disk'])
    resource_usage['Network'] = abs(usage_after['network'] - usage_before['network']) / 1e6  # Convert bytes to MB
    
    network.stop(True)
    
    categories = list(resource_usage.keys())
    values = list(resource_usage.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(categories, values, color=['blue', 'orange', 'green', 'red'])
    plt.xlabel('Resource Type')
    plt.ylabel('Usage (%) or MB')
    plt.title('Resource Usage for BB84 Protocol')
    plt.show()
    
if __name__ == '__main__':
    simulate_bb84()
