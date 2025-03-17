import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Host, Network  # ✅ FIXED: Import Network
from qunetsim.objects import Qubit
import random
import math

def rz_gate_error_experiment(num_qubits=100, key_length_qubits=range(100, 1100, 100), noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5]):
    network = Network.get_instance()  # ✅ FIXED: Network is now defined
    network.start()

    host = Host('Local')
    network.add_host(host)
    host.start()

    error_counts_per_qubits = []
    num_bits_sent = []
    avg_error_rates = []
    key_lengths = []
    total_errors = 0
    total_measurements = 0

    noise_probability_fixed = 0.1
    for n in range(1, num_qubits + 1):
        errors = 0
        for _ in range(n):
            q = Qubit(host)
            q.Z()  # Approximate RZ(π/2)

            if random.random() < noise_probability_fixed:
                noise_type = random.choice(['H', 'X', 'Y'])
                if noise_type == 'H': q.H()
                elif noise_type == 'X': q.X()
                elif noise_type == 'Y': q.Y()

            q.Z()
            measurement = q.measure()

            if measurement == 1:
                errors += 1

        error_rate = (errors / n) * 100
        error_counts_per_qubits.append(error_rate)
        num_bits_sent.append(n)
        key_lengths.append(math.log2(n) if n > 0 else 0)
        total_errors += errors
        total_measurements += n

    for noise_probability in noise_probabilities:
        errors = 0
        for _ in range(num_qubits):
            q = Qubit(host)
            q.Z()

            if random.random() < noise_probability:
                noise_type = random.choice(['H', 'X', 'Y'])
                if noise_type == 'H': q.H()
                elif noise_type == 'X': q.X()
                elif noise_type == 'Y': q.Y()

            q.Z()
            measurement = q.measure()

            if measurement == 1:
                errors += 1

        avg_error_rates.append((errors / num_qubits) * 100)

    quantum_error_rate = total_errors / total_measurements if total_measurements > 0 else 0

    host.stop()
    network.stop(True)

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))
    ax[0].plot(num_bits_sent, error_counts_per_qubits, linestyle='-', color='b')
    ax[1].plot(noise_probabilities, avg_error_rates, linestyle='-', color='r')
    ax[2].plot(num_bits_sent, key_lengths, linestyle='-', color='g')

    plt.tight_layout()
    plt.show()

    print("\n=== Quantum Error Rate ===")
    print(f"Total Errors: {total_errors}")
    print(f"Total Measurements: {total_measurements}")
    print(f"Quantum Error Rate: {quantum_error_rate:.5f}")

if __name__ == "__main__":
    rz_gate_error_experiment()
