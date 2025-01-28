import requests
import json
import os
import argparse
from PyPDF2 import PdfReader

_model_name ="deepseek-r1:1.5b"

# Função para extrair texto do PDF e dividir em blocos
def extract_text_blocks_from_pdf(pdf_path, max_length=3000):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # Divida o texto em blocos de tamanho máximo definido
    blocks = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind(" ")  # Tente dividir no último espaço para evitar cortes bruscos
        if split_index == -1:  # Caso não encontre um espaço, divida pelo limite máximo
            split_index = max_length
        blocks.append(text[:split_index].strip())
        text = text[split_index:].strip()
    
    # Adicione o restante do texto
    if text:
        blocks.append(text.strip())
    
    return blocks

# Função para enviar uma solicitação ao Ollama
def generate_response(prompt):
    api_url = "http://localhost:11434/api/generate"
    model_name = _model_name  # Modelo a ser utilizado

    payload = {
        "model": model_name,
        "prompt": prompt
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=60*10)
        response.raise_for_status()  # Verifica se a resposta é bem-sucedida

        output = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                output += data.get("response", "")
                if data.get("done", False):
                    break
        return output.strip() if output else "Nenhuma resposta gerada pelo modelo."

    except requests.exceptions.RequestException as e:
        return f"Error communicating with API: {e}"

# Função para processar blocos de texto do PDF com o modelo
def process_pdf_with_ollama(pdf_path):
    # Extraia o texto do PDF em blocos
    text_blocks = extract_text_blocks_from_pdf(pdf_path)

    # Resuma ou analise cada bloco separadamente
    consolidated_response = ""
    for i, block in enumerate(text_blocks):
        print(f"Processing block {i + 1} of {len(text_blocks)}...")
        prompt = f"Based on the following text:\n\n{block}\n\nSummarize content or answer related questions."
        response = generate_response(prompt)
        consolidated_response += f"\n--- Block {i + 1} ---\n{response}"

    return consolidated_response.strip()

if __name__ == "__main__":
    # Configuração do argparse para aceitar o nome do arquivo PDF como parâmetro
    parser = argparse.ArgumentParser(description="Process a PDF with the Ollama template with Deepseek-R1 model.")
    parser.add_argument("pdf_path", help="Path to the PDF file to be processed.")
    args = parser.parse_args()

    # Verifica se o arquivo PDF existe
    if not os.path.isfile(args.pdf_path):
        print(f"Error: The PDF file '{args.pdf_path}' not found. Check the path.")
    else:
        try:
            response = process_pdf_with_ollama(args.pdf_path)
            print("\nConsolidated model response:")
            print(response)
        except Exception as e:
            print(f"Error processing PDF: {e}")
