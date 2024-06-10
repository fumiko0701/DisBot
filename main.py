import os
import subprocess
import tkinter as tk
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class BotApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Easy Bot Constructor")
        self.geometry("800x600")
        
        # Cria um frame para o menu lateral
        sidebar_frame = ttk.Frame(self, padding="10 0", style="dark.TFrame")
        sidebar_frame.pack(side="left", fill="y")

        # Estilo para os botões da barra lateral
        style = ttk.Style()
        style.configure("info.TButton", foreground="white", background="#6c757d", font=("Arial", 12))

        # Adiciona seções ao menu lateral
        sections = ["Home", "Account", "Bots", "Settings", "Exit"]
        for section_name in sections:
            section_button = ttk.Button(sidebar_frame, text=section_name, style="info.TButton",
                                        command=lambda s=section_name: self.show_section(s))
            section_button.pack(fill="x", pady=5)

        # Dicionário para armazenar os frames de conteúdo das seções
        self.section_content_frames = {}

        # Variável para armazenar o selectbox
        self.bot_dropdown = None

        # Variável para armazenar o item selecionado no selectbox
        self.selected_project = tk.StringVar()

        # Conteúdo inicial da seção "Home"
        self.show_section("Home")

    def show_section(self, section_name):
        # Limpa o conteúdo atual do frame de conteúdo da seção
        for frame in self.section_content_frames.values():
            frame.destroy()

        # Cria um frame para o conteúdo da seção
        content_frame = ttk.Frame(self, padding="10", style="dark.TFrame")
        content_frame.pack(side="right", fill="both", expand=True)
        self.section_content_frames[section_name] = content_frame

        # Mostra o conteúdo da seção selecionada
        if section_name == "Home":
            self.show_home_content(content_frame)
        elif section_name == "Account":
            self.show_account_content(content_frame)
        elif section_name == "Bots":
            self.show_bots_content(content_frame)
        elif section_name == "Settings":
            self.show_settings_content(content_frame)
        elif section_name == "Exit":
            self.show_exit_content(content_frame)

    def show_home_content(self, parent_frame):
        # Cria o conteúdo da seção "Home"
        home_content_label = ttk.Label(parent_frame, text="Welcome to Home!", font=("Arial", 14))
        home_content_label.pack(pady=20)

    def show_account_content(self, parent_frame):
        # Cria o conteúdo da seção "Account"
        account_content_label = ttk.Label(parent_frame, text="Welcome to Account!", font=("Arial", 14))
        account_content_label.pack(pady=20)

    def show_bots_content(self, parent_frame):
        # Cria o conteúdo da seção "Bots"
        bots_content_frame = ttk.Frame(parent_frame, style="dark.TFrame")
        bots_content_frame.pack(side="top", fill="both", expand=True)

        select_label = ttk.Label(bots_content_frame, text="Selecione o seu projeto:", font=("Arial", 12), padding="0 10", style="light.TLabel")
        select_label.pack()

        # Verifica os diretórios para obter os projetos mybot
        bot_projects = [d for d in os.listdir() if os.path.isdir(d) and "mybot" in d]

        if bot_projects:
            # Cria um frame interno para alinhar a Combobox e o status_label
            combobox_frame = ttk.Frame(bots_content_frame, style="dark.TFrame")
            combobox_frame.pack(pady=5)

            # Cria a caixa de seleção com os projetos mybot
            self.bot_dropdown = ttk.Combobox(combobox_frame, values=bot_projects, state="readonly", textvariable=self.selected_project, width=30)
            self.bot_dropdown.grid(row=0, column=0, padx=5)

            # Label para exibir a mensagem de status
            self.status_label = ttk.Label(combobox_frame, font=("Arial", 14), padding="0 10")
            self.status_label.grid(row=0, column=1, padx=5)

            # Botão para editar o bot
            self.edit_button = ttk.Button(bots_content_frame, text="Editar Bot", style="info.TButton", command=self.edit_bot)
            self.edit_button.pack(pady=10)
            self.edit_button.pack_forget()  # Esconde o botão inicialmente

            self.bot_dropdown.bind("<<ComboboxSelected>>", self.check_bot_settings)  # Verifica os arquivos ao selecionar um projeto
        else:
            # Se não houver projetos mybot encontrados
            no_bot_label = ttk.Label(bots_content_frame, text="Nenhum projeto mybot encontrado.", font=("Arial", 14))
            no_bot_label.pack(pady=20)

    def check_bot_settings(self, event=None):
        # Verifica se existem os arquivos bot.py e settings.json dentro do projeto mybot selecionado
        selected_project = self.selected_project.get()
        if selected_project:
            bot_py_path = os.path.join(selected_project, "bot.py")
            settings_path = os.path.join(selected_project, "data", "static", "settings.json")

            bot_py_exists = os.path.exists(bot_py_path)
            settings_exists = os.path.exists(settings_path)

            if bot_py_exists and settings_exists:
                # Substitui o status_label por um botão "Pronto"
                self.status_label.grid_forget()
                self.ready_button = ttk.Button(self.status_label.master, text="Pronto", style="success.TButton",
                                               command=lambda: self.run_bot_app(selected_project, settings_path))
                self.ready_button.grid(row=0, column=1, padx=5)
                self.edit_button.pack()  # Mostra o botão "Editar Bot"
            else:
                self.status_label.config(text="Erro", background="#dc3545", foreground="white")
                self.edit_button.pack_forget()  # Esconde o botão "Editar Bot" se houver erro

    def run_bot_app(self, directory, settings_path):
        # Lê o nome do bot a partir do arquivo settings.json
        with open(settings_path, 'r') as f:
            settings = json.load(f)
            bot_name = settings.get("botName", "Bot")

        # Define o comando para executar o novo script com o diretório selecionado e o nome do bot
        command = f'python bot_loader.py {directory} "{bot_name}"'
        subprocess.Popen(command, shell=True)

    def edit_bot(self):
        # Limpa o conteúdo da janela
        for frame in self.section_content_frames.values():
            frame.destroy()

        # Cria um frame para editar o bot
        edit_frame = ttk.Frame(self, padding="10", style="dark.TFrame")
        edit_frame.pack(fill="both", expand=True)

        selected_project = self.selected_project.get()
        settings_path = os.path.join(selected_project, "data", "static", "settings.json")

        # Lê os dados do arquivo settings.json
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        # Campos para editar as informações do bot
        fields = {
            "Nome do Bot": settings.get("botName", ""),
            "Bot Token": settings.get("clientID", ""),
            "Prefixo": settings.get("prefix", ""),
            "ID do Dono": settings.get("ownerID", "")
        }

        # Adiciona os campos no frame de edição
        for idx, (label, value) in enumerate(fields.items()):
            ttk.Label(edit_frame, text=label, font=("Arial", 12)).grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(edit_frame, width=30)
            entry.insert(0, value)
            entry.grid(row=idx, column=1, padx=5, pady=5)

    def show_settings_content(self, parent_frame):
        # Cria o conteúdo da seção "Settings"
        settings_content_label = ttk.Label(parent_frame, text="Welcome to Settings!", font=("Arial", 14))
        settings_content_label.pack(pady=20)

    def show_exit_content(self, parent_frame):
        # Cria o conteúdo da seção "Exit"
        exit_content_label = ttk.Label(parent_frame, text="Exiting...", font=("Arial", 14))
        exit_content_label.pack(pady=20)
        self.after(2000, self.quit)  # Sai do aplicativo após 2 segundos

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
