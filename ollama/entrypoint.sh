#!/bin/sh

# Inicie o servidor Ollama em background
ollama serve &

# Aguarde o servidor iniciar
sleep 5

# Faça o pull do modelo necessário (usando a variável MODEL_NAME)
ollama pull "${MODEL_NAME}"

# Mantenha o contêiner rodando
tail -f /dev/null
