import funcoes

def exibir_menu():
    print("\n ===GERENCIADOR===")
    print("1. Adicionar Gasto.")
    print("2. Listar todo os gastos.")
    print("3. Vert total gasto")
    print("0. Sair")
    print("=============================\n")
    

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
    
        match opcao:
            case "1":
                print("\n-Novo Gasto-")
                descricao = input("O que você comprou?")
                valor = float(input("Qual o valor? R$ "))
                categoria = input("Qual a categoria? ")
                
                funcoes.adicionar_gasto(descricao, valor, categoria)
            case "2":
                funcoes.listar_gastos()
            case "3":
                print("\n-Aqui é onde vai somar tudo e mostrar o gasto total")
            case "0":
                print("\nSaindo do programa.")
                break
            case _:
                print("\nOpção Inválida, pcr") #O "_" funciona como o default, ele captura qualquer coisa que não tenha caído nos casos anteriores, ou seja, qualquer outra coisa que o usuário digita.

main()
                
    
   
    