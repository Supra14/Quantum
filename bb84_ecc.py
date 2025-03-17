from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random
from copy import deepcopy

# Helper function to create a random bit (0 or 1)
def random_bit():
    return random.randint(0, 1)

# Function to prepare qubits for Alice based on random bits and bases
def prepare_qubits(alice, length):
    alice_bits = [random_bit() for _ in range(length)]  # Alice's random bits
    alice_bases = [random_bit() for _ in range(length)]  # Alice's random bases (0 = rectilinear, 1 = diagonal)
    qubits = []
    
    for i in range(length):
        q = Qubit(alice)  # Create a new qubit for Alice
        if alice_bits[i] == 1:
            q.X()  # Apply X gate for bit 1
        if alice_bases[i] == 1:
            q.H()  # Apply Hadamard gate for diagonal basis
        qubits.append(q)
    
    return alice_bits, alice_bases, qubits

# Function for Eve to intercept and measure qubits
def eavesdrop(eve, qubits, length):
    eve_bases = [random_bit() for _ in range(length)]  # Eve's random bases
    eve_results = []
    
    for i in range(length):
        q = qubits[i]
        if eve_bases[i] == 1:
            q.H()  # Apply Hadamard gate if Eve uses diagonal basis
        eve_results.append(q.measure())
    
    return eve_bases, eve_results

# Function for Bob to receive and measure qubits
def measure_qubits(bob, qubits, length):
    bob_bases = [random_bit() for _ in range(length)]  # Bob's random bases
    bob_results = []

    for i in range(length):
        try:
            q = qubits[i]
            if bob_bases[i] == 1:
                q.H()  # Apply Hadamard gate if Bob uses diagonal basis
            bob_results.append(q.measure())
        except Exception as e:
            print(f"Error measuring qubit {i}: {e}")
            bob_results.append(None)  # Mark invalid measurement

    return bob_bases, bob_results

# Function to sift the key by matching bases
def sift_key(alice_bases, bob_bases, alice_bits, bob_bits):
    sifted_key_alice = []
    sifted_key_bob = []
    matching_indices = []
    
    for i in range(len(alice_bases)):
        if alice_bases[i] == bob_bases[i]:  # Bases match
            sifted_key_alice.append(alice_bits[i])
            sifted_key_bob.append(bob_bits[i])
            matching_indices.append(i)
    
    return matching_indices, sifted_key_alice, sifted_key_bob

# Function for error correction using repetition coding
def error_correction(sifted_key_alice, sifted_key_bob, repetition_factor):
    corrected_key_alice = []
    corrected_key_bob = []

    for i in range(0, len(sifted_key_alice), repetition_factor):
        block_a = sifted_key_alice[i:i + repetition_factor]
        block_b = sifted_key_bob[i:i + repetition_factor]

        # Take the majority bit in each block
        majority_a = max(set(block_a), key=block_a.count) if block_a else None
        majority_b = max(set(block_b), key=block_b.count) if block_b else None

        if majority_a is not None:
            corrected_key_alice.append(majority_a)
        if majority_b is not None:
            corrected_key_bob.append(majority_b)

    return corrected_key_alice, corrected_key_bob

# BB84 Protocol implementation
def bb84_protocol(length=20, test_cases=5, repetition_factor=3):
    network = Network.get_instance()
    network.start()

    alice = Host('Alice')
    bob = Host('Bob')
    eve = Host('Eve')  # Add Eve to the network
    network.add_host(alice)
    network.add_host(bob)
    network.add_host(eve)

    matching_percentages = []

    for test in range(test_cases):
        print(f"\nTest Case {test + 1}:")

        # Alice prepares qubits
        alice_bits, alice_bases, qubits = prepare_qubits(alice, length)
        print(f"Alice's original bits: {alice_bits}")
        print(f"Alice's bases: {alice_bases} (0 = Rectilinear, 1 = Diagonal)")

        # Eve intercepts the qubits
        eve_qubits = [deepcopy(q) for q in qubits]  # Copy to preserve state
        eve_bases, eve_results = eavesdrop(eve, eve_qubits, length)
        print(f"Eve's bases: {eve_bases} (0 = Rectilinear, 1 = Diagonal)")
        print(f"Eve's results: {eve_results}")

        # Bob receives and measures qubits
        bob_bases, bob_bits = measure_qubits(bob, qubits, length)
        print(f"Bob's bases: {bob_bases} (0 = Rectilinear, 1 = Diagonal)")
        print(f"Bob's measured bits: {bob_bits}")

        # Sift the key
        matching_indices, sifted_key_alice, sifted_key_bob = sift_key(alice_bases, bob_bases, alice_bits, bob_bits)
        print(f"Sifted Key (Alice): {sifted_key_alice}")
        print(f"Sifted Key (Bob): {sifted_key_bob}")

        # Error correction
        corrected_key_alice, corrected_key_bob = error_correction(sifted_key_alice, sifted_key_bob, repetition_factor)
        print(f"Corrected Key (Alice): {corrected_key_alice}")
        print(f"Corrected Key (Bob): {corrected_key_bob}")

        # Calculate matching percentage
        matching_percentage = (len(corrected_key_alice) / length) * 100
        matching_percentages.append(matching_percentage)
        print(f"Matching Percentage: {matching_percentage:.2f}%")

    # Average matching percentage
    average_matching_percentage = sum(matching_percentages) / len(matching_percentages)
    print(f"\nAverage Matching Percentage Over {test_cases} Test Cases: {average_matching_percentage:.2f}%")

    network.stop()

# Execute the BB84 protocol
if __name__ == '__main__':
    bb84_protocol(length=16, test_cases=5, repetition_factor=3)
