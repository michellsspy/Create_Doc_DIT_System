import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import logging

PASTAS = ['doc', 'notebooks', 'scripts', 'pdf', '.info', '.log', '.exec', '.functions', 'markdown']

# Logger global
logger = logging.getLogger(__name__)

def configurar_logger(base_dir: Path):
    log_dir = base_dir / ".log"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Nome do arquivo no formato ano_mes_dia_hora_minuto_segundo.log
    log_filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"
    log_path = log_dir / log_filename

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger.info(f"Arquivo de log criado: {log_path}")

def criar_pastas(base_dir: Path):
    for pasta in PASTAS:
        dir_path = base_dir / pasta
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            logger.info(f"[+] Criada pasta: {dir_path}")
        else:
            logger.info(f"[=] Pasta já existe: {dir_path}")
            
def converte_to_md(arquivo_path: Path, base_dir: Path) -> bool:
    if not arquivo_path.exists():
        logger.error(f"[✗] Arquivo '{arquivo_path}' não encontrado.")
        return False

    try:
        markdown_dir = base_dir / "markdown"
        subprocess.check_call([
            sys.executable, "-m", "nbconvert",
            "--to", "markdown",
            "--output-dir", str(markdown_dir),
            str(arquivo_path)
        ])
        logger.info(f"[✓] Convertido para Markdown com sucesso: {arquivo_path.name}\n")
        return True
    except subprocess.CalledProcessError as e:
        logger.exception(f"[✗] Erro durante a conversão de {arquivo_path.name}: {e}\n")
        return False

            
def main():
    base_dir = Path(__file__).resolve().parent

    configurar_logger(base_dir)

    logger.info("[OK] Biblioteca 'nbconvert' disponível.")
    logger.info("[OK] Iniciando conversão de notebooks para Markdown...")

    criar_pastas(base_dir)

    notebooks_dir = base_dir / "notebooks"
    notebooks = [f for f in notebooks_dir.glob("*.ipynb") if f.is_file()]

    if not notebooks:
        logger.warning("[!] Nenhum arquivo .ipynb encontrado em /notebooks")
        return

    total = len(notebooks)
    convertidos = 0
    falhas = 0

    for arquivo in notebooks:
        sucesso = converte_to_md(arquivo, base_dir)
        if sucesso:
            convertidos += 1
        else:
            falhas += 1

    logger.info("========== RESUMO DA EXECUÇÃO ========")
    logger.info(f"Total de arquivos encontrados______: {total}")
    logger.info(f"Convertidos com sucesso____________: {convertidos}")
    logger.info(f"Falharam na conversão______________: {falhas}")
    logger.info("======================================\n")


if __name__ == "__main__":
    try:
        import nbconvert
    except ImportError as e:
        print("[ERRO] nbconvert não está instalado. Tentando instalar...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "nbconvert"])
            import nbconvert
        except Exception as install_error:
            print(f"[ERRO] Falha ao instalar nbconvert: {install_error}")
            sys.exit(1)

    main()
