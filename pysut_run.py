"""
pySUT - A Python module for automating supply-use io calculations 
=================================================================

Authors: L.Rinaldi, G.Guidicini, N.Golinucci, M.A.Tahavori, M.V.Rocco
         Department of Energy - Politecnico di Milano

"""

#%% Setting parameters

""" Path definition """

database = 'unusam'                   
country = 'mozambique'
year = 2015


""" Number of layers to be considered. If 1 the model will perform an economic single-layer analysis """
nL = 3

""" Maximum % variation to consider rows and columns as balanced """                      
tol = 0.05


"""
Selection of the desired analysis
Options:
    SA - Shock analysis
    RCOT - Rectangular choice of technology optimization
    No - No analysis will be performed
"""
analysis = 'SA'            


"""
Selection of the level of aggregation and 'rectangulization'. 
Levels of aggregation/rectangulization are to be intended as the columns position of the 'headers' sheet in 'tables/database_country_year/indices.xlsx' file
"""
agg_level = 1                                              
rect_level = 0


#%% Processing

from core import core_process
PARAMETERS, INDICES, MATRICES, COEFFICIENTS = core_process(database,country,year,nL,tol,analysis,agg_level,rect_level)