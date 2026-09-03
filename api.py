import requests
from fastapi import FastAPI, Request
import funcoes

app = FastAPI(title="API Gerenciador de Gastos")

# Credenciais da Z-API
ZAPI_INSTANCE = "3F8966DFFB28E10E7A06CAAF6523F126"
ZAPI_TOKEN = "C952EBA8336CD44248E62818"
ZAPI_CLIENT_TOKEN = "Feb26e90488eb414e906ef4dd367726f0S"  # Token gerado em Segurança > Token de segurança da conta

ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"

def enviar_whatsapp(destinatario: str, mensagem: str):
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
    }
    payload = {
        "phone": destinatario,
        "message": mensagem
    }
    resp = requests.post(ZAPI_URL, json=payload, headers=headers)
    print(f"--> Status envio Z-API: {resp.status_code} | Resposta: {resp.text}")

@app.get("/")
def status():
    return {"status": "Online"}

@app.post("/webhook-zapi")
async def webhook_zapi(request: Request):
    dados = await request.json()
    print(">>> DADOS CHEGANDO DA Z-API:", dados)

    # Ignora mensagens enviadas pelo próprio bot/API para não gerar loop infinito
    if dados.get("fromApi", False):
        print(">>> Mensagem ignorada (enviada pela própria API)")
        return {"status": "ignorado_propria_api"}

    # Processa se houver mensagem de texto e não for notificação de status/leitura
    if not dados.get("isStatusReply") and dados.get("text"):
        chat_id = dados.get("phone") or dados.get("chatId")
        texto = dados.get("text", {}).get("message", "").strip()

        # Evita responder mensagens com cabeçalhos emitidos pelo próprio bot
        marcadores_bot = [
            "*PAINEL FINANCEIRO*",
            "*BALANÇO GERAL*",
            "*EXTRATO*",
            "*LANÇAMENTO REGISTRADO*",
            "*ALTERAÇÃO NO EXTRATO*",
            "🤖 *COMANDO",
            "⚠️ *OPS!",
            "⚠️ *NÚMERO"
        ]
        if any(marcador in texto for marcador in marcadores_bot):
            print(">>> Mensagem ignorada (marcador do bot detectado)")
            return {"status": "ignorado_propria_resposta"}

        texto_lower = texto.lower()

        if texto_lower in ["oi", "ola", "olá", "ajuda", "menu", "start"]:
            resposta = (
                "📊 *PAINEL FINANCEIRO PESSOAL* 📊\n"
                "────────────────────────\n"
                "Olá! Estou pronto para ajudar:\n\n"
                "💰 *total* \n"
                "└─ Consulta o valor total de gastos acumulados.\n\n"
                "📋 *listar* \n"
                "└─ Exibe a lista detalhada com cada lançamento.\n\n"
                "➕ *novo <descrição>, <valor>, <categoria>* \n"
                "└─ Ex: `novo Uber, 24.90, Transporte`\n\n"
                "🗑️ *remover <número>* \n"
                "└─ Ex: `remover 3`\n"
                "────────────────────────"
            )
        elif texto_lower == "total":
            resposta = (
                "💵 *BALANÇO GERAL* 💵\n"
                "────────────────────────\n"
                f"{funcoes.somar_total()}\n"
                "────────────────────────"
            )
        elif texto_lower in ["listar", "gastos"]:
            resposta = (
                "📑 *EXTRATO DE LANÇAMENTOS* 📑\n"
                "────────────────────────\n"
                f"{funcoes.listar_gastos()}\n"
                "────────────────────────"
            )
        elif texto_lower.startswith("novo"):
            try:
                partes = texto[4:].strip().split(",")
                desc = partes[0].strip()
                val = float(partes[1].strip())
                cat = partes[2].strip()
                funcoes.adicionar_gasto(desc, val, cat)
                resposta = (
                    "✅ *LANÇAMENTO REGISTRADO!* ✨\n"
                    "────────────────────────\n"
                    f"📝 *Item:* {desc.capitalize()}\n"
                    f"💳 *Valor:* R$ {val:.2f}\n"
                    f"🏷️ *Categoria:* {cat.capitalize()}\n"
                    "────────────────────────"
                )
            except Exception:
                resposta = "⚠️ *OPS! FORMATO INCORRETO* ⚠️\nUse: `novo Descrição, Valor, Categoria`"
        elif texto_lower.startswith("remover"):
            try:
                num = int(texto.split()[1])
                resposta = (
                    "🗑️ *ALTERAÇÃO NO EXTRATO* 🗑️\n"
                    "────────────────────────\n"
                    f"{funcoes.remover_gasto(num)}\n"
                    "────────────────────────"
                )
            except Exception:
                resposta = "⚠️ Use o formato: `remover 1`"
        else:
            resposta = "🤖 Digite *menu* para ver os comandos disponíveis."

        print(f">>> Disparando mensagem de volta para: {chat_id}")
        enviar_whatsapp(chat_id, resposta)

    return {"status": "recebido"}