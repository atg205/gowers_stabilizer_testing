import sympy as sp
d = 3

def fun(input):
    x1, x2,x3 = input
    return ((x1+x2+x3+x1*x3*x2)%2)*2-1

def calculate_gowers_uk(fun, k=2):
    xh_sum = 0
    for x in range(2**d):
        xb = f'{x:0{d}b}'
        for h1 in range(2**k):
            h1b = f'{h1:0{d}b}'

            for h2 in range(2**k):
                h2b = f'{h2:0{d}b}'

                xh1 = tuple(int(xi) ^ int(hi) for xi, hi in zip(xb, h1b))
                xh2 = tuple(int(xi) ^ int(hi) for xi, hi in zip(xb, h2b))
                xh1h2 = tuple(xi ^ int(hi) for xi, hi in zip(xh1, h2b))
                xb_tuple = tuple([int(i) for i in xb])
                xh_sum += fun(xb_tuple) * fun(xh1) * fun(xh2) * fun(xh1h2)

    return xh_sum / (2**k * 2**d * 2**k)
 

print(calculate_gowers_uk(fun,2))
