import subprocess
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
import re
import os
import psutil

# Mapeamento de sequências de escape ANSI para cores tkinter
ANSI_COLORS = {
    '30': 'black', '31': 'red', '32': 'green', '33': 'yellow',
    '34': 'blue', '35': 'magenta', '36': 'cyan', '37': 'white',
    '90': 'grey', '91': 'red', '92': 'green', '93': 'yellow',
    '94': 'blue', '95': 'magenta', '96': 'cyan', '97': 'white'
}

class BotApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Bot Executor")
        self.geometry("800x600")
        
        # Cria um frame para centralizar os widgets
        frame = ttk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Configura a área de texto com fundo preto
        self.text_area = ScrolledText(frame, wrap=WORD, state=DISABLED, bg="black", fg="white", insertbackground="white", width=80, height=20)
        self.text_area.pack(pady=20)
        
        # Botão para iniciar o bot
        self.start_button = ttk.Button(frame, text="Start Bot", bootstyle=SUCCESS, command=self.start_bot)
        self.start_button.pack(side=LEFT, padx=5, pady=10)

        # Botão para parar o bot
        self.stop_button = ttk.Button(frame, text="Stop", bootstyle=DANGER, command=self.stop_bot, state=DISABLED)
        self.stop_button.pack(side=LEFT, padx=5, pady=10)
        
        # Lista para armazenar mensagens de erro
        self.error_output = []
        # Variável para armazenar o processo do bot
        self.proc = None
    
    def start_bot(self):
        # Limpa a área de texto
        self.clear_text()
        
        # Desativa o botão de início enquanto o bot está em execução
        self.start_button.config(state=DISABLED)
        # Ativa o botão de parada
        self.stop_button.config(state=NORMAL)
        
        # Caminho do diretório base do projeto
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Caminho do script do bot
        bot_script = os.path.join(base_dir, 'mybot', 'bot.py')

        # Caminho do ambiente virtual
        if os.name == 'nt':  # Windows
            activate_env = os.path.join(base_dir, '.venv', 'Scripts', 'activate.bat')
            command = f'cmd.exe /c ""{activate_env}" && python -u "{bot_script}""'
        else:  # macOS/Linux
            activate_env = os.path.join(base_dir, '.venv', 'bin', 'activate')
            command = f'bash -c "source \'{activate_env}\' && python -u \'{bot_script}\'"'

        # Verifica se o ambiente virtual e o script do bot existem
        if not os.path.exists(activate_env):
            self.append_text(f"\nO ambiente virtual não foi encontrado: {activate_env}\n", stderr=True)
            return

        if not os.path.exists(bot_script):
            self.append_text(f"\nO script do bot não foi encontrado: {bot_script}\n", stderr=True)
            return

        # Inicia o processo do bot.py
        self.proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            bufsize=1, 
            text=True, 
            shell=True, 
            encoding='utf-8', 
            errors='ignore'
        )
        
        # Cria threads para ler stdout e stderr
        self.stdout_thread = threading.Thread(target=self.stream_output, args=(self.proc.stdout, "stdout"))
        self.stderr_thread = threading.Thread(target=self.stream_output, args=(self.proc.stderr, "stderr", self.error_output))
        
        # Inicia as threads
        self.stdout_thread.start()
        self.stderr_thread.start()
        
        # Cria uma thread para esperar o processo terminar
        self.wait_thread = threading.Thread(target=self.wait_for_process)
        self.wait_thread.start()

    def stop_bot(self):
        if self.proc:
            # Força o término imediato do processo do bot e seus subprocessos
            process = psutil.Process(self.proc.pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
            self.append_text("Parada solicitada!", stderr=True)
            # Limpa o processo
            self.proc = None

            # Aguarda a conclusão das threads
            self.stdout_thread.join()
            self.stderr_thread.join()
            
            # Reativa o botão de início após a conclusão do bot
            self.start_button.config(state=NORMAL)
            # Desativa o botão de parada
            self.stop_button.config(state=DISABLED)

    def stream_output(self, stream, stream_name, output_list=None):
        for line in iter(lambda: stream.readline(), ''):
            if stream_name == "stdout":
                self.append_text(line)
            elif stream_name == "stderr":
                if output_list is not None:
                    output_list.append(line)
                self.append_text(line, stderr=True)
        stream.close()
    
    def append_text(self, text, stderr=False):
        # Configura a área de texto para permitir edição
        self.text_area.config(state=NORMAL)
        
        # Remove e captura as sequências de escape ANSI
        parts = re.split(r'(\x1B\[[0-9;]*m)', text)
        tag = None
        
        for part in parts:
            if re.match(r'\x1B\[[0-9;]*m', part):
                # Sequência de escape ANSI
                codes = part[2:-1].split(';')
                if '0' in codes:  # Reset/Normal
                    tag = None
                else:
                    for code in codes:
                        if code in ANSI_COLORS:
                            tag = code
                            self.text_area.tag_config(tag, foreground=ANSI_COLORS[code])
            else:
                # Texto normal
                self.text_area.insert(END, part, (tag,))
        
        # Adiciona linha ao final
        self.text_area.insert(END, "\n")
        
        # Desativa a edição novamente
        self.text_area.see(END)
        self.text_area.config(state=DISABLED)

    def clear_text(self):
        # Configura a área de texto para permitir edição
        self.text_area.config(state=NORMAL)
        # Limpa o conteúdo da área de texto
        self.text_area.delete(1.0, END)
        # Desativa a edição novamente
        self.text_area.config(state=DISABLED)
    
    def wait_for_process(self):
        # Espera o processo terminar e as threads completarem
        self.proc.wait()
        self.stdout_thread.join()
        self.stderr_thread.join()
        
        # Reativa o botão de início após a conclusão do bot
        self.start_button.config(state=NORMAL)
        
        # Desativa o botão de parada
        self.stop_button.config(state=DISABLED)
        
        # Verifica se o processo ainda existe antes de acessar `returncode`
        if self.proc and self.proc.returncode == 0:
            self.append_text("\nO bot.py foi executado com sucesso!\n")
        elif self.proc:
            self.append_text("\nO bot.py encontrou um erro durante a execução.\n", stderr=True)
            # Mostra as mensagens de erro capturadas
            for error in self.error_output:
                self.append_text(error, stderr=True)

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
