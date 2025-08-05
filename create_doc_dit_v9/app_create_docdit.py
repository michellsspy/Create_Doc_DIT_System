# IMPORTAÇÃO DAS BIBLIOTECAS
import subprocess
import sys
import os
import logging
from pathlib import Path
from datetime import datetime
import platform
import psutil  # pip install psutil (para infos de hardware)
import shutil


# Configuração do arquivo de instalação
# Define o caminho do arquivo de instalação como "install.txt" no diretório atual   
def criar_arquivo_instalacao(caminho_arquivo: Path):
    """
    Cria um arquivo .txt com informações detalhadas da instalação caso não exista.
    Escreve um cabeçalho com título e muitas informações do sistema e ambiente.
    """

    if not caminho_arquivo.exists():
        info = f"""\
===========================================
          SISTEMA: Create Doc DIT System
===========================================

Data da Instalação: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Descrição:
Este arquivo contém informações gerais sobre a instalação do sistema Create Doc DIT.

Arquitetura pós instalação:
    Create_Doc_DIT_System/
    │
    ├── .venv/                      # Ambiente virtual
    ├── doc/                        # Documentos carregados
    ├── .env                        # Variáveis de ambiente
    ├── functions/                  # Funções do sistema   
    │   ├── __init__.py             # Inicialização do módulo
    │   ├── log.py                  # Configuração do logger 
    │   ├── estrutura.py            # Criação de pastas
    │   ├── conversao.py            # Conversão de arquivos
    │   ├── upsert_key_gpt.py       # Inserção de chave da API OpenAI
    │   ├── create_key_gpt.py       # Criação/atualização da chave da API OpenAI
    │   ├── esta_em_venv.py         # Verificação do ambiente virtual
    |   ├── garantir_venv.py        # Garantia do ambiente virtual        
    ├── log/                        # Logs do sistema
    ├── markdown/                   # Arquivos convertidos para Markdown
    ├── notebooks/                  # Notebooks Jupyter
    ├── docdit_app.exe                  # Executável do sistema (se aplicável)

Informações do Ambiente:

- Sistema Operacional: {platform.system()} {platform.release()} ({platform.version()})
- Nome do Host: {platform.node()}
- Arquitetura: {platform.machine()}
- Processador: {platform.processor() or "N/A"}
- Número de CPUs: {psutil.cpu_count(logical=True)}
- Memória RAM Total: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB
- Espaço Disco Disponível (na pasta atual): {round(shutil.disk_usage(caminho_arquivo.parent).free / (1024 ** 3), 2)} GB
- Python Version: {platform.python_version()}
- Python Implementação: {platform.python_implementation()}
- Caminho do Python: {sys.executable}

Variáveis de Ambiente Importantes:
"""

        # Variáveis de ambiente comuns para exibir
        variaveis_ambiente = [
            "PATH", "HOME", "USER", "USERNAME", "VIRTUAL_ENV", "PYTHONPATH", "PYTHONHOME", "OPENAI_API_KEY"
        ]
        for var in variaveis_ambiente:
            valor = os.environ.get(var, "Não definido")
            info += f"  - {var}: {valor}\n"

        info += "\n-------------------------------------------\n"

        with caminho_arquivo.open("w", encoding="utf-8") as f:
            f.write(info)
        print(f"[✓] Arquivo criado: {caminho_arquivo}")
    else:
        print(f"[=] Arquivo já existe: {caminho_arquivo}")

# FUNÇÕES DO SYSTEMA

# Função para verificar se o script está rodando dentro de um ambiente virtual
# Ela verifica se o prefixo base do Python é diferente do prefixo real, ou se a variável de ambiente VIRTUAL_ENV está definida.
# Se estiver, retorna True; caso contrário, retorna False.
def esta_em_venv():
    import sys
    import os
    
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get("VIRTUAL_ENV") is not None
    )

# Função para garantir que o ambiente virtual está ativo
# Ela verifica se o diretório do ambiente virtual existe. Se não existir, cria um novo ambiente virtual.
# Se o script não estiver rodando dentro do ambiente virtual, reinicia o script dentro do ambiente virtual.
# Ela usa o módulo subprocess para chamar o comando de criação do ambiente virtual e reiniciar o script.
# O caminho do ambiente virtual é definido como ".venv" dentro do diretório do script.
# Se o ambiente virtual já existir, não faz nada.
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

