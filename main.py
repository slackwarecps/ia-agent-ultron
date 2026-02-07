import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google import genai # Import correto para a versão nova

load_dotenv()

# --- AJUSTE AQUI: Novo Setup do Gemini ---
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = 'gemini-2.0-flash' # Use o nome oficial disponível

app = Flask(__name__)

RC_URL = os.getenv("ROCKET_URL")
RC_HEADERS = {
    "X-Auth-Token": os.getenv("ROCKET_AUTH_TOKEN"),
    "X-User-Id": os.getenv("ROCKET_USER_ID"),
    "Content-Type": "application/json"
}

def notificar_rocketchat(comando):
    url = f"{RC_URL}/api/v1/chat.postMessage"
    payload = {
        "channel": "general", # Confirme se o nome é 'general' ou 'geral'
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
        # --- AJUSTE AQUI: Nova forma de gerar conteúdo ---
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro Gemini: {str(e)}"
    
@app.route('/webhook-receber', methods=['POST'])
def handle_rocket_message():
    # O Rocket.Chat pode enviar via Form ou JSON
    data = request.form if request.form else request.get_json()
    
    # Extrai os dados do Rocket.Chat
    user_name = data.get('user_name')
    msg_text = data.get('text', '')
    channel_name = data.get('channel_name')

    # REGRA DE OURO SRE: Evitar loop infinito
    # Se a mensagem veio do próprio bot ou do usuário do bot, ignora.
    if user_name == "ultron.bot" or "[IA]" in msg_text:
        return jsonify({}), 200

    print(f"\n>>> [OUVINDO] Mensagem de @{user_name} em #{channel_name}: {msg_text}")

    # Envia para o Gemini (sua função de IA)
    resposta_ia = pensar_e_responder(msg_text)
    
    # O Rocket.Chat espera um JSON com a chave "text" para postar de volta
    return jsonify({
        "text": f"🤖 **[IA]** @{user_name}, {resposta_ia}"
    }), 200

@app.route('/webhook-envio2', methods=['POST'])
def handle_command_envio2():
    data = request.get_json(force=True, silent=True)
    if not data or 'comando' not in data:
        return jsonify({"erro": "Payload inválido."}), 400

    comando_texto = data.get('comando')
    notificar_rocketchat(comando_texto)
    resposta_ia = pensar_e_responder(comando_texto)
    
    return jsonify({
        "status": "sucesso",
        "resposta": resposta_ia
    }), 200
    
@app.route('/webhook', methods=['POST'])
def handle_command():
    data = request.get_json(force=True, silent=True)
    if not data or 'comando' not in data:
        return jsonify({"erro": "Payload inválido."}), 400

    comando_texto = data.get('comando')
    notificar_rocketchat(comando_texto)
    resposta_ia = pensar_e_responder(comando_texto)
    
    return jsonify({
        "status": "sucesso",
        "resposta": resposta_ia
    }), 200


if __name__ == "__main__":
    # No Docker, o debug=True é útil, mas em prod use um WSGI server como Gunicorn
    app.run(host='0.0.0.0', port=5005, debug=True)