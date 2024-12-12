import subprocess
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
import re
import os
import sys
import psutil
from datetime import datetime

ANSI_COLORS = {
    '30': 'black', '31': 'red', '32': 'green', '33': 'yellow',
    '34': 'blue', '35': 'magenta', '36': 'cyan', '37': 'white',
    '90': 'grey', '91': 'red', '92': 'green', '93': 'yellow',
    '94': 'blue', '95': 'magenta', '96': 'cyan', '97': 'white'
}

class BotApp(ttk.Window):
    def __init__(self, directory, bot_name):
        super().__init__(themename="darkly")
        self.title(f"Executando {bot_name}")
        self.geometry("800x600")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 600
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.directory = directory

        frame = ttk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.text_area = ScrolledText(frame, wrap=WORD, state=DISABLED, bg="black", fg="white", insertbackground="white", width=80, height=20)
        self.text_area.pack(pady=20)

        self.start_button = ttk.Button(frame, text="Start Bot", bootstyle=SUCCESS, command=self.start_bot)
        self.start_button.pack(side=LEFT, padx=5, pady=10)

        self.stop_button = ttk.Button(frame, text="Stop", bootstyle=DANGER, command=self.stop_bot, state=DISABLED)
        self.stop_button.pack(side=LEFT, padx=5, pady=10)

        self.error_output = []
        self.proc = None

        self.runtime_label = ttk.Label(self, text="Tempo de execução: 00:00:00", foreground="white")
        self.runtime_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.start_time = None
        self.update_runtime()

    def update_runtime(self):
        if self.start_time is not None:
            elapsed_time = datetime.now() - self.start_time
            formatted_time = str(elapsed_time).split('.')[0]
            self.runtime_label.config(text=f"Tempo de execução: {formatted_time}")
        self.after(1000, self.update_runtime)

    def start_bot(self):
        self.clear_text()
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)

        base_dir = self.directory
        bot_script = os.path.join(base_dir, 'bot.py')
        project_root = os.path.abspath(os.path.join(base_dir, '..'))

        if os.name == 'nt':
            activate_env = os.path.join(project_root, '.venv', 'Scripts', 'activate.bat')
            command = f'cmd.exe /c ""{activate_env}" && python -u "{bot_script}""'
        else:
            activate_env = os.path.join(project_root, '.venv', 'bin', 'activate')
            command = f'bash -c "source \'{activate_env}\' && python -u \'{bot_script}\'"'

        if not os.path.exists(activate_env):
            self.append_text(f"\nO ambiente virtual não foi encontrado: {activate_env}\n", stderr=True)
            return

        if not os.path.exists(bot_script):
            self.append_text(f"\nO script do bot não foi encontrado: {bot_script}\n", stderr=True)
            return

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

        self.stdout_thread = threading.Thread(target=self.stream_output, args=(self.proc.stdout, "stdout"))
        self.stderr_thread = threading.Thread(target=self.stream_output, args=(self.proc.stderr, "stderr", self.error_output))

        self.stdout_thread.start()
        self.stderr_thread.start()

        self.wait_thread = threading.Thread(target=self.wait_for_process)
        self.wait_thread.start()

        self.start_time = datetime.now()

    def stop_bot(self):
        if self.proc:
            process = psutil.Process(self.proc.pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
            self.append_text("Parada solicitada!", stderr=True)
            self.proc = None

            self.stdout_thread.join()
            self.stderr_thread.join()

            self.start_button.config(state=NORMAL)
            self.stop_button.config(state=DISABLED)

        self.start_time = None

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
        self.text_area.config(state=NORMAL)
        parts = re.split(r'(\x1B\[[0-9;]*m)', text)
        tag = None

        for part in parts:
            if re.match(r'\x1B\[[0-9;]*m', part):
                codes = part[2:-1].split(';')
                if '0' in codes:
                    tag = None
                else:
                    for code in codes:
                        if code in ANSI_COLORS:
                            tag = code
                            self.text_area.tag_config(tag, foreground=ANSI_COLORS[code])
            else:
                self.text_area.insert(END, part, (tag,))

        self.text_area.insert(END, "\n")
        self.text_area.see(END)
        self.text_area.config(state=DISABLED)

    def clear_text(self):
        self.text_area.config(state=NORMAL)
        self.text_area.delete(1.0, END)
        self.text_area.config(state=DISABLED)

    def wait_for_process(self):
        self.proc.wait()
        self.stdout_thread.join()
        self.stderr_thread.join()

        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)

        if self.proc and self.proc.returncode == 0:
            self.start_time = None
            self.append_text("\nO bot.py foi executado com sucesso!\n")
        elif self.proc:
            self.append_text("\nO bot.py encontrou um erro durante a execução.\n", stderr=True)
            for error in self.error_output:
                self.append_text(error, stderr=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python bot_loader.py <diretório> <nome_do_bot>")
        sys.exit(1)

    directory = sys.argv[1]
    bot_name = sys.argv[2]

    app = BotApp(directory, bot_name)
    app.mainloop()
