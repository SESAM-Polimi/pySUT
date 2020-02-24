import numpy as np


#%% Shock: matrices variation

"""
This set of functions aims at recalculating the technical coefficient matrices following a perturbation due to a shock
"""

def calc_A_s(A_0,delta_A):   
    """
    This function recalculates the endogenous technical coefficients matrix 'A', 
    following a perturbation 'delta_A' due to a shock
    """
    
    A_s = np.zeros((A_0.shape[0], A_0.shape[1], A_0.shape[2]))
    
    for l in range(A_0.shape[0]):
        A_s[l] = A_0[l] + delta_A[l]
                  
    return(A_s)


def calc_w_s(w_0, delta_w):   
    """
    This function recalculates the value added technical coefficients matrix 'w',
    following a perturbation 'delta_w' due to a shock
    """
    w_s = np.zeros((w_0.shape[0], w_0.shape[1], w_0.shape[2]))

    for l in range(w_0.shape[0]): 
        w_s = w_0 + delta_w
                  
    return(w_s)


def calc_m_s(m_0, delta_m):   
    """
    This function recalculates the imports technical coefficients matrix 'm', 
    following a perturbation 'delta_m' due to a shock
    """
    m_s = np.zeros((m_0.shape[0], m_0.shape[1], m_0.shape[2]))

    for l in range(m_0.shape[0]): 
        m_s = m_0 + delta_m
                  
    return(m_s)


def calc_B_s(B_0,delta_B):
    """
    This function recalculates the exogenous technical coefficients matrix 'B', 
    following a perturbation 'delta_B' due to a shock
    """

    B_s = np.zeros((B_0.shape[0], B_0.shape[1]))
    
    B_s = B_0 + delta_B

    return(B_s)


def calc_Y_s(Y_0,delta_Y):
    """
    This function recalculates the final demand matrix 'Y', 
    following a perturbation 'delta_Y' due to a shock
    """

    Y_s = np.zeros((Y_0.shape[0], Y_0.shape[1], Y_0.shape[2]))

    for l in range(Y_0.shape[0]):                                 
        Y_s = Y_0 + delta_Y

    return(Y_s)



