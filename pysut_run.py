"""
pySUT - A Python module for automating supply-use io calculations 
=================================================================

Authors: L.Rinaldi, G.Guidicini, N.Golinucci, M.A.Tahavori, M.V.Rocco
         Department of Energy - Politecnico di Milano

"""

# ciao cioa ciao

database = 'Eurostat'                   
country = 'Italy'
year = 2014

nL = 1                     # Number of layers to be considered. If 1 the model will perform an economic single-layer analysis

tol = 0.05

analysis = 'SA'            # Options: No - No analysis will be performed
                           #          SA - Shock analysis

agg_level = 0              # Starts from 0. This parameter indicates the aggregation level according to which the aggregation process shall be performed. 
                           # Levels of aggregation are to be intended as the columns of the 'headers' sheet in 'tables/database/country/year/indices.xlsx' file.


# from downloader import*   COMING SOON (HOPEFULLY)

from data_handle import tables_import, sut_to_iot, technical_coefficients, calc_E_0
indices, multi_indices, ML_sut = tables_import(nL, database, year, country)

from pySUT.parsing.parser import sut_aggregation
ML_sut_agg, indices_agg = sut_aggregation(nL, indices, multi_indices, ML_sut, agg_level)

ML_iot_0, x_0, xT_0, check_0, unbalances_0 = sut_to_iot(nL, database, year, country, tol, indices_agg, ML_sut_agg)
ML_iot_coeff_0 = technical_coefficients(ML_iot_0, x_0)
E_0 = calc_E_0(ML_iot_coeff_0,x_0)

from core import analysis_application
ML_iot_1, x_1 = analysis_application(nL, analysis, ML_iot_coeff_0, indices_agg, multi_indices)

from post_process import xlsx_export, dict_delta_1_0

delta_1_0 = xlsx_export(nL, ML_iot_0, ML_iot_1, x_0, x_1, E_0, indices_agg, database, country, year)