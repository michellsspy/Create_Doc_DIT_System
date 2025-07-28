from pathlib import Path
import subprocess

base_dir = Path(__file__).resolve().parent
requirements = base_dir / "requirements.txt"

with open(requirements, "r", encoding="utf-8") as f:
    lista = f.read().strip().splitlines()

print(f"requirements: {lista}")

for lib in lista:
    if lib.strip() and not lib.strip().startswith("#"):
        lib_name = lib.split("==")[0].strip()  # Remove versão para o pip show

        try:
            pip_lib = subprocess.run(["pip", "show", lib_name], check=True, capture_output=True, text=True)
            if lib_name in pip_lib.stdout:
                print(f"Já instalado: {lib}")
            else:
                print(f"Instalando: {lib}")
                subprocess.run(["pip", "install", lib], check=True)
        except subprocess.CalledProcessError:
            print(f"Instalando (não encontrado): {lib}")
            subprocess.run(["pip", "install", lib], check=True)
    else:
        print(f"Pulando: {lib}")
