# How to Set Up and Run DeepSeek-R1 Locally Using Docker and Docker Compose

**DeepSeek-R1** is an advanced AI model designed to handle complex tasks such as logical reasoning, programming, and mathematics. Running it locally offers greater control over data, allows for tailored customization for specific projects, and saves costs associated with external servers. In this tutorial, you'll learn two setup methods: manually with **Docker** and automated with **Docker Compose**.

## Why Run DeepSeek-R1 Locally?

- **Privacy**: Your data stays within your local environment.
- **Cost Savings**: Reduce cloud server expenses.
- **Customization**: Easily adapt the environment to suit your specific needs.

## DeepSeek-R1 Architecture and Deployment

**DeepSeek-R1** is a cutting-edge AI model designed for tackling complex tasks, including logical reasoning and mathematical problem-solving. It combines **reinforcement learning (RL)** and **supervised fine-tuning** to achieve superior performance on benchmarks like AIME and MATH-500. Available in full versions (671B parameters) and distilled variants (1.5B-70B parameters), the model can run locally using tools like **Ollama**, requiring powerful GPUs or optimized hardware.

- **Architecture**: Based on Mixture-of-Experts (MoE), where each token activates 37 billion parameters, enabling advanced reasoning.
- **Training**: Uses RL to enhance reasoning capabilities, with distillation techniques to create smaller models.
- **Local Deployment**: Smaller models (1.5B-70B) run on modest hardware, while full versions require high-performance GPUs.

💡 **Tip**: Distilled models are perfect for experimenting with **DeepSeek-R1** on local machines that lack advanced hardware.

## Manual Setup with Docker

This approach involves manually creating and connecting containers.

**Consider *Ollama* folder**

### Step 1: Set up Ollama

**Ollama** manages the model execution. Use this command to create and start the container:

```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
- -d: Runs the container as a background process.
- -v ollama:/root/.ollama: Creates a volume named ollama to store model data.
- -p 11434:11434: Maps the container port to the same port on the host.
- --name ollama: Names the container ollama.

### Step 2: Download the DeepSeek-R1 Model

Once the **Ollama** container is running, download the **DeepSeek-R1** model:

```sh
docker exec -it ollama ollama pull deepseek-r1:1.5b
```

📚 Explore Other Models: Visit the [Ollama Model Library](https://ollama.com/library/deepseek-r1) for more options. Larger models offer higher accuracy but require more GPU resources.


### Step 3: Configure the Web Interface

Set up **Open Web UI** to interact with the model via your browser:

```sh
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
-p 3000:8080: Maps port 8080 of the container to port 3000 on the host.
--add-host=host.docker.internal:host-gateway: Allows the container to access host services.
-v open-webui:/app/backend/data: Creates a persistent volume for the web interface data.
```

### Step 4: Access the Interface

Open your browser at http://localhost:3000 to interact with **DeepSeek-R1**.

## Automation with Docker Compose

While manual setup works, **Docker Compose** automates service creation and connections for simplicity.

### Project Structure

Organize your project with this structure:

```plaintext
my-deepseek/
│
├── Dockerfile             # Ollama configuration
├── entrypoint.sh          # Initialization script
├── docker-compose.yml     # Docker Compose setup
└── README.md              # Documentation
```

#### Step 1: Write the Dockerfile

In the **Dockerfile**, add instructions to build the **Ollama** container:

```Dockerfile
FROM ollama/ollama:latest

# Copy the script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Set the ENTRYPOINT to the script
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
```

#### Step 2: Create entrypoint.sh

Write **_entrypoint.sh_** in the project root directory to handle **DeepSeek** model initialization:

```sh
#!/bin/sh

# Start the Ollama server in the background
ollama serve --timeout 600 &

# Wait for the server to start
sleep 5

# Pull the required model (using MODEL_NAME variable)
ollama pull "${MODEL_NAME}"

# Keep the container running
tail -f /dev/null
```

#### Step 3: Create docker-compose.yml

Configure services in **_docker-compose.yml_**:

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
      - MODEL_NAME=deepseek-r1:1.5b  # Define the model here

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

#### Step 4: Start Services

With **Docker Compose** configured, start the services:

```bash
docker-compose up --build -d
```

#### Step 5: Access the Interface

Open http://localhost:3000 in your browser to use **DeepSeek-R1**.

#### Step 6: Stop Services

To shut down the containers, use:

```bash
docker-compose down
```

## Using the Ollama API with DeepSeek-R1

Use the **Ollama API** to interact with **DeepSeek-R1** programmatically. Here’s a practical example of integrating the **Ollama API** with Python.

### Python Code Example

#### Create the Virtual Environment

Navigate to your project's **src** folder:

```bash
python3 -m venv venv
```

#### Activate the Virtual Environment

Activate it with:

```bash
source venv/bin/activate
```

#### Install Dependencies from requirements.txt

Install the dependencies:

```bash
pip install -r requirements.txt
```

#### Run Your Code

Execute the script:

```bash
python3 example_prompt.py       # Simple prompt example
python3 example_pdf.py example.pdf  # PDF analysis example (pass PDF as first parameter)
```

#### Deactivate the Virtual Environment

When finished, deactivate it:

```bash
deactivate
```

## Conclusion

By following these methods, you can efficiently and seamlessly run **DeepSeek-R1** on your local machine. Leveraging variables in **Docker Compose** streamlines the process of loading different models in the future. Now it's your turn to explore **DeepSeek-R1**'s capabilities directly in your local environment! 🚀

If you have questions or want to share your experience, leave a comment. Good luck with your AI projects! 😊
