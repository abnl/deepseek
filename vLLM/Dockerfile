# Usa a imagem base compatível com CUDA
FROM nvidia/cuda:12.8.0-cudnn-devel-ubuntu24.04

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências essenciais
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git-lfs && \
    rm -rf /var/lib/apt/lists/*

# Corrige possíveis problemas de Python 3.12 (Ubuntu 24.04)
# RUN ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip

# Cria um ambiente virtual para evitar erros do PEP 668
RUN python3 -m venv /app/venv

# Ativa o ambiente virtual e instala dependências
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install vllm openai torch huggingface_hub

# Define diretório onde o modelo será salvo
WORKDIR /models

# Define o token de autenticação do Hugging Face como argumento de build
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Autentica no Hugging Face e baixa o modelo
RUN /app/venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='deepseek-ai/DeepSeek-R1-Zero', local_dir='/models/DeepSeek-R1-Zero', token='${HF_TOKEN}')"

# Copia o entrypoint para dentro do container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Usa o ambiente virtual para rodar o entrypoint
ENV PATH="/app/venv/bin:$PATH"

# Define o ponto de entrada
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
