from qunetsim.components import Host, Network
from qunetsim.objects import Logger
import random

# Disable logging for cleaner output
Logger.DISABLED = True

# Function to introduce errors in the qubits
def introduce_errors(qubit, error_rate):
    if random.random() < error_rate:
        # Apply a random error (X, Y, or Z gate)
        error_type = random.choice(['X', 'Y', 'Z'])
        if error_type == 'X':
            qubit.X()
        elif error_type == 'Y':
            qubit.Y()
        elif error_type == 'Z':
            qubit.Z()
    return qubit

# Function to compare quantum gates based on error percentage
def compare_gates(error_rate, num_qubits=100):
    # Initialize the network
    network = Network.get_instance()
    network.start()

    # Create two hosts, Alice and Bob
    alice = Host('Alice')
    bob = Host('Bob')
    network.add_host(alice)
    network.add_host(bob)

    # Add connections between Alice and Bob
    alice.add_connection('Bob')
    bob.add_connection('Alice')

    # Start the hosts
    alice.start()
    bob.start()

    # Alice prepares and sends qubits to Bob
    error_count = 0
    for _ in range(num_qubits):
        # Alice creates a qubit in the |0> state
        qubit = alice.get_qubit('Alice')  # Use the correct method
        if qubit is None:
            print("Failed to create a qubit. Skipping this iteration.")
            continue

        # Introduce errors in the qubit
        qubit = introduce_errors(qubit, error_rate)

        # Alice sends the qubit to Bob
        alice.send_qubit('Bob', qubit)

        # Bob receives the qubit and measures it
        received_qubit = bob.get_qubit('Alice', wait=10)
        if received_qubit is not None:
            measurement = received_qubit.measure()
            if measurement != 0:
                error_count += 1
        else:
            print("Failed to receive a qubit from Alice.")

    # Calculate the error percentage
    error_percentage = (error_count / num_qubits) * 100
    print(f"Error rate: {error_rate}, Error percentage: {error_percentage}%")

    # Stop the network
    network.stop(True)

# Main function to compare different error rates
def main():
    error_rates = [0.01, 0.05, 0.1, 0.2]  # Different error rates to compare
    for rate in error_rates:
        compare_gates(rate)

if __name__ == "__main__":
    main()