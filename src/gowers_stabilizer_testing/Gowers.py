import numpy as np
import itertools
import math

###### Gowers norm for complex boolean function F_2 -> C ######
class Gowers:
    """
    Calculate Gower's norm for complex valued functions
    """
    def __init__(self, amplitudes: list, k:int =3, prefactor = True) -> None:
        """
        
        :param d: Dimension of input vector x
        :param k: Grower_k norm
        """
        self.d = int(math.log2(len(amplitudes)))
        self.k = k
        self.amplitudes = amplitudes
        self.prefactor = 2**(self.d*2**(self.k-1)) if prefactor else 1

    def fun(self,input):
        if len(self.amplitudes)== 0:
            x1, x2 = input
            return ((x1 + x2 + x1*x2) % 2) * 2 - 1
        else:
            return self.amplitudes[self.bin_to_int(input)]

    def calculate_gowers_uk(self):
        xh_sum = 0
        all_x = list(itertools.product([0,1], repeat=self.d))
        all_h = list(itertools.product([0,1], repeat=self.d))

        for x in all_x:
            for h_tuple in itertools.product(all_h, repeat=self.k):
                product = 1
                for omega in itertools.product([0,1], repeat=self.k):
                    y = np.array(x)
                    for i, w in enumerate(omega):
                        if w == 1:
                            y = np.bitwise_xor(y, h_tuple[i])
                    val = self.fun(tuple(y))
                    if sum(omega) % 2 == 1:
                        val = np.conjugate(val)
                    product *= val
                xh_sum += product

        # normalize
        total_terms = 2**(self.d*(self.k+1))
        return self.prefactor * xh_sum / total_terms
    
    def bin_to_int(self, arr):
        result = 0
        for i in range(len(arr)):
            result += arr[::-1][i]*2**i
        return result

#g = Gowers(2,3, amplitudes=[math.sqrt(1/3),0,0,math.sqrt(2/3)])
#print(g.calculate_gowers_uk())