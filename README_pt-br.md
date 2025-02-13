# Como Configurar e Rodar o DeepSeek-R1 Localmente: Tutorial com Docker e Docker Compose

O **DeepSeek-R1** é um modelo avançado de IA projetado para executar tarefas complexas, como raciocínio lógico, programação e matemática. Rodá-lo localmente garante maior controle sobre os dados, personalização para projetos específicos e economia com servidores externos. Neste tutorial, você aprenderá duas formas de configurá-lo: manualmente com **Docker** e de forma automatizada com **Docker Compose**.

## Por que Rodar o DeepSeek-R1 Localmente?

- Privacidade: Seus dados permanecem no ambiente local.
- Economia: Reduz custos com servidores em nuvem.
- Personalização: Facilita ajustes no ambiente e personalizações.

## Arquitetura e implantação do DeepSeek-R1

O **DeepSeek-R1** é um modelo de IA de ponta projetado para tarefas complexas, como raciocínio lógico e resolução de problemas matemáticos. Ele combina **aprendizado por reforço** (RL) e ajuste **supervisionado** para alcançar desempenho superior em benchmarks como AIME e MATH-500. Disponível em versões completas (671B parâmetros), versão complexa e maior, e destiladas (1.5B-70B), versão simplificada e reduzida de um modelo de aprendizado de máquina mais complexo e maior, o modelo pode ser executado localmente com ferramentas como **Ollama**, exigindo GPUs potentes ou hardware otimizado.

- **Arquitetura**: Baseado em Mixture-of-Experts (MoE), onde cada token ativa 37 bilhões de parâmetros, possibilitando raciocínio avançado.
- **Treinamento**: Utiliza RL para melhorar capacidades de raciocínio, com técnicas de destilação para criar modelos menores.
- **Implantação Local**: Modelos menores (1.5B-70B) podem ser executados em hardware mais modesto, enquanto versões completas exigem GPUs com alto poder de processamento.

💡 **Dica**: Modelos destilados são ideais para quem deseja experimentar o DeepSeek-R1 em máquinas locais sem depender de recursos avançados.

## Configuração Manual com Docker

Esta abordagem envolve criar e conectar os contêineres manualmente.

**Considere a pasta *Ollama***

### Passo 1: Iniciar o Ollama

O **Ollama** gerencia a execução do modelo. Use o seguinte comando para criar e iniciar o contêiner::

```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
- -d: Roda o contêiner em segundo plano.
- -v ollama:/root/.ollama: Cria um volume chamado ollama para armazenar os dados do modelo.
- -p 11434:11434: Mapeia a porta do contêiner para a mesma porta no host.
- --name ollama: Nomeia o contêiner como ollama.

### Passo 2: Baixar o Modelo DeepSeek-R1

Depois que o contêiner do **Ollama** estiver em execução, baixe o modelo **DeepSeek-R1** com:

```sh
docker exec -it ollama ollama pull deepseek-r1:1.5b
```

📚 Explorar Outros Modelos: Para ver mais opções, acesse a [biblioteca oficial de modelos do Ollama](https://ollama.com/library/deepseek-r1). Modelos maiores oferecem mais precisão, mas podem exigir mais recursos de GPU.

### Passo 3: Configurar a Interface Web

Agora, configure o **Open Web UI** para interagir com o modelo via navegador:

```console
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

- -p 3000:8080: Mapeia a porta 8080 do contêiner para a porta 3000 no host.
- --add-host=host.docker.internal:host-gateway: Permite que o contêiner acesse serviços rodando no host.
- -v open-webui:/app/backend/data: Cria um volume persistente para armazenar os dados da interface web.

### Passo 4: Acessar a Interface

Abra o navegador em http://localhost:3000 para interagir com o modelo **DeepSeek-R1**.

## Automação com Docker Compose

Embora a configuração manual funcione, usar **Docker Compose** automatiza a criação e conexão dos serviços, tornando tudo mais simples.

### Estrutura do Projeto

