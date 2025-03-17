from qiskit import QuantumCircuit
from qiskit import Aer, transpile
from qiskit.providers.aer import AerSimulator
from qiskit import execute

# Create a quantum circuit with 2 qubits
qc = QuantumCircuit(2)

# Apply Hadamard gate to the first qubit
qc.h(0)

# Apply CNOT gate with control qubit 0 and target qubit 1
qc.cx(0, 1)

# Visualize the quantum circuit
print(qc.draw())

# Use AerSimulator instead of Aer.get_backend('statevector_simulator')
simulator = AerSimulator()

# Transpile the circuit for the simulator
qc = transpile(qc, simulator)

# Simulate the circuit
result = simulator.run(qc).result()
statevector = result.get_statevector()

# Display the result
print(statevector)
