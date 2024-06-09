from datetime import datetime
from colorama import Fore, Style


class Console:
    """Instância responsável pela gestão do terminal e pela documentação dos processos ocorridos durante a execução e possiveis erros..."""
    def __init__(self):
        self.start = self.Hello_World
        self.log = self.changelog
        self.sleep = self.sleep_bot


    def Hello_World(self, settings):
        """Mensagem de log inicial, exibe data, hora, nome do bot e prefixo atual."""
        agora = datetime.now()

        dataFormatada = agora.strftime("%Y-%m-%d") #formatei
        horarioFormatado = agora.strftime("%H:%M:%S") #horario formatado


        message = (
            f"{Fore.RED}===============================================================\n"
            f"{Fore.LIGHTYELLOW_EX}         Créditos: Fumiko0701, aka CT ❤️\n"
            f"{Fore.RED}===============================================================\n"
            f"{Fore.WHITE}'{settings['botName']}' {Fore.LIGHTGREEN_EX}iniciado com sucesso!\n"
            f"{Fore.CYAN}Data de inicialização: {horarioFormatado}\n"
            f"Hora de inicialização: {dataFormatada}\n\n"
            f"{Fore.WHITE}Este bot está pronto para "
            f"{Fore.WHITE}responder aos comandos usando o prefixo: '{settings['prefix']}'. {Fore.YELLOW}Fique à vontade "
            f"para explorar suas funcionalidades.\n"
            f"{Fore.RED}===============================================================\n"
            f"{Style.RESET_ALL}" #a cor precisa ser setada pra default após isso
        )
        return print(message)
    

    def changelog(self, tipo, valor=None, subtipo=None, subvalor=None):
        """
        Atualização da changelog, créditos: Fumiko0701, aka CT ❤️
        Visite a pagina no github para mais instruções...

        Função capaz de relatar alterações de varíaveis e mudanças no ambiente settings.json\n
        Função capaz de relatar alterações de data-logs no ambiente 'data/', blacklisted_words.json, etc...\n
        Função capaz de relatar palavras na lista negra\n
        """
        agora = datetime.now()
        horarioFormatado = agora.strftime("%Y-%m-%d")  # formatei
        dataFormatada = agora.strftime("%H:%M:%S")  # HORA

        if tipo == 'empty':
            if valor != 'success' and valor != 'fail':
                print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.YELLOW}Durante uma varredura o arquivo {valor} não foi encontrado OU está mal formatado. {Fore.YELLOW}Tentando Resolver...{Style.RESET_ALL}")
            else:
                if valor == 'success':
                    print(f"{Fore.LIGHTGREEN_EX}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.LIGHTGREEN_EX}SUCESSO!{Fore.YELLOW} O arquivo foi criado e/ou reescrito!{Style.RESET_ALL}")
                else:
                    if subtipo == 'couldnt_read_or_create_file':
                        print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.LIGHTRED_EX}ERRO!{Fore.YELLOW} O Arquivo não pôde ser criado e/ou reescrito. Faça-o manualmente!{Style.RESET_ALL}")
            
        elif tipo == 'prefix':
            if subtipo == 'user':
                # Retorna uma linha de código com texto verde no terminal
                print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}DONO{Fore.GREEN}]# Prefixo alterado para '{Fore.WHITE}{valor}{Fore.GREEN}' por: '{subvalor}'{Style.RESET_ALL}")
            else:
                # Retorna uma linha de código com texto verde no terminal
                print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}DONO{Fore.GREEN}]# Prefixo alterado para '{Fore.WHITE}{valor}{Fore.GREEN}'{Style.RESET_ALL}")
        
        elif tipo == 'word_blacklist':
            if subtipo is not None:
                print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}ADMIN-TOOL{Fore.GREEN}]# A palavra '{Fore.WHITE}{valor}{Fore.GREEN}' foi adicionada à lista de palavras proibidas pelo usuario de ID: '{subtipo}'{Style.RESET_ALL}")
            else:
                print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.YELLOW}ADMIN-TOOL{Fore.GREEN}]# A palavra '{Fore.WHITE}{valor}{Fore.GREEN}' foi adicionada à lista de palavras proibidas.{Style.RESET_ALL}")
        
        elif tipo == 'badword':
            if subtipo is not None:
                print(f"| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}O usuário '{Fore.WHITE}{valor}{Fore.GREEN}' mencionou uma palavra proibida em uma de suas mensagens! {f'{Fore.LIGHTGREEN_EX}E ela foi excluida!' if subtipo else f'{Fore.LIGHTRED_EX}E ela não foi excluida!'}{Style.RESET_ALL}")
            else:
                print(f"| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}O usuário '{Fore.WHITE}{valor}{Fore.GREEN}' mencionou uma palavra proibida em uma de suas mensagens!{Style.RESET_ALL}")

        elif tipo == 'except':
            return print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.YELLOW}Erro capturado = ' {valor} '{Style.RESET_ALL}")

    

    async def sleep_bot(self, ctx, ownerID):
        """Coloca essa espelunca para dormir! -ass CT<3"""
        uid = ctx.author.id
        if uid == ownerID:
            agora = datetime.now()
            horarioFormatado = agora.strftime("%Y-%m-%d")  # formatei
            dataFormatada = agora.strftime("%H:%M:%S")  # HORA
            await ctx.send("Bot entrando em modo de repouso...")
            await ctx.bot.close()
            return print(f"{Fore.BLACK}| {Fore.BLUE}{horarioFormatado} {Fore.BLACK}| {Fore.BLUE}{dataFormatada} {Fore.BLACK}| {Fore.GREEN}#[{Fore.LIGHTYELLOW_EX}SISTEMA{Fore.GREEN}]# {Fore.YELLOW}Pedido de desligamento recebido! Desligando...{Style.RESET_ALL}")
        else:
            await ctx.send("Apenas o dono do bot pode usar essa função!")




