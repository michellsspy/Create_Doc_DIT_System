def criar_pastas(base_dir, pastas, logger):
    for pasta in pastas:
        dir_path = base_dir / pasta
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            logger.info(f"[+] Criada pasta: {dir_path}")
        else:
            logger.info(f"[=] Pasta já existe: {dir_path}")
        if pasta == ".functions":
            from pathlib import Path
            from main import criar_funcoes_padrao
            criar_funcoes_padrao(dir_path)
