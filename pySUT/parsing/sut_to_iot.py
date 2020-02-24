import numpy as np


#%% Aggregation of supply-use tables into IOT-like framework

"""
This set of functions aims at aggregating the sub-matrices of the standard 
supply-use Input-Output framework into a conventional symmetric one.

Reference: Lenzen M., Rueda-Cantuche J.M., "A note on the use of supply-use tables in impact analyses", 
           Statistics and Operations Research Transactions, 2012
"""

def Z_reshape(nL,ML_sut_agg):   
    """
    This function aggregates the Use, Supply and Transaction margins matrices into the IOT-like 'Z' endogenous transaction matrix
    Inputs:
        nL - Number of layers (economic + physical layers)
        ML_sut - Dictionary containing imported multi-layer supply-use tables
    """
    
    V_0 = ML_sut_agg['V']         # Extracting supply matrices
    U_0 = ML_sut_agg['U']         # Extracting use matrices
    TRC_0 = ML_sut_agg['TRC']     # Extracting transaction margin matrices
    
    Z_0 = np.zeros((nL, U_0.shape[1]+V_0.shape[1], V_0.shape[2]+U_0.shape[2]))                         # Defining dimensions of Z
                  
    for l in range(nL):
        Z_0[l, 0:U_0.shape[1], 0:V_0.shape[2]] = TRC_0[l]                                             # TRC matrix substitution
        Z_0[l, 0:U_0.shape[1], V_0.shape[2]:V_0.shape[2]+U_0.shape[2]] = U_0[l]                       # Use matrix substitution
        Z_0[l, U_0.shape[1]:U_0.shape[1]+V_0.shape[1], 0:V_0.shape[2]] = V_0[l]                       # Supply matrix substitution

    return(Z_0)

        
def W_reshape(nL,ML_sut_agg):   
    """
    This function aggregates the value added given by products and by industries into the IOT-like 'W' value added matrix
    Inputs:
        nL - Number of layers (economic + physical layers)
        ML_sut - Dictionary containing imported multi-layer supply-use tables
    """
    
    Wp_0 = ML_sut_agg['Wp']         # Extracting value added by products matrices
    Wi_0 = ML_sut_agg['Wi']         # Extracting value added by industries matrices
 
    W_0 = np.zeros((nL, Wp_0.shape[1], Wp_0.shape[2]+Wi_0.shape[2]))                                   # Defining dimensions of W
                  
    for l in range(nL):
        W_0[l, :, 0:Wp_0.shape[2]] = Wp_0[l]                                                          # Value added by products matrix substitution
        W_0[l, :, Wp_0.shape[2]:Wp_0.shape[2]+Wi_0.shape[2]] = Wi_0[l]                                # Value added by industries matrix substitution

    return(W_0)


def M_reshape(nL,ML_sut_agg):   
    """
    This function aggregates the imports given by products and by industries into the IOT-like 'M' imports matrix
    Inputs:
        nL - Number of layers (economic + physical layers)
        ML_sut - Dictionary containing imported multi-layer supply-use tables
    """

    Mp_0 = ML_sut_agg['Mp']         # Extracting imports by products matrices
    Mi_0 = ML_sut_agg['Mi']         # Extracting imports by industries matrices
     
    M_0 = np.zeros((nL, Mp_0.shape[1], Mp_0.shape[2]+Mi_0.shape[2]))                                   # Defining dimensions of M
                  
    for l in range(nL):
        M_0[l, :, 0:Mp_0.shape[2]] = Mp_0[l]                                                          # Imports by products matrix substitution
        M_0[l, :, Mp_0.shape[2]:Mp_0.shape[2]+Mi_0.shape[2]] = Mi_0[l]                                # Imports by industries matrix substitution

    return(M_0)


def R_reshape(nL,ML_sut_agg):   
    """
    This function aggregates the exogenous transactions given by products and by industries into the IOT-like 'R' exogenous transactions matrix
    Inputs:
        L - Number of layers (economic + physical layers)
        Rp_0 - Exogenous transactions by products
        Ri_0 - Exogenous transactions by industries
    """

    Rp_0 = ML_sut_agg['Rp']         # Extracting exogenous transactions matrix by products matrices
    Ri_0 = ML_sut_agg['Ri']         # Extracting exogenous transactions matrix by industries matrices
     
    R_0 = np.zeros((Rp_0.shape[0], Rp_0.shape[1]+Ri_0.shape[1]))                                   # Defining dimensions of R
                  
    R_0[:, 0:Rp_0.shape[1]] = Rp_0                                                                 # Exogenous transactions by products matrix substitution
    R_0[:, Rp_0.shape[1]:Rp_0.shape[1]+Ri_0.shape[1]] = Ri_0                                       # Exogenous transactions by industries matrix substitution

    return(R_0)




