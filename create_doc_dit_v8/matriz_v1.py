import gradio as gr
import os
import json
from pathlib import Path
from dotenv import load_dotenv, set_key
import tkinter as tk
from tkinter import filedialog

# Função para selecionar diretório usando tkinter
def selecionar_diretorio():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    root.wm_attributes('-topmost', 1)  # Mantém no topo
    diretorio = filedialog.askdirectory(title="Selecione a pasta com os notebooks")
    return diretorio if diretorio else ""

# Função principal que executa todo o processo
def processar_notebooks(token: str, diretorio: str):
    # Salva o token no arquivo .env
    env_path = Path(".env")
    if not env_path.exists():
        env_path.touch()
    set_key(env_path, "OPENAI_API_KEY", token)
    load_dotenv()  # Recarrega as variáveis de ambiente
    
    # Verifica se o diretório existe
    if not os.path.isdir(diretorio):
        return "Erro: Diretório inválido ou inexistente.", None
    
    # Verifica se há arquivos .ipynb no diretório
    arquivos = [f for f in os.listdir(diretorio) if f.endswith(".ipynb")]
    if not arquivos:
        return "Erro: Nenhum arquivo .ipynb encontrado no diretório.", None
    
    # Cria a estrutura de pastas necessária
    os.makedirs("notebooks", exist_ok=True)
    os.makedirs("markdown", exist_ok=True)
    os.makedirs("doc", exist_ok=True)
    
    # Copia os notebooks para a pasta notebooks/
    for arquivo in arquivos:
        os.system(f'copy "{os.path.join(diretorio, arquivo)}" "notebooks\\{arquivo}"')
    
    # Executa o script principal
    try:
        from main import main
        main()
        
        # Verifica se o arquivo foi criado
        dit_path = os.path.join("doc", "DIT.docx")
        if os.path.exists(dit_path):
            mensagem = f"Processamento concluído: {len(arquivos)} notebook(s) convertido(s) para DIT.docx"
            return mensagem, dit_path
        else:
            return "Erro: O arquivo DIT.docx não foi gerado corretamente.", None
    except Exception as e:
        return f"Erro durante o processamento: {str(e)}", None

# Função para limpar os dados
def limpar():
    return "", "", None, ""

# Interface com Gradio
with gr.Blocks(title="Conversor de Notebooks para DIT") as interface:
    gr.Markdown("## Conversor de Notebooks Jupyter para Documento Técnico (DIT)")
    gr.Markdown("Esta ferramenta converte notebooks Jupyter (.ipynb) em um Documento de Implementação Técnica formatado (.docx)")
    
    with gr.Row():
        with gr.Column(scale=1):
            token_input = gr.Textbox(
                label="Token da OpenAI",
                placeholder="Insira seu token da API OpenAI aqui",
                type="password"
            )
            
            with gr.Row():
                diretorio_input = gr.Textbox(
                    label="Diretório dos Notebooks",
                    placeholder="Caminho para a pasta com os arquivos .ipynb"
                )
                diretorio_btn = gr.Button("Procurar", size="sm")
            
            with gr.Row():
                limpar_btn = gr.Button("Limpar Tudo", variant="secondary")
                submeter_btn = gr.Button("Processar Notebooks", variant="primary")

        with gr.Column(scale=1):
            comentario_output = gr.Textbox(
                label="Status do Processamento",
                interactive=False
            )
            arquivo_saida = gr.File(
                label="Documento DIT Gerado",
                interactive=False,
                file_types=[".docx"]
            )
    
    # Lógica dos botões
    submeter_btn.click(
        fn=processar_notebooks,
        inputs=[token_input, diretorio_input],
        outputs=[comentario_output, arquivo_saida]
    )
    
    limpar_btn.click(
        fn=limpar,
        inputs=[],
        outputs=[token_input, diretorio_input, arquivo_saida, comentario_output]
    )
    
    # Configuração do botão de procurar diretório
    diretorio_btn.click(
        fn=selecionar_diretorio,
        outputs=diretorio_input
    )

if __name__ == "__main__":
    interface.launch()