# Função para atualizar o pip para a última versão
# Ela usa o módulo subprocess para chamar o comando de atualização do pip.
def atualizar_pip():
    import subprocess
    import sys
    try:
        print("[⚙️] Atualizando pip para a última versão...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("[✓] pip atualizado.")
    except subprocess.CalledProcessError as e:
        print(f"[✗] Erro ao atualizar pip: {e}")
        sys.exit(1)


# Função para instalar pacotes necessários
# Ela define uma lista de pacotes e suas versões, verifica se cada pacote já está instalado 
def installer_packages():
    import subprocess
    import sys
    
    atualizar_pip()

    pacotes = [
        'ipykernel',
        'langchain==0.1.16',
        'langchain-community==0.0.33',
        'langchain-openai==0.1.3',
        'openai==1.55.3',
        'huggingface_hub==0.22.2',
        'transformers==4.39.3',
        'jinja2==3.1.3',
        'tiktoken==0.6.0',
        'pypdf==4.2.0',
        'yt_dlp==2024.4.9',
        'pydub==0.25.1',
        'beautifulsoup4==4.12.3',
        'python-dotenv',
        'sentence-transformers==2.7.0',
        'langchain-chroma',
        'faiss-cpu',
        'lark',
        'python-docx',
        'gradio==5.39.0',
        'psutil',
        "nbconvert"
    ]
        
        
    # Verifica se está em venv
    if not esta_em_venv():
        print("[⚠️ ] O script não está rodando dentro de um ambiente virtual. Criando um...")
        garantir_venv()
        print("[✓] Ambiente virtual criado com sucesso.")
        # Ao criar o venv, o script reinicia, então aqui provavelmente não chega a continuar
        return
    else:
        print("[✓] Ambiente virtual já está ativo.")

    print("[⚙️] Instalando pacotes necessários...")
    for lib in pacotes:
        if lib.strip() and not lib.strip().startswith("#"):
            lib_name = lib.split("==")[0].strip()
            try:
                # Verifica se pacote já instalado
                pip_show = subprocess.run(
                    [sys.executable, "-m", "pip", "show", lib_name],
                    check=True, capture_output=True, text=True
                )
                if lib_name.lower() in pip_show.stdout.lower():
                    print(f"[✓] Já instalado: {lib}")
                    continue
            except subprocess.CalledProcessError:
                # Não encontrado, vai instalar
                pass

            # Tenta instalar o pacote com flag --no-cache-dir para evitar problemas com arquivos temporários
            print(f"[⚙️] Instalando: {lib}")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", lib, "--no-cache-dir"],
                    check=True
                )
                print(f"[✓] Pacote instalado com sucesso: {lib}")
            except subprocess.CalledProcessError as e:
                print(f"[✗] Erro ao instalar {lib}: {e}. Continuando com próximo pacote...")
        else:
            print(f"[→] Pulando: {lib}")
    print("[✓] Instalação de pacotes concluída.")


# ---------------------------------------------------------------------------------------------------------------------
# Definição das pastas padrão
# Esta lista contém os nomes das pastas que serão criadas no diretório base do projeto  
PASTAS = ['doc', 'notebooks', 'log', 'functions', 'markdown']

# Configuração do logger
# O logger é configurado para registrar mensagens de log no console e em um arquivo de log
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------------------------------------------
# Função para criar as pastas padrão
# Ela verifica se cada pasta já existe. Se não existir, cria a pasta e registra uma mensagem de log.
# Se a pasta for "functions", chama a função criar_funcoes_padrao para inicializar os arquivos padrão dentro dessa pasta.
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
# Função para criar o arquivo de ambiente (.env)
# Ela verifica se o arquivo já existe. Se não existir, cria o arquivo e escreve as variáveis de ambiente padrão.
# As variáveis de ambiente incluem a chave da API do OpenAI e a chave da API do Hugging Face.
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
# Função para criar os arquivos padrão na pasta "functions"
# Ela cria o arquivo __init__.py vazio, e os arquivos log.py, estrutura.py, conversao.py, upsert_key_gpt.py, create_key_gpt.py, esta_em_venv.py e garantir_venv.py com códigos específicos.
# Cada arquivo contém funções específicas para o sistema, como configuração de logger, criação de pastas, conversão de arquivos, inserção de chaves da API do OpenAI, verificação do ambiente virtual e garantia de que o ambiente virtual está ativo.
# Ela registra uma mensagem de log para cada arquivo criado.
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
    
# ---------------------------------------------------------------------------------------------------------------------
# Função principal que executa as etapas de configuração do ambiente
# Ela garante que o ambiente virtual está ativo, instala os pacotes necessários, cria o arquivo de ambiente (.env) e cria as pastas padrão.
# Ao final, imprime uma mensagem de sucesso e orienta o usuário a executar o script principal   
def main():
    garantir_venv()
    installer_packages()
    cria_env(Path(__file__).resolve().parent)
    criar_pastas(Path(__file__).resolve().parent)
    print("[✓] Ambiente configurado com sucesso. Execute 'python main.py' para iniciar.")

# ---------------------------------------------------------------------------------------------------------------------
# Verifica se o script está sendo executado diretamente 
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    caminho_arquivo = base_dir / "informacoes_instalacao.txt"

    if not caminho_arquivo.exists():
        print("Arquivo não existe. Criando arquivo de instalação...")
        criar_arquivo_instalacao(caminho_arquivo)
        print("Arquivo criado. Agora executando main()...")
        main()
        logger.info("[*] Arquivo Dit não criado.")  # Talvez ajustar essa mensagem?
        logger.info("[*] Finalizando o script.")
    else:
        print("Arquivo existe.")