def Y_reshape(nL,ML_sut_agg,indices_agg):   
    """
    This function extends the "products-sized" final demand matrix 'Yp' into a "products+industries-sized" final demand matrix 'Y'. 
    The additional industry-related rows of final demand are null. This is done for the sake of matrices management simplicity.
    Inputs:
        L - Number of layers (economic + physical layers)
        ML_sut - Dictionary containing imported multi-layer supply-use tables
        indices - Dictionary containing indices for the selected database
    """

    Yp_0 = ML_sut_agg['Yp']             # Extracting final demand by products matrices     
    nP = len(indices_agg['prod'])       # Number of products items
    nI = len(indices_agg['ind'])        # Number of industries items
    nY = len(indices_agg['fd'])         # Number of industries items
    
    Y_0  = np.zeros((nL, nP+nI, nY))                                                                  # Defining dimensions of Y
                  
    for l in range(nL):
        Y_0[l, 0:Yp_0.shape[1], 0:Yp_0.shape[2]] = Yp_0[l]                                                          # Final demand by products matrix substitution

    return(Y_0)



#%% Creation of a single dictionary

def ML_iot_0(Z_0, W_0, M_0, Y_0, R_0):
    """
    This function receives the IOT-like generated matrices as input returning a single dictionary for easier management.
    
    Inputs:
        Z_0 - Endogenous transactions matrices
        W_0 - Value added matrices
        M_0 - Import matrices
        Y_0 - Final demand matrices
        R_0 - Direct exogenous transactions matrix 
        E_0 - Embodied exogenous transactions matrix
    Output:
        ML_iot - Dictionary containing IOT-like generated multi-layer matrices
    """    
    
    ML_iot_0 = {
               'Z' : Z_0,
               'W' : W_0,
               'M' : M_0,
               'Y' : Y_0,
               'R' : R_0,
               }
    
    return(ML_iot_0)



#%% Production vectors and balance check

def calc_x_0(nL,ML_iot,indices,database):
    """
    This function calculates the production vector for each layer (economic + physical ones)
    Inputs:
        nL - Number of layers (economic + physical layers)
        ML_iot - Dictionary containing IOT-like generated multi-layer matrices
        indices - Dictionary containing indices (used to extract number of products)
        database - Selected database for the analysis
    """
    
    nP = len(indices['prod'][0])           # Number of products items
    Z_0 = ML_iot['Z']                      # Extracting endogenous transaction matrices         
    Y_0 = ML_iot['Y']                      # Extracting final demand matrices
         
    x_0 = np.zeros((nL,Z_0.shape[1],1))
    
    for l in range(nL):
        if l==0 or database=='Eurostat':
            x_0[l] = np.sum(Z_0[l],1,keepdims=True) + np.sum(Y_0[l],1,keepdims=True)
        elif l!=0 and database!='Eurostat':
            x_0[l,0:nP,:] = np.sum(Z_0[l,0:nP,:],1,keepdims=True) + np.sum(Y_0[l,0:nP,:],1,keepdims=True)

    for l in range(nL):
        for i in range(x_0.shape[1]):
            if x_0[l,i,:] == 0:
                x_0[l,i,:] = 1            
    return(x_0)


def calc_xT_0(nL,ML_iot,indices,database):
    """
    This function calculates the transposed production vector for each layer (economic + physical ones)
    Inputs:
        nL - Number of layers (economic + physical layers)
        ML_iot - Dictionary containing IOT-like generated multi-layer matrices
        indices - Dictionary containing indices (used to extract number of products)
        database - Selected database for the analysis
    """

    nP = len(indices['prod'][0])           # Number of products items    
    Z_0 = ML_iot['Z']                      # Extracting endogenous transaction matrices         
    W_0 = ML_iot['W']                      # Extracting endogenous transaction matrices         
    M_0 = ML_iot['M']                      # Extracting endogenous transaction matrices 
             
    xT_0 = np.zeros((nL,1,Z_0.shape[2]))
    
    for l in range(nL):
        if l==0 or database=='Eurostat':
            xT_0[l] = np.sum(Z_0[l],0,keepdims=True) + np.sum(W_0[l],0,keepdims=True) + np.sum(M_0[l],0,keepdims=True)
        elif l!=0 and database!='Eurostat':
            xT_0[l,:,0:nP] = np.sum(Z_0[l,:,0:nP],0,keepdims=True) + np.sum(W_0[l,:,0:nP],0,keepdims=True) + np.sum(M_0[l,:,0:nP],0,keepdims=True)
        
    for l in range(nL):
        for i in range(xT_0.shape[2]):
            if xT_0[l,:,i] == 0:
                xT_0[l,:,i] = 1
    
    return(xT_0)


def balance_check_0(nL,x_0,xT_0,tol):
    """
    This function checks if row sum and column sum for each layer are balanced 
    according to a given tollerance value (expressed as a percentage)
    """

    check_0 = np.zeros((nL,x_0.shape[1],1))
    unbalances_0 = []     # Initialising an empty list which will be populated with information about unbalanced products/industries for each layer
    
    for l in range(nL):
        for i in range(x_0.shape[1]):
            check_0[l,i,:] = abs(x_0[l,i,:] - xT_0[l,:,i])
            
            if check_0[l,i,0]/x_0[l,i,0] > tol:
                unbalances_0 += [(l,i)]   # Information about layers and products/sectors are registered as a list of tuples
    
    return(check_0, unbalances_0)


    