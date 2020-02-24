import numpy as np


#%% Technical coefficients for the baseline database

"""
This set of functions aims at calculating the technical coefficient matrices for the baseline database
"""

def calc_Z_1(A_s,x_1):   
    """
    This function calculates new endogenous transaction matrices.
    Inputs:
        A_s - Perturbed endogenous coefficients matrices
        x_1 - New output vectors
    Output:
        Z_1 - New endogenous transactions matrices
    """     
    
    Z_1 = np.zeros((A_s.shape[0], A_s.shape[1], A_s.shape[2]))
                  
    for l in range(A_s.shape[0]):
        Z_1[l] = A_s[l] @ np.diagflat(x_1[0])

    return(Z_1)

        
def calc_W_1(w_s,x_1):   
    """
    This function calculates new value added matrices.
    Inputs:
        w_s - Perturbed value added coefficients matrices
        x_1 - New output vectors
    Output:
        W_1 - New value added matrices
    """     
         
    W_1 = np.zeros((w_s.shape[0], w_s.shape[1], w_s.shape[2]))
                  
    for l in range(w_s.shape[0]):
        W_1[l] = w_s[l] @ np.diagflat(x_1[0])

    return(W_1)


def calc_M_1(m_s,x_1):   
    """
    This function calculates new endogenous transaction matrices.
    Inputs:
        m_s - Perturbed import matrices
        x_1 - New output vectors
    Output:
        M_1 - New import matrices
    """     
         
    M_1 = np.zeros((m_s.shape[0], m_s.shape[1], m_s.shape[2]))
                  
    for l in range(m_s.shape[0]):
        M_1[l] = m_s[l] @ np.diagflat(x_1[0])

    return(M_1)


#%% Creation of a single dictionary

def ML_iot_1(Z_1, W_1, M_1, Y_1, R_1,E_1):
    
    ML_iot_1 = {
               'Z' : Z_1,
               'W' : W_1,
               'M' : M_1,
               'Y' : Y_1,
               'R' : R_1,
               'E' : E_1
               }
    
    return(ML_iot_1)
    
