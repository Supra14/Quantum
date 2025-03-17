import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random
import math

def pauli_x_error_experiment(num_qubits=100, noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5]):
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

    # First Experiment: Error Rate vs. Number of Qubits (Fixed Noise Probability)
    noise_probability_fixed = 0.1
    print("\n--- Error Tracking for Each Qubit Sent (Fixed Noise Probability) ---")
    for n in range(1, num_qubits + 1):
        errors = 0
        for _ in range(n):
            q = Qubit(host)  # Assigning a host
            q.X()  # Apply Pauli-X gate

            if random.random() < noise_probability_fixed:
                noise_type = random.choice(['H', 'Z', 'Y'])  # Random noise type
                if noise_type == 'H':
                    q.H()
                elif noise_type == 'Z':
                    q.Z()
                elif noise_type == 'Y':
                    q.Y()

            q.X()  # Apply Pauli-X again
            measurement = q.measure()

            if measurement == 1:  # Check for actual errors
                errors += 1

        error_rate = (errors / n) * 100  # Convert to percentage
        error_counts_per_qubits.append(error_rate)
        num_bits_sent.append(n)
        key_lengths.append(math.log2(n) if n > 0 else 0)  # Assuming key length = log₂(n)
        total_errors += errors
        total_measurements += n  # Accumulate total measurements
        print(f"Bits Sent: {n}, Error Rate: {error_rate:.2f}%, Key Length: {key_lengths[-1]:.2f}")

    # Second Experiment: Error Rate vs. Noise Probability (Fixed Number of Qubits)
    print("\n--- Error Tracking for Different Noise Probabilities ---")
    for noise_probability in noise_probabilities:
        errors = 0
        for _ in range(num_qubits):
            q = Qubit(host)  # Assigning a host
            q.X()  # Apply Pauli-X gate

            if random.random() < noise_probability:
                noise_type = random.choice(['H', 'Z', 'Y'])  # Random noise type
                if noise_type == 'H':
                    q.H()
                elif noise_type == 'Z':
                    q.Z()
                elif noise_type == 'Y':
                    q.Y()

            q.X()  # Apply Pauli-X again
            measurement = q.measure()

            if measurement == 1:  # Check for actual errors
                errors += 1

        error_rate = (errors / num_qubits) * 100  # Convert to percentage
        avg_error_rates.append(error_rate)
        print(f"Noise Probability: {noise_probability:.2f}, Error Rate: {error_rate:.2f}%")

    host.stop()
    network.stop(True)

    # Compute Quantum Error Rate
    quantum_error_rate = total_errors / total_measurements if total_measurements > 0 else 0

    # Plot three graphs side by side
    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    # First Graph: Error Rate vs. Number of Qubits
    ax[0].plot(num_bits_sent, error_counts_per_qubits, linestyle='-', color='b')
    ax[0].set_xlabel('Number of Qubits Sent')
    ax[0].set_ylabel('Error Rate (%)')
    ax[0].set_title(f'Error Rate vs. Number of Qubits (Noise={noise_probability_fixed})')
    ax[0].grid()

    # Second Graph: Error Rate vs. Noise Probability
    ax[1].plot(noise_probabilities, avg_error_rates, linestyle='-', color='r')
    ax[1].set_xlabel('Noise Probability')
    ax[1].set_ylabel('Error Rate (%)')
    ax[1].set_title('Error Rate vs. Noise Probability')
    ax[1].grid()

    # Third Graph: Number of Qubits vs. Key Length
    ax[2].plot(num_bits_sent, key_lengths, linestyle='-', color='g')
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
    pauli_x_error_experiment(100, noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5])
