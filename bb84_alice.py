import socket
import random
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit

def bb84_alice(length=20):
    network = Network.get_instance()
    network.start()
    alice = Host('Alice')
    network.add_host(alice)

    alice_bits = [random.randint(0, 1) for _ in range(length)]
    alice_bases = [random.randint(0, 1) for _ in range(length)]
    qubits = []

    for i in range(length):
        q = Qubit(alice)
        if alice_bits[i] == 1:
            q.X()  # Flip the qubit if bit is 1
        if alice_bases[i] == 1:
            q.H()  # Apply Hadamard if basis is 1
        qubits.append(q)

    for q in qubits:
        alice.send_qubit('Bob', q)  # Send qubits to Bob

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 65432))
    data = sock.recv(1024).decode('utf-8')
    bob_bases = list(map(int, data.split(',')))

    sifted_bits = [alice_bits[i] for i in range(length) if alice_bases[i] == bob_bases[i]]
    common_indices = [i for i in range(length) if alice_bases[i] == bob_bases[i]]
    
    revealed_count = len(sifted_bits) // 4
    revealed_indices = random.sample(common_indices, revealed_count)
    revealed_bits = [sifted_bits[i] for i in revealed_indices]

    sock.sendall(','.join(map(str, revealed_indices)).encode('utf-8'))
    sock.sendall(','.join(map(str, revealed_bits)).encode('utf-8'))

    sock.close()
    final_key_alice = [sifted_bits[i] for i in range(len(sifted_bits)) if i not in revealed_indices]
    
    print(f"Final secret key (Alice): {final_key_alice}")
    network.stop()

if __name__ == '__main__':
    bb84_alice()
