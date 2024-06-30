import os
import re
import sys
from datetime import datetime
from colorama import Fore, Style

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from UTILS import get_settings

settings = get_settings()
ownerID = settings['ownerID']

class Console:
    """Instância responsável pela gestão do terminal e pela documentação dos processos ocorridos durante a execução e possíveis erros..."""
    def __init__(self):
        """
        Atribuições iniciais da classe.
        """
        self.start = self.Hello_World
        self.log = self.changelog
        self.runlog = self.write_to_log
        self.sleep = self.sleep_bot

        # Encontre o diretório raiz do projeto
        current_directory = os.path.dirname(os.path.abspath(__file__))  # Caminho da pasta atual do script
        project_root = os.path.dirname(current_directory)  # Caminho do diretório raiz do projeto

        # Definir o diretório de logs dentro da pasta "mybot"
        self.log_directory = os.path.join(project_root, "logs")

        # Criar a pasta de logs se ela não existir
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def Hello_World(self, settings):
        """Mensagem de log inicial, exibe data, hora, nome do bot e prefixo atual."""
        agora = datetime.now()
        dataFormatada = agora.strftime("%Y-%m-%d")
        horarioFormatado = agora.strftime("%H:%M:%S")

        message = (
            f"{Fore.RED}===============================================================\n"
            f"{Fore.LIGHTYELLOW_EX}         Créditos: Fumiko0701, aka CT ❤️\n"
            f"{Fore.RED}===============================================================\n"
            f"{Fore.WHITE}'{settings['botName']}' {Fore.LIGHTGREEN_EX}iniciado com sucesso!\n"
            f"{Fore.CYAN}Data de inicialização: {dataFormatada}\n"
            f"Hora de inicialização: {horarioFormatado}\n\n"
            f"{Fore.WHITE}Este bot está pronto para "
            f"{Fore.WHITE}responder aos comandos usando o prefixo: '{settings['prefix']}'. {Fore.YELLOW}Fique à vontade "
            f"para explorar suas funcionalidades.\n"
            f"{Fore.RED}===============================================================\n"
            f"{Style.RESET_ALL}" # a cor precisa ser setada pra default após isso
        )
        print(message)
        self.write_to_log(message.strip())

    def changelog(self, tipo, valor=None, subtipo=None, subvalor=None):
        """
        Atualização da changelog, créditos: Fumiko0701, aka CT ❤️
        Visite a página no github para mais instruções...

        Função capaz de relatar alterações de variáveis e mudanças no ambiente settings.json\n
        Função capaz de relatar alterações de data-logs no ambiente 'data/', blacklisted_words.json, etc...\n
        Função capaz de relatar palavras na lista negra\n
        """
        agora = datetime.now()
        horarioFormatado = agora.strftime("%Y-%m-%d")  # formatei
        dataFormatada = agora.strftime("%H:%M:%S")  # HORA

        log_message = ""
        if tipo == 'empty':
            if valor != 'success' and valor != 'fail':
                log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.YELLOW}Durante uma varredura o arquivo {valor} não foi encontrado OU está mal formatado. {Fore.YELLOW}Tentando Resolver...{Style.RESET_ALL}"
            else:
                if valor == 'success':
                    log_message = f"{Fore.LIGHTGREEN_EX}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.LIGHTGREEN_EX}SUCESSO!{Fore.YELLOW} O arquivo foi criado e/ou reescrito!{Style.RESET_ALL}"
                else:
                    if subtipo == 'couldnt_read_or_create_file':
                        log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.LIGHTRED_EX}ERRO!{Fore.YELLOW} O Arquivo não pôde ser criado e/ou reescrito. Faça-o manualmente!{Style.RESET_ALL}"
            
        elif tipo == 'prefix':
            if subtipo == 'user':
                log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}DONO{Fore.GREEN}]# Prefixo alterado para '{Fore.WHITE}{valor}{Fore.GREEN}' por: '{subvalor}'{Style.RESET_ALL}"
            else:
                log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}DONO{Fore.GREEN}]# Prefixo alterado para '{Fore.WHITE}{valor}{Fore.GREEN}'{Style.RESET_ALL}"
        
        elif tipo == 'word_blacklist':
            if subtipo is not None:
                log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}ADMIN-TOOL{Fore.GREEN}]# A palavra '{Fore.WHITE}{valor}{Fore.GREEN}' foi adicionada à lista de palavras proibidas pelo usuário de ID: '{subtipo}'{Style.RESET_ALL}"
            else:
                log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}ADMIN-TOOL{Fore.GREEN}]# A palavra '{Fore.WHITE}{valor}{Fore.GREEN}' foi adicionada à lista de palavras proibidas.{Style.RESET_ALL}"
        
        elif tipo == 'badword':
            if subtipo is not None:
                log_message = f"| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}O usuário '{Fore.WHITE}{valor}{Fore.GREEN}' mencionou uma palavra proibida em uma de suas mensagens! {f'{Fore.LIGHTGREEN_EX}E ela foi excluída!' if subtipo else f'{Fore.LIGHTRED_EX}E ela não foi excluída!'}{Style.RESET_ALL}"
            else:
                log_message = f"| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}O usuário '{Fore.WHITE}{valor}{Fore.GREEN}' mencionou uma palavra proibida em uma de suas mensagens!{Style.RESET_ALL}"

        elif tipo == 'except':
            log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.YELLOW}Erro capturado = ' {valor} '{Style.RESET_ALL}"
        
        elif tipo == 'initload':
            log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.BLACK}#{Fore.WHITE}[{Fore.RED}SISTEMA{Fore.WHITE}]{Fore.BLACK}# {Fore.YELLOW}Pacotes carregados na inicialização! {Style.RESET_ALL}"
        
        if log_message:
            print(log_message)


    def write_to_log(self, message):
        """aka runlog. Escreve a mensagem no arquivo de log."""
        message_cleaned = self.clean_message(message)
        log_file_path = os.path.join(self.log_directory, f"init_{datetime.now().strftime('%Y.%m.%d')}.txt")
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message_cleaned}\n")


    def clean_message(self, message):
        """Remove caracteres especiais da mensagem."""
        return re.sub(r'[^\x00-\x7F]+', '', message)
    
    async def sleep_bot(self, ctx):
        """Coloca essa espelunca para dormir! -ass CT<3"""
        uid = ctx.author.id
        if uid == ownerID:
            agora = datetime.now()
            horarioFormatado = agora.strftime("%Y-%m-%d")  # formatei
            dataFormatada = agora.strftime("%H:%M:%S")  # HORA
            
            #await ctx.bot.close()
            log_message = f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.YELLOW}Pedido de desligamento recebido! Desligando...{Style.RESET_ALL}"
            print(log_message)
            self.write_to_log(log_message.strip())
            
            return True, "Bot entrando em modo de repouso..."
        else:
            return False, "Apenas meu dono pode usar essa função!"
