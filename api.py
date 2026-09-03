import requests
from fastapi import FastAPI, Request
import funcoes

app = FastAPI(title="API Gerenciador de Gastos")

TELEGRAM_TOKEN = "8542743670:AAHnviEyFGGH6N926aD-WL2g2DEu7D6fw0Q"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def enviar_mensagem_telegram(chat_id, texto):
    payload = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown"
    }
    requests.post(TELEGRAM_API_URL, json=payload)

@app.post("/telegram")
async def webhook_telegram(request: Request):
    dados = await request.json()
    
    # Valida se a requisição contém uma mensagem com texto
    if "message" in dados and "text" in dados["message"]:
        chat_id = dados["message"]["chat"]["id"]
        texto = dados["message"]["text"].strip()
        texto_lower = texto.lower()

        if texto_lower in ["/start", "oi", "ola", "ajuda"]:
            resposta = (
                "🤖 *Gerenciador de Gastos*\n\n"
                "• `total` -> Ver saldo total\n"
                "• `listar` -> Exibir todos os gastos\n"
                "• `novo Descrição, Valor, Categoria` -> Adicionar gasto\n"
                "• `remover N` -> Remover item pelo número"
            )
        elif texto_lower == "total":
            resposta = funcoes.somar_total()
        elif texto_lower in ["listar", "gastos"]:
            resposta = funcoes.listar_gastos()
        elif texto_lower.startswith("novo"):
            try:
                partes = texto[4:].strip().split(",")
                desc = partes[0].strip()
                val = float(partes[1].strip())
                cat = partes[2].strip()
                resposta = funcoes.adicionar_gasto(desc, val, cat)
            except Exception:
                resposta = "❌ Use o formato: `novo Lanche, 25.50, Alimentacao`"
        elif texto_lower.startswith("remover"):
            try:
                num = int(texto.split()[1])
                resposta = funcoes.remover_gasto(num)
            except Exception:
                resposta = "❌ Use o formato: `remover 2`"
        else:
            resposta = "Comando não reconhecido. Digite `ajuda` para ver as opções."

        enviar_mensagem_telegram(chat_id, resposta)

    return {"ok": True}