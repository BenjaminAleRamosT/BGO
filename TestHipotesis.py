import pandas as pd
from scipy.stats import mannwhitneyu

instancias = ['scpnrh2','scpnrh4','scpnrh5']


for instancia in instancias:
    # Crear un diccionario para almacenar los datos de cada columna de "MH"
    data = pd.read_csv('./Resultados/fitness_'+instancia+'.csv')
    
    mh_data = {}

# Iterar sobre los valores únicos de la columna "MH"
    for mh_value in data['MH'].unique():
        # Filtrar el DataFrame original para cada valor único de "MH"
        mh_subset = data[data['MH'] == mh_value]
        
        # Almacenar los datos en el diccionario usando el valor de "MH" como clave
        mh_data[mh_value] = mh_subset['FITNESS'].tolist()

    # Crear un nuevo DataFrame con los datos reducidos
    df = pd.DataFrame.from_dict(mh_data)

    # Crear un diccionario para almacenar los resultados del test
    resultados_wilcoxon = {}

    # Columna con la que comparar (en este caso, 'GO')
    columna_referencia = 'GO'

    # Iterar sobre las columnas para realizar la prueba de Wilcoxon
    for columna in df.columns:
        if columna != columna_referencia:
            # Realizar el test de Wilcoxon
            statistic, p_value = mannwhitneyu(df[columna], df[columna_referencia], alternative='less')
        
            # Almacenar el resultado en el diccionario
            resultados_wilcoxon[columna] = {'Estadística': statistic, 'Valor p': p_value}

    # Crear un DataFrame a partir del diccionario de resultados
    resultados_df = pd.DataFrame(resultados_wilcoxon).T

    resultados_df.to_csv('./Resultados/TestHipotesis/Wilcoxon_'+instancia+'.csv')

    # Mostrar los resultados
    print(resultados_df)
    # Muestra el nuevo DataFrame
    #print(reduced_data)