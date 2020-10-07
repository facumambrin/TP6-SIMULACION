import random

# condiciones iniciales

HV = 99999999999999999  # todo:check
T = 0
TF = 0  # todo: check

# variables de control
J = 1
E = 1

PORCENTAJE_OCURRENCIA_CABOJATE = 0

############################

TPLL = 0
TPSJ = [HV for i in range(J)]
TPSE = [HV for i in range(E)]

# estado
NSC = 0
NSI = 0
UAJ = ['-' for i in range(J)]  # indica si lo ultimo que atendió el jefe i es CABOTAJE o INTERNACIONAL

# para calculo de resultados
STOE = [0 for i in range(E)]
STOJ = [0 for i in range(J)]
ITOE = [0 for i in range(E)]
ITOJ = [0 for i in range(J)]

# modes: PRE_PANDEMIA, POST_PANDEMIA
mode = 'PRE_PANDEMIA'

# pruebas
NTI = 0
NTC = 0


# funciones accesorias

# todo:check diferencias entre pre y post
def inicializar_variables(m):
    global mode, TF, PORCENTAJE_OCURRENCIA_CABOJATE
    mode = m
    if m == 'PRE_PANDEMIA':
        TF = 4000000
        PORCENTAJE_OCURRENCIA_CABOJATE = 0.45

    else:
        TF = 5000000
        PORCENTAJE_OCURRENCIA_CABOJATE = 0.20


def buscar_menor_TPS(tps):
    v_min = HV
    indice = 0
    for i, v in enumerate(tps):
        if v <= v_min:
            v_min = v
            indice = i
    return indice


def buscar_libre(tps):
    libres = [i for i, v in enumerate(tps) if v == HV]
    return libres[0] if len(libres) else 0  # el primero que este libre, si no el primero


# def get_IA():
#     R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
#     if mode == 'PRE_PANDEMIA':
#         try:
#             # r = 4.6985 * (((1 / ((1 - R1) ** 1.06019)) - 1) ** 0.3146039136726861) antes
#             r = 6.9268 * (((1 / ((1 - R1) ** 0.468033)) - 1) ** 0.3658848926127840)
#             return r
#         except ZeroDivisionError:
#             return 0.99
#
#     else:  # POST_PANDEMIA
#         try:
#             r = 318.58 * (((1 / ((1 - R1) ** 0.0034559)) - 1) ** 0.4614887627486271)
#             return r
#         except ZeroDivisionError:
#             return 0.99
#
#
# def get_TAE():
#     R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
#     if mode == 'PRE_PANDEMIA':
#         try:
#             r = 45.789 * (((1 / ((1 - R1) ** 0.0488377)) - 1) ** 0.3133028385237170)
#             return r
#         except ZeroDivisionError:
#             return 0.99
#
#     else:  # POST_PANDEMIA
#         try:
#             r = 129.61 * (((1 / ((1 - R1) ** 0.00279955)) - 1) ** 0.3482379161443098)
#             return r
#         except ZeroDivisionError:
#             return 0.99
#
#
# def get_TAJ():
#     R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
#     if mode == 'PRE_PANDEMIA':
#         try:
#             r = 23.229 * (((1 / ((1 - R1) ** 0.32924)) - 1) ** 0.3109549426288131)
#             return r
#         except ZeroDivisionError:
#             return 0.99
#
#     else:  # POST_PANDEMIA
#         try:
#             r = 13.618 * (((1 / ((1 - R1) ** 0.991375)) - 1) ** 0.2445466105839773)
#             return r
#         except ZeroDivisionError:
#             return 0.99

def get_IA():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if R1 == 1.0:
        return 0.99
    else:
        if mode == 'PRE_PANDEMIA':
            return 6.9268 * (((1 / ((1 - R1) ** 0.468033)) - 1) ** 0.3658848926127840)
        else:
            return 318.58 * (((1 / ((1 - R1) ** 0.0034559)) - 1) ** 0.4614887627486271)


