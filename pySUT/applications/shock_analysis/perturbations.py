import numpy as np
import pandas as pd

#%% Creation of empty perturbed coefficient and final demand matrices

def SA_delta_dict(nL, indices_agg):
    """
    This function exports empty and ready-to-modify technical coefficient and final demand matrices. 
    It will require the user to confirm the modifications made on the excel files.
    Afterwords, the excel files will be reimported and ordered into a dictionary.
    Inputs:
        nL             - Number of layers (economic + physical layers)
        indices_agg    - Dictionary containing aggregated indices
    Outputs:
        ML_delta_coeff - Dictionary containing perturbed multi-layer coefficents
    """
        
    nP_agg = len(indices_agg['prod'])      # Number of products items
    nI_agg = len(indices_agg['ind'])       # Number of industries items
    nW_agg = len(indices_agg['vadd'])      # Number of value added items
    nM_agg = len(indices_agg['imp'])       # Number of imports items
    nY_agg = len(indices_agg['fd'])        # Number of final demand items
    nR_agg = len(indices_agg['exog'])      # Number of satellite items

    delta_A = np.zeros((nL,nP_agg+nI_agg,nP_agg+nI_agg))
    delta_w = np.zeros((nL,nW_agg,nP_agg+nI_agg))    
    delta_m = np.zeros((nL,nM_agg,nP_agg+nI_agg))  
    delta_Y = np.zeros((nL,nP_agg+nI_agg,nY_agg))    
    delta_B = np.zeros((nL,nR_agg,nP_agg+nI_agg))     
    
    for l in range(nL):
        if l==0:
            delta_economic = pd.ExcelWriter('pySUT/applications/shock_analysis/perturbed_matrices/delta_economic_layer.xlsx', engine='xlsxwriter') 
            pd.DataFrame(delta_A[l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_economic,'delta_A')
            pd.DataFrame(delta_w[l], index=indices_agg['vadd'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_economic,'delta_w')
            pd.DataFrame(delta_m[l], index=indices_agg['imp'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_economic,'delta_m')
            pd.DataFrame(delta_Y[l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['fd']).to_excel(delta_economic,'delta_Y')            
            pd.DataFrame(delta_B[l], index=indices_agg['exog'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_economic,'delta_B')
            delta_economic.save()
        else:
            delta_physical = pd.ExcelWriter('pySUT/applications/shock_analysis/perturbed_matrices/delta_physical_layer_'+str(l)+'.xlsx', engine='xlsxwriter')
            pd.DataFrame(delta_A[l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_physical,'delta_A')
            pd.DataFrame(delta_w[l], index=indices_agg['vadd'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_physical,'delta_w')
            pd.DataFrame(delta_m[l], index=indices_agg['imp'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_physical,'delta_m')
            pd.DataFrame(delta_Y[l], index=indices_agg['prod']+indices_agg['ind'], columns=indices_agg['fd']).to_excel(delta_physical,'delta_Y')            
            pd.DataFrame(delta_B[l], index=indices_agg['exog'], columns=indices_agg['prod']+indices_agg['ind']).to_excel(delta_physical,'delta_B')
            delta_physical.save()
            
    ready = 'N'
    while ready != 'K':
        ready = input("Please, apply the desired perturbations to the empty variation matrices from the excel files in 'perturbet_matrices' folder'.\nOnce finished, close the excel files and type 'K':\n\n")      
    
    for l in range(nL):
        if l==0:
            delta_economic = 'pySUT/applications/shock_analysis/perturbed_matrices/delta_economic_layer.xlsx'                        
            delta_A[l] = pd.read_excel(delta_economic,"delta_A", header=0, index_col=0).values
            delta_w[l] = pd.read_excel(delta_economic,"delta_w", header=0, index_col=0).values
            delta_m[l] = pd.read_excel(delta_economic,"delta_m", header=0, index_col=0).values
            delta_Y[l] = pd.read_excel(delta_economic,"delta_Y", header=0, index_col=0).values
            delta_B[l] = pd.read_excel(delta_economic,"delta_B", header=0, index_col=0).values
        else:
            delta_physical = 'pySUT/applications/shock_analysis/perturbed_matrices/delta_physical_layer_'+str(l)+'.xlsx'                       
            delta_A[l] = pd.read_excel(delta_physical,"delta_A", header=0, index_col=0).values
            delta_w[l] = pd.read_excel(delta_physical,"delta_w", header=0, index_col=0).values
            delta_m[l] = pd.read_excel(delta_physical,"delta_m", header=0, index_col=0).values
            delta_Y[l] = pd.read_excel(delta_physical,"delta_Y", header=0, index_col=0).values
            delta_B[l] = pd.read_excel(delta_physical,"delta_B", header=0, index_col=0).values
    
    
    ML_delta_coeff = {
                       'delta_A' : delta_A,
                       'delta_w' : delta_w,
                       'delta_m' : delta_m,
                       'delta_Y' : delta_Y,
                       'delta_B' : delta_B,
                       }

    return(ML_delta_coeff)       
            
            
            
            
            