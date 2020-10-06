import random

# condiciones iniciales

HV = 99999999999999999  # todo:check
T = 0
TF = 0  # todo: check

# variables de control
J = 2
E = 3

############################
# 'I': atendió un internacional. 'C': atendió un cabotaje
atencion_jefes = ['A' for i in range(J)]

TPLL = 0
TPSJ = [HV for i in range(J)]
TPSE = [HV for i in range(E)]

NSC = 0
NSI = 0
NT = 0
NTI = 0  # total de compradores internacionales que entraron al sistema
NTC = 0  # total de compradores de cabotaje que entraron al sistema

STLLI = 0
STLLC = 0
STSC = 0
STSI = 0
STOE = [0 for i in range(E)]
STOJ = [0 for i in range(J)]
STAE = [0 for i in range(E)]
STAJ = [0 for i in range(E)]
ITOE = [0 for i in range(E)]
ITOJ = [0 for i in range(J)]


# modes: PRE_PANDEMIA, POST_PANDEMIA
mode = 'PRE_PANDEMIA'


# funciones accesorias

# todo:check diferencias entre pre y post
def inicializar_variables(m):
    global mode, TF
    mode = m
    if m == 'PRE_PANDEMIA':
        TF = 100000

    else:
        TF = 100000


def buscar_menor_TPS(tps):
    v_min = HV
    indice = 0
    for i, v in enumerate(tps):
        if v < v_min:
            v_min = v
            indice = i
    return indice


def buscar_libre(tps):
    libres = [i for i, v in enumerate(tps) if v == HV]
    return libres[0] if len(libres) else 0  # el primero que este libre, si no el primero


def get_IA():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if mode == 'PRE_PANDEMIA':
        try:
            r = 4.6985 * (((1 / ((1 - R1) ** 1.06019)) - 1) ** 0.3146039136726861)
            return r
        except ZeroDivisionError:
            return 0.99

    else:  # POST_PANDEMIA
        try:
            r = 318.58 * (((1 / ((1 - R1) ** 0.0034559)) - 1) ** 0.4614887627486271)
            return r
        except ZeroDivisionError:
            return 0.99


def get_TAE():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if mode == 'PRE_PANDEMIA':
        try:
            r = 45.789 * (((1 / ((1 - R1) ** 0.0488377)) - 1) ** 0.3133028385237170)
            return r
        except ZeroDivisionError:
            return 0.99

    else:  # POST_PANDEMIA
        try:
            r = 129.61 * (((1 / ((1 - R1) ** 0.00279955)) - 1) ** 0.3482379161443098)
            return r
        except ZeroDivisionError:
            return 0.99


def get_TAJ():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if mode == 'PRE_PANDEMIA':
        try:
            r = 23.229 * (((1 / ((1 - R1) ** 0.32924)) - 1) ** 0.3109549426288131)
            return r
        except ZeroDivisionError:
            return 0.99

    else:  # POST_PANDEMIA
        try:
            r = 13.618 * (((1 / ((1 - R1) ** 0.991375)) - 1) ** 0.2445466105839773)
            return r
        except ZeroDivisionError:
            return 0.99


def llegada():
    global T, E, TPLL, NT, NSI, STLL, NSC, STOE, STOJ, STLLC, STLLI, NTI, NTC
    T = TPLL
    IA = get_IA()
    TPLL = TPLL + IA
    NT += 1
    r = random.random()
    if r <= 0.45:
        # cabotaje
        NSC += 1
        NTC += 1
        STLLC += T
        if NSC <= E:
            # atiende empleado
            jj = buscar_libre(TPSE)
            STOE[jj] += T - ITOE[jj]
            TAE = get_TAE()
            TPSE[jj] = T + TAE
            STAE[jj] = STAE[jj] + TAE
        else:
            ii = buscar_libre(TPSJ)
            if TPSJ[ii] == HV:
                # atiende jefe
                STOJ[ii] += T - ITOJ[ii]
                TAJ = get_TAJ()
                TPSJ[ii] = T + TAJ
                STAJ[ii] += TAJ
                atencion_jefes[ii] = 'C'
    else:
        # internacional
        NSI += 1
        NTI += 1
        STLLI += T
        if NSI <= J:
            ii = buscar_libre(TPSJ)
            STOJ[ii] += T - ITOJ[ii]
            TAJ = get_TAJ()
            TPSJ[ii] = T + TAJ
            atencion_jefes[ii] = 'I'


def salida_jefe(ind):
    global T, E, TPLL, NT, NSI, STLL, NSC, STOE, STOJ, STSC, STSI
    T = TPSJ[ind]
    if atencion_jefes[ind] == 'C':
        # atendió un cabotaje anteriormente
        NSC -= 1
        STSC += T
    else:
        NSI -= 1
        STSI += T
    if NSI >= J:
        # hay internacional para atender
        TAJ = get_TAJ()
        TPSJ[ind] = T + TAJ
        STAJ[ind] += TAJ
    else:
        if NSC >= E:
            # atiende cabotaje
            TAJ = get_TAJ()
            TPSJ[ind] = T + TAJ
            STAJ[ind] += TAJ
        else:
            # tampoco hay de cabotaje para atender
            ITOJ[ind] = T
            TPSJ[ind] = HV


def salida_empleado(ind):
    global T, E, TPLL, NT, NSI, STLL, NSC, STOE, STOJ, STSC
    T = TPSE[ind]
    STSC += T
    NSC -= NSC
    if NSC >= E:
        TAE = get_TAE()
        TPSE[ind] = T + TAE
        STAE[ind] += TAE
    else:
        ITOE[ind] = T
        TPSE[ind] = HV


def mostrar_resultados():
    print('MOSTRANDO RESULTADOS')

    print('JEFES----------------------------------------')
    for i in range(J):
        print(f'PORCENTAJE TIEMPO OCIOSO DEL JEFE {i}: {(STOJ[i] / T) * 100}')

    print('EMPLEADOS------------------------------------')
    for i in range(E):
        print(f'PORCENTAJE TIEMPO OCIOSO DEL EMPLEADO {i}: {(STOE[i] / T) * 100}')
        print('------------')

    print('CLIENTES CABOTAJE----------------------------')
    print(f'PROMEDIO TIEMPO DE ESPERA DE COMPRADORES CABOTAJE: {(STSC - STLLC) / NTC}')

    print('CLIENTES INTERNACIONAL-----------------------')
    print(f'PROMEDIO TIEMPO DE ESPERA DE COMPRADORES INTERNACIONAL: {(STSI - STLLI) / NTI}')


def prueba():
    print(f'NSC: {NSC}')
    print(f'NSI: {NSI}')


def simulacion(m):
    inicializar_variables(m)
    print(f'Comienza simulacion...modo:{m}')
    while T <= TF:
        i = buscar_menor_TPS(TPSJ)
        j = buscar_menor_TPS(TPSE)

        if TPLL <= TPSJ[i] and TPLL <= TPSE[j]:  # todo: check OR instead of AND
            llegada()
        else:
            if TPSJ[i] <= TPSE[j]:
                salida_jefe(i)
            else:
                salida_empleado(j)

    print('finaliza simulacion...')
    mostrar_resultados()
    prueba()


# comienzo simulacion
simulacion('PRE_PANDEMIA')
#simulacion('POST_PANDEMIA')
