from pathlib import Path
import os

def upsert_key_gpt(base_dir: Path):
    upsert_path = base_dir / "key"
    file_path = upsert_path / "OPENAI_API_KEY.txt"

    # Garante que o diretório seja criado com base no base_dir informado
    os.makedirs(upsert_path, exist_ok=True)

    get_key = input("Cole aqui o token da OpenAI: ")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(get_key)

    print(f"Token salvo em '{file_path}'")
    return get_key
    