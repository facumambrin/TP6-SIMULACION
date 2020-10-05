import random

# condiciones iniciales

HV = 99999999999999999  # todo:check
T = 0
TF = 1000  # todo: check

# variables de control
J = 1
E = 3

############################
# 'I': atendió un internacional. 'C': atendió un cabotaje
atencion_jefes = ['A' for i in range(J)]

TPLL = 0
TPSJ = [0 for i in range(J)]
TPSE = [0 for i in range(E)]

NSC = 0
NSI = 0
NT = 0

STLL = 0
STSE = [0 for i in range(E)]
STSJ = [0 for i in range(J)]
STOE = [0 for i in range(E)]
STOJ = [0 for i in range(J)]
STAE = [0 for i in range(E)]
STAJ = [0 for i in range(E)]
ITOE = [0 for i in range(E)]
ITOJ = [0 for i in range(J)]

modes = {
    'PRE_PANDEMIA': 0,
    'POST_PANDEMIA': 1
}

# modes: PRE_PANDEMIA, POST_PANDEMIA

mode = 'PRE_PANDEMIA'


# funciones accesorias

# todo:check diferencias entre pre y post
def inicializar_variables(m):
    global mode, T
    mode = m
    if m == 'PRE_PANDEMIA':
        T = 300

    else:
        T = 200


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
        return 4.6985 * (((1 / ((1 - R1) ** 1.06019)) - 1) ** 0.31406039136726861)

    else:  # POST_PANDEMIA
        return 318.58 * (((1 / ((1 - R1) ** 0.0034559)) - 1) ** 0.4614887627486271)


def get_TAE():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if mode == 'PRE_PANDEMIA':
        return 45.789 * (((1 / ((1 - R1) ** 0.0488377)) - 1) ** 0.3133028385237170)

    else:  # POST_PANDEMIA
        return 129.61 * (((1 / ((1 - R1) ** 0.00279955)) - 1) ** 0.3482379161443098)


def get_TAJ():
    R1 = float('{:.2f}'.format(random.random()))  # only two decimals of random
    if mode == 'PRE_PANDEMIA':
        return 23.229 * (((1 / ((1 - R1) ** 0.32924)) - 1) ** 0.3109549426288131)

    else:  # POST_PANDEMIA
        return 13.618 * (((1 / ((1 - R1) ** 0.991375)) - 1) ** 0.2445466105839773)


def llegada():
    global T, E, TPLL, NT, NSI, STLL, NSC, STOE, STOJ
    T = TPLL
    IA = get_IA()
    TPLL = TPLL + IA
    NT += 1
    STLL += T
    r = random.random()
    if r <= 0.45:
        # cabotaje
        NSC += 1
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
        if NSI <= J:
            ii = buscar_libre(TPSJ)
            STOJ[ii] += T - ITOJ[ii]
            TAJ = get_TAJ()
            TPSJ[ii] = T + TAJ
            atencion_jefes[ii] = 'I'


def salida_jefe(ind):
    global T, E, TPLL, NT, NSI, STLL, NSC, STOE, STOJ
    T = TPSJ[ind]
    STSJ[ind] += T
    if atencion_jefes[ind] == 'C':
        # atendió un cabotaje anteriormente
        NSC -= 1
    else:
        NSI -= 1
    if NSC >= J:
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
    global T, E, TPLL, NT, NSI, STLL, NSC, STOE, STOJ
    T = TPSE[ind]
    STSE[ind] += T
    NSC -= NSC
    if NSC >= E:
        TAE = get_TAE()
        TPSE[ind] = T + TAE
        STAE[ind] += TAE
    else:
        ITOE[ind] = T
        TPSE[ind] = HV


def simulacion(m):
    inicializar_variables(m)
    while T <= TF:
        i = buscar_menor_TPS(TPSJ)
        j = buscar_menor_TPS(TPSE)

        if TPLL <= TPSJ[i] and TPLL <= TPSE[j]:
            llegada()
        else:
            if TPSJ[i] <= TPSE[j]:
                salida_jefe(i)
            else:
                salida_empleado(j)


# comienzo simulacion
simulacion('PRE_PANDEMIA')
# simulacion('POST_PANDEMIA')
