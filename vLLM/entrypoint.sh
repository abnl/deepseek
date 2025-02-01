#!/bin/bash

echo "Iniciando vLLM com modelo DeepSeek-R1:1.5b baixado dentro do container..."

# Verifica se CUDA está disponível
if ! command -v nvidia-smi &> /dev/null
then
    echo "CUDA não encontrado! Certifique-se de que os drivers NVIDIA estão instalados."
    exit 1
fi

# Aguarda um pouco para garantir que tudo está pronto
sleep 5

# Usa o ambiente virtual para rodar o vLLM
/app/venv/bin/python -m vllm.entrypoints.openai.api_server --model /models/DeepSeek-R1-Zero --host 0.0.0.0 --port 8000
