import numpy as np
import pandas as pd

#%% Aggregation

def sut_aggregation(nL, indices, multi_indices, ML_sut, agg_level):
    """ 
    This function performs aggregation of sectors accordingly to how the indices are defined in the dedicated .xlsx file.
    Inputs:
        nL            - Number of layers (economic + physical layers)
        indices       - Dictionary containing indices for the selected database
        multi_indices - Dictionary containing multi-indices for the selected database
        ML_sut        - Dictionary containing imported multi-layer supply-use tables
        agg_level     - Aggregation level, corresponding to the indices header position
    Outputs:
        ML_sut_agg    - Dictionary containing aggregated multi-layer supply-use tables
        indices_agg   - Dictionary containing aggregated indices        
    """
    
    nI_agg = len(list(set(indices['ind'][agg_level])))
    nP_agg = len(list(set(indices['prod'][agg_level])))
    nW_agg = len(list(set(indices['vadd'][agg_level])))
    nM_agg = len(list(set(indices['imp'][agg_level])))
    nY_agg = len(list(set(indices['fd'][agg_level])))
    nR_agg = len(list(set(indices['exog'][agg_level])))
    
    U_0   = np.zeros((nL,nP_agg,nI_agg))     # Initialising an empty multi-layer use matrix
    TRC_0 = np.zeros((nL,nP_agg,nP_agg))     # Initialising an empty multi-layer transaction margins matrix
    V_0   = np.zeros((nL,nI_agg,nP_agg))     # Initialising an empty multi-layer supply matrix
    Wp_0  = np.zeros((nL,nW_agg,nP_agg))     # Initialising an empty multi-layer value added by products matrix
    Wi_0  = np.zeros((nL,nW_agg,nI_agg))     # Initialising an empty multi-layer value added by industries matrix
    Mp_0  = np.zeros((nL,nM_agg,nP_agg))     # Initialising an empty multi-layer imports by products matrix
    Mi_0  = np.zeros((nL,nM_agg,nI_agg))     # Initialising an empty multi-layer imports by industries matrix
    Yp_0  = np.zeros((nL,nP_agg,nY_agg))     # Initialising an empty multi-layer final demand matrix
    Rp_0  = np.zeros((nL,nR_agg,nP_agg))     # Initialising an empty multi-layer exogenous transactions by products matrix
    Ri_0  = np.zeros((nL,nR_agg,nI_agg))     # Initialising an empty multi-layer exogenous transactions by industries matrix
        
    indInd  = multi_indices['ind']
    prodInd = multi_indices['prod']
    vaddInd = multi_indices['vadd']
    impInd  = multi_indices['imp']
    fdInd   = multi_indices['fd']
    exogInd = multi_indices['exog']


    for l in range(nL):
        V   = pd.DataFrame(ML_sut['V'][l,:,:], index=indInd, columns=prodInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        U   = pd.DataFrame(ML_sut['U'][l,:,:], index=prodInd, columns=indInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        TRC = pd.DataFrame(ML_sut['TRC'][l,:,:], index=prodInd, columns=prodInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Wp  = pd.DataFrame(ML_sut['Wp'][l,:,:], index=vaddInd, columns=prodInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Wi  = pd.DataFrame(ML_sut['Wi'][l,:,:], index=vaddInd, columns=indInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Mp  = pd.DataFrame(ML_sut['Mp'][l,:,:], index=impInd, columns=prodInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Mi  = pd.DataFrame(ML_sut['Mi'][l,:,:], index=impInd, columns=indInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Yp  = pd.DataFrame(ML_sut['Yp'][l,:,:], index=prodInd, columns=fdInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        
        V_0[l]   = V.values
        U_0[l]   = U.values
        TRC_0[l] = TRC.values
        Wp_0[l]  = Wp.values
        Wi_0[l]  = Wi.values
        Mp_0[l]  = Mp.values
        Mi_0[l]  = Mi.values
        Yp_0[l]  = Yp.values
        
    Rp_0 = pd.DataFrame(ML_sut['Rp'], index=exogInd, columns=prodInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum() 
    Ri_0 = pd.DataFrame(ML_sut['Ri'], index=exogInd, columns=indInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum() 
    
    ML_sut_agg = {
                'U'   : U_0,
                'TRC' : TRC_0,
                'V'   : V_0,
                'Wp'  : Wp_0,
                'Wi'  : Wi_0,
                'Mp'  : Mp_0,
                'Mi'  : Mi_0,
                'Yp'  : Yp_0,
                'Rp'  : Rp_0,
                'Ri'  : Ri_0,
                }

    indInd_agg  = list(set(indices['ind'][agg_level]))
    indInd_agg.sort()
    prodInd_agg = list(set(indices['prod'][agg_level]))
    prodInd_agg.sort()
    vaddInd_agg = list(set(indices['vadd'][agg_level]))
    vaddInd_agg.sort()    
    impInd_agg  = list(set(indices['imp'][agg_level]))
    impInd_agg.sort()    
    fdInd_agg   = list(set(indices['fd'][agg_level]))
    fdInd_agg.sort()    
    exogInd_agg = list(set(indices['exog'][agg_level]))
    exogInd_agg.sort()   
    
    indices_agg = {
               'prod'    : prodInd_agg,
               'ind'     : indInd_agg,
               'vadd'    : vaddInd_agg,
               'imp'     : impInd_agg,
               'fd'      : fdInd_agg,
               'exog'    : exogInd_agg,
               'headers' : indices['headers']
               }

    return(ML_sut_agg, indices_agg)
