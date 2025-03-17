import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random
import math

def quantum_gate_error_experiment(gate_name, apply_gate, num_qubits=100, noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5]):
    network = Network.get_instance()
    network.start()

    host = Host('Local')
    network.add_host(host)
    host.start()

    error_counts = []
    avg_error_rates = []
    num_bits_sent = list(range(1, num_qubits + 1))
    key_length_qubits = list(range(100, 1100, 100))
    key_lengths = [math.log2(n) for n in key_length_qubits]

    noise_probability_fixed = 0.1
    total_errors = 0

    for n in num_bits_sent:
        errors = 0
        for _ in range(n):
            q = Qubit(host)
            apply_gate(q)

            if random.random() < noise_probability_fixed:
                noise_type = random.choice(['X', 'Z', 'Y'])
                if noise_type == 'X': q.X()
                elif noise_type == 'Z': q.Z()
                elif noise_type == 'Y': q.Y()

            apply_gate(q)
            measurement = q.measure()
            if measurement == 1:
                errors += 1

        error_counts.append((errors / n) * 100)
        total_errors += errors

    for noise_probability in noise_probabilities:
        errors = 0
        for _ in range(num_qubits):
            q = Qubit(host)
            apply_gate(q)

            if random.random() < noise_probability:
                noise_type = random.choice(['X', 'Z', 'Y'])
                if noise_type == 'X': q.X()
                elif noise_type == 'Z': q.Z()
                elif noise_type == 'Y': q.Y()

            apply_gate(q)
            measurement = q.measure()
            if measurement == 1:
                errors += 1

        avg_error_rates.append((errors / num_qubits) * 100)

    host.stop()
    network.stop(True)

    quantum_error_rate = total_errors / (num_qubits * (num_qubits + 1) / 2)  # Normalized error rate
    return num_bits_sent, error_counts, noise_probabilities, avg_error_rates, key_length_qubits, key_lengths, quantum_error_rate

def apply_s_gate(q):
    """Simulate the S gate using Z and Hadamard operations."""
    q.Z()
    q.H()
    q.H()

def apply_t_gate(q):
    """Simulate the T gate using Z and Hadamard operations."""
    q.Z()
    q.H()
    q.H()

if __name__ == "__main__":
    print("\nRunning S-Gate Error Experiment...")
    s_bits, s_errors, s_noises, s_avg_errors, s_keys, s_key_lengths, s_error_rate = quantum_gate_error_experiment("S", apply_s_gate)

    print("\nRunning T-Gate Error Experiment...")
    t_bits, t_errors, t_noises, t_avg_errors, t_keys, t_key_lengths, t_error_rate = quantum_gate_error_experiment("T", apply_t_gate)

    # Plot Results (Both gates in same graphs)
    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    # Error Rate vs. Number of Qubits
    ax[0].plot(s_bits, s_errors, linestyle='-', color='b', label="S Gate")
    ax[0].plot(t_bits, t_errors, linestyle='-', color='r', label="T Gate")
    ax[0].set_xlabel('Number of Qubits Sent')
    ax[0].set_ylabel('Error Rate (%)')
    ax[0].set_title('Error Rate vs. Number of Qubits')
    ax[0].grid()
    ax[0].legend()

    # Error Rate vs. Noise Probability
    ax[1].plot(s_noises, s_avg_errors, linestyle='-', color='b', label="S Gate")
    ax[1].plot(t_noises, t_avg_errors, linestyle='-', color='r', label="T Gate")
    ax[1].set_xlabel('Noise Probability')
    ax[1].set_ylabel('Error Rate (%)')
    ax[1].set_title('Error Rate vs. Noise Probability')
    ax[1].grid()
    ax[1].legend()

    # Number of Qubits vs. Key Length (Fix: Different linestyle for visibility)
    ax[2].plot(s_keys, s_key_lengths, linestyle='--', color='b', label="S Gate")
    ax[2].plot(t_keys, t_key_lengths, linestyle='-', color='r', label="T Gate")
    ax[2].set_xlabel('Number of Qubits Sent')
    ax[2].set_ylabel('Key Length (log₂ N)')
    ax[2].set_title('Number of Qubits vs. Key Length')
    ax[2].grid()
    ax[2].legend()

    plt.tight_layout()
    plt.show()

    # Quantum Error Rate Summary
    print("\n=== Quantum Error Rate Comparison ===")
    print(f"S-Gate Quantum Error Rate: {s_error_rate:.5f}")
    print(f"T-Gate Quantum Error Rate: {t_error_rate:.5f}")
