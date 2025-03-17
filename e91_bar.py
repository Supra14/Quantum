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

def simulate_e91():
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
    
    e91(sender, receiver, num_bits)
    
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
    plt.title('Resource Usage for E91 Protocol')
    plt.show()
    
if __name__ == '__main__':
    simulate_e91()
