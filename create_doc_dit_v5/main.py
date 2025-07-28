import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import logging

# ---------------------------------------------------------------------------------------------------------------------
def main():
    try:
        import nbconvert
    except ImportError:
        print("[ERRO] nbconvert não está instalado. Tentando instalar...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "nbconvert"])
        except Exception as install_error:
            print(f"[ERRO] Falha ao instalar nbconvert: {install_error}")
            sys.exit(1)
        
    from pathlib import Path
    import os
    base_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(base_dir / "functions"))

    from functions.log import configurar_logger
    from functions.estrutura import criar_pastas as criar_pastas_dinamico
    from functions.conversao import converte_to_md
    from functions.upsert_key_gpt import upsert_key_gpt
    from functions.crete_key_gpt import crete_key_gpt

    global logger
    logger = configurar_logger(base_dir)

    logger.info("[OK] Biblioteca 'nbconvert' disponível.")
    logger.info("[OK] Iniciando conversão de notebooks para Markdown...")


    notebooks_dir = base_dir / "notebooks"
    notebooks = [f for f in notebooks_dir.glob("*.ipynb") if f.is_file()]

    if not notebooks:
        logger.warning("[!] Nenhum arquivo .ipynb encontrado em /notebooks")
        return

    total = len(notebooks)
    convertidos = 0
    falhas = 0

    for arquivo in notebooks:
        sucesso = converte_to_md(arquivo, base_dir, logger)
        if sucesso:
            convertidos += 1
        else:
            falhas += 1

    logger.info("========== RESUMO DA EXECUÇÃO ========")
    logger.info(f"Total de arquivos encontrados______: {total}")
    logger.info(f"Convertidos com sucesso____________: {convertidos}")
    logger.info(f"Falharam na conversão______________: {falhas}")
    logger.info("======================================\n")

    print()
    resposta = input("Deseja criar um arquivo Dit? (S/n): ").strip().lower()
    if resposta in ["s", "sim", ""]:
        
        # Criação do arquivo de chave da OpenAI
        crete_key_gpt(base_dir)
    
        dit_path = base_dir / "doc" / "notebooks.docx"
        with open(dit_path, "w", encoding="utf-8") as dit_file:
            for arquivo in notebooks:
                dit_file.write(f"{arquivo.name}\n")
        logger.info(f"[+] Arquivo Dit criado: {dit_path}")
    else:
        logger.info("[=] Criação do arquivo Dit cancelada.")


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
