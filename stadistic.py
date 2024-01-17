import pandas as pd
from scipy.stats import friedmanchisquare, rankdata, mannwhitneyu
from scipy import stats
from itertools import combinations, permutations
# Supongamos que tienes un DataFrame llamado 'data' con las columnas 'MH' y 'FITNESS'
# Aquí se crea un ejemplo similar al que proporcionaste
instancias = ['scp41','scpc5','scpd5','scpnre5']


for instancia in instancias:
    data = pd.read_csv('./Resultados/fitness_'+instancia+'.csv')
    
    # Análisis de resultados
    metaheuristics = data['MH'].unique()
    num_instances = len(metaheuristics)
    num_repetitions = len(data) // num_instances
    results = data['FITNESS'].values.reshape(num_instances, num_repetitions)
    
    # Calcular el ranking para cada algoritmo en cada instancia
    ranked_data = rankdata(results, axis=1)
    
    # Calcular el ranking promedio para cada algoritmo
    mean_ranks = ranked_data.mean(axis=0)
    
    # Iterar a través de las metaheurísticas y realizar la prueba de Shapiro-Wilk
    for mh in metaheuristics:
        mh_data = data[data['MH'] == mh]['FITNESS']
        statistic, p_value = stats.shapiro(mh_data)
        
        # Imprimir los resultados de la prueba para cada metaheurística
        # print(f"Metaheurística: {mh}")
        # print("Estadístico de prueba:", statistic)
        # print("Valor p asociado:", p_value)
        
        # Comprobar si se rechaza la hipótesis nula
        # if p_value < 0.05:
            # print(f"Los datos de {mh} NO siguen una distribución normal (se rechaza la hipótesis nula).")
        # else:
            # print(f"Los datos de {mh} siguen una distribución normal (no se rechaza la hipótesis nula).")
        
        # print("\n")
    
    # Aplicar el test de Friedman
    f_statistic, p_value = friedmanchisquare(*ranked_data.transpose())
    
    print('\nInstancia:')
    print(instancia)
    
    # Imprimir resultados
    # print("Resultados:")
    # print(results)
    # print("\nRanking promedio:")
    # print(mean_ranks)
    # print("Estadístico F de Friedman:", f_statistic)
    # print("Valor p asociado:", p_value)
    
    if True:
        # print('p menor a 0.05,', 
        #       'por lo que no se puede rechazar la hipotesis nula',
        #       '(no hay diferencias significativas)',
        #       'por lo que se continua con el test de wilcoxon')
        num_metaheuristics = len(metaheuristics)
        wilcoxon_matrix = pd.DataFrame(index=metaheuristics, columns=metaheuristics)
        
        # Realizar pruebas Wilcoxon-Mann-Whitney entre todas las combinaciones de metaheurísticas
        for mh1, mh2 in permutations(metaheuristics, 2):
            data_mh1 = data[data['MH'] == mh1]['FITNESS']
            data_mh2 = data[data['MH'] == mh2]['FITNESS']
            
            # Realizar la prueba Wilcoxon
            statistic, p_value = mannwhitneyu(data_mh1, data_mh2, alternative='less')
            
            # Almacenar el valor p en la matriz (puedes usar otras estadísticas según sea necesario)
            wilcoxon_matrix.loc[mh1, mh2] = p_value
            # wilcoxon_matrix.loc[mh2, mh1] = p_value  # Los valores son simétricos
        
            # Imprimir el nombre de las metaheurísticas y los resultados de la prueba
            # print(f"Comparación entre {mh1} y {mh2}:")
            # print("Estadístico:", statistic)
            # print("Valor p asociado:", p_value)
            # print("")
        
        
        # Imprimir la matriz de resultados de las pruebas Wilcoxon
        print("Matriz de resultados de las pruebas Wilcoxon-Mann-Whitney:")
        print(wilcoxon_matrix)
     