Organize os arquivos do projeto com a seguinte estrutura:

```
my-deepseek/
│
├── Dockerfile             # Configuração do Ollama
├── entrypoint.sh          # Script de inicialização
├── docker-compose.yml     # Configuração do Docker Compose
└── README.md              # Documentação
```

#### Passo 1: Criar o arquivo Dockerfile

No arquivo **Dockerfile**, adicione as instruções para criar o contêiner do **Ollama**:

```Dockerfile
FROM ollama/ollama:latest

# Copie o script para dentro do contêiner
COPY entrypoint.sh /entrypoint.sh

# Torne o script executável
RUN chmod +x /entrypoint.sh

# Configure o ENTRYPOINT para o script
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
```

#### Passo 2: Criar o arquivo entrypoint.sh

Crie um arquivo chamado **entrypoint.sh** na raiz do projeto que será o responsável por carregar o modelo do **Deepseek** que iremos usar:

```sh
#!/bin/sh

# Inicie o servidor Ollama em background
ollama serve --timeout 600 &

# Aguarde o servidor iniciar
sleep 5

# Faça o pull do modelo necessário (usando a variável MODEL_NAME)
ollama pull "${MODEL_NAME}"

# Mantenha o contêiner rodando
tail -f /dev/null
```

#### Passo 3: Criar o Arquivo docker-compose.yml

No arquivo **docker-compose.yml**, configure os serviços:

```yaml
version: '3.8'

networks:
  ai_network:
    driver: bridge

services:
  ollama:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ollama
    volumes:
      - ollama:/root/.ollama
    ports:
      - "11434:11434"
    networks:
      - ai_network
    environment:
      - MODEL_NAME=deepseek-r1:1.5b  # Defina o modelo aqui

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    depends_on:
      - ollama
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: always
    networks:
      - ai_network

volumes:
  ollama:
  open-webui:
```

#### Passo 4: Subir os Serviços

Com o Docker Compose configurado, inicie os serviços com:

```bash
docker-compose up --build -d
```

#### Passo 5: Acessar a Interface

Abra http://localhost:3000 no navegador para usar o DeepSeek-R1.

#### Passo 6: Encerrar os Serviços

Para desligar os contêineres, use:

```bash
docker-compose down
```

## Usando a API do Ollama com o DeepSeek-R1

Você pode usar a API do **Ollama** para interagir com o modelo **DeepSeek-R1** de forma programática. Aqui está um exemplo prático em **Python** para integrar o modelo em um aplicativo:

### Exemplo de Código em Python

#### Crie o Virtual Environment

No terminal, navegue até a pasta do seu projeto **src**:

```bash
python3 -m venv venv
```

#### Ative o Virtual Environment

Ative o ambiente virtual executando o comando abaixo:

```bash
source venv/bin/activate
```

#### Instale as Dependências a Partir do requirements.txt

Após criar o ambiente virtual e ativá-lo, use o seguinte comando para instalar todas as dependências listadas no requirements.txt:

```bash
pip install -r requirements.txt
```
Isso instalará exatamente as versões dos pacotes especificadas no arquivo.

#### Execute seu código

Com o ambiente virtual ativo, rode o script:

```bash
python3 example_prompt.py # Exemplo de prompt simples
python3 example_pdf.py example.pdf # Exemplo de análise de pdf passado como primeiro parametro
```

#### Desative o _Virtual Environment_

Quando terminar, você pode desativar o virtual environment com o comando:

```bash
deactivate
```

Isso retorna o terminal para o estado original.

## Conclusão

Com estas abordagens, você pode rodar o **DeepSeek-R1** localmente de forma eficiente e organizada. Usar variáveis no **Docker Compose** simplifica o carregamento de diferentes modelos no futuro. Agora é sua vez de explorar as capacidades do **DeepSeek-R1** diretamente no seu ambiente local! 🚀

Caso tenha dúvidas ou queira compartilhar sua experiência, deixe seu comentário. Boa sorte com seus projetos de IA! 😊
