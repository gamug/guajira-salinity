
salinity_exclude_cols = ['OBJECTID', 'ID_TOTAL', 'ID_PROYECT', 'No_Consecu', 'Origen', 'F30']

salinity_missing_cols = [
    'Plancha', 'Prof_Pozo', 'Prof_Seco', 'Tipo_de_Ni', 'Método_de', 'Prof_Húme', 'sigsonia__',
    'pH_Humedo', 'Cond_seco1', 'T_seco1', 'Sal_seco_1', 'STD_Seco1', 'Sal_seco_1',
    'sigsonia_1', 'Sitio', 'Observacio', 'Sitio'
]

salinity_data_dictionary = {
    'OBJECTID': int, 'ID_TOTAL': int, 'ID_PROYECT': int, 'Plancha': float, 'No_Consecu': int, 'Tipo_de_Ca': 'category',
    'Sitio': str, 'Origen': str, 'X': float, 'Y': float, 'Uso_del_Su': 'category', 'Condición': 'category', 'Prof_Pozo': float,
    'Tipo_de_Ni': 'category', 'Método_de': 'category', 'Prof_Seco': float, 'Prof_Húme': float, 'Observacio': str, 'pH_seco': float,
    'Cond_Seco': float, 'T_Seco': float, 'STD_seco': float, 'Sal_seco': float, 'sigsonia__': float, 'pH_Humedo': float,
    'Cond_seco1': float, 'T_seco1': float, 'STD_Seco1': float, 'Sal_seco_1': float, 'sigsonia_1': float, 'F30': str, 'CE': float,
    'SAL': float, 'sigsonia__': float
}