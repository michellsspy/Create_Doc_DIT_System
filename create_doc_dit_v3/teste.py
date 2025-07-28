import os

def insert_or_alter_key_gpt():
    file_path = "key/OPENAI_API_KEY.txt"

    get_key = input("Cole aqui o token da OpenAI: ")
        
    # Garante que a pasta 'key/' exista
    os.makedirs("key", exist_ok=True)

    with open(file_path, "w") as file:
        file.write(get_key)

    print("Token salvo em 'key/OPENAI_API_KEY.txt'")
    return get_key

def crete_key_gpt():
    file_path = "key/OPENAI_API_KEY.txt"

    # Verifica se o arquivo já existe
    if os.path.exists(file_path):
        print(f"O arquivo '{file_path}' já existe.")
        with open(file_path, "r") as f:
            key = f.read().strip()
        print("Token atual:\n", key)
        resp = input("Deseja alterar o token? (s/n): ").strip().lower()
        if resp == 's':
            insert_or_alter_key_gpt()
        else:
            print("Nenhuma alteração foi feita.")
        return key
    else:
        insert_or_alter_key_gpt()
crete_key_gpt()