import math
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, plot_state_city
import numpy as np
from collections import defaultdict
from qiskit_aer.primitives import SamplerV2
from tqdm import tqdm
from qiskit.quantum_info import random_clifford
from qiskit.circuit.random import random_circuit
from collections import defaultdict
import json
import datetime

SHOTS = 1



def apply_W(qc: QuantumCircuit, qreg, x, y, alpha, beta):
    """
    x_xor_y = np.bitwise_xor(x, y)[0][0]
    alpha_xor_beta = np.bitwise_xor(alpha, beta)[0][0]

    x_bits = format(x_xor_y, f'0{len(qreg)}b')
    a_bits = format(alpha_xor_beta, f'0{len(qreg)}b')

    for i, (xb, ab) in enumerate(zip(x_bits, a_bits)):
        if xb == '1':
            qc.x(qreg[i])
        if ab == '1':
            qc.z(qreg[i])
    
    """

    x_xor_y = np.bitwise_xor(x, y)[0][0]
    alpha_xor_beta = np.bitwise_xor(alpha, beta)[0][0] 

    x_xor_y_bin = np.binary_repr(x_xor_y)
    x_xor_y_bin = (len(qreg)-len(x_xor_y_bin)) * '0' + x_xor_y_bin

    alpha_xor_beta_bin = np.binary_repr(alpha_xor_beta)
    alpha_xor_beta_bin = (len(qreg)-len(alpha_xor_beta_bin)) * '0' + alpha_xor_beta_bin
    

    for i, (a,b) in enumerate(zip(x_xor_y_bin, alpha_xor_beta_bin)):
        if int(a) and int(b):
            qc.sdg(qreg[i])
            qc.h(qreg[i])
        elif int(a):
            qc.h(qreg[i])
        elif int(b):
            qc.z(qreg[i])
    
n = 4


def perform_circuit(C,draw = False):
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

    bell_qc.barrier()
    for j in range(n):
        # bell state first and second copy
        bell_qc.cx(psi1[j], psi2[j])
        bell_qc.h(psi1[j])

        # bell state third and fourth copy
        bell_qc.cx(psi3[j], psi4[j])
        bell_qc.h(psi3[j])

    bell_qc.barrier()
    bell_qc.measure(psi1, cx)
    bell_qc.measure(psi2, calpha)
    bell_qc.measure(psi3, cy)
    bell_qc.measure(psi4, cbeta)

    if draw:
        bell_qc.draw(output="mpl", fold=-1)
        plt.show()

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

    m_qc.barrier()

    apply_W(m_qc, psi5, x,y,alpha, beta)
    apply_W(m_qc, psi6, x,y,alpha, beta)

    m_qc.barrier()
    m_qc.measure(psi5, c_psi_x)
    m_qc.measure(psi6, c_psi_y)

    if draw:
        print(f'x {x}, y {y}, alpha {alpha}, beta {beta}, xy {np.bitwise_xor(x[0][0], y[0][0])}, alphabeta {np.bitwise_xor(alpha[0][0], beta[0][0])}')
        m_qc.draw(output="mpl", fold=-1)
        plt.show()

    # Second measurement
    sampler = SamplerV2(options = dict(backend_options = dict()))
    job = sampler.run([m_qc], shots = SHOTS)
    second_result = job.result()[0]

    x = second_result.data['c_psi_x'].array
    y = second_result.data['c_psi_y'].array

    x_int = int(x[0][0])
    y_int = int(y[0][0])

    x_bits = format(x_int, f'0{n}b')
    y_bits = format(y_int, f'0{n}b')

    # compute parity
    parity = 0
    for b in x_bits + y_bits:
        parity ^= int(b)

    # map to ±1
    return (-1) ** (parity)



def get_random_clifford_circuit(n):
    cliff = random_clifford(n)
    return cliff.to_circuit()

result_dict = defaultdict(list)

ALPHA1 = 0.95
AlPHA2 = 0.5
GAMMA = ALPHA1 ** 6 - (3* AlPHA2 + 1) / 4
DELTA = 0.2 # max failure prob 
m = int((8*math.log(2/DELTA, 2))/GAMMA ** 2)
print(m)
for circuit_type in ['clifford','random']:
    print(circuit_type)
    for _ in range(50):
        result = []
        if circuit_type == 'random':
            C = random_circuit(n,3,measure=False)
            C = C.decompose()
        else:
            C = get_random_clifford_circuit(n)
        for _ in range(m):
            try:
                result.append(perform_circuit(C,draw=False))
            except:
                print("Regenerating random circuit")
                C = random_circuit(n,4)
                C = C.decompose()

        eta = sum(result) /len(result)
        threshold = ALPHA1 ** 6 - GAMMA / 2
        final_outcome = 1 if eta > threshold / 2 else 0
        result_dict[circuit_type].append(eta)
        print(final_outcome)

        result_dict['threshold'].append(threshold)
print(result_dict)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"iteration_results_{timestamp}.json"
with open(filename,"w") as file:
    json.dump(result_dict, file)
#plt.show()