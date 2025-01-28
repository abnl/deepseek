FROM ollama/ollama:latest

# Copie o script para dentro do contêiner
COPY entrypoint.sh /entrypoint.sh

# Torne o script executável
RUN chmod +x /entrypoint.sh

# Configure o ENTRYPOINT para o script
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
