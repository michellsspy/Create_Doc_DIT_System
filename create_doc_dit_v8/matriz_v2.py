import gradio as gr
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv, set_key
import tkinter as tk
from tkinter import filedialog
import subprocess
import sys

def selecionar_diretorio():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    diretorio = filedialog.askdirectory(title="Selecione a pasta com os notebooks")
    return diretorio if diretorio else ""

def processar_notebooks(token: str, diretorio: str):
    try:
        # Configuração inicial
        env_path = Path(".env")
        env_path.write_text(f"OPENAI_API_KEY={token}\n", encoding="utf-8")
        load_dotenv()
        
        # Verificações de diretório
        if not os.path.isdir(diretorio):
            return "Erro: Diretório inválido ou inexistente.", None
        
        arquivos = [f for f in os.listdir(diretorio) if f.endswith(".ipynb")]
        if not arquivos:
            return "Erro: Nenhum arquivo .ipynb encontrado.", None
        
        # Preparação do ambiente
        pastas = ["notebooks", "markdown", "doc"]
        for pasta in pastas:
            shutil.rmtree(pasta, ignore_errors=True)
            os.makedirs(pasta, exist_ok=True)
        
        # Cópia dos notebooks
        for arquivo in arquivos:
            shutil.copy2(
                os.path.join(diretorio, arquivo),
                os.path.join("notebooks", arquivo)
            )
        
        # Execução do processo principal
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return f"Erro na execução: {result.stderr}", None
        
        dit_path = os.path.join("doc", "DIT.docx")
        if os.path.exists(dit_path):
            return f"Sucesso! {len(arquivos)} notebooks processados.", dit_path
        else:
            return "Erro: DIT.docx não foi gerado.", None
            
    except Exception as e:
        return f"Erro crítico: {str(e)}", None

def limpar():
    return "", "", None, ""

with gr.Blocks(title="Conversor de Notebooks para DIT") as interface:
    
    # Botão para criar token (canto superior direito)
    gr.HTML("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <h2 style="margin: 0;">Conversor de Notebooks Jupyter para Documento Técnico (DIT)</h2>
        <a href='https://platform.openai.com/settings/organization/admin-keys' target='_blank'>
            <button class='gr-button gr-button-lg gr-button-primary'
                style='background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer;'>
                Criar Token OpenAI
            </button>
        </a>
    </div>
    <p>Esta ferramenta converte notebooks Jupyter (.ipynb) em um Documento de Implementação Técnica formatado (.docx)</p>
    """)
    
    with gr.Row():
        with gr.Column():
            token_input = gr.Textbox(
                label="Token OpenAI",
                placeholder="Insira seu token da API OpenAI aqui...",
                type="password"
            )
            
            with gr.Row():
                diretorio_input = gr.Textbox(
                    label="Diretório dos Notebooks",
                    placeholder="Caminho para a pasta com os arquivos .ipynb"
                )
                diretorio_btn_source = gr.Button("📁 Procurar")
            
            with gr.Row():
                limpar_btn = gr.Button("🔄 Limpar")
                processar_btn = gr.Button("⚙️ Processar", variant="primary")
        
        with gr.Column():
            status_output = gr.Textbox(label="Status")
            arquivo_output = gr.File(label="Documento Gerado")

    diretorio_btn_source.click(selecionar_diretorio, outputs=diretorio_input)
    processar_btn.click(
        processar_notebooks,
        inputs=[token_input, diretorio_input],
        outputs=[status_output, arquivo_output]
    )
    limpar_btn.click(
        limpar,
        outputs=[token_input, diretorio_input, arquivo_output, status_output]
    )

if __name__ == "__main__":
    interface.launch(server_port=7860)