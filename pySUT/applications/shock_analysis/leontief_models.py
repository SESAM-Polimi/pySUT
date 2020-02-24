import numpy as np


#%% Leontief Production Model
"""
This set of functions apply the Leontief Production Model on the set database
"""


def calc_L_1(A_s):
    """
    This function returns the Leontief Inverse Matrix.
    Input:
       A_s - Shocked endogenous technical coefficients matrix
    """
    
    L_1 = np.zeros((A_s.shape[0],A_s.shape[1],A_s.shape[2]))

    for l in range(A_s.shape[0]):
        L_1[l] = np.linalg.inv(np.eye(A_s.shape[1]) - A_s[l])

    return(L_1)


def calc_Y_tot_1(Y_s):
    """
    This function returns the total final demand vector performinf the column sum of the final demand matrix.
    Input:
       Y_s - Shocked final demand matrix
    """
    
    Y_tot_1 = np.zeros((Y_s.shape[0],Y_s.shape[1],1))    

    for l in range(Y_s.shape[0]):
        Y_tot_1[l] = np.sum(Y_s[l],1,keepdims=True)
    
    return(Y_tot_1)


def calc_x_1(L_1,Y_tot_1):
    """
    This function returns the new production vector following a perturbation due to a shock.
    Inputs:
       L - Leontief Inverse Matrix
       Y_tot - Total final demand vector
    """
    
    x_1   = np.zeros((L_1.shape[0],L_1.shape[1],1))    

    for l in range(L_1.shape[0]):
        x_1[l] = L_1[l] @ Y_tot_1[l]
    
    return(x_1)
    


#%% Leontief Impact Model
"""
This set of functions apply the Leontief Impact Model on the set database
"""


def calc_R_1(B_s, L_1, Y_tot_1):
    """
    Production-based approach (PBA).
    This function returns the direct exogenous transactions matrix 'R_1'
    Inputs:
        B_s - Shocked exogenous techical coefficient matrix
        L - Leontief Inverse Matrix
        Y_tot - Total final demand vector
    """
    
    R_1 = B_s @ np.diagflat(L_1[0] @ Y_tot_1[0])
        
    return(R_1)
        

def calc_E_1(B_s, L_1, Y_tot):
    """
    Consumption-based approach (CBA).
    This function returns the embodied exogenous transactions matrix 'E_1'
    Inputs:
        B_s - Shocked exogenous techical coefficient matrix
        L - Leontief Inverse Matrix
        Y_tot - Total final demand vector
    """
    
    E_1 = (B_s @ L_1[0]) @ np.diagflat(Y_tot[0])
        
    return(E_1)
    

#%% Leontief Price Model

        