import numpy as np
import pandas as pd

#%% Creation of empty perturbed coefficient and final demand matrices

def SA_delta_dict(nL, multi_indices_agg, agg_level, rect_level):
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
        
    nP_agg = len(multi_indices_agg['prod'])      # Number of products items
    nI_agg = len(multi_indices_agg['ind'])       # Number of industries items
    nW_agg = len(multi_indices_agg['vadd'])      # Number of value added items
    nM_agg = len(multi_indices_agg['imp'])       # Number of imports items
    nY_agg = len(multi_indices_agg['fd'])        # Number of final demand items
    nR_agg = len(multi_indices_agg['exog'])      # Number of satellite items

    delta_A = np.zeros((nL,nP_agg+nI_agg,nP_agg+nI_agg))
    delta_w = np.zeros((nL,nW_agg,nP_agg+nI_agg))    
    delta_m = np.zeros((nL,nM_agg,nP_agg+nI_agg))  
    delta_Y = np.zeros((nL,nP_agg+nI_agg,nY_agg))    
    delta_B = np.zeros((nL,nR_agg,nP_agg+nI_agg))     
    
    for l in range(nL):
        if l==0:
            delta_economic = pd.ExcelWriter('pySUT/applications/SA/perturbed_matrices/delta_economic_layer.xlsx', engine='xlsxwriter') 
            pd.DataFrame(delta_A[l], index=multi_indices_agg['prod'].append(multi_indices_agg['ind']), columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_economic,'delta_A')
            pd.DataFrame(delta_w[l], index=multi_indices_agg['vadd'], columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_economic,'delta_w')
            pd.DataFrame(delta_m[l], index=multi_indices_agg['imp'], columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_economic,'delta_m')
            pd.DataFrame(delta_Y[l], index=multi_indices_agg['prod'].append(multi_indices_agg['ind']), columns=multi_indices_agg['fd']).to_excel(delta_economic,'delta_Y')            
            pd.DataFrame(delta_B[l], index=multi_indices_agg['exog'], columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_economic,'delta_B')
            delta_economic.save()
        else:
            delta_physical = pd.ExcelWriter('pySUT/applications/SA/perturbed_matrices/delta_physical_layer_'+str(l)+'.xlsx', engine='xlsxwriter')
            pd.DataFrame(delta_A[l], index=multi_indices_agg['prod'].append(multi_indices_agg['ind']), columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_physical,'delta_A')
            pd.DataFrame(delta_w[l], index=multi_indices_agg['vadd'], columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_physical,'delta_w')
            pd.DataFrame(delta_m[l], index=multi_indices_agg['imp'], columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_physical,'delta_m')
            pd.DataFrame(delta_Y[l], index=multi_indices_agg['prod'].append(multi_indices_agg['ind']), columns=multi_indices_agg['fd']).to_excel(delta_physical,'delta_Y')            
            pd.DataFrame(delta_B[l], index=multi_indices_agg['exog'], columns=multi_indices_agg['prod'].append(multi_indices_agg['ind'])).to_excel(delta_physical,'delta_B')
            delta_physical.save()
            
    ready = 'N'
    while ready != 'K':
        ready = input("Please, apply the desired perturbations to the empty variation matrices from the excel files in 'perturbet_matrices' folder'.\nOnce finished, close the excel files and type 'K':\n\n")      
    
    for l in range(nL):
        if l==0:
            delta_economic = 'pySUT/applications/SA/perturbed_matrices/delta_economic_layer.xlsx'                        
            delta_A[l] = np.delete(pd.read_excel(delta_economic,"delta_A", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_w[l] = np.delete(pd.read_excel(delta_economic,"delta_w", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_m[l] = np.delete(pd.read_excel(delta_economic,"delta_m", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_Y[l] = np.delete(pd.read_excel(delta_economic,"delta_Y", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_B[l] = np.delete(pd.read_excel(delta_economic,"delta_B", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
        else:
            delta_physical = 'pySUT/applications/SA/perturbed_matrices/delta_physical_layer_'+str(l)+'.xlsx'                       
            delta_A[l] = np.delete(pd.read_excel(delta_physical,"delta_A", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_w[l] = np.delete(pd.read_excel(delta_physical,"delta_w", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_m[l] = np.delete(pd.read_excel(delta_physical,"delta_m", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_Y[l] = np.delete(pd.read_excel(delta_physical,"delta_Y", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
            delta_B[l] = np.delete(pd.read_excel(delta_physical,"delta_B", header=agg_level+rect_level+1, index_col=0).values, 0, 1)
    
    
    ML_delta_coeff = {
                       'delta_A' : delta_A,
                       'delta_w' : delta_w,
                       'delta_m' : delta_m,
                       'delta_Y' : delta_Y,
                       'delta_B' : delta_B,
                       }

    return(ML_delta_coeff)       
            
            
            
            
            