def get_TAE():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if R1 == 1.0:
        return 0.99
    else:
        if mode == 'PRE_PANDEMIA':
            return 45.789 * (((1 / ((1 - R1) ** 0.0488377)) - 1) ** 0.3133028385237170)
        else:
            return 13.618 * (((1 / ((1 - R1) ** 0.991375)) - 1) ** 0.2445466105839773)


def get_TAJ():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if R1 == 1.0:
        return 0.99
    else:
        if mode == 'PRE_PANDEMIA':
            return 23.229 * (((1 / ((1 - R1) ** 0.32924)) - 1) ** 0.3109549426288131)
        else:
            return 318.58 * (((1 / ((1 - R1) ** 0.0034559)) - 1) ** 0.4614887627486271)


def llegada():
    global T, TPLL, NSI, NSC, STOE, STOJ, NTI, NTC, TPSJ, TPSE
    T = TPLL
    # print(f'T: {T}')
    IA = get_IA()
    TPLL = TPLL + IA
    r = random.random()
    if r <= PORCENTAJE_OCURRENCIA_CABOJATE:
        # cabotaje
        NSC += 1
        NTC += 1
        if NSC <= E:
            # atiende empleado
            jj = buscar_libre(TPSE)
            STOE[jj] += T - ITOE[jj]
            TAE = get_TAE()
            TPSE[jj] = T + TAE
        else:
            ii = buscar_libre(TPSJ)
            if TPSJ[ii] == HV:
                # atiende jefe
                STOJ[ii] += T - ITOJ[ii]
                TAJ = get_TAJ()
                TPSJ[ii] = T + TAJ
                UAJ[ii] = 'C'
    else:
        # internacional
        NSI += 1
        NTI += 1
        ii = buscar_libre(TPSJ)
        if NSI <= J and TPSJ[ii] == HV:
            STOJ[ii] += T - ITOJ[ii]
            TAJ = get_TAJ()
            TPSJ[ii] = T + TAJ
            UAJ[ii] = 'I'


def salida_jefe(ind):
    global T, NSI, NSC, ITOJ, TPSJ, UAJ
    T = TPSJ[ind]
    if UAJ[ind] == 'C':
        # atendió un cabotaje anteriormente
        NSC -= 1
    else:
        NSI -= 1

    if NSI >= J:
        # hay internacional para atender
        TAJ = get_TAJ()
        TPSJ[ind] = T + TAJ
        UAJ[ind] = 'I'
    else:
        if NSC >= E:
            # atiende cabotaje
            TAJ = get_TAJ()
            TPSJ[ind] = T + TAJ
            UAJ[ind] = 'C'
        else:
            # tampoco hay de cabotaje para atender
            ITOJ[ind] = T
            TPSJ[ind] = HV


def salida_empleado(ind):
    global T, NSC, ITOE, TPSE
    T = TPSE[ind]
    NSC -= 1
    if NSC >= E:
        TAE = get_TAE()
        TPSE[ind] = T + TAE
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


def prueba():
    print(f'NSC: {NSC}')
    print(f'NSI: {NSI}')
    print(f'NTI: {NTI}')
    print(f'NTC: {NTC}')


def simulacion(m):
    inicializar_variables(m)
    print(f'Comienza simulacion...modo:{m}')
    while T <= TF:
        i = buscar_menor_TPS(TPSJ)
        j = buscar_menor_TPS(TPSE)

        if TPSJ[i] <= TPSE[j]:
            if TPSJ[i] <= TPLL:
                salida_jefe(i)
            else:
                llegada()
        else:
            if TPSE[j] <= TPLL:
                salida_empleado(j)
            else:
                llegada()

    print('finaliza simulacion...')
    mostrar_resultados()
    prueba()


# comienzo simulacion
# simulacion('PRE_PANDEMIA')
simulacion('POST_PANDEMIA')
