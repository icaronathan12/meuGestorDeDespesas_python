import json
import os

ARQUIVO  = "gastos.json"

def carregar_gastos():
    #Se o arquivo não existir, retorna uma lista vazia
    if not os.path.exists(ARQUIVO):
        return []
    
    #Se existir, abre e lê os dados
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_gastos(gastos):
    #Salva a lista formatada no arquivo JSON
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=4, ensure_ascii=False)
    
def adicionar_gasto(descricao, valor, categoria):
    gastos = carregar_gastos()
    
    novo_gasto = {
        "descricao": descricao,
        "valor": valor,
        "categoria": categoria
    }

    gastos.append(novo_gasto)
    salvar_gastos(gastos)
    print(f"\n Gasto '{descricao}' de R${valor} adicionado com sucesso!")

def listar_gastos():
    gastos = carregar_gastos()
    
    if not gastos:
        print("\nNenhum gasto registrado até agora.")
        return
    
    print("\n===== LISTA DE GASTOS =====")
    for i, gasto in enumerate(gastos, 1):
        print(f"{i}. {gasto['descricao']} / R${gasto['valor']:.2f} / {gasto['categoria']}")
        print("==============================")
    
def somar_total():
    gastos = carregar_gastos()
    
    if not gastos:
        print("\nNenhum gasto registrado até agora.")
        return

    total = 0
    
    for gasto in gastos:
        total += gasto['valor']
    
    print(f"\nTotal de gastos acumulados: R$ {total:.2f} ")
    
def total_categoria(categoria_busca):
    gastos = carregar_gastos()
    
    if not gastos:
        print("\nNenhum gasto registrado até agora.")
        return
    
    encontrados = False
    valor_categoria = 0
    
    print("\n===== Gastos por Categoria =====")
    for gasto in gastos:
        if gasto['categoria'].strip().lower() == categoria_busca.strip().lower():
            print(f"{gasto['descricao']} / R$ {gasto['valor']:.2f}")
            valor_categoria += gasto['valor']
            encontrados = True
        
    if not encontrados:
        print(f"A categoria {categoria_busca.upper()} ainda não apresenta nenhum gasto!")
    else:
        print("========================================")
        print(f"Subtotal da categoria {categoria_busca.upper()}: R$ {valor_categoria:.2f}")