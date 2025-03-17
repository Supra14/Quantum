import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random
import math

def s_gate_error_experiment(num_qubits=100, key_length_qubits=range(100, 1100, 100), noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5]):
    network = Network.get_instance()
    network.start()

    host = Host('Local')
    network.add_host(host)
    host.start()

    error_counts_per_qubits = []
    num_bits_sent = []
    avg_error_rates = []
    key_lengths = []
    total_errors = 0  # Track total errors
    total_measurements = 0  # Track total qubits processed

    noise_probability_fixed = 0.1
    for n in range(1, num_qubits + 1):
        errors = 0
        for _ in range(n):
            q = Qubit(host)
            q.Z()  # Simulating S-gate using Z and Hadamard
            q.H()
            q.H()

            if random.random() < noise_probability_fixed:
                noise_type = random.choice(['X', 'Z', 'Y'])
                if noise_type == 'X': q.X()
                elif noise_type == 'Z': q.Z()
                elif noise_type == 'Y': q.Y()

            q.H()
            q.H()
            q.Z()  # Undo phase shift

            measurement = q.measure()
            if measurement == 1:
                errors += 1

        error_rate = (errors / n) * 100
        error_counts_per_qubits.append(error_rate)
        num_bits_sent.append(n)
        total_errors += errors
        total_measurements += n  # Accumulate total measurements

    for noise_probability in noise_probabilities:
        errors = 0
        for _ in range(num_qubits):
            q = Qubit(host)
            q.Z()
            q.H()
            q.H()

            if random.random() < noise_probability:
                noise_type = random.choice(['X', 'Z', 'Y'])
                if noise_type == 'X': q.X()
                elif noise_type == 'Z': q.Z()
                elif noise_type == 'Y': q.Y()

            q.H()
            q.H()
            q.Z()

            measurement = q.measure()
            if measurement == 1:
                errors += 1

        error_rate = (errors / num_qubits) * 100
        avg_error_rates.append(error_rate)

    for n in key_length_qubits:
        key_lengths.append(math.log2(n))

    host.stop()
    network.stop(True)

    # Compute Quantum Error Rate
    quantum_error_rate = total_errors / total_measurements if total_measurements > 0 else 0

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    ax[0].plot(num_bits_sent, error_counts_per_qubits, linestyle='-', color='b')
    ax[0].set_xlabel('Number of Qubits Sent')
    ax[0].set_ylabel('Error Rate (%)')
    ax[0].set_title(f'Error Rate vs. Number of Qubits (Noise={noise_probability_fixed})')
    ax[0].grid()

    ax[1].plot(noise_probabilities, avg_error_rates, linestyle='-', color='r')
    ax[1].set_xlabel('Noise Probability')
    ax[1].set_ylabel('Error Rate (%)')
    ax[1].set_title('Error Rate vs. Noise Probability')
    ax[1].grid()

    ax[2].plot(key_length_qubits, key_lengths, linestyle='-', color='g')
    ax[2].set_xlabel('Number of Qubits Sent')
    ax[2].set_ylabel('Key Length (log₂ N)')
    ax[2].set_title('Number of Qubits vs. Key Length')
    ax[2].grid()

    plt.tight_layout()
    plt.show()

    # Print Quantum Error Rate
    print("\n=== Quantum Error Rate ===")
    print(f"Total Errors: {total_errors}")
    print(f"Total Measurements: {total_measurements}")
    print(f"Quantum Error Rate: {quantum_error_rate:.5f}")

if __name__ == "__main__":
    s_gate_error_experiment()
