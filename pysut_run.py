"""
pySUT - A Python module for automating supply-use io calculations

DATABASE: EXIOBASE_3.3.17_hsut_2011
=================================================================

Authors: L.Rinaldi, G.Guidicini, N.Golinucci, M.A.Tahavori, M.V.Rocco
         Department of Energy - Politecnico di Milano

"""


# analysis = 'SA'            # Options: No - No analysis will be performed
                             #          SA - Shock analysis

agg_level = ["countryName","flowAggName"]           # Levels of aggregation are to be intended as the 'headers' sheet in 'indices.xlsx' file.     
                           

# from downloader import*   COMING SOON (HOPEFULLY)

from data_handle import tables_import, sut_to_iot, technical_coefficients
indices, multi_indices, ML_sut = tables_import()

from pySUT.parsing.parser import sut_aggregation
ML_sut_agg, indices_agg = sut_aggregation(indices, multi_indices, ML_sut, agg_level)

ML_iot_0, x_0, xT_0 = sut_to_iot(indices_agg, ML_sut_agg)
ML_iot_coeff_0 = technical_coefficients(ML_iot_0, x_0)



# WORK IN PROGRESS
# E_0 = calc_E_0(ML_iot_coeff_0,x_0)

# from core import analysis_application
# ML_iot_1, x_1 = analysis_application(analysis, ML_iot_coeff_0, indices_agg, multi_indices)

# from post_process import xlsx_export

# delta_1_0 = xlsx_export(ML_iot_0, ML_iot_1, x_0, x_1, indices_agg)