import random
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import time

def alice_protocol(host_A, bits, bases):
    # Prepare qubits based on bits and bases
    qubits = []
    for i in range(len(bits)):
        qubit = Qubit(host_A)
        if bits[i] == 1:
            qubit.X()  # Flip qubit to |1> if the bit is 1
        if bases[i] == 1:
            qubit.H()  # Apply Hadamard gate for diagonal basis
        qubits.append(qubit)

    # Send qubits to Bob
    for qubit in qubits:
        host_A.send_qubit('B', qubit, await_ack=True)

def bob_protocol(host_B, n_bits):
    # Bob chooses random bases to measure
    bob_bases = [random.randint(0, 1) for _ in range(n_bits)]
    received_bits = []
    
    # Bob receives and measures qubits
    for _ in range(n_bits):
        qubit = host_B.get_data_qubit('A')
        if qubit is not None:
            if bob_bases[_] == 1:
                qubit.H()  # Apply Hadamard gate for diagonal basis
            received_bits.append(qubit.measure())
        else:
            received_bits.append(None)  # Handle any missing qubits

    return bob_bases, received_bits

def classical_basis_comparison(alice_bases, bob_bases):
    # Compare bases and keep only the bits where the bases match
    matching_indices = [i for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
    return matching_indices

def bb84_protocol():
    n_bits = 20  # Number of bits Alice sends to Bob
    network = Network.get_instance()
    network.start()

    # Create Alice and Bob
    host_A = Host('A')
    host_B = Host('B')

    # Add the connection between Alice and Bob
    host_A.add_connection('B')
    host_B.add_connection('A')
    network.add_host(host_A)
    network.add_host(host_B)

    host_A.start()
    host_B.start()

    time.sleep(1)  # Allow network to stabilize

    # Alice's random bits and bases
    alice_bits = [random.randint(0, 1) for _ in range(n_bits)]
    alice_bases = [random.randint(0, 1) for _ in range(n_bits)]

    # Start Alice's protocol
    alice_protocol(host_A, alice_bits, alice_bases)

    # Bob receives the qubits and measures them
    bob_bases, bob_measurements = bob_protocol(host_B, n_bits)

    # Compare the bases
    matching_indices = classical_basis_comparison(alice_bases, bob_bases)

    # Extract the key (bits where Alice's and Bob's bases match)
    alice_key = [alice_bits[i] for i in matching_indices]
    bob_key = [bob_measurements[i] for i in matching_indices]

    # Print results
    print(f"Alice's bits:       {alice_bits}")
    print(f"Alice's bases:      {alice_bases}")
    print(f"Bob's bases:        {bob_bases}")
    print(f"Bob's measurements: {bob_measurements}")
    print(f"Matching indices:   {matching_indices}")
    print(f"Alice's key:        {alice_key}")
    print(f"Bob's key:          {bob_key}")

    # Stop the network
    time.sleep(2)
    network.stop(True)

# Main program execution
if __name__ == '__main__':
    bb84_protocol()
