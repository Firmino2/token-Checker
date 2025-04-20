# Discord Token Checker
# Autor: Firminoh7
# GitHub: https://github.com/Firmino2
#
# Licença MIT
# Copyright (c) 2025 Firminoh7
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import requests
import time
import os
from datetime import datetime
import threading
import queue
import logging
import base64

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TokenCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Token Checker")
        self.root.geometry("600x400")
        self.root.configure(bg="#2C2F33")
        self.root.minsize(600, 400)

        # Estilo
        self.bg_color = "#2C2F33"
        self.fg_color = "#FFFFFF"
        self.button_color = "#7289DA"
        self.button_hover = "#677BC4"

        # Fila e controle
        self.request_queue = queue.Queue()
        self.rate_limit_delay = 1
        self.max_retries = 3

        # Variáveis para interface
        self.progress_var = tk.DoubleVar()
        self.valid_count = tk.IntVar()
        self.invalid_count = tk.IntVar()

        # Créditos codificados em Base64
        self.author_encoded = "RmlybWlub2g3"  # Firminoh7
        self.github_encoded = "RmlybWlubzI="  # Firmino2

        # Interface
        self.create_widgets()

    def decode_credits(self, encoded_text):
        try:
            return base64.b64decode(encoded_text).decode('utf-8')
        except Exception as e:
            logging.error(f"Erro ao decodificar créditos: {e}")
            return "Desconhecido"

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=8)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.map("TButton", background=[("active", self.button_hover)])

        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        title_label = ttk.Label(main_frame, text="Discord Token Checker", 
                               font=("Arial", 18, "bold"), style="TLabel")
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15), sticky="ew")

        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

        self.select_button = ttk.Button(button_frame, text="Selecionar Arquivo", 
                                       command=self.select_file, style="TButton")
        self.select_button.grid(row=0, column=0, padx=5)

        self.check_button = ttk.Button(button_frame, text="Iniciar Verificação", 
                                      command=self.start_checking, state="disabled", style="TButton")
        self.check_button.grid(row=0, column=1, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Limpar Logs", 
                                      command=self.clear_logs, style="TButton")
        self.clear_button.grid(row=0, column=2, padx=5)

        self.credits_button = ttk.Button(button_frame, text="Créditos", 
                                        command=self.show_credits, style="TButton")
        self.credits_button.grid(row=0, column=3, padx=5)

        self.log_area = scrolledtext.ScrolledText(main_frame, height=12, 
                                                bg="#23272A", fg=self.fg_color, 
                                                font=("Arial", 10), state="disabled")
        self.log_area.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")

        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.grid(row=3, column=0, columnspan=4, pady=5, sticky="ew")

        status_frame = tk.Frame(main_frame, bg=self.bg_color)
        status_frame.grid(row=4, column=0, columnspan=4, pady=5, sticky="ew")

        self.status_label = ttk.Label(status_frame, text="Status: Aguardando", 
                                    font=("Arial", 10), style="TLabel")
        self.status_label.pack(side="left", padx=10)

        tk.Label(status_frame, text="Válidos:", bg=self.bg_color, fg="#00FF00", 
                font=("Arial", 10)).pack(side="left", padx=5)
        tk.Label(status_frame, textvariable=self.valid_count, bg=self.bg_color, fg="#00FF00", 
                font=("Arial", 10)).pack(side="left", padx=2)
        tk.Label(status_frame, text="Inválidos:", bg=self.bg_color, fg="#FF0000", 
                font=("Arial", 10)).pack(side="left", padx=5)
        tk.Label(status_frame, textvariable=self.invalid_count, bg=self.bg_color, fg="#FF0000", 
                font=("Arial", 10)).pack(side="left", padx=2)

        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def show_credits(self):
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Créditos")
        credits_window.geometry("300x150")
        credits_window.configure(bg=self.bg_color)
        credits_window.transient(self.root)
        credits_window.grab_set()

        tk.Label(credits_window, text="Discord Token Checker", font=("Arial", 14, "bold"), 
                bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        tk.Label(credits_window, text=f"Desenvolvido por: {self.decode_credits(self.author_encoded)}", 
                font=("Arial", 10), bg=self.bg_color, fg=self.fg_color).pack()
        tk.Label(credits_window, text=f"GitHub: github.com/{self.decode_credits(self.github_encoded)}", 
                font=("Arial", 10), bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        tk.Button(credits_window, text="Fechar", command=credits_window.destroy, 
                 bg=self.button_color, fg=self.fg_color, activebackground=self.button_hover).pack(pady=10)

    def clear_logs(self):
        self.log_area.configure(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state="disabled")

    def log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")
        logging.info(message)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path = file_path
            self.log(f"Arquivo selecionado: {file_path}")
            self.check_button.config(state="normal")
        else:
            self.log("Nenhum arquivo selecionado")

    def check_token(self, token, attempt=1):
        headers = {"Authorization": token}
        try:
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get('username', 'Desconhecido')
                user_id = user_data.get('id', 'Desconhecido')
                return token, "Válido", username, user_id
            elif response.status_code == 401:
                return token, "Inválido", None, None
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                self.rate_limit_delay = max(self.rate_limit_delay, retry_after)
                if attempt <= self.max_retries:
                    time.sleep(retry_after)
                    return self.check_token(token, attempt + 1)
                return token, f"Limite de requisições atingido após {self.max_retries} tentativas", None, None
            else:
                return token, f"Erro desconhecido: {response.status_code}", None, None
        except requests.exceptions.RequestException as e:
            return token, f"Erro de conexão: {e}", None, None

    def save_valid_tokens(self, valid_tokens):
        output_dir = os.path.dirname(self.file_path) if self.file_path else "."
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"valid_tokens_{timestamp}.txt")
        
        try:
            with open(output_file, 'w') as f:
                for token, username, user_id in valid_tokens:
                    f.write(f"Token: {token}, Usuário: {username}, ID: {user_id}\n")
            self.log(f"Tokens válidos salvos em: {output_file}")
        except Exception as e:
            self.log(f"Erro ao salvar tokens válidos: {e}")

    def process_queue(self):
        valid_tokens = []
        total_tokens = 0
        processed = 0

        while not self.request_queue.empty():
            token = self.request_queue.get()
            total_tokens += 1
            token, result, username, user_id = self.check_token(token)
            processed += 1
            
            if result == "Válido":
                log_message = f"Token {processed}/{total_tokens}: Válido (Token: {token}, Usuário: {username}, ID: {user_id})"
                self.valid_count.set(self.valid_count.get() + 1)
                valid_tokens.append((token, username, user_id))
            else:
                log_message = f"Token {processed}/{total_tokens}: {result}"
                self.invalid_count.set(self.invalid_count.get() + 1)
                
            self.log(log_message)
            self.status_label.config(text=f"Status: Verificando {processed}/{total_tokens}")
            self.progress_var.set((processed / total_tokens) * 100)
            
            time.sleep(self.rate_limit_delay)

        if valid_tokens:
            self.save_valid_tokens(valid_tokens)
        
        self.status_label.config(text="Status: Verificação concluída")
        self.check_button.config(state="normal")
        self.log(f"Verificação concluída. {len(valid_tokens)} tokens válidos encontrados.")

    def start_checking(self):
        try:
            with open(self.file_path, 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado!")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo: {e}")
            return

        if not tokens:
            messagebox.showwarning("Aviso", "Nenhum token encontrado no arquivo!")
            return

        self.check_button.config(state="disabled")
        self.valid_count.set(0)
        self.invalid_count.set(0)
        self.progress_var.set(0)
        self.log(f"Iniciando verificação de {len(tokens)} tokens...")
        
        while not self.request_queue.empty():
            self.request_queue.get()

        for token in tokens:
            self.request_queue.put(token)

        threading.Thread(target=self.process_queue, daemon=True).start()

def main():
    root = tk.Tk()
    app = TokenCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()