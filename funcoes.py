import os
import json

ARQUIVO = "gastos.json"

def carregar_gastos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_gastos(gastos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=4, ensure_ascii=False)

# MUDANÇA 1: Troca de print por return
def adicionar_gasto(descricao, valor, categoria):
    gastos = carregar_gastos()
    novo_gasto = {
        "descricao": descricao.capitalize(),
        "valor": float(valor),
        "categoria": categoria.capitalize()
    }
    gastos.append(novo_gasto)
    salvar_gastos(gastos)
    return f"✅ Gasto '{novo_gasto['descricao']}' de R$ {novo_gasto['valor']:.2f} adicionado com sucesso!"

# MUDANÇA 2: Concatenação das linhas para retornar um texto único
def listar_gastos():
    gastos = carregar_gastos()
    if not gastos:
        return "Nenhum gasto registrado até agora."
    
    linhas = ["📋 *LISTA DE GASTOS:*"]
    for i, gasto in enumerate(gastos, 1):
        linhas.append(f"{i}. {gasto['descricao']} | R$ {gasto['valor']:.2f} | {gasto['categoria']}")
    
    return "\n".join(linhas)

# MUDANÇA 3: Tratamento de lista vazia direto no return
def somar_total():
    gastos = carregar_gastos()
    if not gastos:
        return "Nenhum gasto registrado até agora."
    
    total = sum(gasto['valor'] for gasto in gastos)
    return f"💰 *Total acumulado:* R$ {total:.2f}"

# MUDANÇA 4: Filtro acumulando texto em vez de múltiplos prints
def total_categoria(categoria_busca):
    gastos = carregar_gastos()
    if not gastos:
        return "Nenhum gasto registrado até agora."
    
    filtrados = [g for g in gastos if g['categoria'].strip().lower() == categoria_busca.strip().lower()]
    
    if not filtrados:
        return f"A categoria '{categoria_busca.upper()}' não possui gastos registrados."
    
    linhas = [f"📂 *Gastos na categoria {categoria_busca.upper()}:*"]
    total = 0
    for gasto in filtrados:
        linhas.append(f"- {gasto['descricao']} | R$ {gasto['valor']:.2f}")
        total += gasto['valor']
        
    linhas.append("-----------------------------")
    linhas.append(f"Subtotal: R$ {total:.2f}")
    return "\n".join(linhas)

# MUDANÇA 5: Recebe o número/índice por parâmetro direto da mensagem
def remover_gasto(indice_ou_numero):
    gastos = carregar_gastos()
    if not gastos:
        return "Nenhum gasto registrado para remover."
    
    try:
        index = int(indice_ou_numero) - 1
        if 0 <= index < len(gastos):
            gasto_removido = gastos.pop(index)
            salvar_gastos(gastos)
            return f"🗑️ Gasto '{gasto_removido['descricao']}' removido com sucesso!"
        return "❌ Número fora da lista. Envie um número válido."
    except (ValueError, TypeError):
        return "❌ Formato inválido. Envie apenas o número do gasto."

# MUDANÇA 6: Recebe os novos campos prontos da requisição
def editar_gasto(indice_ou_numero, nova_desc=None, novo_valor=None, nova_cate=None):
    gastos = carregar_gastos()
    if not gastos:
        return "Nenhum gasto registrado para editar."
        
    try:
        index = int(indice_ou_numero) - 1
        if not (0 <= index < len(gastos)):
            return "❌ Número fora da lista."
            
        gasto = gastos[index]
        if nova_desc:
            gasto['descricao'] = nova_desc.capitalize()
        if novo_valor is not None:
            gasto['valor'] = float(novo_valor)
        if nova_cate:
            gasto['categoria'] = nova_cate.capitalize()
            
        salvar_gastos(gastos)
        return f"✏️ Gasto #{indice_ou_numero} atualizado com sucesso!"
    except (ValueError, TypeError):
        return "❌ Valor numérico inválido informado para edição."

def gerar_relatorio():
    gastos = carregar_gastos()
    if not gastos:
        return "Nenhum gasto registrado até agora."
    
    nome_arquivo = "relatorio_gastos.txt"
    total = sum(gasto['valor'] for gasto in gastos)
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("=" * 30 + "\n")
        f.write("      Relatório de Gastos\n")
        f.write("=" * 30 + "\n")
        for i, gasto in enumerate(gastos, 1):
            f.write(f"{i}. {gasto['descricao']} / R${gasto['valor']:.2f} / Categoria: {gasto['categoria']}\n")
        f.write("=" * 30 + "\n")
        f.write(f"Total Geral: {total:.2f}\n")
        f.write("=" * 30 + "\n")
    
    return f"📄 Relatório gerado com sucesso no servidor como '{nome_arquivo}'!"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')