import pandas as pd
import numpy as np

#%% Tables import


def indicesImport(database,  year, country):
    """
    This function will import the indices for standard matrices from a ready-to-use database for a given country and year.
    Inputs:
        database - Database selected for the analysis
        year     - Year selected for the analysis
        country  - Country selected for the analysis
    Outputs:
        indices       - Dictionary containing indices for the selected database
        multi_indices - Dictionary containing multi-indices for the selected database
    """
        
    headers = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/indices.xlsx',"headers", header=None, index_col=None).values.tolist()     # Importing headers for each indices column

    indProd = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/indices.xlsx',"prod", header=0, index_col=None).values.T.tolist()      # Products indices
    indInd  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/indices.xlsx',"ind", header=0, index_col=None).values.T.tolist()       # Industries indices
    indVadd = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/indices.xlsx',"vadd", header=0, index_col=None).values.T.tolist()      # Value added indices
    indImp  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/indices.xlsx',"imp", header=0, index_col=None).values.T.tolist()       # Imports indices
    indFd   = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/indices.xlsx',"fd", header=0, index_col=None).values.T.tolist()        # Final demand indices
    indExog = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/indices.xlsx',"exog", header=0, index_col=None).values.T.tolist()      # Exogenous resources indices                 

    indices = {
               'prod'    : indProd,
               'ind'     : indInd,
               'vadd'    : indVadd,
               'imp'     : indImp,
               'fd'      : indFd,
               'exog'    : indExog,
               'headers' : headers
               }

    # Multi-indices generation
    mindProd = pd.MultiIndex.from_arrays(indProd, names=headers[0])   # Products multi-index
    mindInd  = pd.MultiIndex.from_arrays(indInd, names=headers[0])    # Industries multi-index
    mindVadd = pd.MultiIndex.from_arrays(indVadd, names=headers[0])   # Value added multi-index
    mindImp  = pd.MultiIndex.from_arrays(indImp, names=headers[0])    # Imports multi-index
    mindFd   = pd.MultiIndex.from_arrays(indFd, names=headers[0])     # Final demand multi-index
    mindExog = pd.MultiIndex.from_arrays(indExog, names=headers[0])   # Exogenous resources multi-index

    multi_indices = {
               'prod'    : mindProd,
               'ind'     : mindInd,
               'vadd'    : mindVadd,
               'imp'     : mindImp,
               'fd'      : mindFd,
               'exog'    : mindExog,
               'headers' : headers
               }
        
    return(indices, multi_indices)



def sutImport(nL, database, year, country, indices):
    """
    This function will import the standard matrices from a ready-to-use database for a given country and year.
    Eurostat supply-use database is currently the only available database pySUT is currently able to import and download into the desired format.
    The user may also create his own database in the 'tables' folder minding to provide data with the same structure as for Eurostat ones
    
    Inputs:
        nL       - Number of layers (economic + physical layers)
        database - Database selected for the analysis
        year     - Year selected for the analysis
        country  - Country selected for the analysis
        indices  - Dictionary containing indices for the selected database
    Output:
        ML_sut   - Dictionary containing imported multi-layer supply-use tables
    """

    nP = len(indices['prod'][0])     # Number of products items
    nI = len(indices['ind'][0])      # Number of industries items
    nW = len(indices['vadd'][0])     # Number of value added items
    nM = len(indices['imp'][0])      # Number of imports items
    nY = len(indices['fd'][0])       # Number of final demand items
    
    U_0   = np.zeros((nL,nP,nI))     # Initialising an empty multi-layer use matrix
    TRC_0 = np.zeros((nL,nP,nP))     # Initialising an empty multi-layer transaction margins matrix
    V_0   = np.zeros((nL,nI,nP))     # Initialising an empty multi-layer supply matrix
    Wp_0  = np.zeros((nL,nW,nP))     # Initialising an empty multi-layer value added by products matrix
    Wi_0  = np.zeros((nL,nW,nI))     # Initialising an empty multi-layer value added by industries matrix
    Mp_0  = np.zeros((nL,nM,nP))     # Initialising an empty multi-layer imports by products matrix
    Mi_0  = np.zeros((nL,nM,nI))     # Initialising an empty multi-layer imports by industries matrix
    Yp_0  = np.zeros((nL,nP,nY))     # Initialising an empty multi-layer final demand matrix
          
    for l in range(nL):    
        if l==0:   # Layer 0 == economic layer            
            U_0[l]   = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','use',header=None,index_col=None)                # Economic use matrix import 
            TRC_0[l] = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','trc',header=None,index_col=None)                # Economic transaction margins matrix import
            V_0[l]   = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','supply',header=None,index_col=None)             # Economic supply matrix import
            Wi_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','va_ind',header=None,index_col=None)             # Economic value added by industries matrix import
            Wp_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','va_prod',header=None,index_col=None)            # Economic value added by products matrix import
            Mi_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','imp_ind',header=None,index_col=None)            # Economic import by industries matrix import
            Mp_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','imp_prod',header=None,index_col=None)           # Economic import by products matrix import
            Yp_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/economic_layer.xlsx','fd',header=None,index_col=None)                 # Economic final demand matrix import           
        else:            
            U_0[l]   = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','use',header=None,index_col=None)                # Physical use matrices import 
            TRC_0[l] = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','trc',header=None,index_col=None)                # Physical transaction margins matrices import
            V_0[l]   = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','supply',header=None,index_col=None)             # Physical supply matrices import
            Wi_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','va_ind',header=None,index_col=None)             # Physical value added by industries matrices import
            Wp_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','va_prod',header=None,index_col=None)            # Physical value added by products matrices import
            Mi_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','imp_ind',header=None,index_col=None)            # Physical import by industries matrices import
            Mp_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','imp_prod',header=None,index_col=None)           # Physical import by products matrices import
            Yp_0[l]  = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/layers/physical_layer_'+str(l)+'.xlsx','fd',header=None,index_col=None)                 # Physical final demand matrices import             

    Rp_0 = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/satellite_accounts.xlsx','exog_prod',header=None,index_col=None)     # Exogenous transactions by products matrix import
    Ri_0 = pd.read_excel('pySUT/tables/'+str(database)+'_'+str(country)+'_'+str(year)+'/satellite_accounts.xlsx','exog_ind',header=None,index_col=None)      # Exogenous transactions by industries matrix import
    
    ML_sut = {
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


    return(ML_sut)


