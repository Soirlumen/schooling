import numpy as np
from scipy.linalg import null_space

A = np.array([[2, 1, 1], [0, 4, 0], [4, -2, 2]])
ns = null_space(A)
ns * np.sign(ns[0, 0])  # Remove the sign ambiguity of the vector
ns.real[abs(ns.real) < 1e-15] = 0
# ns[0]*=(1/ns[0])
# ns[2]=ns[2]*(1/ns[0])


mlem = (1 / ns[0])
for paraf in ns:
    print(paraf * mlem)

# print(ns[2])

##ns.imag[abs(ns.imag)<1e-15]=0
# print(ns)
