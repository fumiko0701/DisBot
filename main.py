import os
import subprocess
import tkinter as tk
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class BotApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")

        # Obtem a largura e altura da tela
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()  # Adicione esta linha
        
        # Define as proporções para a janela do aplicativo (ligeiramente menores)
        self.window_width = int(self.screen_width * 0.44)
        self.window_height = int(self.screen_height * 0.6)

        # Centraliza a janela na tela
        x_position = (self.screen_width - self.window_width) // 2
        y_position = (self.screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")
        self.title("Easy Bot Constructor")
        self.resizable(False, False)  # Bloqueia a configuração de redimensionamento da janela

        # Cria um frame para o menu lateral
        sidebar_frame = ttk.Frame(self, padding="10 0", style="dark.TFrame")
        sidebar_frame.pack(side=LEFT, fill=Y)

        # Estilo para os botões da barra lateral
        style = ttk.Style()
        style.configure("info.TButton", foreground="white", background="#0d141f", font=("Arial", 12), bordercolor="#0d141f")
        style.map("info.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '#23272a'), ('active', '#23272a')],
                  bordercolor=[('pressed', '#2c2f33'), ('active', '#2c2f33')],
                  relief=[('pressed', 'groove'), ('!pressed', 'gray')])

        # Adiciona seções ao menu lateral
        sections = ["Home", "Account", "Bots", "Settings", "Exit"]
        for idx, section_name in enumerate(sections):
            section_button = ttk.Button(sidebar_frame, text=section_name, style="info.TButton",
                                        command=lambda s=section_name: self.show_section(s))

            section_button.pack(ipadx=15, ipady=1, pady=5, padx=10, fill=X)

        # Dicionário para armazenar os frames de conteúdo das seções
        self.section_content_frames = {}

        # Conteúdo inicial da seção "Home"
        self.current_section = None
        self.show_section("Home")

    def show_section(self, section_name):
        if self.current_section == section_name:
            return

        self.current_section = section_name

        # Limpa o conteúdo atual do frame de conteúdo da seção
        for frame in self.section_content_frames.values():
            frame.destroy()

        # Cria um frame para o conteúdo da seção
        content_frame = ttk.Frame(self, padding="10")
        content_frame.place(x=200, y=0, width=self.window_width - 200, height=self.window_height)
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
        home_content_label.place(x=20, y=20)

    def show_account_content(self, parent_frame):
        # Cria o conteúdo da seção "Account"
        account_content_label = ttk.Label(parent_frame, text="Bem-vindo à Conta!", font=("Arial", 14))
        account_content_label.place(x=20, y=20)

    def show_bots_content(self, parent_frame):
        # Cria o conteúdo da seção "Bots"
        select_label = ttk.Label(parent_frame, text="Selecione o seu projeto:", font=("Arial", 12), background="", foreground="white")

        select_label.place(relx=0.05, rely=0.05)

        # Verifica os diretórios para obter os projetos mybot
        bot_projects = [d for d in os.listdir() if os.path.isdir(d) and "mybot" in d]

        if bot_projects:
            # Cria a caixa de seleção com os projetos mybot
            self.selected_project = tk.StringVar()
            self.bot_dropdown = ttk.Combobox(parent_frame, values=bot_projects, state="readonly", textvariable=self.selected_project, width=30)
            self.bot_dropdown.place(relx=0.05, rely=0.1)

            # Label para exibir a mensagem de status
            self.status_label = ttk.Label(parent_frame, font=("Arial", 14), padding="0 10")
            self.status_label.place_forget()

            # Botão para editar o bot
            self.edit_button = ttk.Button(parent_frame, text="Editar Bot", style="info.TButton", command=self.show_edit_sidebar)
            self.edit_button.place_forget()  # Esconde o botão "Editar Bot" inicialmente

            self.bot_dropdown.bind("<<ComboboxSelected>>", self.check_bot_settings)  # Verifica os arquivos ao selecionar um projeto
        else:
            # Se não houver projetos mybot encontrados
            no_bot_label = ttk.Label(parent_frame, text="Nenhum projeto mybot encontrado.", font=("Arial", 14))
            no_bot_label.place(relx=0.05, rely=0.1)

    def check_bot_settings(self, event=None):
        # Verifica se existem os arquivos bot.py e settings.json dentro do projeto mybot selecionado
        selected_project = self.selected_project.get()
        if selected_project:
            bot_py_path = os.path.join(selected_project, "bot.py")
            settings_path = os.path.join(selected_project, "data", "static", "settings.json")

            bot_py_exists = os.path.exists(bot_py_path)
            settings_exists = os.path.exists(settings_path)

            if bot_py_exists & settings_exists:
                # Substitui o status_label por um botão "Pronto"
                self.status_label.place_forget()
                self.ready_button = ttk.Button(self, text="Pronto", style="success.TButton",
                                               command=lambda: self.run_bot_app(selected_project, settings_path))
                self.ready_button.place(relx=0.525, rely=0.112)
                self.edit_button.place(relx=0.80, rely=0.9)  # Mostra o botão "Editar Bot"
            else:
                self.status_label.config(text="Erro: Arquivo bot.py ou settings.json não encontrado", background="#4d0702", foreground="white")
                self.status_label.place(relx=0.6, rely=0.1)
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
        # Desativa a Combobox e os botões "Pronto" e "Editar Bot"
        self.bot_dropdown.config(state="disabled")
        self.ready_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.DISABLED)

        self.edit_sidebar = ttk.Frame(self, padding="10", style="dark.TFrame")
        self.edit_sidebar.place(x=self.window_width, y=0, width=400, height=self.window_height)

        # Botão para fechar a barra lateral de edição
        close_button = ttk.Button(self.edit_sidebar, text="X", style="danger.TButton", command=self.hide_edit_sidebar)
        close_button.place(x=330, y=2, width=32, height=32)

        # Adiciona campos de entrada na barra lateral de edição
        selected_project = self.selected_project.get()
        settings_path = os.path.join(selected_project, "data", "static", "settings.json")
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        self.fields = {
            "Nome do Bot": settings.get("botName", ""),
            "Bot Token": settings.get("botToken", ""),
            "Prefixo": settings.get("prefix", ""),
            "ID do Dono": settings.get("ownerID", "")
        }

        for idx, (label_text, value) in enumerate(self.fields.items()):
            ###select_label = ttk.Label(parent_frame, text="Selecione o seu projeto:", font=("Arial", 12), background="", foreground="white")
            label = ttk.Label(self.edit_sidebar, text=label_text, font=("Arial", 10), background="dark gray", foreground="white")  # Reduzindo o tamanho da letra
            label.place(x=20, y=45 + (idx * 35))  # Ajustando a posição vertical para mais espaço

            entry = ttk.Entry(self.edit_sidebar, font=("Arial", 9))  # Reduzindo o tamanho da letra
            entry.insert(0, value)
            entry.place(x=130, y=40 + (idx * 35), width=230, height=30)  # Reduzindo o tamanho dos campos de entrada
            self.fields[label_text] = entry

        # Botão para salvar as alterações
        save_button = ttk.Button(self.edit_sidebar, text="Salvar Alterações", style="success.TButton",
                                command=lambda: self.save_settings(selected_project, settings_path))
        save_button.place(x=20, y=250, width=360, height=30)  # Ajustando a posição vertical para mais espaço

        # Anima a barra lateral de edição (efeito deslizante)
        self.animate_sidebar(self.edit_sidebar, direction="in")


    def hide_edit_sidebar(self):
        # Ativa a Combobox e os botões "Pronto" e "Editar Bot"
        self.bot_dropdown.config(state="readonly")
        self.ready_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.NORMAL)

        # Anima a barra lateral de edição (efeito deslizante)
        self.animate_sidebar(self.edit_sidebar, direction="out")

    def save_settings(self, project_directory, settings_path):
        # Obtém os valores dos campos de entrada
        updated_settings = {label: entry.get() for label, entry in self.fields.items()}

        # Carrega as configurações existentes do arquivo settings.json
        with open(settings_path, 'r') as f:
            existing_settings = json.load(f)

        # Atualiza apenas as chaves existentes no arquivo settings.json com os novos valores dos campos de entrada
        for label, value in updated_settings.items():
            original_key = None
            if label == "Nome do Bot":
                original_key = "botName"
            elif label == "Bot Token":
                original_key = "botToken"
            elif label == "Prefixo":
                original_key = "prefix"
            elif label == "ID do Dono":
                original_key = "ownerID"

            if original_key and original_key in existing_settings:  # Verifica se a chave existe no arquivo existente
                existing_settings[original_key] = value

        # Salva as alterações de volta no arquivo settings.json
        with open(settings_path, 'w') as f:
            json.dump(existing_settings, f, indent=4)

        # Oculta a barra lateral de edição após salvar
        self.hide_edit_sidebar()

    def animate_sidebar(self, sidebar, direction="in"):
        if direction == "in":
            for x in range(self.window_width, self.window_width - 400, -10):
                sidebar.place(x=x, y=0)
                sidebar.update()
        elif direction == "out":
            for x in range(self.window_width - 400, self.window_width, 10):
                sidebar.place(x=x, y=0)
                sidebar.update()
            sidebar.destroy()


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
        success_label.place(x=10, y=260, width=380, height=30)

    def show_settings_content(self, parent_frame):
        # Cria o conteúdo da seção "Settings"
        settings_content_label = ttk.Label(parent_frame, text="Bem-vindo às Configurações!", font=("Arial", 14))
        settings_content_label.place(x=20, y=20)

    def show_exit_content(self, parent_frame):
        # Cria o conteúdo da seção "Exit"
        exit_content_label = ttk.Label(parent_frame, text="Saindo...", font=("Arial", 14))
        exit_content_label.place(x=20, y=20)
        self.after(2000, self.quit)  # Sai do aplicativo após 2 segundos

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
