import json
import os


def get_settings():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    caminho_settings = os.path.join(root_dir, 'data', 'static', 'settings.json')
    with open(caminho_settings, 'r') as settings_file:
        settings = json.load(settings_file)
    settings['ownerID'] = int(settings['ownerID'])  # Convertendo ownerID para inteiro
    return settings


from CONSOLE_RESPONSE import Console
console = Console()

# TODO: CÓDIGO DE MUDAR AS CONFIGURAÇÕES DEVERÁ SER FEITO NESSA PÁGINA
def setPrefix(prefix, uid, ownerID):
    if uid == ownerID:
        old_prefix = getPrefix()
        try:
            settings = get_settings()  # Carregar as configurações
            settings['prefix'] = prefix  # Atualizar o prefixo nas configurações
            
            # Salvar as configurações de volta no arquivo settings.json
            caminho_settings = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'static', 'settings.json'))
            with open(caminho_settings, 'w') as settings_file:
                json.dump(settings, settings_file, indent=4)
            
            return True, prefix  # Retorna True e o novo prefixo
        except Exception as e:
            print(f"Erro ao tentar setar prefixo!: {e}")
            return False, None
    else:
        print("Permissão negada: Apenas o dono pode usar esse comando!")
        return False, None


def getPrefix():
    """Obtem o prefixo atual do Bot, salvo através da settings.json"""
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'settings.json')
    with open(caminho_arquivo, 'r') as settings_file:
        settings = json.load(settings_file)
        return settings.get('prefix', 'plz')




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

