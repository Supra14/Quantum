from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Function to apply Hadamard gate to a 16-bit input stream
def apply_hadamard_to_stream(input_stream):
    # Create a quantum circuit with 16 qubits
    qc = QuantumCircuit(16)

    # Encode the input stream into the qubits
    for i in range(16):
        if input_stream[i] == '1':
            qc.x(i)  # Apply X gate to flip the qubit to |1> if the bit is '1'

    # Apply the Hadamard gate to each qubit
    for i in range(16):
        qc.h(i)  # Apply Hadamard gate to the qubit

    # Get the statevector after applying the gates
    state = Statevector.from_instruction(qc)

    # Measure the resulting statevector (simulate a measurement manually)
    probabilities = state.probabilities_dict()

    # Collapse the statevector to one outcome (random sampling based on probabilities)
    measured_state = max(probabilities, key=probabilities.get)  # Most probable outcome

    return measured_state

# Example usage
input_stream = "1101001010111101"  # 16-bit input stream as a string of '0's and '1's
output_stream = apply_hadamard_to_stream(input_stream)

# Display the input and output
print(f"Input Stream: {input_stream}")
print(f"Output Stream: {output_stream}")
