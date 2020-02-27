import numpy as np


#%% Aggregation of supply-use tables into IOT-like framework

"""
This set of functions aims at aggregating the sub-matrices of the standard 
supply-use Input-Output framework into a conventional symmetric one.

Reference: Lenzen M., Rueda-Cantuche J.M., "A note on the use of supply-use tables in impact analyses", 
           Statistics and Operations Research Transactions, 2012
"""

def Z_reshape(ML_sut_agg):   
    """
    This function aggregates the Use, Supply and Transaction margins matrices into the IOT-like 'Z' endogenous transaction matrix
    Inputs:
        ML_sut - Dictionary containing imported multi-layer supply-use tables
    """
    
    V_0 = ML_sut_agg['V']         # Extracting supply matrices
    U_0 = ML_sut_agg['U']         # Extracting use matrices
    
    Z_0 = np.zeros((U_0.shape[0]+V_0.shape[0], V_0.shape[1]+U_0.shape[1]))                     # Defining dimensions of Z
                  
    Z_0[0:U_0.shape[0], V_0.shape[1]:V_0.shape[1]+U_0.shape[1]] = U_0                          # Use matrix substitution
    Z_0[U_0.shape[0]:U_0.shape[0]+V_0.shape[0], 0:V_0.shape[1]] = V_0                          # Supply matrix substitution

    return(Z_0)

        

def R_reshape(nL,ML_sut_agg):   
    """
    This function aggregates the exogenous transactions given by products and by industries into the IOT-like 'R' exogenous transactions matrix
    Inputs:
        Rp_0 - Exogenous transactions by products
        Ri_0 - Exogenous transactions by industries
    """

    Rp_0 = ML_sut_agg['Rp']         # Extracting exogenous transactions matrix by products matrices
    Ri_0 = ML_sut_agg['Ri']         # Extracting exogenous transactions matrix by industries matrices
     
    R_0 = np.zeros((Rp_0.shape[0], Rp_0.shape[1]+Ri_0.shape[1]))                                   # Defining dimensions of R
                  
    R_0[:, 0:Rp_0.shape[1]] = Rp_0                                                                 # Exogenous transactions by products matrix substitution
    R_0[:, Rp_0.shape[1]:Rp_0.shape[1]+Ri_0.shape[1]] = Ri_0                                       # Exogenous transactions by industries matrix substitution

    return(R_0)




def Y_reshape(ML_sut_agg,indices_agg):   
    """
    This function extends the "products-sized" final demand matrix 'Yp' into a "products+industries-sized" final demand matrix 'Y'. 
    The additional industry-related rows of final demand are null. This is done for the sake of matrices management simplicity.
    Inputs:
        ML_sut - Dictionary containing imported multi-layer supply-use tables
        indices - Dictionary containing indices for the selected database
    """

    Yp_0 = ML_sut_agg['Yp']             # Extracting final demand by products matrices     
    nP = len(indices_agg['prod'])       # Number of products items
    nI = len(indices_agg['ind'])        # Number of industries items
    nY = len(indices_agg['fd'])         # Number of industries items
    
    Y_0  = np.zeros((nP+nI, nY))                                                                  # Defining dimensions of Y
                  
    Y_0[0:Yp_0.shape[0], 0:Yp_0.shape[1]] = Yp_0                                                  # Final demand by products matrix substitution

    return(Y_0)



#%% Creation of a single dictionary

def ML_iot_0(Z_0,Y_0):
    """
    This function receives the IOT-like generated matrices as input returning a single dictionary for easier management.
    
    Inputs:
        Z_0 - Endogenous transactions matrices
        Y_0 - Final demand matrices
        R_0 - Direct exogenous transactions matrix 
    Output:
        ML_iot - Dictionary containing IOT-like generated multi-layer matrices
    """    
    
    ML_iot_0 = {
               'Z' : Z_0,
               'Y' : Y_0,
               # 'R' : R_0,
               }
    
    return(ML_iot_0)



#%% Production vectors and balance check

def calc_x_0(ML_iot,indices):
    """
    This function calculates the production vector for each layer (economic + physical ones)
    Inputs:
        ML_iot - Dictionary containing IOT-like generated multi-layer matrices
        indices - Dictionary containing indices (used to extract number of products)
    """
    
    Z_0 = ML_iot['Z']                      # Extracting endogenous transaction matrices         
    Y_0 = ML_iot['Y']                      # Extracting final demand matrices
          
    x_0 = np.sum(Z_0,1,keepdims=True) + np.sum(Y_0,1,keepdims=True)

    for i in range(x_0.shape[0]):
        if x_0[i,:] == 0:
            x_0[i,:] = 1            
    
    return(x_0)


def calc_xT_0(ML_iot,indices):
    """
    This function calculates the transposed production vector for each layer (economic + physical ones)
    Inputs:
        ML_iot - Dictionary containing IOT-like generated multi-layer matrices
        indices - Dictionary containing indices (used to extract number of products)
    """

    Z_0 = ML_iot['Z']                      # Extracting endogenous transaction matrices                     
    
    xT_0 = np.sum(Z_0,0,keepdims=True)
        
    for i in range(xT_0.shape[1]):
        if xT_0[:,i] == 0:
            xT_0[:,i] = 1
    
    return(xT_0)


