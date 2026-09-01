import funcoes

def exibir_menu():
    print("\n ===GERENCIADOR===")
    print("1. Adicionar Gasto.")
    print("2. Listar todo os gastos.")
    print("3. Ver total gasto")
    print("4. Ver total por categoria")
    print("5. Remover gasto")
    print("0. Sair")
    print("=============================\n")
    

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
    
        match opcao:
            case "1":
                print("\n=====Novo Gasto=====")
                descricao = input("O que você comprou? ").capitalize()
                valor = float(input("Qual o valor? R$ "))
                categoria = input("Qual a categoria? ").capitalize()
                
                funcoes.adicionar_gasto(descricao, valor, categoria)
            case "2":
                funcoes.listar_gastos()
            case "3":
                funcoes.somar_total()
            case "4":
                categoria = input("Qual categoria deseja procurar? ")
                funcoes.total_categoria(categoria)
            case "5":
                funcoes.remover_gasto()
            case "0":
                print("\nSaindo do programa.")
                break
            case _:
                print("\nOpção Inválida, pcr") #O "_" funciona como o default, ele captura qualquer coisa que não tenha caído nos casos anteriores, ou seja, qualquer outra coisa que o usuário digita.

main()