import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Setup Gemini 2.5 Flash
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

app = Flask(__name__)

# Configurações Rocket.Chat (Vindas do seu .env recuperado)
RC_URL = os.getenv("ROCKET_URL")
RC_HEADERS = {
    "X-Auth-Token": os.getenv("ROCKET_AUTH_TOKEN"),
    "X-User-Id": os.getenv("ROCKET_USER_ID"),
    "Content-Type": "application/json"
}

def notificar_rocketchat(comando):
    """Envia uma notificação simples para o canal #geral"""
    url = f"{RC_URL}/api/v1/chat.postMessage"
    payload = {
        "channel": "#general",
        "text": f"📢 **SRE Insight:** Fabão disparou o comando: `{comando}`"
    }
    try:
        requests.post(url, headers=RC_HEADERS, json=payload, timeout=5)
    except Exception as e:
        print(f">>> [RC ERROR] Falha ao notificar canal: {e}")

def pensar_e_responder(texto):
    contexto = "Responda de forma técnica, direta e sucinta (máximo 140 caracteres)."
    prompt = f"{contexto}\nComando recebido: {texto}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro Gemini: {str(e)}"

@app.route('/webhook', methods=['POST'])
def handle_command():
    data = request.get_json(force=True, silent=True)
    if not data or 'comando' not in data:
        return jsonify({"erro": "Payload inválido."}), 400

    comando_texto = data.get('comando')
    
    # --- Nova Funcionalidade: Notifica o canal antes de processar ---
    notificar_rocketchat(comando_texto)

    resposta_ia = pensar_e_responder(comando_texto)
    
    print(f"\n>>> [LOG] Comando: {comando_texto}")
    print(f">>> [LOG] Resposta: {resposta_ia}")

    return jsonify({
        "status": "sucesso",
        "resposta": resposta_ia
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)