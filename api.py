import requests
from fastapi import FastAPI, Request
import funcoes

app = FastAPI(title="API Gerenciador de Gastos")

# Credenciais da Z-API
ZAPI_INSTANCE = "3F8966DFFB28E10E7A06CAAF6523F126"
ZAPI_TOKEN = "C952EBA8336CD44248E62818"
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"

def enviar_whatsapp(destinatario: str, mensagem: str):
    headers = {"Content-Type": "application/json"}
    payload = {
        "phone": destinatario,
        "message": mensagem
    }
    requests.post(ZAPI_URL, json=payload, headers=headers)

@app.get("/")
def status():
    return {"status": "Online"}

@app.post("/webhook-zapi")
async def webhook_zapi(request: Request):
    dados = await request.json()

    # Processa apenas se tiver texto e não for notificação de leitura/status
    if not dados.get("isStatusReply") and dados.get("text"):
        is_group = dados.get("isGroup", False)
        
        # Só executa se a mensagem vier de um grupo
        if is_group:
            # O campo 'phone' no webhook de grupo da Z-API contém o ID do grupo (ex: 120363xxx@g.us)
            chat_id = dados.get("phone")
            texto = dados.get("text", {}).get("message", "").strip()

            # Trava anti-loop: ignora as mensagens geradas pelo próprio bot no grupo
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
                return {"status": "ignorado_propria_resposta"}

            texto_lower = texto.lower()

            if texto_lower in ["oi", "ola", "olá", "ajuda", "menu", "start"]:
                resposta = (
                    "📊 *PAINEL FINANCEIRO PESSOAL* 📊\n"
                    "────────────────────────\n"
                    "Olá! Estou aqui para te ajudar a manter as contas em dia. Veja o que posso fazer:\n\n"
                    "💰 *total* \n"
                    "└─ Consulta o valor total de gastos acumulados.\n\n"
                    "📋 *listar* \n"
                    "└─ Exibe a lista detalhada com cada lançamento.\n\n"
                    "➕ *novo <descrição>, <valor>, <categoria>* \n"
                    "└─ Ex: `novo Uber, 24.90, Transporte`\n\n"
                    "🗑️ *remover <número>* \n"
                    "└─ Ex: `remover 3` (apaga o item da posição 3)\n"
                    "────────────────────────\n"
                    "💡 _Dica: Digite exatamente os comandos acima para gerenciar._"
                )

            elif texto_lower == "total":
                resultado = funcoes.somar_total()
                resposta = (
                    "💵 *BALANÇO GERAL* 💵\n"
                    "────────────────────────\n"
                    f"{resultado}\n"
                    "────────────────────────"
                )

            elif texto_lower in ["listar", "gastos"]:
                resultado = funcoes.listar_gastos()
                resposta = (
                    "📑 *EXTRATO DE LANÇAMENTOS* 📑\n"
                    "────────────────────────\n"
                    f"{resultado}\n"
                    "────────────────────────"
                )

            elif texto_lower.startswith("novo"):
                try:
                    partes = texto[4:].strip().split(",")
                    desc = partes[0].strip()
                    val = float(partes[1].strip())
                    cat = partes[2].strip()
                    
                    resultado = funcoes.adicionar_gasto(desc, val, cat)
                    resposta = (
                        "✅ *LANÇAMENTO REGISTRADO!* ✨\n"
                        "────────────────────────\n"
                        f"📝 *Item:* {desc.capitalize()}\n"
                        f"💳 *Valor:* R$ {val:.2f}\n"
                        f"🏷️ *Categoria:* {cat.capitalize()}\n"
                        "────────────────────────\n"
                        "💾 _Dados salvos com sucesso na planilha!_"
                    )
                except Exception:
                    resposta = (
                        "⚠️ *OPS! FORMATO INCORRETO* ⚠️\n"
                        "────────────────────────\n"
                        "Para registrar um novo gasto, use as vírgulas:\n\n"
                        "👉 `novo Descrição, Valor, Categoria`\n\n"
                        "📌 *Exemplo prático:*\n"
                        "`novo Almoço executivo, 35.00, Alimentação`"
                    )

            elif texto_lower.startswith("remover"):
                try:
                    num = int(texto.split()[1])
                    resultado = funcoes.remover_gasto(num)
                    resposta = (
                        "🗑️ *ALTERAÇÃO NO EXTRATO* 🗑️\n"
                        "────────────────────────\n"
                        f"{resultado}\n"
                        "────────────────────────"
                    )
                except Exception:
                    resposta = (
                        "⚠️ *NÚMERO NÃO IDENTIFICADO* ⚠️\n"
                        "────────────────────────\n"
                        "Envie o comando acompanhado do índice numérico:\n\n"
                        "👉 `remover 1`\n"
                        "_(Consulte a lista com *listar* para ver os números)_"
                    )

            else:
                resposta = (
                    "🤖 *COMANDO NÃO RECONHECIDO* 🤔\n"
                    "────────────────────────\n"
                    "Não entendi o que você enviou.\n\n"
                    "Envie *menu* ou *ajuda* para ver a lista de comandos disponíveis."
                )

            enviar_whatsapp(chat_id, resposta)

    return {"status": "recebido"}