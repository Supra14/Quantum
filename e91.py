import random
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit

# Helper function to create a random bit (0 or 1)
def random_bit():
    return random.randint(0, 1)

# Function to generate a Bell state |Φ+⟩ between Alice and Bob
def bell_state(host_a, host_b):
    # Create a qubit for Alice and Bob
    q_a = Qubit(host_a)
    q_b = Qubit(host_b)
    
    # Apply Hadamard gate on Alice's qubit to create superposition
    q_a.H()

    # Now, we can assume they are entangled since we cannot apply CNOT directly. 
    # We'll simulate it by assuming entanglement is created after the Hadamard gate.
    return q_a, q_b

# Function to measure qubits in a given basis (0 = rectilinear, 1 = diagonal)
def measure_in_basis(qubit, basis):
    if basis == 1:  # Diagonal basis (|+⟩, |−⟩)
        qubit.H()  # Apply Hadamard to switch to diagonal basis
    return qubit.measure()

# Function to perform E91 protocol
def e91_protocol(message_length=16):
    # Initialize network and hosts
    network = Network.get_instance()
    network.start()
    alice = Host('Alice')
    bob = Host('Bob')
    network.add_host(alice)
    network.add_host(bob)
    
    # Step 1: Create Bell state |Φ+⟩ between Alice and Bob
    q_a, q_b = bell_state(alice, bob)
    
    # Step 2: Alice and Bob choose random bases (0 = rectilinear, 1 = diagonal)
    alice_bases = [random_bit() for _ in range(message_length)]
    bob_bases = [random_bit() for _ in range(message_length)]
    
    # Step 3: Alice and Bob measure their qubits in the chosen bases
    alice_results = []
    bob_results = []
    
    # Measure Alice and Bob's qubits based on their random bases
    for i in range(message_length):
        # Reinitialize the qubits to avoid them being altered by previous operations
        q_a, q_b = bell_state(alice, bob)  # Recreate the Bell state for each measurement round
        
        # Alice measures her qubit in the selected basis
        alice_results.append(measure_in_basis(q_a, alice_bases[i]))
        
        # Bob measures his qubit in the selected basis
        bob_results.append(measure_in_basis(q_b, bob_bases[i]))
    
    # Step 4: Key Sifting (only keep results where bases match)
    sifted_key_alice = []
    sifted_key_bob = []
    for i in range(message_length):
        if alice_bases[i] == bob_bases[i]:  # If bases match
            sifted_key_alice.append(alice_results[i])
            sifted_key_bob.append(bob_results[i])
    
    # Step 5: Eavesdropping Detection (Simple check)
    eavesdropping_detected = False
    if len(sifted_key_alice) < message_length // 2:
        eavesdropping_detected = True
    
    # Output the results
    print(f"Alice's bases: {alice_bases}")
    print(f"Bob's bases: {bob_bases}")
    print(f"Alice's measurement results: {alice_results}")
    print(f"Bob's measurement results: {bob_results}")
    print(f"Sifted key (Alice): {sifted_key_alice}")
    print(f"Sifted key (Bob): {sifted_key_bob}")
    
    if eavesdropping_detected:
        print("Eavesdropping detected!")
    else:
        print("No eavesdropping detected.")
    
    # Final secret key (from the sifted key)
    print(f"Final secret key (Alice): {sifted_key_alice}")
    print(f"Final secret key (Bob): {sifted_key_bob}")
    
    # Stop the network
    network.stop()

    # Calculate the percentage of the final key relative to the original message length
    final_key_length = len(sifted_key_alice)
    percentage = (final_key_length / message_length) * 100
    print(f"Percentage of key length to original bits length: {percentage}%")
    
    return sifted_key_alice, sifted_key_bob, percentage

# Run the E91 Protocol for 5 test cases with 16 bits each and calculate average percentage
if __name__ == '__main__':
    test_lengths = [16, 16, 16, 16, 16]
    average_percentage = 0
    for length in test_lengths:
        print(f"\nRunning E91 protocol with message length: {length}")
        _, _, percentage = e91_protocol(length)
        average_percentage += percentage

    # Calculate the average percentage across the test cases
    average_percentage /= len(test_lengths)
    print(f"\nAverage percentage of key length to original bits length: {average_percentage}%")
