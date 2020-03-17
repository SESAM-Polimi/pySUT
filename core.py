"""
pySUT - A Python module for automating supply-use io calculations 
=================================================================

Authors: L.Rinaldi, G.Guidicini, N.Golinucci, M.A.Tahavori, M.V.Rocco
         Department of Energy - Politecnico di Milano
"""


def core_process(database,country,year,nL,tol,analysis,agg_level,rect_level):
    
    
    from data_handle import tables_import, sut_to_iot, technical_coefficients, calc_E_0
    indices, multi_indices, ML_sut = tables_import(nL, database, year, country)

    
    from pySUT.parsing.parser import sut_aggregation
    ML_sut_agg, multi_indices_agg = sut_aggregation(nL, indices, multi_indices, ML_sut, agg_level,rect_level)
    
    ML_iot_0, x_0, xT_0, check_0, unbalances_0 = sut_to_iot(nL, database, year, country, tol, multi_indices_agg, ML_sut_agg)
    ML_iot_coeff_0 = technical_coefficients(ML_iot_0, x_0)
    ML_iot_coeff_0['E_0'] = calc_E_0(ML_iot_coeff_0,x_0)
    
        
    if analysis == 'SA':
        
        from pySUT.applications.SA.shock_analysis import shock_analysis    
        ML_iot_1,x_1 = shock_analysis(nL, analysis, ML_iot_coeff_0, multi_indices_agg, multi_indices, agg_level, rect_level)

    
    if analysis == 'RCOT':
        
        from pySUT.parsing.parser import rectangulization
        ML_RCOT_0, ML_RCOT_coeff_0, indices_RCOT = rectangulization(nL, indices, multi_indices_agg, ML_iot_0, ML_iot_coeff_0, agg_level, rect_level)

        from pySUT.applications.rcot import rcot    
        ML_iot_1,x_1 = rcot(nL, analysis, ML_iot_coeff_0, multi_indices_agg, multi_indices)        
        

    
    # from post_process import xlsx_export, dict_delta_1_0
    
    # delta_1_0 = xlsx_export(nL, ML_iot_0, ML_iot_1, x_0, x_1, E_0, indices_agg, database, country, year)


    
    PARAMETERS = {
              'database'  : database,
              'country'   : country,
              'year'      : year,
              'n layers'  : nL,
              'tolerance' : tol,
              'analysis'  : analysis,
              'agg_level' : agg_level,
              'rect_level': rect_level
              }


    INDICES = {
               'full indices': indices,
               'full multi-indices': multi_indices,
               'aggregated multi-indices': multi_indices_agg,
               } 
    

    MATRICES = {
                'starting SUT': ML_sut,
                'aggregated starting SUT': ML_sut_agg,
                'IOT-like starting SUT': ML_iot_0,
                'IOT-like perturbed SUT': ML_iot_1    
                }

    
    COEFFICIENTS = {
                    'IOT-like starting SU coefficients': ML_iot_coeff_0
                    }

    
    if analysis == 'RCOT':
        INDICES['rectangulized indices'] = indices_RCOT
        MATRICES['IOT-like rectangulized starting SUT'] = ML_RCOT_0
        COEFFICIENTS['IOT-like rectangulized starting SU coefficients'] = ML_RCOT_coeff_0
        
                     
    return(PARAMETERS, INDICES, MATRICES, COEFFICIENTS)