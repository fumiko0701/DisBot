import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

class HomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home")
        self.geometry("800x600")
        self.configure(background="#f8f9fa")  # Cor de fundo cinza claro
        
        # Frame lateral
        self.sidebar_frame = tk.Frame(self, bg="#6c757d", width=200)  # Cor cinza escuro
        self.sidebar_frame.pack(side="left", fill="y")
        
        # Área central para exibição de conteúdo
        self.content_frame = tk.Frame(self, bg="#e9ecef")  # Cor cinza claro
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Label inicial
        self.current_label = ttk.Label(self.content_frame, text="Welcome to Home!", font=("Arial", 14))
        self.current_label.pack(pady=20, fill="both", expand=True)

        # Estilo para os botões da barra lateral
        style = ttk.Style(self)
        style.configure("Sidebar.TButton", foreground="white", font=("Arial", 12), background="#6c757d")  # Cor cinza escuro

        # Botões na barra lateral
        self.buttons = ["Home", "Account", "Bots", "Audit Logs", "Config", "Exit"]
        self.buttons_widgets = []
        for button_text in self.buttons:
            button = ttk.Button(self.sidebar_frame, text=button_text, style="Sidebar.TButton",
                                command=lambda b=button_text: self.on_button_click(b))
            button.pack(fill="x", padx=10, pady=5)
            self.buttons_widgets.append(button)

    def on_button_click(self, button_text):
        # Limpa o conteúdo atual
        self.current_label.pack_forget()

        # Exibe a mensagem correspondente ao botão clicado
        if button_text == "Bots":
            self.show_bots()
        else:
            self.current_label = ttk.Label(self.content_frame, text=f"Welcome to {button_text}!", font=("Arial", 14))
            self.current_label.pack(pady=20, fill="both", expand=True)

    def show_bots(self):
        # Remove a selectbox anterior, se existir
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Verifica os diretórios para obter os projetos mybot
        bot_projects = [d for d in os.listdir() if os.path.isdir(d) and "mybot" in d]

        if bot_projects:
            # Cria a caixa de seleção com os projetos mybot
            bot_dropdown = tk.StringVar()
            bot_dropdown.set("Select Bot Project")
            bot_menu = tk.OptionMenu(self.content_frame, bot_dropdown, *bot_projects)
            bot_menu.config(font=("Arial", 12), bg="#e9ecef")  # Estilo da selectbox (cor cinza claro)
            bot_menu["menu"].config(font=("Arial", 12))  # Estilo do menu suspenso
            bot_menu.pack(pady=20)
        else:
            # Se não houver projetos mybot encontrados
            messagebox.showinfo("No Bot Projects", "No 'mybot' projects found in the current directory.")

if __name__ == "__main__":
    app = HomeApp()
    app.mainloop()
