# 🔍 Multi-Source RAG Assistant

Este projeto é um assistente de Recuperação de Informação (RAG - Retrieval Augmented Generation) que permite consultas em múltiplas fontes, como arquivos PDF, documentos Word, vídeos do YouTube, sites e mais. Ele utiliza modelos de linguagem da OpenAI e integração com o LangChain, FAISS e outras ferramentas de NLP.

---

## ⚙️ Tecnologias e Dependências

Este projeto foi desenvolvido originalmente em **Linux Ubuntu**, e seu funcionamento completo depende da instalação das bibliotecas abaixo:

### 📦 Bibliotecas Python

- `ipykernel`
- `langchain==0.1.16`
- `langchain-community==0.0.33`
- `langchain-openai==0.1.3`
- `openai==1.55.3`
- `huggingface_hub==0.22.2`
- `transformers==4.39.3`
- `jinja2==3.1.3`
- `tiktoken==0.6.0`
- `pypdf==4.2.0`
- `yt_dlp==2024.4.9`
- `pydub==0.25.1`
- `beautifulsoup4==4.12.3`
- `sentence-transformers==2.7.0`
- `langchain-chroma`
- `faiss-cpu`
- `lark`
- `python-dotenv`
- `python-docx`

### 🛠️ Dependências do Sistema

- `ffmpeg`  
- `ffprobe`

Essas dependências são fundamentais para o correto funcionamento de manipulação de vídeos, extração de áudio e transcrições.

---

## 🚀 Instalação Automática

Para recriar todo o ambiente automaticamente, basta executar o seguinte script:

```bash
python installer.py
