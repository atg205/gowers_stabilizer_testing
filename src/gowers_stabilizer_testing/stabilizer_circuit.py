from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, plot_state_city
import numpy as np
from collections import defaultdict
from qiskit_aer.primitives import SamplerV2

from qiskit.quantum_info import random_clifford

SHOTS = 1



def apply_W(qc: QuantumCircuit, qreg, x, y, alpha, beta):
    x_xor_y = np.bitwise_xor(x, y)[0][0]
    alpha_xor_beta = np.bitwise_xor(alpha, beta)[0][0] 

    x_xor_y_bin = np.binary_repr(x_xor_y)
    x_xor_y_bin = (len(qreg)-len(x_xor_y_bin)) * '0' + x_xor_y_bin

    alpha_xor_beta_bin = np.binary_repr(alpha_xor_beta)
    alpha_xor_beta_bin = (len(qreg)-len(alpha_xor_beta_bin)) * '0' + alpha_xor_beta_bin

    for i, (a,b) in enumerate(zip(x_xor_y_bin[::-1], alpha_xor_beta_bin[::-1])):
        if int(a) and int(b):
            qc.sdg(qreg[i])
            qc.h(qreg[i])
        elif int(a):
            qc.h(qreg[i])
        elif int(b):
            qc.z(qreg[i])
    
n = 4


def perform_circuit(C):
    psi1 = QuantumRegister(n, 'psi1')

    psi2 = QuantumRegister(n, 'psi2')
    psi3 = QuantumRegister(n, 'psi3')
    psi4 = QuantumRegister(n, 'psi4')


    cx = ClassicalRegister(n, 'cx')
    calpha = ClassicalRegister(n, 'calpha')
    cy = ClassicalRegister(n, 'cy')
    cbeta = ClassicalRegister(n, 'cbeta')

    bell_qc = QuantumCircuit(
        psi1, psi2, psi3, psi4,
        cx,calpha,cy,cbeta,
    )



    bell_qc.compose(C, qubits=psi1, inplace=True)
    bell_qc.compose(C, qubits=psi2, inplace=True)
    bell_qc.compose(C, qubits=psi3, inplace=True)
    bell_qc.compose(C, qubits=psi4, inplace=True)


    for j in range(n):
        # bell state first and second copy
        bell_qc.cx(psi1[j], psi2[j])
        bell_qc.h(psi1[j])

        # bell state third and fourth copy
        bell_qc.cx(psi3[j], psi4[j])
        bell_qc.h(psi3[j])


    bell_qc.measure(psi1, cx)
    bell_qc.measure(psi2, calpha)
    bell_qc.measure(psi3, cy)
    bell_qc.measure(psi4, cbeta)

    # First measurement
    sampler = SamplerV2(options = dict(backend_options = dict()))
    job = sampler.run([bell_qc], shots = SHOTS)
    first_result = job.result()[0]

    x = first_result.data['cx'].array
    alpha = first_result.data['calpha'].array
    y = first_result.data['cy'].array
    beta = first_result.data['cbeta'].array

    ###     Actual measurement circuit      ###
    psi5 = QuantumRegister(n, 'psi5')
    psi6 = QuantumRegister(n, 'psi6')

    c_psi_x = ClassicalRegister(n, 'c_psi_x')
    c_psi_y = ClassicalRegister(n, 'c_psi_y')

    m_qc = QuantumCircuit(
        psi5, psi6, c_psi_x, c_psi_y
    )

    m_qc.compose(C, qubits=psi5, inplace=True)
    m_qc.compose(C, qubits=psi6, inplace=True)

    apply_W(m_qc, psi5, x,y,alpha, beta)
    apply_W(m_qc, psi6, x,y,alpha, beta)


    m_qc.measure(psi5, c_psi_x)
    m_qc.measure(psi6, c_psi_y)



    # Second measurement
    sampler = SamplerV2(options = dict(backend_options = dict()))
    job = sampler.run([m_qc], shots = SHOTS)
    second_result = job.result()[0]

    x = second_result.data['c_psi_x'].array
    y = second_result.data['c_psi_y'].array
    z = np.bitwise_xor(x,y)
    expectation_value = sum([(-1) ** (1-int(z_item[0])) for z_item in z])

    print(expectation_value)
    return expectation_value

cliff = random_clifford(n,seed=42)
C = cliff.to_circuit()

result = []
for i in range(50):
    result.append(perform_circuit(C))

print(sum(result) / len(result))
#m_qc.draw(output="mpl", fold=-1)
#plt.show()