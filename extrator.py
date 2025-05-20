# Verifica e instala dependências necessárias
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "tk"])
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

import os
import shutil
import zipfile
import traceback
import threading
import time

cancelado = False  # Flag de cancelamento global

def processar_arquivo(origem, pasta_destino):
    nome, ext = os.path.splitext(os.path.basename(origem))
    contador = 1
    while True:
        novo_nome = f"{nome} ({contador}){ext}" if contador > 1 else f"{nome}{ext}"
        destino = os.path.join(pasta_destino, novo_nome)
        if not os.path.exists(destino):
            return destino
        contador += 1

def decompilar_jar(origem, pasta_destino):
    nome, _ = os.path.splitext(os.path.basename(origem))
    pasta_decompilado = os.path.join(pasta_destino, f"{nome}_decompilado")
    os.makedirs(pasta_decompilado, exist_ok=True)
    with zipfile.ZipFile(origem, 'r') as jar:
        jar.extractall(pasta_decompilado)
    return pasta_decompilado

def log_erros(erros, pasta_destino):
    if erros:
        with open(os.path.join(pasta_destino, "erros.log"), 'w', encoding='utf-8') as f:
            f.write("\n".join(erros))

def executar(pasta_origem, decompilar, progresso_label, barra_progresso, botao_iniciar, botao_cancelar):
    global cancelado
    cancelado = False
    botao_iniciar.config(state=tk.DISABLED)
    botao_cancelar.config(state=tk.NORMAL)

    try:
        nome_base = os.path.basename(os.path.normpath(pasta_origem))
        pasta_destino = f"Arquivos da pasta {nome_base}"
        os.makedirs(pasta_destino, exist_ok=True)

        total_arquivos = sum(len(files) for _, _, files in os.walk(pasta_origem))
        contador = 0
        erros = []

        with open(os.path.join(pasta_destino, "lista_arquivos.txt"), 'w', encoding='utf-8') as log_file:
            for raiz, _, arquivos in os.walk(pasta_origem):
                for arquivo in arquivos:
                    if cancelado:
                        progresso_label.config(text="⚠️ Processo cancelado pelo usuário.")
                        barra_progresso["value"] = 0
                        botao_iniciar.config(state=tk.NORMAL)
                        botao_cancelar.config(state=tk.DISABLED)
                        return

                    origem = os.path.join(raiz, arquivo)
                    try:
                        if decompilar and arquivo.lower().endswith('.jar'):
                            destino = decompilar_jar(origem, pasta_destino)
                        else:
                            destino = processar_arquivo(origem, pasta_destino)
                            shutil.copy2(origem, destino)

                        log_file.write(f"{os.path.basename(destino)}\n")
                        contador += 1

                        progresso = (contador / total_arquivos) * 100
                        barra_progresso["value"] = progresso
                        progresso_label.config(text=f"Progresso: {contador}/{total_arquivos} arquivos")
                        progresso_label.update()
                    except Exception as e:
                        erros.append(f"ERRO: {origem} -> {str(e)}")

        log_erros(erros, pasta_destino)
        if not cancelado:
            messagebox.showinfo("✅ Concluído", f"{contador} arquivos processados com sucesso.")
        else:
            messagebox.showwarning("⚠️ Cancelado", "Processo foi cancelado.")
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Erro", str(e))
    finally:
        botao_iniciar.config(state=tk.NORMAL)
        botao_cancelar.config(state=tk.DISABLED)

def abrir_interface():
    def selecionar_pasta():
        pasta = filedialog.askdirectory()
        if pasta:
            entrada_pasta.delete(0, tk.END)
            entrada_pasta.insert(0, pasta)

    def iniciar_processamento():
        pasta = entrada_pasta.get()
        decompilar = var_decompilar.get()
        if not pasta or not os.path.isdir(pasta):
            messagebox.showwarning("Aviso", "Selecione uma pasta válida.")
            return
        threading.Thread(target=executar, args=(pasta, decompilar, progresso_label, barra_progresso, botao_iniciar, botao_cancelar)).start()

    def cancelar_processamento():
        global cancelado
        cancelado = True

    janela = tk.Tk()
    janela.title("🔍 Extrator e Decompilador de Arquivos")
    janela.geometry("550x350")
    janela.resizable(False, False)

    # Interface
    tk.Label(janela, text="Selecione a pasta de origem:").pack(pady=10)
    entrada_pasta = tk.Entry(janela, width=60)
    entrada_pasta.pack()
    tk.Button(janela, text="📁 Procurar", command=selecionar_pasta).pack(pady=5)

    var_decompilar = tk.BooleanVar()
    tk.Checkbutton(janela, text="Decompilar arquivos .jar", variable=var_decompilar).pack(pady=10)

    botao_iniciar = tk.Button(janela, text="▶️ Iniciar", command=iniciar_processamento)
    botao_iniciar.pack(pady=5)

    botao_cancelar = tk.Button(janela, text="❌ Cancelar", command=cancelar_processamento, state=tk.DISABLED)
    botao_cancelar.pack()

    barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=400, mode="determinate")
    barra_progresso.pack(pady=15)

    progresso_label = tk.Label(janela, text="")
    progresso_label.pack()

    tk.Label(janela, text="by ChatGPT + você 😎", font=("Arial", 8), fg="gray").pack(side=tk.BOTTOM, pady=10)

    janela.mainloop()

if __name__ == "__main__":
    abrir_interface()
