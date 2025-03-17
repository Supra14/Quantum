from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import time

def quantum_gate_example():
    # Initialize a network and start it
    network = Network.get_instance()
    network.start()

    # Create two hosts (nodes) for quantum communication
    host_A = Host('A')
    host_B = Host('B')

    # Add the hosts to the network
    host_A.add_connection('B')
    host_B.add_connection('A')

    # Add the hosts to the network (important step)
    network.add_host(host_A)
    network.add_host(host_B)

    # Start the hosts
    host_A.start()
    host_B.start()

    # Allow some time for the network to stabilize
    time.sleep(1)

    # Create a qubit on host A
    qubit_A = Qubit(host_A)

    # Apply a Hadamard gate to the qubit
    qubit_A.H()
    print("Applied Hadamard Gate to Qubit at Host A")

    # Send the qubit from Host A to Host B
    host_A.send_qubit('B', qubit_A, await_ack=True)

    # Host B receives the qubit
    qubit_B = host_B.get_data_qubit('A')

    # Apply a Pauli-X (NOT) gate to the received qubit
    qubit_B.X()
    print("Applied X Gate to Qubit at Host B")

    # Measure the qubit and print the result
    measurement = qubit_B.measure()
    print(f"Measurement result at Host B: {measurement}")

    # Stop the network
    time.sleep(2)
    network.stop(True)

# Main program execution
if __name__ == '__main__':
    quantum_gate_example()
