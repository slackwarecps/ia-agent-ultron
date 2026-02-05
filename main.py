import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
raw_key = os.getenv("GOOGLE_API_KEY")
if raw_key:
    print(f">>> [SRE CHECK] Chave carregada: {raw_key[:5]}...{raw_key[-4:]}")
else:
    print(">>> [SRE CHECK] NENHUMA CHAVE ENCONTRADA NO ENV!")

# Setup Ultron (Gemini 1.5 Flash)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    # No seu main.py, altere para um dos nomes que apareceram na sua lista:
    model = genai.GenerativeModel('gemini-2.5-flash')

    # OU, se quiser a inteligência máxima (mas com um pouco mais de latência):
    # model = genai.GenerativeModel('gemini-3-pro-preview')
except Exception as e:
    print(f">>> [SRE ERROR] Falha ao carregar modelo: {e}")

app = Flask(__name__)

def pensar_e_responder(texto):
    contexto = "Responda de forma técnica, direta e sucinta (máximo 140 caracteres)."
    prompt = f"{contexto}\nComando recebido: {texto}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao processar no Gemini: {str(e)}"

@app.route('/webhook', methods=['POST'])
def handle_command():
    print("\n" + "="*50)
    print(">>> [SRE LOG] Requisição recebida no Webhook!")
    
    data = request.get_json(force=True, silent=True)
    
    if not data or 'comando' not in data:
        print(">>> [ERRO] Payload inválido.")
        return jsonify({"erro": "Payload inválido."}), 400

    comando_texto = data.get('comando')
    print(f">>> [DEBUG] Processando comando: {comando_texto}")

    # Processamento
    resposta_ia = pensar_e_responder(comando_texto)
    
    # --- LOG DA RESPOSTA NO TERMINAL ---
    print("-" * 30)
    print("🤖 RESPOSTA DO ULTRON:")
    print(resposta_ia)
    print("-" * 30)
    print(">>> [SUCESSO] Fluxo finalizado.")
    print("="*50 + "\n")

    return jsonify({
        "status": "sucesso",
        "usuario": "Ultron",
        "resposta": resposta_ia
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)