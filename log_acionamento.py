#!/usr/bin/python
# -*- coding: utf-8 -*-

# importando os módulos necessários
from epics import camonitor, PV, caput
import time
import sys

# criando so objetos que irão monitorar as PVs de pressão
leit_1 = PV('VAC:int1-RB')
leit_2 = PV('VAC:int2-RB')

# criando os objetos de pv de acionamento das válvulas
acio_1 = PV('VAC:rele0')
acio_2 = PV('VAC:rele1')

# definindo o limite no nível de vácuo
limite = -7

# definindo variáveis de PV
rele0 = 'VAC:rele0'
rele1 = 'VAC:rele1'
pressao = 'VAC:int1-RB'
pressao = 'VAC:int2-RB'

# definindo estado 
estado = 'fechado'

# loop principal
while (1):

    # if para verificar o estado do sistema

    # estado de abertura da valvula
    if (leit_1.value <= limite and leit_2.value <= limite):
        # acoes a serem tomadas no estado 
        caput(rele0,1)
        caput(rele1,0)
        # tempo de espera do pulso necessario para abertura da valvula
        # futuramente substituir para o sensor  de fim de curso da valvula
        time.sleep(2)
        caput(rele0,0)

    
    # estado de fechamento da valvula
    elif ((leit_1.value > limite or leit_2.value > limite)):
        # acoes a serem tomadas no estado
        caput(rele0,0)
        caput(rele1,1)
        # tempo de espera do puldo necessario para fechamento da valvula
        # futuramente substituir para o sensor de fim de curso da valvula
        time.sleep(2)
        caput(rele1,0)


