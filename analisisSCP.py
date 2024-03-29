import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from util import util
from BD.sqlite import BD

dirResultado = './Resultados/'
archivoResumenFitness = open(f'{dirResultado}resumen_fitness_SCP.csv', 'w')
archivoResumenTimes = open(f'{dirResultado}resumen_times_SCP.csv', 'w')
archivoResumenPercentage = open(f'{dirResultado}resumen_percentage_SCP.csv', 'w')

archivoResumenFitness.write("instance")
archivoResumenTimes.write("instance")
archivoResumenPercentage.write("instance")

#archivoResumenFitness.write("instance,best,avg. fitness, std fitness,best,avg. fitness, std fitness,best,avg. fitness, std fitness, best,avg. fitness, std fitness\n")
#archivoResumenTimes.write("instance, min time (s), avg. time (s), std time (s), min time (s), avg. time (s), std time (s), min time (s), avg. time (s), std time (s), min time (s), avg. time (s), std time (s)\n")
#archivoResumenPercentage.write("instance, avg. XPL%, avg. XPT%, avg. XPL%, avg. XPT%, avg. XPL%, avg. XPT%, avg. XPL%, avg. XPT%\n")


graficos = False


incluye_gwo = False
incluye_psa = False
incluye_woa = False
incluye_sca = False
incluye_go = False

bd = BD()

instancias = bd.obtenerInstancias(f'''
                                  'scp41','scpc5','scpd5','scpnre5'
                                  ''')

