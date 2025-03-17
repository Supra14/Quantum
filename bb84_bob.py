import socket
import random
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit

def bb84_bob(length=20):
    network = Network.get_instance()
    network.start()
    bob = Host('Bob')
    network.add_host(bob)

    qubits = [bob.get_qubit('Alice') for _ in range(length)]  
    bob_bases = [random.randint(0, 1) for _ in range(length)]
    bob_bits = []

    for i in range(length):
        q = qubits[i]
        if q is not None:  
            if bob_bases[i] == 1:
                q.H()  
            bob_bits.append(q.measure())
        else:
            bob_bits.append(None)  

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 65432))
    sock.listen()
    conn, _ = sock.accept()

    conn.sendall(','.join(map(str, bob_bases)).encode('utf-8'))

    data = conn.recv(1024).decode('utf-8')
    revealed_indices = list(map(int, data.split(',')))
    data = conn.recv(1024).decode('utf-8')
    revealed_bits_alice = list(map(int, data.split(',')))

    sifted_bits = [bob_bits[i] for i in range(length) if bob_bases[i] == bob_bases[i] and bob_bits[i] is not None]
    revealed_bits_bob = [sifted_bits[i] for i in revealed_indices]

    if revealed_bits_bob == revealed_bits_alice:
        print("No eavesdropping detected.")
    else:
        print("Potential eavesdropping detected.")

    final_key_bob = [sifted_bits[i] for i in range(len(sifted_bits)) if i not in revealed_indices]

    print(f"Final secret key (Bob): {final_key_bob}")
    network.stop()

if __name__ == '__main__':
    bb84_bob()
