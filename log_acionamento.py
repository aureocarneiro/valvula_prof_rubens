#!/usr/bin/python
# -*- coding: utf-8 -*-

# importando os módulos necessários
from epics import PV, caput
import time
import sys

# criando so objetos que irão monitorar as PVs de pressão
leit_1 = PV('VAC:int1-RB')
leit_2 = PV('VAC:int2-RB')

# criando os objetos de pv de acionamento das válvulas
acio_1 = PV('VAC:rele0')
acio_2 = PV('VAC:rele1')

# criando os objetos de pv de chaves de fim de curso
chave_open = PV('VAC:memoria4')
chave_close = PV('VAC:memoria5')

# definindo o limite no nível de vácuo
limite = -7

# definindo variáveis de PV
rele0 = 'VAC:rele0'
rele1 = 'VAC:rele1'
rele2 = 'VAC:rele2'
rele3 = 'VAC:rele3'
pressao = 'VAC:int1-RB'
pressao = 'VAC:int2-RB'
memoria0 = 'VAC:memoria0'
memoria1 = 'VAC:memoria1'
memoria2 = 'VAC:memoria2'
memoria3 = 'VAC:memoria3'
memoria4 = 'VAC:memoria4'
memoria5 = 'VAC:memoria5'
entrada0 = 'VAC:entrada0'
entrada1 = 'VAC:entrada1'
entrada4 = 'VAC:entrada4'
entrada5 = 'VAC:entrada5'

# definindo estado 
state = 0

# definindo sinais
up = 1
down = 0 

# definindo tempo de duty cicle
dutycycle = 0.5

# loop principal
while (1):

    # pré configuração inicial
    state0 = 0
    state1 = 0
    caput('VAC:memoria0', 0)
    caput('VAC:memoria1', 0)

    # if para verificar o estado do sistema

    # estado de abertura da valvula
    while(leit_1.value <= limite and leit_2.value <= limite and chave_open.value == 1):
        # acoes a serem tomadas no estado
        state0 = 1
        state1 = 0
        #caput(memoria0,state0)
        #caput(memoria1,state1)

    
    # estado de fechamento da valvula
    while(leit_1.value > limite or leit_2.value > limite and chave_open.value == 1):
        # acoes a serem tomadas no estado 
        caput('VAC:memoria1',1)
        caput('VAC:memoria0',0)


