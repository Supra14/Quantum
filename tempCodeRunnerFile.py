import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit

def hadamard_error_experiment(num_qubits=100):
    network = Network.get_instance()
    network.start()

    bob = Host('Bob')
    alice = Host('Alice')

    bob.add_connection('Alice')
    alice.add_connection('Bob')

    network.add_host(bob)
    network.add_host(alice)

    bob.start()
    alice.start()

    error_counts = []
    num_bits_sent = []

    for n in range(1, num_qubits + 1):
        errors = 0
        for _ in range(n):
            q = Qubit(bob)
            q.H()  # Apply Hadamard gate

            send_status = bob.send_qubit(q, 'Alice', await_ack=True)
            if isinstance(send_status, str):  # If failure, debug
                print(f"Failed to send qubit: {send_status}")
                continue

            received_q = alice.get_data_qubit(sender='Bob', wait=10)
            if received_q is None:
                print("Alice did not receive the qubit.")
                continue

            received_q.H()
            measurement = received_q.measure()
            if measurement != 0:  # Expecting always 0 if no error
                errors += 1

        error_rate = errors / n
        error_counts.append(error_rate)
        num_bits_sent.append(n)

    bob.stop()
    alice.stop()
    network.stop(True)

    plt.plot(num_bits_sent, error_counts, marker='o', linestyle='-')
    plt.xlabel('Number of Qubits Sent')
    plt.ylabel('Error Rate')
    plt.title('Error Rate of Hadamard Gate vs. Number of Qubits Sent')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    hadamard_error_experiment(100)
