\    
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
    