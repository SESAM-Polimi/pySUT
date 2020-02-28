import numpy as np
import pandas as pd

#%% Aggregation

def sut_aggregation(indices, multi_indices, ML_sut, agg_level):
    """ 
    This function performs aggregation of sectors accordingly to how the indices are defined in the dedicated .xlsx file.
    Inputs:
        indices       - Dictionary containing indices for the selected database
        multi_indices - Dictionary containing multi-indices for the selected database
        ML_sut        - Dictionary containing imported multi-layer supply-use tables
        agg_level     - Aggregation level, corresponding to the indices header position
    Outputs:
        ML_sut_agg    - Dictionary containing aggregated multi-layer supply-use tables
        indices_agg   - Dictionary containing aggregated indices        
    """
    
        
    indInd  = multi_indices['ind']
    prodInd = multi_indices['prod']
    fdInd   = multi_indices['fd']
    # exogInd = multi_indices['exog']

    V_0   = pd.DataFrame(ML_sut['V'], index=indInd, columns=prodInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
    U_0   = pd.DataFrame(ML_sut['U'], index=prodInd, columns=indInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
    Yp_0  = pd.DataFrame(ML_sut['Yp'], index=prodInd, columns=fdInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
                
    # Rp_0 = pd.DataFrame(ML_sut['Rp'], index=exogInd, columns=prodInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum() 
    # Ri_0 = pd.DataFrame(ML_sut['Ri'], index=exogInd, columns=indInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum() 
    
    ML_sut_agg = {
                'U'   : U_0,
                'V'   : V_0,
                'Yp'  : Yp_0,
                # 'Rp'  : Rp_0,
                # 'Ri'  : Ri_0,
                }

    indInd_agg  = V_0.index
    prodInd_agg = U_0.index
    fdInd_agg   = Yp_0.index
    # exogInd_agg = list(set(indices['exog'][agg_level]))
    # exogInd_agg.sort()   
    
    indices_agg = {
               'prod'    : prodInd_agg,
               'ind'     : indInd_agg,
               'fd'      : fdInd_agg,
               # 'exog'    : exogInd_agg,
               'headers' : indices['headers']
               }

    return(ML_sut_agg, indices_agg)
