
salinity_correlation_excludes = [
    'Uso_del_Su', #doesn't have any relationship
    'Sal_seco', #has a correlation of 1 with the scope variable
    'CE', #is redundant with Cond_Seco
    'STD_seco', #is redundant with Cond_Seco
    'Cond_Seco', # possible leakage with scope variable (0.988 of correlation)
    'pH_seco' #Has low correlation with scope variable
]

salinity_exclude_cols = ['OBJECTID', 'ID_TOTAL', 'ID_PROYECT', 'No_Consecu', 'Origen', 'F30', 'Condición']

salinity_missing_cols = [
    'Plancha', 'Prof_Pozo', 'Prof_Seco', 'Tipo_de_Ni', 'Método_de', 'Prof_Húme', 'sigsonia__',
    'pH_Humedo', 'Cond_seco1', 'T_seco1', 'Sal_seco_1', 'STD_Seco1', 'Sal_seco_1',
    'sigsonia_1', 'Sitio', 'Observacio', 'Sitio'
]

salinity_group_use_aliases = {
    'Forestal': ['Forestal', 'forestal'],
    'Ganadería': ['Ganadería', 'Ganadero', 'Ganaderia', 'ganaderia'],
    'Forestal-Ganaderia': ['Forestal - Ganaderia', 'Ganaderia - Forestal', 'Forestal y ganaderia'],
    'Urbano': ['Urbano'],
    'Rancheria-Ganaderia': ['Rancheria y Ganaderia', 'Gananderia y Rancheria', 'Ganaderia y Rancheria'],
    'Agricultura': ['Agricultura', 'agricultura', 'Agricultutra'],
    'Agricultura-Ganadería': ['Agricultura y Ganaderia', 'Agricultura - Ganaderia', 'Agricultura y ganaderia', 'Agricultura, ganaderia', 'Agricultura-Ganaderia'],
    'Otro': ['Agricultura, ganaderia y rancheria', 'Colegio', 'Industrial', '-', 'Urbano y Ganaderia', 'otro', 'Agricultura, forestal',
             'Rancheria y agricultura', 'Industria', 'Urbano y Rancheria', 'Rancheria', 'Cantera y Finca', 'Finca', 'Agricultura - Forestal- Ganaderia',
             'Agricultura - Ganaderia - Forestal', 'Reserva hidrica', 'Ranchería']
}

salinity_data_dictionary = {
    'OBJECTID': int, 'ID_TOTAL': int, 'ID_PROYECT': int, 'Plancha': float, 'No_Consecu': int, 'Tipo_de_Ca': 'category',
    'Sitio': str, 'Origen': str, 'X': float, 'Y': float, 'Uso_del_Su': 'category', 'Condición': 'category', 'Prof_Pozo': float,
    'Tipo_de_Ni': 'category', 'Método_de': 'category', 'Prof_Seco': float, 'Prof_Húme': float, 'Observacio': str, 'pH_seco': float,
    'Cond_Seco': float, 'T_Seco': float, 'STD_seco': float, 'Sal_seco': float, 'sigsonia__': float, 'pH_Humedo': float,
    'Cond_seco1': float, 'T_seco1': float, 'STD_Seco1': float, 'Sal_seco_1': float, 'sigsonia_1': float, 'F30': str, 'CE': float,
    'SAL': float, 'sigsonia__': float
}

salinity_numeric_cols = [col for col, typ in salinity_data_dictionary.items() 
                if typ in [int, float] and col not in salinity_missing_cols
                and col not in salinity_exclude_cols]
salinity_cat_cols = [col for col, typ in salinity_data_dictionary.items() 
                if typ in ['category', str] and col not in salinity_missing_cols
                and col not in salinity_exclude_cols]