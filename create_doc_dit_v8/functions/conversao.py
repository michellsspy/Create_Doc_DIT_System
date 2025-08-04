import subprocess
import sys

def converte_to_md(arquivo_path, base_dir, logger):
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
