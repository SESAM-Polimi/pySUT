"""
pySUT - A Python module for automating supply-use io calculations 
=================================================================

Authors: L.Rinaldi, G.Guidicini, N.Golinucci, M.A.Tahavori, M.V.Rocco
         Department of Energy - Politecnico di Milano
"""


def analysis_application(nL, analysis, ML_iot_coeff_0, indices_agg, multi_indices):
    """
    This function represents the actual core of the model, performing the desired type of analysis.
    Inputs:
        nL             - Number of layers (economic + physical layers)
        analysis       - Desired type of analysis
        ML_iot_coeff_0 - Dictionary containing technical coefficients for the IOT-like tables
        indices_agg    - Dictionary containing aggregated indices
        multi_indices  - Dictionary containing multi-indices for the selected database
    Output:
        ML_iot_1       - Dictionary containing perturbed IOT-like tables
        x_1            - Perturbed output vectors       
    """
    
    if analysis == 'SA':
        
        print('\n\nSHOCK ANALYSIS\n')
        
        """
        SHOCK ANALYSIS 
        The user will be required to input perturbed technical coefficients/final demand matrices. 
        The Leontief Production, Impact and Price Models are then applied.
        """
        
        from pySUT.applications.shock_analysis.perturbations import SA_delta_dict
        from pySUT.applications.shock_analysis.shocked_matrices import calc_A_s, calc_w_s, calc_m_s, calc_B_s, calc_Y_s
        from pySUT.applications.shock_analysis.leontief_models import calc_L_1, calc_Y_tot_1, calc_x_1, calc_R_1, calc_E_1
        from pySUT.applications.tables_recalc import calc_Z_1, calc_W_1, calc_M_1, ML_iot_1
        
        ML_delta_coeff = SA_delta_dict(nL, indices_agg)
        
        A_0 = ML_iot_coeff_0['A']                # Extracting initial endogenous coefficients matrices
        w_0 = ML_iot_coeff_0['w']                # Extracting initial value added coefficients matrices
        m_0 = ML_iot_coeff_0['m']                # Extracting initial imports coefficients matrices
        B_0 = ML_iot_coeff_0['B']                # Extracting initial exogenous coefficients matrix
        Y_0 = ML_iot_coeff_0['Y']                # Extracting initial final demand matrices
        
        delta_A = ML_delta_coeff['delta_A']      # Extracting perturbations on endogenous coefficients matrices
        delta_w = ML_delta_coeff['delta_w']      # Extracting perturbations on value added coefficients matrices
        delta_m = ML_delta_coeff['delta_m']      # Extracting perturbations on imports coefficients matrices
        delta_B = ML_delta_coeff['delta_B']      # Extracting perturbations on exogenous coefficients matrix
        delta_Y = ML_delta_coeff['delta_Y']      # Extracting perturbations on final demand matrices
        
        A_1 = calc_A_s(A_0, delta_A)           # Calculating perturbed endogenous coefficients matrices
        w_1 = calc_w_s(w_0, delta_w)           # Calculating perturbed value added coefficients matrices
        m_1 = calc_m_s(m_0, delta_m)           # Calculating perturbed imports coefficients matrices
        B_1 = calc_B_s(B_0, delta_B)           # Calculating perturbed exogenous coefficients matrix
        Y_1 = calc_Y_s(Y_0, delta_Y)           # Calculating perturbed final demand matrices    
        
        
        # Application of Leontief Models
        
        # Leontief Production Model
        L = calc_L_1(A_1)                          # Leontief Inverse Matrix
        Y_tot_1 = calc_Y_tot_1(Y_1)              # Calculating the total final demand vector
        x_1 = calc_x_1(L,Y_tot_1)                # Calculating the new level of production required
        
        # Leontief Impact Model
        R_1 = calc_R_1(B_1,L,Y_tot_1)            # Calculating the direct exogenous transactions matrix
        E_1 = calc_E_1(B_1,L,Y_tot_1)            # Calculating the embodied exogenous transactions matrix
        
        # Leontief Price Model
        
        
    # Calculation of new absolute values matrices
    Z_1 = calc_Z_1(A_1,x_1)                    # Calculating new endogenous transaction matrices
    W_1 = calc_W_1(w_1,x_1)                    # Calculating new value added matrices
    M_1 = calc_M_1(m_1,x_1)                    # Calculating new imports matrices
    
    ML_iot_1 = ML_iot_1(Z_1,W_1,M_1,Y_1,R_1,E_1)
    
    return(ML_iot_1,x_1)