from organizando_dados import *

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

#Seaborn
import seaborn as sns
# ===== Resultados gerais separados por iluminação =====

def organiza_resultado_Piluminacao(dicionario_objetos):
    cont_acertos = 0
    cont_erros = 0
    cont_nd = 0
    cont = 0

    for config, objeto in dicionario_objetos.items():
        
        for nome, resultado in objeto.items():
            #print(f'{nome}:')
            if nome == 'Arruelas':
                for i in resultado:
                    if 'no detection' in i:
                        cont_nd +=1
                        cont +=1
                        #print(i)
                    elif ("Porca" or "Parafuso") in i:
                        cont_erros +=1
                        cont +=1
                        #print(i)
                    elif (i.count("Arruela") or i.count("Abracadeira")) == 1:
                        #print(i)
                        cont +=1
                        cont_acertos +=1
                    elif (i.count("Arruela") or i.count("Abracadeira")) != 1:
                        #print(i)
                        cont +=1
                        cont_erros +=1

    print(f'Número de casos para as 8 iluminações: {cont}')

    return (cont_acertos, cont_erros, cont_nd)
            
def confusion_matrix_v2(x_label, y_label, config, tipo):
    mc_arruelas_amb = np.zeros([len(y_label[1][tipo]), len(y_label[1][tipo])], float)
    mc_valores_absolutos = np.zeros([len(y_label[1][tipo]), len(y_label[1][tipo])], int)

    cont_percent = 0
    cont_j = 0
    coluna = 0
  
    for i, val_x in enumerate(y_label[1][tipo]):
        for j, val_y in enumerate(x_label[config][tipo]):
            cont_j +=1
            if val_x == val_y:
                cont_percent += 1
            if cont_j%5 == 0: 
                mc_arruelas_amb[i][coluna] = cont_percent/5 
                mc_valores_absolutos[i][coluna] = cont_percent
                cont_percent = 0
                coluna +=1
                if coluna == len(x_label[config][tipo])/5: coluna = 0

    return mc_arruelas_amb, mc_valores_absolutos

def valores_metricas(matriz_inteiros): 
    VP = 0 #São os casos em que a classe foi corretamente identificada como ela mesma.
    FN = 0 #São os casos em que a classe foi incorretamente identificada como outra classe (erros de omissão).
    FP = 0 #São os casos em que uma classe foi incorretamente identificada como outra classe.
    VN = 0 #São os casos em que as outras classes foram corretamente identificadas como não sendo a classe de interesse.
    

    tam_real = np.power(len(matriz_inteiros[1]), 2) * 5

    for i in range(len(matriz_inteiros[1])):
        VP += matriz_inteiros[i, i]
        FN += 5 - matriz_inteiros[i,i]
        FP += sum(matriz_inteiros[i,:]) - matriz_inteiros[i,i]
    
    VN = tam_real - VP - FP - FN

    precisao = VP/(VP + FP)
    evocacao = VP/(VP+FN)
    acuracia = (VP + VN)/(VP + FN + FP + VN)
        

    return (precisao, evocacao, acuracia)

