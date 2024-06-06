import re

def objetos():
    return {"Arruelas":[], "Parafusos":[], "Porcas":[]}

def ler_arquivo(result):
    dados = []
    with open(result, 'r') as arquivo:
        for linha in arquivo:
   
            # 0: Imagem
            # 1: Velocidade

            if linha[0] == 'i':
                lista = linha.strip().split('/')
                lista.insert(0, 0)
                dados.append(lista)
            elif linha[0] == 'S':
                lista = linha.strip().split('/')
                lista.insert(0, 1)
                dados.append(lista)

            #dados.append(linha.strip().split(' '))

    return dados

def key(valor):
    key = valor
    if key == "Img_Amb":
        key = "Ambiente"
        
    elif key == "Img_50-50":
        key = "Config_50-50"
    elif key == "Img_50-100":
        key = "Config_50-100"
    elif key == "Img_100-50":
        key = "Config_100-50"
    elif key == "Img_100-100":
        key = "Config_100-100"
    elif key == "Img_100-0":
        key = "Config_100-0"
    elif key == "Img_R&B":
        key = "Config_R&B"
    else:
        key = "Config_R"
    
    return key
    
def organiza(valor):

    return re.sub('1088x1920 ', '', valor)
    
def separa_dados(valor, ilu):
    key_ext = key(valor[9])
    key_int = valor[10]
    caminho = valor[11].split(' ')
    classe, velocidade = str, str
    
    if len(caminho) > 5:
        final = re.split(r'[:,]', valor[11])
        if len(final) > 3:
            classe = 'more detections'
            velocidade = ""
        else:
            classe = final[1].strip()
            velocidade = final[2]
            
    else:
        classe = 'no detection'
        velocidade = caminho[len(caminho)-1]
    
    #print(len(caminho)) ====> (> 5 para ok || <= 5 para no detection)
    if classe == ('no detection' or 'more detections'):
        classe_velocidade = " ".join([classe, velocidade])
    else:
        classe_velocidade = " ".join([organiza(classe), velocidade])
 
    ilu[key_ext][key_int].append(classe_velocidade)

def organiza_print(dicionario_objetos):
    cont = 0
    for config, objeto in dicionario_objetos.items():
        print(f'======{config}======')
        for nome, resultado in objeto.items():
            print(f'{nome}:')
            for i in resultado:
                print(i)
                cont += 1

        #print(f'{config}:{objeto}')
    print(cont)
    
def dados_slurm():
    result = "slurm-395780.out"
    dados = ler_arquivo(result)

    #dicionário de todos os objetos de analise separadas por tipo + velocidade do processo geral
    #objetos = {"Arruelas":[], "Parafusos":[], "Porcas":[], "Velocidade":[]}

    #Dicionário para separar os objetos por iluminação
    iluminacao = {"Ambiente":objetos(), 
                  "Config_50-100":objetos(), 
                  "Config_50-50":objetos(), 
                  "Config_100-50":objetos(), 
                  "Config_100-100":objetos(),
                  "Config_100-0":objetos(), 
                  "Config_R&B":objetos(), 
                  "Config_R":objetos()
                  }

    #Lista para separar os dados de velocidade por iluminação
    velocidade = []
    
    #Lembrar que para preencher do jeito que eu quero, precisa ser o seguinte:
    # -> Um dicionário com os campos de iluminação
    # -> Que contém mais um dicionário para separar entre os tipos e velocidade (porcas, arruelas, parafusos)
    # -> Cada uma dessa chaves do dicionário interno deve ser uma lista que contém as informações de: classe e velocidade de processamento
    
    for i in range(len(dados)):
        #print(valor)
        if dados[i][0] == 0:
            separa_dados(dados[i], iluminacao)
        elif dados[i][0] == 1:
            #define_vel(valor, iluminacao)
            pass #Preciso definir isso meelhor! Achar um método para colocar a velocidade na posição correta
    
    #print(len(iluminacao["Config_100-50"]['Parafusos']))

    #for valor in iluminacao["Config_100-50"]['Parafusos']:
     #   print(valor)
    return iluminacao

def ler_arquivo_corretos(caminho):
    dados = {'Arruelas':[], 'Parafusos':[], 'Porcas':[]}

    with open(caminho, 'r') as arquivo:
        tipo = str
        for linha in arquivo:
            if linha.strip().split(':')[0] == "Tipo":
                tipo = str(linha.strip().split(':')[1])
            else:
                dados[tipo].append(linha.strip().split(':')[1] )
    
    return dados

#======Para Matriz de Confusão======

#Função que organiza os dados esperados
def dados_corretos():
    dados_corretos = ler_arquivo_corretos("dados_corretos.out")

    dados_corretos_final = {'Arruelas':[], 'Parafusos':[], 'Porcas':[]}
    dados_corretos_final_2 = {'Arruelas':[], 'Parafusos':[], 'Porcas':[]}

    for key, _ in dados_corretos.items():
        for vint in dados_corretos[key]:
            dados_corretos_final_2[key].append(str(vint))
            for _ in range(5): #melhorar isso daqui, seria melhor remver esse for
                dados_corretos_final[key].append(str(vint))
            

    return (dados_corretos_final, dados_corretos_final_2)

#Função exepcionalmente para a configuração 100-50
def dados_corretos_100_50():
    dados = dados_corretos()

    for i in range(20, 25):
        dados[0]['Parafusos'][i] = "Parafuso de cabeca chata com sextavado interno"
        
    dados[1]['Parafusos'][4] = "Parafuso de cabeca chata com sextavado interno"
    for i in range(25, 30):
        dados[0]['Parafusos'][i] = "Parafuso sem cabeca com sextavado interno e com ponta concava"

    dados[1]['Parafusos'][5] = "Parafuso sem cabeca com sextavado interno e com ponta concava"

    return dados

#Função que organiza os dados obtidos
def dados_obtidos():
    dados_obtidos_final = {"Ambiente":objetos(), 
                  "Config_50-100":objetos(), 
                  "Config_50-50":objetos(), 
                  "Config_100-50":objetos(), 
                  "Config_100-100":objetos(),
                  "Config_100-0":objetos(), 
                  "Config_R&B":objetos(), 
                  "Config_R":objetos()}

    data_set = dados_slurm()

    for config, objeto in data_set.items():
        for key, _ in objeto.items():
            for vint in objeto[key]:
                nome = vint.strip().split('  ')[0]
                nome2 = nome.replace("1 ", "", 1)
                dados_obtidos_final[config][key].append(str(nome2)) #veja isso daqui

    return dados_obtidos_final
    
# dados_corretos()
# dados_corretos_100_50()
# dados_obtidos()
# main()