for instancia in instancias:
    # print(instancia)
    
    blob = bd.obtenerArchivos(instancia[1])
    corrida = 1
    
    archivoFitness = open(f'{dirResultado}fitness_'+instancia[1]+'.csv', 'w')
    archivoFitness.write('MH,FITNESS\n')
    
    
    #blob = bd.obtenerArchivos(instancia[0])
    #corrida = 1
    
    #archivoFitness = open(f'{dirResultado}fitness_'+instancia[0].split(".")[0]+'.csv', 'w')
    #archivoFitness.write('MH,FITNESS\n')

    fitnessSCA = [] 
    fitnessGWO = [] 
    fitnessWOA = [] 
    fitnessPSA = []
    fitnessBGO = []

    timeSCA = []
    timeGWO = []
    timeWOA = []
    timePSA = []
    timeBGO = []

    xplSCA = [] 
    xplGWO = [] 
    xplWOA = [] 
    xplPSA = []
    xplBGO = []


    xptSCA = []
    xptGWO = []
    xptWOA = []
    xptPSA = []
    xptBGO = []
    
    bestFitnessSCA = []
    bestFitnessGWO = []
    bestFitnessWOA = []
    bestFitnessPSA = []
    bestFitnessBGO = []


    bestTimeSCA = []
    bestTimeGWO = []
    bestTimeWOA = []
    bestTimePSA = []
    bestTimeBGO = []
    
    for d in blob:
        
        nombreArchivo = d[0]
        archivo = d[1]
        
        direccionDestiono = './Resultados/Transitorio/'+nombreArchivo+'.csv'
        print(direccionDestiono)
        print("-------------------------------------------------------------------------------")
        util.writeTofile(archivo,direccionDestiono)
        
        data = pd.read_csv(direccionDestiono)
        print(data)

        mh = nombreArchivo.split('_')[0]
        if mh == 'GO':
            mh = 'BGO'

        if mh == "GWO" and incluye_gwo == False:
            archivoResumenFitness.write(",best,avg. fitness, std fitness")
            archivoResumenTimes.write(", min time (s), avg. time (s), std time (s)")
            archivoResumenPercentage.write(", avg. XPL%, avg. XPT%")
            incluye_gwo = True

        if mh == "BGO" and incluye_go == False:
            archivoResumenFitness.write(",best,avg. fitness, std fitness")
            archivoResumenTimes.write(", min time (s), avg. time (s), std time (s)")
            archivoResumenPercentage.write(", avg. XPL%, avg. XPT%")
            incluye_go = True
            
        if mh == "PSA" and incluye_psa == False:
            archivoResumenFitness.write(",best,avg. fitness, std fitness")
            archivoResumenTimes.write(", min time (s), avg. time (s), std time (s)")
            archivoResumenPercentage.write(", avg. XPL%, avg. XPT%")
            incluye_psa = True
            
        if mh == "WOA" and incluye_woa == False:
            archivoResumenFitness.write(",best,avg. fitness, std fitness")
            archivoResumenTimes.write(", min time (s), avg. time (s), std time (s)")
            archivoResumenPercentage.write(", avg. XPL%, avg. XPT%")
            incluye_woa = True
            
        if mh == "SCA" and incluye_sca == False:
            archivoResumenFitness.write(",best,avg. fitness, std fitness")
            archivoResumenTimes.write(", min time (s), avg. time (s), std time (s)")
            archivoResumenPercentage.write(", avg. XPL%, avg. XPT%")
            incluye_sca = True
            

        problem = nombreArchivo.split('_')[1]
        # print(mh)
        # print(problem)

        iteraciones = data['iter']
        fitness     = data['fitness']
        time        = data['time']
        xpl         = data['XPL']
        xpt         = data['XPT']
        div         = data['DIV']
        # print(fitness)

        if mh == 'PSA':
            fitnessPSA.append(np.min(fitness))
            timePSA.append(np.round(np.sum(time),3))
            xplPSA.append(np.round(np.mean(xpl), decimals=2))
            xptPSA.append(np.round(np.mean(xpt), decimals=2))
            archivoFitness.write(f'PSA,{str(np.min(fitness))}\n')
            
        if mh == 'SCA':
            fitnessSCA.append(np.min(fitness))
            timeSCA.append(np.round(np.sum(time),3))
            xplSCA.append(np.round(np.mean(xpl), decimals=2))
            xptSCA.append(np.round(np.mean(xpt), decimals=2))
            archivoFitness.write(f'SCA,{str(np.min(fitness))}\n')
            
        if mh == 'GWO':
            fitnessGWO.append(np.min(fitness))
            timeGWO.append(np.round(np.sum(time),3))
            xplGWO.append(np.round(np.mean(xpl), decimals=2))
            xptGWO.append(np.round(np.mean(xpt), decimals=2))
            archivoFitness.write(f'GWO,{str(np.min(fitness))}\n')
            
        if mh == 'WOA':
            fitnessWOA.append(np.min(fitness))
            timeWOA.append(np.round(np.sum(time),3))
            xplWOA.append(np.round(np.mean(xpl), decimals=2))
            xptWOA.append(np.round(np.mean(xpt), decimals=2))
            archivoFitness.write(f'WOA,{str(np.min(fitness))}\n')
            
        if mh == 'BGO':
            fitnessBGO.append(np.min(fitness))
            timeBGO.append(np.round(np.sum(time),3))
            xplBGO.append(np.round(np.mean(xpl), decimals=2))
            xptBGO.append(np.round(np.mean(xpt), decimals=2))
            archivoFitness.write(f'BGO,{str(np.min(fitness))}\n')

        if graficos:

            fig , ax = plt.subplots()
            ax.plot(iteraciones,div)
            ax.set_title(f'Diversity {mh} \n {problem} run {corrida}')
            ax.set_ylabel("Diversity")
            ax.set_xlabel("Iteration")
            plt.savefig(f'{dirResultado}Graficos/Diversity_{mh}_{problem}_{corrida}.pdf')
            # print('a')
            plt.close('all')
            print(f'Grafico de diversidad realizado {mh} {problem} ')

            fig , ax = plt.subplots()
            ax.plot(iteraciones,fitness)
            ax.set_title(f'Convergence {mh} \n {problem} run {corrida}')
            ax.set_ylabel("Fitness")
            ax.set_xlabel("Iteration")
            plt.savefig(f'{dirResultado}Graficos/Coverange_{mh}_{problem}_{corrida}.pdf')
            plt.close('all')
            print(f'Grafico de covergencia realizado {mh} {problem} ')
            
            figPER, axPER = plt.subplots()
            axPER.plot(iteraciones, xpl, color="r", label=r"$\overline{XPL}$"+": "+str(np.round(np.mean(xpl), decimals=2))+"%")
            axPER.plot(iteraciones, xpt, color="b", label=r"$\overline{XPT}$"+": "+str(np.round(np.mean(xpt), decimals=2))+"%")
            axPER.set_title(f'XPL% - XPT% {mh} \n {problem} run {corrida}')
            axPER.set_ylabel("Percentage")
            axPER.set_xlabel("Iteration")
            axPER.legend(loc = 'upper right')
            plt.savefig(f'{dirResultado}Graficos/Percentage_{mh}_{problem}_{corrida}.pdf')
            plt.close('all')
            print(f'Grafico de exploracion y explotacion realizado para {mh}, problema: {problem}, corrida: {corrida} ')
        
            fig , ax = plt.subplots()
            ax.plot(iteraciones,time)
            ax.set_title(f'Time {mh} \n {problem} run {corrida}')
            ax.set_ylabel("Time")
            ax.set_xlabel("Iteration")
            plt.savefig(f'{dirResultado}Graficos/Time_{mh}_{problem}_{corrida}.pdf')
            plt.close('all')
            print(f'Grafico de covergencia realizado {mh} {problem} ')
        
        
        
        corrida +=1
        
        if corrida == 32:
            corrida = 1
        
        #os.remove('./Resultados/Transitorio/'+nombreArchivo+'.csv')
        
    #archivoResumenFitness.write(f'''{problem},{np.min(fitnessGWO)},{np.round(np.average(fitnessGWO),3)},{np.round(np.std(fitnessGWO),3)},{np.min(fitnessPSA)},{np.round(np.average(fitnessPSA),3)},{np.round(np.std(fitnessPSA),3)},{np.min(fitnessSCA)},{np.round(np.average(fitnessSCA),3)},{np.round(np.std(fitnessSCA),3)},{np.min(fitnessWOA)},{np.round(np.average(fitnessWOA),3)},{np.round(np.std(fitnessWOA),3)},{np.min(fitnessGO)},{np.round(np.average(fitnessGO),3)},{fitnessGO} \n''')
    #archivoResumenTimes.write(f'''{problem},{np.min(timeGWO)},{np.round(np.average(timeGWO),3)},{np.round(np.std(timeGWO),3)},{np.min(timePSA)},{np.round(np.average(timePSA),3)},{np.round(np.std(timePSA),3)},{np.min(timeSCA)},{np.round(np.average(timeSCA),3)},{np.round(np.std(timeSCA),3)},{np.min(timeWOA)},{np.round(np.average(timeWOA),3)},{np.round(np.std(timeWOA),3)},{np.min(timeGO)},{np.round(np.average(timeGO),3)},{np.round(np.std(timeGO),3)} \n''')
    #archivoResumenPercentage.write(f'''{problem},{np.round(np.average(xplGWO),3)},{np.round(np.average(xptGWO),3)},{np.round(np.average(xplPSA),3)},{np.round(np.average(xptPSA),3)},{np.round(np.average(xplSCA),3)},{np.round(np.average(xptSCA),3)},{np.round(np.average(xplWOA),3)},{np.round(np.average(xptGO),3)},{np.round(np.average(xplGO),3)},{np.round(np.average(xptGO),3)} \n''')

    if incluye_gwo:
        archivoResumenFitness.write(f''',{np.min(fitnessGWO)},{np.round(np.average(fitnessGWO),3)},{np.round(np.std(fitnessGWO),3)}''')
        archivoResumenTimes.write(f''',{np.min(timeGWO)},{np.round(np.average(timeGWO),3)},{np.round(np.std(timeGWO),3)}''')
        archivoResumenPercentage.write(f''',{np.round(np.average(xplGWO),3)},{np.round(np.average(xptGWO),3)}''')

    if incluye_go:
        archivoResumenFitness.write(f''',{np.min(fitnessBGO)},{np.round(np.average(fitnessBGO),3)},{np.round(np.std(fitnessBGO),3)}''')
        archivoResumenTimes.write(f''',{np.min(timeBGO)},{np.round(np.average(timeBGO),3)},{np.round(np.std(timeBGO),3)}''')
        archivoResumenPercentage.write(f''',{np.round(np.average(xplBGO),3)},{np.round(np.average(xptBGO),3)}''')

    if incluye_sca:
        archivoResumenFitness.write(f''',{np.min(fitnessSCA)},{np.round(np.average(fitnessSCA),3)},{np.round(np.std(fitnessSCA),3)}''')
        archivoResumenTimes.write(f''',{np.min(timeSCA)},{np.round(np.average(timeSCA),3)},{np.round(np.std(timeSCA),3)}''')
        archivoResumenPercentage.write(f''',{np.round(np.average(xplSCA),3)},{np.round(np.average(xptSCA),3)}''')
        
    if incluye_psa:
        archivoResumenFitness.write(f''',{np.min(fitnessPSA)},{np.round(np.average(fitnessPSA),3)},{np.round(np.std(fitnessPSA),3)}''')
        archivoResumenTimes.write(f''',{np.min(timePSA)},{np.round(np.average(timePSA),3)},{np.round(np.std(timePSA),3)}''')
        archivoResumenPercentage.write(f''',{np.round(np.average(xplPSA),3)},{np.round(np.average(xplPSA),3)}''')
        
    if incluye_woa:
        archivoResumenFitness.write(f''',{np.min(fitnessWOA)},{np.round(np.average(fitnessWOA),3)},{np.round(np.std(fitnessWOA),3)}''')
        archivoResumenTimes.write(f''',{np.min(timeWOA)},{np.round(np.average(timeWOA),3)},{np.round(np.std(timeWOA),3)}''')
        archivoResumenPercentage.write(f''',{np.round(np.average(xplWOA),3)},{np.round(np.average(xplWOA),3)}''')

    blob = bd.obtenerMejoresArchivos(instancia[1],"")
    
    for d in blob:

        nombreArchivo = d[4]
        archivo = d[5]
        print(archivo)

        direccionDestiono = './Resultados/Transitorio/'+nombreArchivo+'.csv'
        util.writeTofile(archivo,direccionDestiono)
        

        data = pd.read_csv(direccionDestiono)
        # print('##################################',direccionDestiono ,data.shape)
        mh = nombreArchivo.split('_')[0]
        if mh == 'GO':
            mh = 'BGO'
        
        problem = nombreArchivo.split('_')[1]

        iteraciones = data['iter']
        fitness     = data['fitness']
        time        = data['time']
        xpl         = data['XPL']
        xpt         = data['XPT']
        
        if mh == 'PSA':
            bestFitnessPSA      = fitness
            bestTimePSA         = time
        if mh == 'SCA':
            bestFitnessSCA      = fitness
            bestTimeSCA         = time
        if mh == 'GWO':
            bestFitnessGWO      = fitness
            bestTimeGWO         = time
        if mh == 'WOA':
            bestFitnessWOA      = fitness
            bestTimeWOA         = time
        if mh == 'BGO':
            bestFitnessBGO      = fitness
            bestTimeBGO         = time


        #os.remove('./Resultados/Transitorio/'+nombreArchivo+'.csv')

    print("------------------------------------------------------------------------------------------------------------")
    figPER, axPER = plt.subplots()
    if incluye_gwo:
        axPER.plot(iteraciones, bestFitnessGWO, color="r", label="GWO")
    if incluye_sca:
        axPER.plot(iteraciones, bestFitnessSCA, color="b", label="SCA")
    if incluye_psa:
        axPER.plot(iteraciones, bestFitnessPSA, color="g", label="PSA")
    if incluye_woa:
        axPER.plot(iteraciones, bestFitnessWOA, color="y", label="WOA")
    if incluye_go:
        axPER.plot(iteraciones, bestFitnessBGO, color="y", label="BGO")
    axPER.set_title(f'Coverage \n {problem}')
    axPER.set_ylabel("Fitness")
    axPER.set_xlabel("Iteration")
    axPER.legend(loc = 'upper right')
    plt.savefig(f'{dirResultado}/Best/fitness_{problem}.pdf')
    plt.close('all')
    print(f'Grafico de fitness realizado {problem} ')
    
    figPER, axPER = plt.subplots()
    axPER.plot(iteraciones, bestTimeGWO, color="r", label="GWO")
    axPER.plot(iteraciones, bestTimeSCA, color="b", label="SCA")
    axPER.plot(iteraciones, bestTimePSA, color="g", label="PSA")
    # axPER.plot(iteraciones, bestTimeWOA, color="y", label="WOA")
    axPER.plot(iteraciones, bestTimeBGO, color="y", label="BGO")
    axPER.set_title(f'Time (s) \n {problem}')
    axPER.set_ylabel("Time (s)")
    axPER.set_xlabel("Iteration")
    axPER.legend(loc = 'lower right')
    plt.savefig(dirResultado+"/Best/time_"+problem+'.pdf')
    plt.close('all')
    print(f'Grafico de time realizado {problem} ')
    
    
    archivoFitness.close()
    
    print("------------------------------------------------------------------------------------------------------------")
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    # datos = pd.read_csv(dirResultado+"/fitness_"+instancia[0].split(".")[0]+'.csv')
    # figFitness, axFitness = plt.subplots()
    # axFitness = sns.boxplot(x='MH', y='FITNESS', data=datos)
    # axFitness.set_title(f'Fitness \n{instancia[0].split(".")[0]}', loc="center", fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
    # axFitness.set_ylabel("Fitness")
    # axFitness.set_xlabel("Metaheuristics")
    # figFitness.savefig(dirResultado+"/boxplot/boxplot_fitness_"+instancia[0].split(".")[0]+'.pdf')
    # plt.close('all')
    # print(f'Grafico de boxplot con fitness para la instancia {instancia[0].split(".")[0]} realizado con exito')
    
    # figFitness, axFitness = plt.subplots()
    # axFitness = sns.violinplot(x='MH', y='FITNESS', data=datos, gridsize=50)
    # axFitness.set_title(f'Fitness \n{instancia[0].split(".")[0]}', loc="center", fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
    # axFitness.set_ylabel("Fitness")
    # axFitness.set_xlabel("Metaheuristics")
    # figFitness.savefig(dirResultado+"/violinplot/violinplot_fitness_"+instancia[0].split(".")[0]+'.pdf')
    # plt.close('all')
    # print(f'Grafico de violines con fitness para la instancia {instancia[0].split(".")[0]} realizado con exito')
    
    # os.remove(dirResultado+"/fitness_"+instancia[0].split(".")[0]+'.csv')
    
    #print("------------------------------------------------------------------------------------------------------------")

    datos = pd.read_csv(dirResultado+"fitness_"+instancia[1]+'.csv')
    figFitness, axFitness = plt.subplots()
    axFitness = sns.boxplot(x='MH', y='FITNESS', data=datos)
    axFitness.set_title(f'Fitness \n{instancia[1]}', loc="center", fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
    axFitness.set_ylabel("Fitness")
    axFitness.set_xlabel("Metaheuristics")
    figFitness.savefig(dirResultado+"/boxplot/boxplot_fitness_"+instancia[1]+'.pdf')
    plt.close('all')
    print(f'Grafico de boxplot con fitness para la instancia {instancia[1]} realizado con exito')
    
    figFitness, axFitness = plt.subplots()
    axFitness = sns.violinplot(x='MH', y='FITNESS', data=datos, gridsize=50)
    axFitness.set_title(f'Fitness \n{instancia[1]}', loc="center", fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
    axFitness.set_ylabel("Fitness")
    axFitness.set_xlabel("Metaheuristics")
    figFitness.savefig(dirResultado+"/violinplot/violinplot_fitness_"+instancia[1]+'.pdf')
    plt.close('all')
    print(f'Grafico de violines con fitness para la instancia {instancia[1]} realizado con exito')
    
    #os.remove(dirResultado+"/fitness_"+instancia[1]+'.csv')
    
    print("------------------------------------------------------------------------------------------------------------")


archivoResumenFitness.close()
archivoResumenTimes.close()
archivoResumenPercentage.close()
        