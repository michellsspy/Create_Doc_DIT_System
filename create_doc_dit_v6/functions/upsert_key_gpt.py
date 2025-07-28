from pathlib import Path
import os

def upsert_key_gpt(base_dir: Path):
    venv_dir = base_dir / ".env"

    get_key = input("Cole aqui o token da conta OpenAI: ")
    with open(venv_dir, "w", encoding="utf-8") as env_file:
        env_file.write("# Variáveis de ambiente\n")
        env_file.write(f"OPENAI_API_KEY='{get_key}'\n")
        env_file.write("HUGGINGFACE_API_KEY=''\n")
    print("[✓] Arquivo env criado com sucesso.")

    print(f"Token salvo em '{venv_dir}'")
    return get_key
    