#!/bin/python
import numpy as np

def cal_C(value, D, b):
    l, u = D
    return 1 - (1/2)*(np.exp((l-value)/b) + np.exp((value-u)/b))


def boundedlaplacemechanism(value, D: tuple, b, epsilon, delta): 
    '''
    density function of Wq(bounded laplace mechanism)
    D : the support for x(value)
    b : variance -> requires checkup. 
    sensitivity : the minimal difference 
    '''
    if type(D) == None :
        return 0
    # assign boundaries
    l, u  = D

    if (value < l) | (value > u) : return 0
    
    # Theorem 4.4(Fixed Point)
    dQ = abs(u - l)
    
    # calculate Cl, Cl_dQ #Definition3.4
    Cl = cal_C(l, D, b)
    Cl_dQ = cal_C(l + dQ, D, b)
    
    dC = Cl_dQ / Cl
    # print(f'Cl is {Cl} and Cl_dQ is {Cl_dQ}')
    # print(f'dC is {dC}')

    if b < dQ/(epsilon - np.log(dC) - np.log(1 - delta)) :
        # print('the variance does not suffice the preconditions')
        # print('editing b ...')
        b = dQ/(epsilon - np.log(dC) - np.log(1 - delta))
        # print(f"the value of b is {b}")
        # update b

    # Here we do not calculate Cq 
    # Instead we calculate the function and then sum the output calculations
    theRange = np.linspace(l, u, num = 10**4)
    e_term = np.exp(-(abs(theRange - value)/b)) 
    output_calculation  = (1/(2*b))*(e_term)
    
    # sum the output calculation and normalize
    theSum = output_calculation.sum()
    density = output_calculation/theSum 
    
    # the function will output a randomized output!
    randomized_output = np.random.choice(theRange, 1, p=density)

    return randomized_output.item()