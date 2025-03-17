import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random
import math

def s_gate_error_experiment_with_eve(num_qubits=100, eve_probability=0.2, noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5]):
    network = Network.get_instance()
    network.start()

    bob = Host('Bob')    
    alice = Host('Alice')  
    eve = Host('Eve')    

    network.add_host(bob)
    network.add_host(alice)
    network.add_host(eve)

    bob.start()
    alice.start()
    eve.start()

    error_counts_per_qubits = []
    num_bits_sent = []
    avg_error_rates = []
    key_lengths = []
    eve_errors = 0  
    total_errors = 0
    total_measurements = 0  

    noise_probability_fixed = 0.2  

    print("\n--- Error Tracking for Each Qubit Sent (Fixed Noise Probability) ---")
    for n in range(1, num_qubits + 1):
        errors = 0
        for _ in range(n):
            q = Qubit(bob)
            q.Z()  # Simulating S-gate using Z and Hadamard
            q.H()
            q.H()

            # Eve intercepts with probability eve_probability
            if random.random() < eve_probability:
                q.measure()
                eve_errors += 1  

                q = Qubit(eve)  
                q.Z()
                q.H()
                q.H()
                error_gate = random.choice(['X', 'Z', 'Y'])  
                if error_gate == 'X': q.X()
                elif error_gate == 'Z': q.Z()
                elif error_gate == 'Y': q.Y()

            # Introduce noise (regardless of Eve’s interference)
            if random.random() < noise_probability_fixed:
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

        error_rate = (errors / n) * 100
        error_counts_per_qubits.append(error_rate)
        num_bits_sent.append(n)
        total_errors += errors
        total_measurements += n  

        print(f"Bits Sent: {n}, Error Rate: {error_rate:.2f}%, Eve Errors: {eve_errors}")

    print("\n--- Error Tracking for Different Noise Probabilities ---")
    for noise_probability in noise_probabilities:
        errors = 0
        for _ in range(num_qubits):
            q = Qubit(bob)
            q.Z()
            q.H()
            q.H()

            # Eve intercepts
            if random.random() < eve_probability:
                q.measure()
                eve_errors += 1  

                q = Qubit(eve)
                q.Z()
                q.H()
                q.H()
                error_gate = random.choice(['X', 'Z', 'Y'])  
                if error_gate == 'X': q.X()
                elif error_gate == 'Z': q.Z()
                elif error_gate == 'Y': q.Y()

            # Introduce noise regardless of Eve
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
        print(f"Noise Probability: {noise_probability:.2f}, Error Rate: {error_rate:.2f}%")

    for n in range(100, 1100, 100):
        key_lengths.append(math.log2(n))

    bob.stop()
    alice.stop()
    eve.stop()
    network.stop(True)

    # Compute Quantum Error Rate
    quantum_error_rate = total_errors / total_measurements if total_measurements > 0 else 0
    eve_disturbance_rate = eve_errors / total_measurements if total_measurements > 0 else 0

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    ax[0].plot(num_bits_sent, error_counts_per_qubits, linestyle='-', color='b')
    ax[0].set_xlabel('Number of Qubits Sent')
    ax[0].set_ylabel('Error Rate (%)')
    ax[0].set_title(f'Error Rate vs. Number of Qubits (Noise={noise_probability_fixed}, Eve={eve_probability})')
    ax[0].grid()

    ax[1].plot(noise_probabilities, avg_error_rates, linestyle='-', color='r')
    ax[1].set_xlabel('Noise Probability')
    ax[1].set_ylabel('Error Rate (%)')
    ax[1].set_title('Error Rate vs. Noise Probability')
    ax[1].grid()

    ax[2].plot(range(100, 1100, 100), key_lengths, linestyle='-', color='g')
    ax[2].set_xlabel('Number of Qubits Sent')
    ax[2].set_ylabel('Key Length (log₂ N)')
    ax[2].set_title('Number of Qubits vs. Key Length')
    ax[2].grid()

    plt.tight_layout()
    plt.show()

    print("\n=== Quantum Error Rate ===")
    print(f"Total Errors: {total_errors}")
    print(f"Total Measurements: {total_measurements}")
    print(f"Quantum Error Rate: {quantum_error_rate:.5f}")
    print(f"Eve's Disturbance Rate: {eve_disturbance_rate:.5f}")

if __name__ == "__main__":
    s_gate_error_experiment_with_eve(100, eve_probability=0.2, noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5])
