from pathlib import Path
import os

def crete_key_gpt(base_dir: Path):
    venv_dir = base_dir / ".env"

    if os.path.exists(venv_dir):
        print(f"O arquivo '{venv_dir}' já existe.")
        with open(venv_dir, "r", encoding="utf-8") as f:
            key = f.read().strip()
        print("Token atual:\n", key)
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
    