import os
import json

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
        
def remover_gasto():
    gastos = carregar_gastos()
    
    if not gastos:
        print("\nNenhum gasto registrado até agora.")
        return

    listar_gastos()
    
    try:
        escolha = int(input("\nDigite o número do gasto que deseja remover: "))
        index = escolha - 1

        if 0 <= index < len(gastos):
            gasto_removido = gastos.pop(index)
            salvar_gastos(gastos)
            print(f"\nGasto {gasto_removido['descricao'].upper()} removido com sucesso!")
        
        else:
            print("\nNúmero inválido. Tente novamente.")
    
    except ValueError:
        print("\nDigite um número válido!")

def editar_gasto():
    gastos = carregar_gastos()
    
    if not gastos:
        print("\nNenhum gasto registrado até agora.")
        return
    
    listar_gastos()
    
    try:
        escolha = int(input("\nDigite o número do gasto que deseja alterar: "))
        index = escolha - 1
        
        if 0 <= index < len(gastos):
            gasto_atual = gastos[index]
            
            print("\n=====Editando Gasto===== ")
            print(f"{gasto_atual['descricao']} / R$ {gasto_atual['valor']}")
            
            nova_desc = input("\nNova descriçao: ").capitalize()
            if nova_desc:
                gasto_atual['descricao'] = nova_desc
            
            try:
                novo_valor = float(input("\nNovo valor: R$ "))
                if novo_valor:
                    gasto_atual['valor'] = novo_valor
            except ValueError:
                print("Valor inválido! O valor antigo será mantido.")
            
            nova_cate = input("\nDigite a nova categoria: ").capitalize()
            if nova_cate:
                gasto_atual['categoria'] = nova_cate
                
            salvar_gastos(gastos)
            print("Gasto editado com sucesso!")
    
        else:
            print("Número inválido. Tente novamente.")
        
    except ValueError:
        print("Valor inválido. Digite um número!")
            
def gerar_relatorio():
    gastos = carregar_gastos()
    
    if not gastos:
        print("\nNenhum gasto registrado até agora.")
        return
    
    nome_arquivo = "relatorio_gastos.txt"
    total = sum(gasto['valor'] for gasto in gastos)
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("=" * 30 + "\n") #O f.write grava o texto diretamente dentro do arquivo, o print interage com o terminal. Genial
        f.write("      Relatório de Gastos\n")
        f.write("=" * 30 + "\n")
        
        for i, gasto in enumerate(gastos, 1):
            f.write(f"{i}. {gasto['descricao']} / R${gasto['valor']:.2f} / Categoria: {gasto['categoria']}\n")
            
        f.write("=" * 30 + "\n")
        f.write(f"Total Geral: {total:.2f}\n")
        f.write("=" * 30 + "\n")
    
    print(f"Relatório exportado para '{nome_arquivo}'")
    
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
