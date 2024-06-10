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
        self.resizable(False, False)  # Bloqueia a configuração de redimensionamento da janela
        
        # Cria um frame para o menu lateral
        sidebar_frame = ttk.Frame(self, padding="10 0", style="dark.TFrame")
        sidebar_frame.pack(side="left", fill="y")

        # Estilo para os botões da barra lateral
        style = ttk.Style()
        style.configure("info.TButton", foreground="white", background="#2c2f33", font=("Arial", 12), bordercolor="#2c2f33")

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
        home_content_label = ttk.Label(parent_frame, text="Bem-vindo à Home!", font=("Arial", 14))
        home_content_label.pack(pady=20)

    def show_account_content(self, parent_frame):
        # Cria o conteúdo da seção "Account"
        account_content_label = ttk.Label(parent_frame, text="Bem-vindo à Conta!", font=("Arial", 14))
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
            self.edit_button = ttk.Button(bots_content_frame, text="Editar Bot", style="info.TButton", command=self.show_edit_sidebar)
            self.edit_button.place(x=500, y=520)  # Alinha o botão no canto inferior direito
            self.edit_button.place_forget()  # Esconde o botão "Editar Bot" inicialmente

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
                self.edit_button.place(x=500, y=520)  # Mostra o botão "Editar Bot" no canto inferior direito
            else:
                self.status_label.config(text="Erro", background="#dc3545", foreground="white")
                self.edit_button.place_forget()  # Esconde o botão "Editar Bot" se houver erro

    def run_bot_app(self, directory, settings_path):
        # Lê o nome do bot a partir do arquivo settings.json
        with open(settings_path, 'r') as f:
            settings = json.load(f)
            bot_name = settings.get("botName", "Bot")

        # Define o comando para executar o novo script com o diretório selecionado e o nome do bot
        command = f'python bot_loader.py "{directory}" "{bot_name}"'
        subprocess.Popen(command, shell=True)

    def show_edit_sidebar(self):
        self.edit_sidebar = ttk.Frame(self, padding="10", style="dark.TFrame")
        self.edit_sidebar.place(x=500, y=0, relheight=1, width=400)  # Inicialmente posiciona a barra fora da tela à direita

        selected_project = self.selected_project.get()
        settings_path = os.path.join(selected_project, "data", "static", "settings.json")
        print("[LENDO] Caminho do arquivo settings.json:", settings_path)  # Adiciona este print statement

        # Lê os dados do arquivo settings.json
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        # Campos para editar as informações do bot
        self.fields = {
            "Nome do Bot": settings.get("botName", ""),
            "Bot Token": settings.get("clientID", ""),
            "Prefixo": settings.get("prefix", ""),
            "ID do Dono": settings.get("ownerID", "")
        }

        self.entries = {}

        # Adiciona os campos na barra lateral de edição e preenche com os valores atuais
        for idx, (label, value) in enumerate(self.fields.items()):
            ttk.Label(self.edit_sidebar, text=label, font=("Arial", 12)).grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.edit_sidebar, width=30)
            entry.insert(0, value)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[label] = entry

        # Botão para salvar alterações
        save_button = ttk.Button(self.edit_sidebar, text="Salvar Alterações", style="success.TButton", command=self.save_changes)
        save_button.grid(row=len(self.fields), column=0, columnspan=2, pady=10)

        # Animação suave da barra lateral
        self.animate_sidebar(800, 300, 20)

    def animate_sidebar(self, start_x, end_x, step):
        if start_x > end_x:
            self.edit_sidebar.place(x=start_x, y=0, relheight=1, width=400)
            self.after(10, self.animate_sidebar, start_x - step, end_x, step)

    def save_changes(self):
        selected_project = self.selected_project.get()
        settings_path = os.path.join(selected_project, "data", "static", "settings.json")
        print("[SALVANDO] Caminho do arquivo settings.json:", settings_path)  # Adiciona este print statement

        # Carrega as configurações existentes do arquivo settings.json
        with open(settings_path, 'r') as f:
            existing_settings = json.load(f)

        # Atualiza os valores das chaves existentes com os novos valores dos campos de entrada
        for label, entry in self.entries.items():
            key = label.replace(" ", "")
            original_key = ""
            if key == "NomedoBot":
                original_key = "botName"
            elif key == "BotToken":
                original_key = "clientID"
            elif key == "Prefixo":
                original_key = "prefix"
            elif key == "IDdoDono":
                original_key = "ownerID"
            if original_key in existing_settings:  # Verifica se a chave existe no arquivo existente
                new_value = entry.get()
                print(f"Chave: {original_key}, Novo valor: {new_value}")
                existing_settings[original_key] = new_value

        # Salva as alterações de volta no arquivo settings.json
        with open(settings_path, 'w') as f:
            json.dump(existing_settings, f, indent=4)

        # Exibe uma mensagem de sucesso na barra lateral de edição
        success_label = ttk.Label(self.edit_sidebar, text="Alterações salvas com sucesso!", font=("Arial", 14), style="success.TLabel")
        success_label.grid(row=len(self.fields) + 1, column=0, columnspan=2, pady=10)

    def show_settings_content(self, parent_frame):
        # Cria o conteúdo da seção "Settings"
        settings_content_label = ttk.Label(parent_frame, text="Bem-vindo às Configurações!", font=("Arial", 14))
        settings_content_label.pack(pady=20)

    def show_exit_content(self, parent_frame):
        # Cria o conteúdo da seção "Exit"
        exit_content_label = ttk.Label(parent_frame, text="Saindo...", font=("Arial", 14))
        exit_content_label.pack(pady=20)
        self.after(2000, self.quit)  # Sai do aplicativo após 2 segundos

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
