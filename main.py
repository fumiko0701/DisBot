import os
import subprocess
import tkinter as tk
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class BotApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight() 
        self.window_width = int(self.screen_width * 0.44)
        self.window_height = int(self.screen_height * 0.6)
        x_position = (self.screen_width - self.window_width) // 2
        y_position = (self.screen_height - self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")
        self.title("Easy Bot Constructor")
        self.resizable(False, False)
        sidebar_frame = ttk.Frame(self, padding="10 0", style="dark.TFrame")
        sidebar_frame.pack(side=LEFT, fill=Y)
        style = ttk.Style()
        style.configure("info.TButton", foreground="white", background="#0d141f", font=("Arial", 12), bordercolor="#0d141f")
        style.map("info.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '#23272a'), ('active', '#23272a')],
                  bordercolor=[('pressed', '#2c2f33'), ('active', '#2c2f33')],
                  relief=[('pressed', 'groove'), ('!pressed', 'gray')])
        sections = ["Home", "Account", "Bots", "Settings", "Exit"]
        for idx, section_name in enumerate(sections):
            section_button = ttk.Button(sidebar_frame, text=section_name, style="info.TButton",
                                        command=lambda s=section_name: self.show_section(s))
            section_button.pack(ipadx=15, ipady=1, pady=5, padx=10, fill=X)
        self.section_content_frames = {}
        self.current_section = None
        self.show_section("Home")

    def show_section(self, section_name):
        if self.current_section == section_name:
            return
        self.current_section = section_name
        for frame in self.section_content_frames.values():
            frame.destroy()
        content_frame = ttk.Frame(self, padding="10")
        content_frame.place(x=200, y=0, width=self.window_width - 200, height=self.window_height)
        self.section_content_frames[section_name] = content_frame
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
        home_content_label = ttk.Label(parent_frame, text="Bem-vindo à Home!", font=("Arial", 14))
        home_content_label.place(x=20, y=20)

    def show_account_content(self, parent_frame):
        account_content_label = ttk.Label(parent_frame, text="Bem-vindo à Conta!", font=("Arial", 14))
        account_content_label.place(x=20, y=20)

    def show_bots_content(self, parent_frame):
        select_label = ttk.Label(parent_frame, text="Selecione o seu projeto:", font=("Arial", 12), background="", foreground="white")
        select_label.place(relx=0.05, rely=0.05)
        bot_projects = [d for d in os.listdir() if os.path.isdir(d) and "mybot" in d]
        if bot_projects:
            self.selected_project = tk.StringVar()
            self.bot_dropdown = ttk.Combobox(parent_frame, values=bot_projects, state="readonly", textvariable=self.selected_project, width=30)
            self.bot_dropdown.place(relx=0.05, rely=0.1)
            self.status_label = ttk.Label(parent_frame, font=("Arial", 14), padding="0 10")
            self.status_label.place_forget()
            self.edit_button = ttk.Button(parent_frame, text="Editar Bot", style="info.TButton", command=self.show_edit_sidebar)
            self.edit_button.place_forget()
            self.bot_dropdown.bind("<<ComboboxSelected>>", self.check_bot_settings)
        else:
            no_bot_label = ttk.Label(parent_frame, text="Nenhum projeto mybot encontrado.", font=("Arial", 14))
            no_bot_label.place(relx=0.05, rely=0.1)

    def check_bot_settings(self, event=None):
        selected_project = self.selected_project.get()
        if selected_project:
            bot_py_path = os.path.join(selected_project, "bot.py")
            settings_path = os.path.join(selected_project, "data", "static", "settings.json")
            bot_py_exists = os.path.exists(bot_py_path)
            settings_exists = os.path.exists(settings_path)
            if bot_py_exists & settings_exists:
                self.status_label.place_forget()
                self.ready_button = ttk.Button(self, text="Pronto", style="success.TButton",
                                               command=lambda: self.run_bot_app(selected_project, settings_path))
                self.ready_button.place(relx=0.525, rely=0.112)
                self.edit_button.place(relx=0.80, rely=0.9)
            else:
                self.status_label.config(text="Erro: Arquivo bot.py ou settings.json não encontrado", background="#4d0702", foreground="white")
                self.status_label.place(relx=0.6, rely=0.1)
                self.edit_button.place_forget()

    def run_bot_app(self, directory, settings_path):
        with open(settings_path, 'r') as f:
            settings = json.load(f)
            bot_name = settings.get("botName", "Bot")
        command = f'python bot_loader.py "{directory}" "{bot_name}"'
        subprocess.Popen(command, shell=True)

    def show_edit_sidebar(self):
        self.bot_dropdown.config(state="disabled")
        self.ready_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.DISABLED)
        self.edit_sidebar = ttk.Frame(self, padding="10", style="dark.TFrame")
        self.edit_sidebar.place(x=self.window_width, y=0, width=400, height=self.window_height)
        close_button = ttk.Button(self.edit_sidebar, text="X", style="danger.TButton", command=self.hide_edit_sidebar)
        close_button.place(x=330, y=2, width=32, height=32)
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
            label = ttk.Label(self.edit_sidebar, text=label_text, font=("Arial", 10), background="dark gray", foreground="white")
            label.place(x=20, y=45 + (idx * 35))
            entry = ttk.Entry(self.edit_sidebar, font=("Arial", 9))
            entry.insert(0, value)
            entry.place(x=130, y=40 + (idx * 35), width=230, height=30)
            self.fields[label_text] = entry
        save_button = ttk.Button(self.edit_sidebar, text="Salvar Alterações", style="success.TButton",
                                command=lambda: self.save_settings(selected_project, settings_path))
        save_button.place(x=20, y=250, width=360, height=30)
        self.animate_sidebar(self.edit_sidebar, direction="in")

    def hide_edit_sidebar(self):
        self.bot_dropdown.config(state="readonly")
        self.ready_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.NORMAL)
        self.animate_sidebar(self.edit_sidebar, direction="out")

    def save_settings(self, project_directory, settings_path):
        updated_settings = {label: entry.get() for label, entry in self.fields.items()}
        with open(settings_path, 'r') as f:
            existing_settings = json.load(f)
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
            if original_key and original_key in existing_settings:
                existing_settings[original_key] = value
        with open(settings_path, 'w') as f:
            json.dump(existing_settings, f, indent=4)
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
        with open(settings_path, 'r') as f:
            existing_settings = json.load(f)
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
            if original_key in existing_settings:
                new_value = entry.get()
                existing_settings[original_key] = new_value
        with open(settings_path, 'w') as f:
            json.dump(existing_settings, f, indent=4)
        success_label = ttk.Label(self.edit_sidebar, text="Alterações salvas com sucesso!", font=("Arial", 14), style="success.TLabel")
        success_label.place(x=10, y=260, width=380, height=30)

    def show_settings_content(self, parent_frame):
        settings_content_label = ttk.Label(parent_frame, text="Bem-vindo às Configurações!", font=("Arial", 14))
        settings_content_label.place(x=20, y=20)

    def show_exit_content(self, parent_frame):
        exit_content_label = ttk.Label(parent_frame, text="Saindo...", font=("Arial", 14))
        exit_content_label.place(x=20, y=20)
        self.after(2000, self.quit)

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
