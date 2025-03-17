from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import random

# Helper function to create a random bit (0 or 1)
def random_bit():
    return random.randint(0, 1)

# Function to prepare qubits for Alice based on random bits and bases
def prepare_qubits(alice, length):
    alice_bits = [random_bit() for _ in range(length)]  # Alice's random bits
    alice_bases = [random_bit() for _ in range(length)]  # Alice's random bases (0 = rectilinear, 1 = diagonal)
    qubits = []
    
    for i in range(length):
        q = Qubit(alice)  # Create a new qubit
        if alice_bits[i] == 1:
            q.X()  # Apply X gate for bit 1 (to flip the qubit)
        if alice_bases[i] == 1:
            q.Y()  # Apply Pauli-Y gate for diagonal basis
        qubits.append(q)
    
    return alice_bits, alice_bases, qubits

# Function for Bob to receive and measure qubits
def measure_qubits(bob, qubits, length):
    bob_bases = [random_bit() for _ in range(length)]  # Bob's random bases
    bob_results = []
    
    for i in range(length):
        q = qubits[i]
        if bob_bases[i] == 1:
            q.Y()  # Apply Pauli-Y gate if Bob uses diagonal basis
        bob_results.append(q.measure())
    
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

# Function to publicly reveal some bits and bases for verification
def reveal_bases_and_bits(matching_indices, sifted_key_alice, sifted_key_bob, reveal_count):
    revealed_indices = random.sample(range(len(sifted_key_alice)), reveal_count)
    revealed_bases = [matching_indices[i] for i in revealed_indices]
    revealed_bits_alice = [sifted_key_alice[i] for i in revealed_indices]
    revealed_bits_bob = [sifted_key_bob[i] for i in revealed_indices]
    
    return revealed_bases, revealed_bits_alice, revealed_bits_bob

# BB84 Protocol implementation using QunetSim
def bb84_protocol(length=20):
    # Initialize network and hosts
    network = Network.get_instance()
    network.start()
    alice = Host('Alice')
    bob = Host('Bob')
    network.add_host(alice)
    network.add_host(bob)

    # Alice prepares qubits
    alice_bits, alice_bases, qubits = prepare_qubits(alice, length)
    print(f"Alice's bits: {alice_bits}")
    print(f"Alice's bases: {alice_bases} (0 = R, 1 = D)")

    # Send qubits from Alice to Bob
    for q in qubits:
        alice.send_qubit('Bob', q)

    # Bob receives and measures qubits
    bob_bases, bob_bits = measure_qubits(bob, qubits, length)
    print(f"Bob's bases: {bob_bases} (0 = R, 1 = D)")
    print(f"Bob's measured bits: {bob_bits}")

    # Sift the key based on matching bases
    matching_indices, sifted_key_alice, sifted_key_bob = sift_key(alice_bases, bob_bases, alice_bits, bob_bits)
    print(f"Sifted key (Alice): {sifted_key_alice}")
    print(f"Sifted key (Bob): {sifted_key_bob}")

    # Publicly reveal some bits and bases for verification (25% of the sifted key)
    revealed_count = len(sifted_key_alice) // 4  # Reveal 25% of the sifted key
    revealed_bases, revealed_bits_alice, revealed_bits_bob = reveal_bases_and_bits(matching_indices, sifted_key_alice, sifted_key_bob, revealed_count)
    print(f"\nPublicly revealed indices: {revealed_bases}")
    print(f"Revealed bits (Alice): {revealed_bits_alice}")
    print(f"Revealed bits (Bob): {revealed_bits_bob}")

    # Verify revealed bits
    if revealed_bits_alice == revealed_bits_bob:
        print("No eavesdropping detected, revealed bits match.")
    else:
        print("Potential eavesdropping detected, revealed bits do not match!")

    # Final secret key (remove revealed indices)
    final_key_alice = [sifted_key_alice[i] for i in range(len(sifted_key_alice)) if i not in revealed_bases]
    final_key_bob = [sifted_key_bob[i] for i in range(len(sifted_key_bob)) if i not in revealed_bases]
    print(f"\nFinal secret key (Alice): {final_key_alice}")
    print(f"Final secret key (Bob): {final_key_bob}")

    # Stop the network
    network.stop()

# Execute the BB84 protocol
if __name__ == '__main__':
    bb84_protocol()
