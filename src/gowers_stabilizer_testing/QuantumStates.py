from qiskit.quantum_info import random_clifford
import matplotlib.pyplot as plt

class QuantumStates:
    def __init__(self, dim=2) -> None:
        self.dim = dim

    def get_stabilizer_state(self):
        pass


cliff = random_clifford(3)
qc = cliff.to_circuit()
qc.draw(output="mpl", fold=-1)
plt.show()
