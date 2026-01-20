import sympy as sp
d = 2

def fun(input):
    x1, x2 = input
    return (x1+x2)%2

def calculate_gowers_uk(fun, k=2):
    xh_sum = 0
    for x in range(2**d):
        for h in range(2**k):
            xh_mod = (x+h)%(2**d)
            fun_input = f'{xh_mod:0{d}b}'
            fun_input_tuple = tuple([int(t) for t in fun_input])
            print(fun(fun_input_tuple))

calculate_gowers_uk(fun,2)