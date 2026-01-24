from Gowers import Gowers
import qutip as qp
import numpy as np

cliffords = list(qp.gates.qubit_clifford_group())
state = qp.tensor(qp.fock(2), qp.fock(2))   # |00⟩

cliff_gates = np.random.randint(0, len(cliffords),10)
for gate in cliff_gates:
    state = qp.tensor(cliffords[gate],qp.identity(2)) * state


cliff_gates = np.random.randint(0, len(cliffords),10)
for gate in cliff_gates:
    state = qp.tensor(qp.identity(2),cliffords[gate]) * state
#state = qp.bell_state()
state = qp.tensor(qp.gates.t_gate(), qp.identity(2)) * state

#state = qp.gates.t_gate() * state

gn = Gowers(amplitudes=list(state)).calculate_gowers_uk()
print(gn)