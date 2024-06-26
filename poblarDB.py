from BD.sqlite import BD
import json

bd = BD()


scp = True
ben = False
mhs = ['BGO','GWO','PSA','SCA']
cantidad = 0

DS_actions = [
    'V1-STD', 'V1-COM', 'V1-PS', 'V1-ELIT',
    'V2-STD', 'V2-COM', 'V2-PS', 'V2-ELIT',
    'V3-STD', 'V3-COM', 'V3-PS', 'V3-ELIT',
    'V4-STD', 'V4-COM', 'V4-PS', 'V4-ELIT',
    'S1-STD', 'S1-COM', 'S1-PS', 'S1-ELIT',
    'S2-STD', 'S2-COM', 'S2-PS', 'S2-ELIT',
    'S3-STD', 'S3-COM', 'S3-PS', 'S3-ELIT',
    'S4-STD', 'S4-COM', 'S4-PS', 'S4-ELIT',
]

paramsML = json.dumps({
    'MinMax'        : 'min',
    'DS_actions'    : DS_actions,
    'gamma'         : 0.4,
    'policy'        : 'e-greedy',
    'qlAlphaType'   : 'static',
    'rewardType'    : 'withPenalty1',
    'stateQ'        : 2
})

if scp:
    # poblar ejecuciones SCP
    instancias = bd.obtenerInstancias(f'''
                                      'scpnrh2','scpnrh4','scpnrh5'
                                      ''')
    print(instancias)
    iteraciones = 30
    experimentos = 31
    poblacion = 40
    for instancia in instancias:

        for mh in mhs:
            data = {}
            data['MH']          = mh
            data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)},DS:V3-ELIT,repair:complex,cros:0.9;mut:0.20'
            data['ML']          = ''
            data['paramML']     = ''
            data['ML_FS']       = ''
            data['paramML_FS']  = ''
            data['estado']      = 'pendiente'

            cantidad +=experimentos
            bd.insertarExperimentos(data, experimentos, instancia[0])
            
if ben:
    # poblar ejecuciones Benchmark
    instancias = bd.obtenerInstancias(f'''
                                      'F3'
                                      ''')
    iteraciones = 1000
    experimentos = 1
    poblacion = 40
    for instancia in instancias:
        for mh in mhs:
            data = {}
            data['MH']          = mh
            data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)}'
            data['ML']          = ''
            data['paramML']     = ''
            data['ML_FS']       = ''
            data['paramML_FS']  = ''
            data['estado']      = 'pendiente'

            cantidad +=experimentos
            bd.insertarExperimentos(data, experimentos, instancia[0])

print("------------------------------------------------------------------")
print(f'Se ingresaron {cantidad} experimentos a la base de datos')
print("------------------------------------------------------------------")

