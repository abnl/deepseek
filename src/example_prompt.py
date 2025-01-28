import requests
import json

_model_name ="deepseek-r1:1.5b"

def generate_response(prompt):
    # URL do servidor local do Ollama
    api_url = "http://localhost:11434/api/generate"
    model_name = _model_name  # Modelo a ser utilizado

    # Configuração da solicitação
    payload = {
        "model": model_name,
        "prompt": prompt
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Envia uma solicitação POST à API
        response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=60*10)
        response.raise_for_status()  # Verifica se a resposta é bem-sucedida

        # Processa a resposta linha por linha
        output = ""
        for line in response.iter_lines():
            if line:  # Ignora linhas vazias
                try:
                    data = json.loads(line.decode("utf-8"))  # Decodifica e processa a linha JSON
                    output += data.get("response", "")  # Concatena a resposta
                    if data.get("done", False):  # Verifica se o processamento terminou
                        break
                except json.JSONDecodeError as e:
                    print(f"Erro ao interpretar linha JSON: {e}")

        return output.strip() if output else "Nenhuma resposta gerada pelo modelo."

    except requests.exceptions.RequestException as e:
        return f"Erro ao se comunicar com a API: {e}"

# Exemplo de uso
prompt = "Explique o conceito de aprendizado por reforço em termos simples."
output = generate_response(prompt)
print("Resposta do modelo:", output)
