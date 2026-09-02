from fastapi import FastAPI, Form, Response
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
import funcoes

app = FastAPI(title="API Gerenciador de Gastos")

#Modelos de dados para documentação e testes no Swagger
class NovoGasto(BaseModel):
    descricao: str
    valor: float
    categoria: str

class EdicaoGasto(BaseModel):
    descricao: str | None = None
    valor: float | None = None
    categoria: str | None = None

#ROTAS REST (Acessíveis pelo navegador / Swagger)

@app.get("/")
def status():
    return {"status": "Online", "mensagem": "API do Gerenciador de Gastos ativa"}

@app.get("/gastos")
def listar():
    return {"resposta": funcoes.listar_gastos()}

@app.get("/gastos/total")
def total():
    return {"resposta": funcoes.somar_total()}

@app.get("/gastos/categoria/{categoria}")
def por_categoria(categoria: str):
    return {"resposta": funcoes.total_categoria(categoria)}

@app.post("/gastos")
def adicionar(gasto: NovoGasto):
    msg = funcoes.adicionar_gasto(gasto.descricao, gasto.valor, gasto.categoria)
    return {"resposta": msg}

@app.delete("/gastos/{indice}")
def remover(indice: int):
    msg = funcoes.remover_gasto(indice)
    return {"resposta": msg}

@app.put("/gastos/{indice}")
def editar(indice: int, dados: EdicaoGasto):
    msg = funcoes.editar_gasto(indice, dados.descricao, dados.valor, dados.categoria)
    return {"resposta": msg}

#ROTA DO WEBHOOK (Usada pela Twilio / WhatsApp)

@app.post("/whatsapp")
async def webhook_whatsapp(Body: str = Form(...)):
    texto = Body.strip()
    texto_lower = texto.lower()
    
    #Roteamento básico de comandos via mensagem
    if texto_lower == "total":
        resposta_texto = funcoes.somar_total()
    elif texto_lower in ["listar", "gastos"]:
        resposta_texto = funcoes.listar_gastos()
    elif texto_lower.startswith("novo"):
        #Exemplo esperado: novo Almoço, 30.50, Alimentação
        try:
            partes = texto[4:].strip().split(",")
            desc = partes[0].strip()
            val = float(partes[1].strip())
            cat = partes[2].strip()
            resposta_texto = funcoes.adicionar_gasto(desc, val, cat)
        except Exception:
            resposta_texto = "❌ Formato inválido! Use: novo Descrição, Valor, Categoria"
    else:
        resposta_texto = (
            "🤖 *Comandos disponíveis:*\n"
            "• *total* -> Ver total gasto\n"
            "• *listar* -> Ver todos os gastos\n"
            "• *novo <desc>, <valor>, <cat>* -> Adicionar gasto"
        )

    #Formata a resposta no padrão XML que a Twilio lê e entrega no WhatsApp
    twiml = MessagingResponse()
    twiml.message(resposta_texto)
    
    return Response(content=str(twiml), media_type="application/xml")