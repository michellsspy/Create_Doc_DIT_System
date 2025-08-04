import gradio as gr
import os
import json

# Função que transforma arquivos de texto em estrutura simulada de DIT
def gerar_dit(token: str, diretorio: str):
    if not token.strip():
        return "Erro: Token não pode estar vazio.", None

    if not os.path.isdir(diretorio):
        return "Erro: Diretório inválido ou inexistente.", None

    arquivos = [f for f in os.listdir(diretorio) if f.endswith(".txt")]
    if not arquivos:
        return "Erro: Nenhum arquivo .txt encontrado no diretório.", None

    estrutura_dit = []

    for arquivo in arquivos:
        caminho = os.path.join(diretorio, arquivo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
            estrutura_dit.append({
                "arquivo": arquivo,
                "conteudo": conteudo.strip()
            })
        except Exception as e:
            return f"Erro ao ler {arquivo}: {str(e)}", None

    # Criação do arquivo JSON (DIT)
    os.makedirs("saida", exist_ok=True)
    caminho_saida = os.path.join("saida", "DIT_transformado.json")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(estrutura_dit, f, indent=2, ensure_ascii=False)

    comentario = f"Transformação concluída: {len(arquivos)} arquivo(s) processado(s)."
    return comentario, caminho_saida

# Função para limpar os dados
def limpar():
    return "", "", None, ""

# Interface com Gradio
with gr.Blocks() as interface:
    with gr.Row():
        with gr.Column(scale=1):
            token_input = gr.Textbox(label="Token GPT", placeholder="Insira o token aqui")
            diretorio_input = gr.Textbox(label="Caminho Local dos Documentos", placeholder="Ex: C:/meus_docs")
            with gr.Row():
                limpar_btn = gr.Button("Limpar")
                submeter_btn = gr.Button("Submeter")

        with gr.Column(scale=1):
            comentario_output = gr.Textbox(label="Comentário de Sucesso", interactive=False)
            arquivo_saida = gr.File(label="Arquivo DIT (JSON)", interactive=False)

    # Lógica dos botões
    submeter_btn.click(fn=gerar_dit,
                       inputs=[token_input, diretorio_input],
                       outputs=[comentario_output, arquivo_saida])

    limpar_btn.click(fn=limpar,
                     inputs=[],
                     outputs=[token_input, diretorio_input, arquivo_saida, comentario_output])

if __name__ == "__main__":
    interface.launch()