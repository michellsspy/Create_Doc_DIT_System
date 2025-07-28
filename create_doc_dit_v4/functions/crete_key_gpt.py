from pathlib import Path
import os

def crete_key_gpt(base_dir: Path):
    create_path = base_dir / "key"
    file_path = create_path / "OPENAI_API_KEY.txt"

    if os.path.exists(file_path):
        print(f"O arquivo '{file_path}' já existe.")
        with open(file_path, "r", encoding="utf-8") as f:
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
    