import json
import os
import sys

#IMPORTANDO CONSOLERESPONSE
sys.path.append(os.path.join(os.path.dirname(__file__), 'data/static'))
#IMPORTANDO CONSOLERESPONSE
from CONSOLE_RESPONSE import Console
console = Console() #meu console

#PARTE QUE IMPORTA ⬇️⬇️⬇️⬇️⬇️⬇️

class TEXT_admin:
    """Instância responsável por gerir todo conteúdo relacionado à texto..."""
    class get:
        """Obtem um valor ou chama o resultado de uma função predefinida..."""
        @staticmethod
        def blacklisted_words(parametro=None):
            """
            Palavras na lista negra, créditos: Fumiko0701, aka CT ❤️

            Args:
                parametro0 (None): Obtém todas as palavras na lista-negra.
                parametro1 (String): Verifica se a string é uma palavra na lista-negra.

            Returns:
                if (None): return list
                if (String): return bool
            """
            def carregar_palavras_ofensivas():
                try:
                    caminho_arquivo = os.path.join(os.path.dirname(__file__), '../../data/blacklisted_words.json')
                    with open(caminho_arquivo, 'r') as blcklistwords:
                        blacklistedWords = json.load(blcklistwords)
                    return blacklistedWords
                except (json.decoder.JSONDecodeError, FileNotFoundError):
                    console.log('empty','blacklisted_words.json')
                    try:
                        caminho_arquivo = os.path.join(os.path.dirname(__file__), '../../data/blacklisted_words.json')
                        with open(caminho_arquivo, 'w') as emptyjson:
                            emptyjson.write("[]")
                        console.log('empty', 'success')
                    except:
                        console.log('empty','fail', 'couldnt_read_or_create_file')
                    return []

            if parametro is None:
                return carregar_palavras_ofensivas()
            else:
                palavras_ofensivas = carregar_palavras_ofensivas()
                mensagemToda = parametro.content if hasattr(parametro, 'content') else parametro #redundancia
                mensagemToda.lower()
                #ESTOU USANDO LOWER() DUAS VEZES COMO FORMA DE GARANTIA...
                mensagemMinuscula = mensagemToda.lower()
                palavrasEmLista = mensagemMinuscula.split()
                for palavra in palavras_ofensivas:
                    if palavra in palavrasEmLista:
                        return True
                return False

    class save:
        """Salva um valor ou efetua uma alteração em uma instância passada atráves de uma função predefinida..."""
        @staticmethod
        def blacklisted_word(palavras, nova_palavra, uid=None):
            #adicionar na lista
            palavraAddNaLista = nova_palavra.lower()
            palavras.append(palavraAddNaLista)
            #salvando no arquivo
            caminho_arquivo = os.path.join(os.path.dirname(__file__), '../../data/blacklisted_words.json')
            with open(caminho_arquivo, 'w') as saving_blacklisted_word:
                json.dump(palavras, saving_blacklisted_word, indent=4)
            if uid != None:
                return console.log('word_blacklist', palavraAddNaLista, uid)
            else:
                return console.log('word_blacklist', palavraAddNaLista)


