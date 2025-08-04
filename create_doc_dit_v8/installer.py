import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import logging

def esta_em_venv():
    import sys
    import os
    
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get("VIRTUAL_ENV") is not None
    )

def garantir_venv():
    import os
    import sys
    import subprocess
    from pathlib import Path
    
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / ".venv"

    if not venv_dir.exists():
        print("[⚙️ ] Ambiente virtual '.venv' não encontrado. Criando...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
        print("[✓] Ambiente virtual criado com sucesso.")

    if not esta_em_venv():
        print("[🔄] Reiniciando o script dentro do ambiente virtual...")
        if os.name == "nt":
            python_venv = venv_dir / "Scripts" / "python.exe"
        else:
            python_venv = venv_dir / "bin" / "python"
        os.execv(str(python_venv), [str(python_venv)] + sys.argv)


def installer_packages():
    import subprocess
    import sys

    pacotes = [
        "ipykernel",
        "langchain==0.1.16",
        "langchain-community==0.0.33",
        "langchain-openai==0.1.3",
        "openai==1.55.3",
        "huggingface_hub==0.22.2",
        "transformers==4.39.3",
        "jinja2==3.1.3",
        "tiktoken==0.6.0",
        "pypdf==4.2.0",
        "yt_dlp==2024.4.9",
        "pydub==0.25.1",
        "beautifulsoup4==4.12.3",
        "python-dotenv",
        "sentence-transformers==2.7.0",
        "langchain-chroma",
        "faiss-cpu",
        "lark",
        "nbconvert"
    ]

    for lib in pacotes:
        if lib.strip() and not lib.strip().startswith("#"):
            lib_name = lib.split("==")[0].strip()
            try:
                pip_lib = subprocess.run([sys.executable, "-m", "pip", "show", lib_name], check=True, capture_output=True, text=True)
                if lib_name in pip_lib.stdout:
                    print(f"Já instalado: {lib}")
                else:
                    print(f"Instalando: {lib}")
                    subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
            except subprocess.CalledProcessError:
                print(f"Instalando (não encontrado): {lib}")
                subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
        else:
            print(f"Pulando: {lib}")


# ---------------------------------------------------------------------------------------------------------------------

PASTAS = ['doc', 'notebooks', 'scripts', 'pdf', 'info', 'log', 'functions', 'markdown', 'key', 'packages']

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------------------------------------------
def criar_pastas(base_dir: Path):
    for pasta in PASTAS:
        dir_path = base_dir / pasta
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            logger.info(f"[+] Criada pasta: {dir_path}")
            if pasta == "functions":
                criar_funcoes_padrao(dir_path)
        else:
            logger.info(f"[=] Pasta já existe: {dir_path}")

# ---------------------------------------------------------------------------------------------------------------------
def cria_env(base_dir: Path):
    venv_dir = base_dir / ".env"
    if not venv_dir.exists():
        print("[⚙️ ] Arquivo env não encontrado...")
        with open(venv_dir, "w", encoding="utf-8") as env_file:
            env_file.write("# Variáveis de ambiente\n")
            env_file.write("OPENAI_API_KEY=\n")
            env_file.write("HUGGINGFACE_API_KEY=\n")
        print("[✓] Arquivo env criado com sucesso.")
    else:
        print("[=] Arquivo '.env' já existe.")
          
# ---------------------------------------------------------------------------------------------------------------------
def criar_funcoes_padrao(functions_dir: Path):
    logger.info(f"[*] Inicializando arquivos padrão em {functions_dir}")

    (functions_dir / "__init__.py").write_text("", encoding="utf-8")

    log_code = '''\
import logging
import sys
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def configurar_logger(base_dir: Path):
    log_dir = base_dir / "log"
    log_dir.mkdir(parents=True, exist_ok=True)

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
    return logger
'''
    (functions_dir / "log.py").write_text(log_code, encoding="utf-8")
    logger.info("[+] Criado: log.py")

    estrutura_code = '''\
def criar_pastas(base_dir, pastas, logger):
    for pasta in pastas:
        dir_path = base_dir / pasta
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            logger.info(f"[+] Criada pasta: {dir_path}")
        else:
            logger.info(f"[=] Pasta já existe: {dir_path}")
        if pasta == "functions":
            from pathlib import Path
            from main import criar_funcoes_padrao
            criar_funcoes_padrao(dir_path)
'''
    (functions_dir / "estrutura.py").write_text(estrutura_code, encoding="utf-8")
    logger.info("[+] Criado: estrutura.py")

    conversao_code = '''\
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
        logger.info(f"[✓] Convertido para Markdown com sucesso: {arquivo_path.name}\\n")
        return True
    except subprocess.CalledProcessError as e:
        logger.exception(f"[✗] Erro durante a conversão de {arquivo_path.name}: {e}\\n")
        return False
'''
    (functions_dir / "conversao.py").write_text(conversao_code, encoding="utf-8")
    logger.info("[+] Criado: conversao.py")

# ---------------------------------------------------------------------------------------------------------------------
    upsert_key_gpt_code = '''\
from pathlib import Path
import os

def upsert_key_gpt(base_dir: Path):
    venv_dir = base_dir / ".env"

    get_key = input("Cole aqui o token da conta OpenAI: ")
    with open(venv_dir, "w", encoding="utf-8") as env_file:
        env_file.write("# Variáveis de ambiente\\n")
        env_file.write(f"OPENAI_API_KEY='{get_key}'\\n")
        env_file.write("HUGGINGFACE_API_KEY=''\\n")
    print("[✓] Arquivo env criado com sucesso.")

    print(f"Token salvo em '{venv_dir}'")
    return get_key
    '''
    (functions_dir / "upsert_key_gpt.py").write_text(upsert_key_gpt_code, encoding="utf-8")
    logger.info("[+] Criado: upsert_key_gpt.py")

# ---------------------------------------------------------------------------------------------------------------------
    create_key_gpt_code = '''\
from pathlib import Path
import os

def create_key_gpt(base_dir: Path):
    venv_dir = base_dir / ".env"

    if os.path.exists(venv_dir):
        print(f"O arquivo '{venv_dir}' já existe.")
        with open(venv_dir, "r", encoding="utf-8") as f:
            key = f.read().strip()
        print("Token atual:\\n", key)
        resp = input("Deseja alterar o token? (s/n): ").strip().lower()
        if resp == 's':
            from functions.upsert_key_gpt import upsert_key_gpt
            return upsert_key_gpt(base_dir)
        else:
            print("Nenhuma alteração foi feita.")
        return key
    else:
        from functions.upsert_key_gpt import upsert_key_gpt
        return upsert_key_gpt(base_dir)
    '''
    (functions_dir / "create_key_gpt.py").write_text(create_key_gpt_code, encoding="utf-8")
    logger.info("[+] Criado: create_key_gpt.py")

# ---------------------------------------------------------------------------------------------------------------------
    esta_em_venv_code = '''\
def esta_em_venv():
    import sys
    import os
    
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get("VIRTUAL_ENV") is not None
    )
    '''
    (functions_dir / "esta_em_venv.py").write_text(esta_em_venv_code, encoding="utf-8")
    logger.info("[+] Criado: esta_em_venv.py")

# ---------------------------------------------------------------------------------------------------------------------
    garantir_venv_code = '''\    
def garantir_venv():
    import os
    import sys
    import subprocess
    from pathlib import Path
    
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / ".venv"

    if not venv_dir.exists():
        print("[⚙️ ] Ambiente virtual '.venv' não encontrado. Criando...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
        print("[✓] Ambiente virtual criado com sucesso.")

    if not garantir_venv():
        print("[🔄] Reiniciando o script dentro do ambiente virtual...")
        if os.name == "nt":
            python_venv = venv_dir / "Scripts" / "python.exe"
        else:
            python_venv = venv_dir / "bin" / "python"
        os.execv(str(python_venv), [str(python_venv)] + sys.argv)
    '''
    (functions_dir / "garantir_venv.py").write_text(garantir_venv_code, encoding="utf-8")
    logger.info("[+] Criado: esta_em_venv.py")
    
# Criar_funcoes_padrao (no final do script)
def main():
    garantir_venv()
    installer_packages()
    cria_env(Path(__file__).resolve().parent)
    criar_pastas(Path(__file__).resolve().parent)
    print("[✓] Ambiente configurado com sucesso. Execute 'python main.py' para iniciar.")

if __name__ == "__main__":
    main()
    logger.info("[*] Arquivo Dit não criado.")
    logger.info("[*] Finalizando o script.")
