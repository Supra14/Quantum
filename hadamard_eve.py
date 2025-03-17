import numpy as np
import matplotlib.pyplot as plt
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random
import math

def hadamard_error_experiment_with_eve(num_qubits=100, eve_probability=0.2, noise_probabilities=[0.01, 0.05, 0.1, 0.2, 0.3, 0.5]):
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
            q.H()  

            if random.random() < eve_probability:
                q.measure()
                eve_errors += 1  

                q = Qubit(eve)
                q.H()
                error_gate = random.choice(['X', 'Z', 'Y'])
                if error_gate == 'X': q.X()
                elif error_gate == 'Z': q.Z()
                elif error_gate == 'Y': q.Y()

            if random.random() < noise_probability_fixed:
                noise_type = random.choice(['X', 'Z', 'Y'])
                if noise_type == 'X': q.X()
                elif noise_type == 'Z': q.Z()
                elif noise_type == 'Y': q.Y()

            q.H()  
            measurement = q.measure()

            if measurement == 1:
                errors += 1

        error_rate = (errors / n) * 100
        error_counts_per_qubits.append(error_rate)
        num_bits_sent.append(n)
        total_errors += errors
        total_measurements += n

        print(f"Bits Sent: {n}, Error Rate: {error_rate:.2f}%, Eve Errors: {eve_errors}")

    bob.stop()
    alice.stop()
    eve.stop()
    network.stop(True)

    quantum_error_rate = total_errors / total_measurements if total_measurements > 0 else 0
    eve_disturbance_rate = eve_errors / total_measurements if total_measurements > 0 else 0

    print("\n=== Quantum Error Rate ===")
    print(f"Total Errors: {total_errors}")
    print(f"Total Measurements: {total_measurements}")
    print(f"Quantum Error Rate: {quantum_error_rate:.5f}")
    print(f"Eve's Disturbance Rate: {eve_disturbance_rate:.5f}")

if __name__ == "__main__":
    hadamard_error_experiment_with_eve(100, eve_probability=0.2)
