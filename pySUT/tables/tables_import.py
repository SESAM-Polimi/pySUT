import pandas as pd
import numpy as np
import os
import zipfile

#%% Tables import


def indicesImport():
    """
    This function will import the indices for standard matrices from a ready-to-use database for a given country and year.
    Outputs:
        indices       - Dictionary containing indices for the selected database
        multi_indices - Dictionary containing multi-indices for the selected database
    """
    
    dataFileName = 'pySUT/tables/indices.xlsx'

    headers    = pd.read_excel(dataFileName,"headers", header=None, index_col=None).values.tolist()
    headers_ex = pd.read_excel(dataFileName,"headers_ex", header=None, index_col=None).values.tolist()
    indProd    = pd.read_excel(dataFileName,"productIndex", header=None, index_col=None, skiprows=1).values.T.tolist() 
    indInd     = pd.read_excel(dataFileName,"sectorIndex", header=None, index_col=None, skiprows=1).values.T.tolist()
    indFd      = pd.read_excel(dataFileName,"finalDemandIndex", header=None, index_col=None, skiprows=1).values.T.tolist()
    indEx      = pd.read_excel(dataFileName,"exTransIndex", header=None, index_col=None, skiprows=1).values.T.tolist()

    indices = {
                'prod'    : indProd,
                'ind'     : indInd,
                'fd'      : indFd,
                'exog'    : indEx,
                'headers' : headers
                }

    # Multi-indices generation
    mindProd = pd.MultiIndex.from_arrays(indProd, names=headers[0])   # Products multi-index
    mindInd  = pd.MultiIndex.from_arrays(indInd, names=headers[0])    # Industries multi-index
    mindFd   = pd.MultiIndex.from_arrays(indFd, names=headers[0])     # Final demand multi-index
    mindEx   = pd.MultiIndex.from_arrays(indEx, names=headers_ex[0])     # Exogenous resources multi-index
    
    multi_indices = {
                'prod'    : mindProd,
                'ind'     : mindInd,
                'fd'      : mindFd,
                'exog'    : mindEx,
                'headers' : headers
                }
    
        
    return(indices, multi_indices)



def sutImport(indices):
    """
    This function will import the standard matrices from a ready-to-use database for a given country and year.
    Eurostat supply-use database is currently the only available database pySUT is currently able to import and download into the desired format.
    The user may also create his own database in the 'tables' folder minding to provide data with the same structure as for Eurostat ones
    
    Inputs:
        indices  - Dictionary containing indices for the selected database
    Output:
        ML_sut   - Dictionary containing imported multi-layer supply-use tables
    """
    

    sut   = zipfile.ZipFile('pySUT/tables/sut.zip')
    U_0   = pd.read_csv(sut.open('use.csv'), sep=";", header=None, index_col=None).values                  # Economic use matrix import 
    V_0   = pd.read_csv(sut.open('supply.csv'), sep=";", header=None, index_col=None).values.transpose()   # Economic supply matrix import
    Yp_0  = pd.read_csv(sut.open('fd.csv'), sep=";", header=None, index_col=None).values                   # Economic final demand matrix import           
    
    ML_sut = {
               'U'   : U_0,
               'V'   : V_0,
               'Yp'  : Yp_0,
               }

    
    # Rp_0 = pd.read_excel('pySUT/tables/satellite_accounts.xlsx','exog_prod',header=None,index_col=None)     # Exogenous transactions by products matrix import
    # Ri_0 = pd.read_excel('pySUT/tables/satellite_accounts.xlsx','exog_ind',header=None,index_col=None)      # Exogenous transactions by industries matrix import
        
    ML_sut = {
               'U'   : U_0,
               'V'   : V_0,
               'Yp'  : Yp_0,
               # 'Rp'  : Rp_0,
               # 'Ri'  : Ri_0,
               }


    return(ML_sut)


