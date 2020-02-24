import numpy as np


#%% Importing tables

def tables_import(nL, database, year, country):
    """
    Calling functions dedicated to import indices and downloaded/prepared supply-use tables 
    Inputs:
        nL       - Number of layers (economic + physical layers)
        database - Database selected for the analysis
        year     - Year selected for the analysis
        country  - Country selected for the analysis
    Outputs:
        indices       - Dictionary containing indices for the selected database
        multi_indices - Dictionary containing multi-indices for the selected database
        ML_sut        - Dictionary containing imported multi-layer supply-use tables
    """
    
    from pySUT.tables.tables_import import indicesImport, sutImport
    indices, multi_indices = indicesImport(database,  year, country)
    ML_sut = sutImport(nL, database, year, country, indices)
    
    return(indices, multi_indices, ML_sut)



#%% Reshaping supply-use multilayer tables into IOT-like multilayer framework + check balance

def sut_to_iot(nL, database, year, country, tol, indices_agg, ML_sut_agg):    
    """
    This function converts the prepared supply-use multi-layer tables into an IOT-like framework and checks balance for each layer. 
    Inputs:
        nL          - Number of layers (economic + physical layers)
        database    - Database selected for the analysis
        year        - Year selected for the analysis
        country     - Country selected for the analysis
        tol         - Percentage tollerance to be respected to consider a row/column as balanced
        indices_agg - Dictionary containing aggregated indices
        ML_sut_agg  - Dictionary containing aggregated multi-layer supply-use tables
    Outputs:
        ML_iot_0      - Dictionary containing aggregated IOT-like tables
        x_0           - Multi-layer output vectors
        xT_0          - Multi-layer outlays vectors
        check_0       - nL-d array containing the difference between output and outlays vectors for each layer
        unbalances_0  - List of tuples containing information about (layer, row) positions of potential unbalances 
    """
    
    from pySUT.parsing.sut_to_iot import Z_reshape, W_reshape, M_reshape, R_reshape, Y_reshape, ML_iot_0, calc_x_0, calc_xT_0, balance_check_0
    
    Z_0 = Z_reshape(nL,ML_sut_agg)
    W_0 = W_reshape(nL,ML_sut_agg)
    M_0 = M_reshape(nL,ML_sut_agg)
    R_0 = R_reshape(nL,ML_sut_agg)
    Y_0 = Y_reshape(nL,ML_sut_agg,indices_agg)
    
    ML_iot_0 = ML_iot_0(Z_0, W_0, M_0, Y_0, R_0)
    
    x_0 = calc_x_0(nL,ML_iot_0,indices_agg,database)
    xT_0 = calc_xT_0(nL,ML_iot_0,indices_agg,database)
    
    check_0, unbalances_0 = balance_check_0(nL,x_0,xT_0,tol)

    return(ML_iot_0, x_0, xT_0, check_0, unbalances_0)


#%% Technical coefficients calculation
    
def technical_coefficients(ML_iot_0, x_0):
    """
    This function calculates the technical coefficients for the aggregated IOT-like multi-layer framework.
    N.B.: technical coefficients for the physical layers would be calculated as a function of the economic production vector.
    Inputs:
        ML_iot_0       - Dictionary containing aggregated IOT-like tables
        x_0            - Multi-layer output vectors
    Outputs:
        ML_iot_coeff_0 - Dictionary containing technical coefficients for the IOT-like tables
    """
    
    from pySUT.applications.technical_coefficients import calc_A_0, calc_w_0, calc_m_0, calc_B_0, calc_ML_iot_coeff
        
    Z_0 = ML_iot_0['Z']         # Extracting endogenous transactions matrices
    W_0 = ML_iot_0['W']         # Extracting value added matrices
    M_0 = ML_iot_0['M']         # Extracting imports matrices
    Y_0 = ML_iot_0['Y']         # Extracting imports matrices
    R_0 = ML_iot_0['R']         # Extracting exogenous transactions matrix

    A_0 = calc_A_0(Z_0,x_0)
    w_0 = calc_w_0(W_0,x_0)
    m_0 = calc_m_0(M_0,x_0)
    B_0 = calc_B_0(R_0,x_0)
    
    ML_iot_coeff_0 = calc_ML_iot_coeff(A_0, w_0, m_0, B_0, Y_0)
    
    return(ML_iot_coeff_0)

    
#%% Initial embodied exogenous transactions matrix calculation
    
def calc_E_0(ML_iot_coeff_0,x_0):
    """
    This function calculates the initial embodied exogenous transaction matrix.
    Inputs:
        ML_iot_coeff_0 - Dictionary containing technical coefficients for the IOT-like tables
        x_0            - Multi-layer output vectors
    Outputs:
        E_0            - Initial embodied exogenous transaction matrix
    """
    
    B_0 = ML_iot_coeff_0['B']
    A_0 = ML_iot_coeff_0['A'][0]
    Y_0 = ML_iot_coeff_0['Y'][0]
    Y_tot_0 = np.sum(Y_0,1,keepdims=True)
    
    L_0 = np.linalg.inv(np.eye(A_0.shape[0]) - A_0)
    
    E_0 = (B_0 @ L_0) @ np.diagflat(Y_tot_0)

    return(E_0)


    