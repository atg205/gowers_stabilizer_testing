import numpy as np
import itertools
import math

###### Gowers norm for complex boolean function F_2 -> C ######
class Gowers:
    """
    Calculate Gower's norm for complex valued functions
    """
    def __init__(self,d:int,k:int, fun: list) -> None:
        """
        
        :param d: Dimension of input vector x
        :param k: Grower_k norm
        """
        self.d = d
        self.k = k

    def fun(self,input):
        x1, x2, x3, x4 = input
        return ((x1 + x2 + x3 + x1*x2*x3) % 2) * 2 - 1

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
        total_terms = 2**(d*(k+1))
        return xh_sum / total_terms


