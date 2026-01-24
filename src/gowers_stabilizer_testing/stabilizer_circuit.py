from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, plot_state_city
import numpy as np
from collections import defaultdict




def apply_W(qc, qreg, c_x, c_alpha):
    for j in range(len(qreg)):
        with qc.if_test((c_x[j], 1)):
            qc.x(qreg[j])
        with qc.if_test((c_alpha[j], 1)):
            qc.z(qreg[j])



n = 4

psi = QuantumRegister(n, 'psi')
psi_star = QuantumRegister(n, 'psi_star')

psi_copy1 = QuantumRegister(n, 'psi1')
psi_copy2 = QuantumRegister(n, 'psi2')

c_x = ClassicalRegister(n, 'x')
c_alpha = ClassicalRegister(n, 'alpha')

c_psi_x = ClassicalRegister(n, 'psi_x')
c_psi_y = ClassicalRegister(n, 'psi_y')

qc = QuantumCircuit(
    psi, psi_star,
    psi_copy1, psi_copy2,
    c_x, c_alpha,
    c_psi_x, c_psi_y
)

for j in range(n):
    qc.cx(psi[j], psi_star[j])
    qc.h(psi[j])

qc.measure(psi, c_x)
qc.measure(psi_star, c_alpha)


apply_W(qc, psi_copy1, c_x, c_alpha)
apply_W(qc, psi_copy2, c_x, c_alpha)

qc.measure(psi_copy1, c_psi_x)
qc.measure(psi_copy2, c_psi_y)

# Use Aer's qasm_simulator
simulator = AerSimulator() 
# Execute the circuit on the qasm
# simulator
 
# Grab results from the job
result = simulator.run(qc).result() 
# Return counts
counts = result.get_counts(qc)

expectation_value = 0
for bitstring, count in counts.items():
    x = np.array([int(b) for b in bitstring[0:n]], dtype=int)
    y = np.array([int(b) for b in bitstring[n+1:2*n+1]], dtype=int)
    z = np.bitwise_xor(x,y)
    z_int = z.dot(2**np.arange(z.size)[::-1]) 
    expectation_value += ((-1) ** z_int) * count
    
print(expectation_value)
plot_histogram(counts, title='Counts')

qc.draw(output="mpl", fold=-1)
plt.show()