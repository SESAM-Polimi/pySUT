"""
pySUT - A Python module for automating supply-use io calculations 
=================================================================

Authors: L.Rinaldi, G.Guidicini, N.Golinucci, M.A.Tahavori, M.V.Rocco
         Department of Energy - Politecnico di Milano
"""

import numpy as np
import pandas as pd



#%% Calculation of variations

def dict_delta_1_0(ML_iot_0,ML_iot_1,x_0,x_1,E_0):
    """
    This function calculates the variations from the initial to the after-perturbation situation in order to evaluate impacts.
    This information are stored into a dictionary.
    Inputs:
        ML_iot_0  - Dictionary containing initial IOT-like tables
        ML_iot_1  - Dictionary containing perturbed IOT-like tables
        x_0       - Multi-layer initial output vectors
        x_1       - Perturbed output vectors       
        E_0       - Initial embodied exogenous transaction matrix
    Outputs:
        delta_1_0 - Dictionary containing variations from the initial to the after-perturbation situation
    """

    Z_0 = ML_iot_0['Z']
    Z_1 = ML_iot_1['Z']

    W_0 = ML_iot_0['W']
    W_1 = ML_iot_1['W']

    M_0 = ML_iot_0['M']
    M_1 = ML_iot_1['M']

    Y_0 = ML_iot_0['Y']
    Y_1 = ML_iot_1['Y']

    R_0 = ML_iot_0['R']
    R_1 = ML_iot_1['R']

    E_1 = ML_iot_1['E']
    
    delta_Z = np.zeros((Z_0.shape[0], Z_0.shape[1], Z_0.shape[2]))
    delta_W = np.zeros((W_0.shape[0], W_0.shape[1], W_0.shape[2]))
    delta_M = np.zeros((M_0.shape[0], M_0.shape[1], M_0.shape[2]))
    delta_Y = np.zeros((Y_0.shape[0], Y_0.shape[1], Y_0.shape[2]))
    delta_x = np.zeros((x_0.shape[0], x_0.shape[1], x_0.shape[2]))
    
    for l in range(Z_0.shape[0]):
        delta_Z[l] = Z_1[l] - Z_0[l]
        delta_W[l] = W_1[l] - W_0[l]
        delta_M[l] = M_1[l] - M_0[l]
        delta_Y[l] = Y_1[l] - Y_0[l]
        delta_x[l] = x_1[l] - x_0[l]
    
    delta_R = R_1 - R_0
    delta_E = E_1 - E_0
   
    delta_1_0 = {
                 'delta_Z': delta_Z,
                 'delta_W': delta_W,
                 'delta_M': delta_M,
                 'delta_Y': delta_Y,
                 'delta_x': delta_x,
                 'delta_R': delta_R,   
                 'delta_E': delta_E,
                }
    
    return(delta_1_0)


#%% Export in excel file
    
def xlsx_export(nL, ML_iot_0, ML_iot_1, x_0, x_1, E_0, indices_agg, database, country, year):
    """
    This function exports the new variations calculated in the 'dict_delta_1_0' functions into xlsx files.
    """
        
    delta_1_0 = dict_delta_1_0(ML_iot_0,ML_iot_1,x_0,x_1,E_0)

    for l in range(nL):
        if l == 0:
            output_economic = pd.ExcelWriter('pySUT/output/'+str(database)+'/'+str(country)+'/'+str(year)+'/output_economic.xlsx', engine='xlsxwriter') 
            pd.DataFrame(delta_1_0['delta_Z'][l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_economic,'delta_A')
            pd.DataFrame(delta_1_0['delta_W'][l], index=indices_agg['vadd'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_economic,'delta_W')
            pd.DataFrame(delta_1_0['delta_M'][l], index=indices_agg['imp'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_economic,'delta_M')
            pd.DataFrame(delta_1_0['delta_Y'][l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['fd']).to_excel(output_economic,'delta_Y')
            pd.DataFrame(delta_1_0['delta_x'][l], index=indices_agg['prod']+indices_agg['ind']).to_excel(output_economic,'delta_x')
            output_economic.save()
        else:
            output_physical = pd.ExcelWriter('pySUT/output/'+str(database)+'/'+str(country)+'/'+str(year)+'/output_physical_'+str(l)+'.xlsx', engine='xlsxwriter') 
            pd.DataFrame(delta_1_0['delta_Z'][l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_physical,'delta_A')
            pd.DataFrame(delta_1_0['delta_W'][l], index=indices_agg['vadd'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_physical,'delta_W')
            pd.DataFrame(delta_1_0['delta_M'][l], index=indices_agg['imp'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_physical,'delta_M')
            pd.DataFrame(delta_1_0['delta_Y'][l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['fd']).to_excel(output_physical,'delta_Y')
            pd.DataFrame(delta_1_0['delta_x'][l], index=indices_agg['prod']+indices_agg['ind']).to_excel(output_physical,'delta_x')
            output_physical.save()

    output_satellite = pd.ExcelWriter('pySUT/output/'+str(database)+'/'+str(country)+'/'+str(year)+'/output_satellite.xlsx', engine='xlsxwriter') 
    pd.DataFrame(delta_1_0['delta_R'][0], index=indices_agg['exog'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_satellite,'delta_R')
    pd.DataFrame(delta_1_0['delta_E'][0], index=indices_agg['exog'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(output_satellite,'delta_E')
    output_satellite.save()
    
    return(delta_1_0)