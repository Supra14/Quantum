from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random

# Helper function to create a random bit (0 or 1)
def random_bit():
    return random.randint(0, 1)

# Function to prepare qubits for Alice based on random bits
def prepare_qubits_b92(alice, length):
    alice_bits = [random_bit() for _ in range(length)]  # Alice's random bits
    qubits = []

    for bit in alice_bits:
        q = Qubit(alice)  # Create a new qubit
        if bit == 1:
            q.X()  # State |1⟩
        else:
            q.H()  # State |+⟩
        qubits.append(q)
    
    return alice_bits, qubits

# Function for Bob to receive and measure qubits
def measure_qubits_b92(bob, qubits, length):
    bob_results = []
    bob_bases = [random_bit() for _ in range(length)]  # Bob's random bases

    for i in range(length):
        q = qubits[i]
        if bob_bases[i] == 1:
            q.H()  # Measure in the Hadamard basis
        measurement = q.measure()
        bob_results.append(measurement)
    
    return bob_bases, bob_results

# Sift key by retaining bits that correspond to Bob detecting a qubit
def sift_key_b92(alice_bits, bob_results):
    sifted_key = []
    for alice_bit, bob_result in zip(alice_bits, bob_results):
        if alice_bit != bob_result:
            sifted_key.append(alice_bit)
    return sifted_key

# B92 Protocol implementation
def b92_protocol(length=20, test_cases=5):
    network = Network.get_instance()
    network.start()

    alice = Host('Alice')
    bob = Host('Bob')
    network.add_host(alice)
    network.add_host(bob)

    for test in range(test_cases):
        print(f"\nTest Case {test + 1}:")

        # Alice prepares qubits
        alice_bits, qubits = prepare_qubits_b92(alice, length)
        print(f"Alice's original bits: {alice_bits}")

        # Bob receives and measures qubits
        bob_bases, bob_results = measure_qubits_b92(bob, qubits, length)
        print(f"Bob's bases: {bob_bases} (0 = Standard basis, 1 = Diagonal basis)")
        print(f"Bob's results: {bob_results}")

        # Sift the key
        sifted_key = sift_key_b92(alice_bits, bob_results)
        print(f"Sifted Key: {sifted_key}")

    network.stop()

# Execute the B92 protocol
if __name__ == '__main__':
    b92_protocol(length=16, test_cases=5)
