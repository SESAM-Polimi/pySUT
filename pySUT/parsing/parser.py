import numpy as np
import pandas as pd

#%% Aggregation

def sut_aggregation(nL, indices, multi_indices, ML_sut, agg_level,rect_level):
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
        V   = pd.DataFrame(ML_sut['V'][l,:,:], index=indInd, columns=prodInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum()
        U   = pd.DataFrame(ML_sut['U'][l,:,:], index=prodInd, columns=indInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum()
        TRC = pd.DataFrame(ML_sut['TRC'][l,:,:], index=prodInd, columns=prodInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Wp  = pd.DataFrame(ML_sut['Wp'][l,:,:], index=vaddInd, columns=prodInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Wi  = pd.DataFrame(ML_sut['Wi'][l,:,:], index=vaddInd, columns=indInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Mp  = pd.DataFrame(ML_sut['Mp'][l,:,:], index=impInd, columns=prodInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Mi  = pd.DataFrame(ML_sut['Mi'][l,:,:], index=impInd, columns=indInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Yp  = pd.DataFrame(ML_sut['Yp'][l,:,:], index=prodInd, columns=fdInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=[agg_level,rect_level],axis=1).sum()
        
        V_0[l]   = V.values
        U_0[l]   = U.values
        TRC_0[l] = TRC.values
        Wp_0[l]  = Wp.values
        Wi_0[l]  = Wi.values
        Mp_0[l]  = Mp.values
        Mi_0[l]  = Mi.values
        Yp_0[l]  = Yp.values
        
    Rp_0 = pd.DataFrame(ML_sut['Rp'].values, index=exogInd, columns=prodInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum() 
    Ri_0 = pd.DataFrame(ML_sut['Ri'].values, index=exogInd, columns=indInd).groupby(level=[agg_level,rect_level],axis=0).sum().groupby(level=agg_level,axis=1).sum() 
    
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

    indInd_agg  = V.index
    prodInd_agg = U.index
    vaddInd_agg = Wp.index
    impInd_agg  = Mp.index
    fdInd_agg   = Yp.columns
    exogInd_agg = Rp_0.index
    
    multi_indices_agg = {
               'prod'    : prodInd_agg,
               'ind'     : indInd_agg,
               'vadd'    : vaddInd_agg,
               'imp'     : impInd_agg,
               'fd'      : fdInd_agg,
               'exog'    : exogInd_agg,
               'headers' : indices['headers']
               }
        
    return(ML_sut_agg, multi_indices_agg)



def rectangulization(nL, indices, indices_agg, ML_iot_0, ML_iot_coeff_0, agg_level, rect_level):
    """ 
    This function performs rectangulization of multi-layer coefficients matrices accordingly to how the indices are defined in the dedicated .xlsx file.
    Inputs:
        nL             - Number of layers (economic + physical layers)
        indices        - Dictionary containing indices for the selected database
        multi_indices  - Dictionary containing multi-indices for the selected database
        ML_iot_coeff_0 - Dictionary containing technical coefficients for the IOT-like tables
        agg_level      - Aggregation level, corresponding to the indices header position
    Outputs:
        ML_RCOT_coeff  - Dictionary containing aggregated multi-layer supply-use tables
    """
    
    nI_agg = len(list(set(indices['ind'][agg_level])))
    nP_agg = len(list(set(indices['prod'][agg_level])))
    nW_agg = len(list(set(indices['vadd'][agg_level])))
    nM_agg = len(list(set(indices['imp'][agg_level])))
    nY_agg = len(list(set(indices['fd'][agg_level])))
    nR_agg = len(list(set(indices['exog'][agg_level])))

    nI_rcot = len(list(set(indices['ind'][rect_level])))
    nP_rcot = len(list(set(indices['prod'][rect_level])))
    nW_rcot = len(list(set(indices['vadd'][rect_level])))
    nM_rcot = len(list(set(indices['imp'][rect_level])))
    nY_rcot = len(list(set(indices['fd'][rect_level])))
    nR_rcot = len(list(set(indices['exog'][rect_level])))

        
    ZR_0   = np.zeros((nL,nP_rcot+nI_agg,nP_agg+nI_agg))     # Initialising an empty multi-layer endogenous transactions matrices
    WR_0   = np.zeros((nL,nW_rcot,nP_agg+nI_agg))            # Initialising an empty multi-layer value added matrices
    MR_0   = np.zeros((nL,nM_rcot,nP_agg+nI_agg))            # Initialising an empty multi-layer imports matrices
    YR_0   = np.zeros((nL,nP_rcot+nI_agg,nY_agg))            # Initialising an empty multi-layer final demand matrices
    RR_0   = np.zeros((nL,nR_rcot,nP_agg+nI_agg))            # Initialising an empty multi-layer exogenous transactions matrices

    AR_0   = np.zeros((nL,nP_rcot+nI_agg,nP_agg+nI_agg))     # Initialising an empty multi-layer endogenous transactions matrices
    wR_0   = np.zeros((nL,nW_rcot,nP_agg+nI_agg))            # Initialising an empty multi-layer value added matrices
    mR_0   = np.zeros((nL,nM_rcot,nP_agg+nI_agg))            # Initialising an empty multi-layer imports matrices
    BR_0   = np.zeros((nL,nR_rcot,nP_agg+nI_agg))            # Initialising an empty multi-layer exogenous transactions matrices

       
    indInd  = indices_agg['ind']
    prodInd = indices_agg['prod']
    vaddInd = indices_agg['vadd']
    impInd  = indices_agg['imp']
    fdInd   = indices_agg['fd']
    exogInd = indices_agg['exog']

    zInd = prodInd.append(indInd)
    zInd = zInd.swaplevel(0,1)
    

    for l in range(nL):
        Z   = pd.DataFrame(ML_iot_0['Z'][l,:,:], index=zInd, columns=zInd).groupby(level=rect_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        W   = pd.DataFrame(ML_iot_0['W'][l,:,:], index=vaddInd, columns=zInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        M   = pd.DataFrame(ML_iot_0['M'][l,:,:], index=impInd, columns=zInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        Y   = pd.DataFrame(ML_iot_0['Y'][l,:,:], index=zInd, columns=fdInd).groupby(level=rect_level,axis=0).sum().groupby(level=rect_level,axis=1).sum()

        A   = pd.DataFrame(ML_iot_coeff_0['A'][l,:,:], index=zInd, columns=zInd).groupby(level=rect_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        w   = pd.DataFrame(ML_iot_coeff_0['w'][l,:,:], index=vaddInd, columns=zInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        m   = pd.DataFrame(ML_iot_coeff_0['m'][l,:,:], index=impInd, columns=zInd).groupby(level=agg_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
        
        ZR_0[l] = Z.values
        WR_0[l] = W.values
        MR_0[l] = M.values
        YR_0[l] = Y.values
        
        AR_0[l] = A.values
        wR_0[l] = w.values
        mR_0[l] = m.values

        
    RR_0   = pd.DataFrame(ML_iot_0['R'], index=exogInd, columns=zInd).groupby(level=rect_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
    BR_0   = pd.DataFrame(ML_iot_coeff_0['B'], index=exogInd, columns=zInd).groupby(level=rect_level,axis=0).sum().groupby(level=agg_level,axis=1).sum()
    

    ML_RCOT_0 = {
                'Z' : ZR_0,
                'W' : WR_0,
                'M' : MR_0,
                'Y' : YR_0,
                'R' : RR_0,
                }

    ML_RCOT_coeff_0 = {
                      'A' : AR_0,
                      'w' : wR_0,
                      'm' : mR_0,
                      'Y' : YR_0,
                      'B' : BR_0,
                      }

    
    indices_RCOT = {
                   'prod/ind' : zInd,
                   'vadd'     : vaddInd,
                   'imp'      : impInd,
                   'fd'       : fdInd,
                   'exog'    : exogInd,
                   'headers' : indices['headers']
                   }
    
    
    return(ML_RCOT_0, ML_RCOT_coeff_0, indices_RCOT)
    
    
    
    
    