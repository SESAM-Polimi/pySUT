import numpy as np


#%% Technical coefficients for the baseline database

"""
This set of functions aims at calculating the technical coefficient matrices for the baseline database
"""

def calc_A_0(Z_0,x_0):   
    """
    This function calculates the technical coefficients matrix 'A_0' starting from the endogneous transaction matrix 'Z_0'
    Inputs:
        Z_0 - Endogneous transactions matrix
        x_0 - Total production vector
    The coefficients for all the layers, both economic and physical ones, 
    will be calculated as a function of the economic production vector 'x_0[0]'
    """
                      
    A_0= Z_0 @ np.linalg.inv(np.diagflat(x_0))

    return(A_0)

        

def calc_B_0(R_0,x_0):
    """
    This function calculates the technical coefficients matrix 'B' starting from the exogenous transaction matrix 'R'
    Inputs:
        R - Exogenous transactions matrix
        x - Total production vector
    The exogenous coefficients will be calculated as a function of the economic production vector 'x[0]'
    """
                
    B_0 = R_0 @ np.linalg.inv(np.diagflat(x_0))

    return(B_0)


#%% Creation of a single dictionary

def calc_ML_iot_coeff(A_0,Y_0):
    """
    This function receives the IOT-like generated matrices as input returning a single dictionary for easier management.
    
    Inputs:
        A_0 - Endogenous transactions coefficient matrices
    Output:
        ML_iot_coeff - Dictionary containing IOT-like generated multi-layer coefficient matrices
    """    
    
    ML_iot_coeff = {
               'A' : A_0,
               # 'B' : B_0,
               'Y' : Y_0,
               }
    
    return(ML_iot_coeff)
    
