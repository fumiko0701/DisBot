#código para mudar as configs
import json
import os
from CONSOLE_RESPONSE import Console

console = Console() #meu console


# TODO: CÓDIGO DE MUDAR AS CONFIGURAÇÕES DEVERÁ SER FEITO NESSA PÁGINA
def getPrefix():
    """Obtem o prefixo atual do Bot, salvo através da settings.json"""
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'settings.json')
    with open(caminho_arquivo, 'r') as settings_file:
        settings = json.load(settings_file)
        return settings.get('prefix', 'plz')


def setPrefix(prefix, uid, ownerID, settings):
    """Define o prefixo atual do Bot, salvo através da settings.json
    
    Verifica se UID = OWNERID, para efetuar a devida alteração
    Lê settings para obter its.'prefix'"""
    if uid == ownerID:     
        try:
            settings['prefix'] = prefix #peguei a chave prefix do json passado.
            
            caminho_arquivo = os.path.join(os.path.dirname(__file__), 'settings.json')
            with open(caminho_arquivo, 'w') as settings_file:
                json.dump(settings, settings_file, indent=4)

            return True, prefix  #retorna True e o novo prefixo
        except Exception as e:
            return print(f"Erro ao tentar setar prefixo!: {e}")
    else:
        return False, None  #retorna False e None (nenhum novo prefixo)

class MAIN_Color:
    rgb_color = (229, 23, 23)  # Red color
    hex_color = int(''.join(f'{value:02x}' for value in rgb_color), 16)
    

class CommandList:
    def __init__(self):

        current_directory = os.path.dirname(__file__)
        
        self.file_path = os.path.join(current_directory, '..', 'commandlist.json') #um diretorio acima

    def check(self, key, item):
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            if key in data and item in data[key]:
                return  # O item já existe na chave
            data.setdefault(key, []).append(item)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

