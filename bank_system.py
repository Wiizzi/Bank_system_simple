# Nome do usuário
usuario = input("Nome de usuário: ") 

# Primeiro acesso
import time
print(f"Olá, Bem vindo ao nosso Sistema bancário {usuario}!")
time.sleep(2)


# Váriaveis dos dados do Usuário
saldo = 0.0
limite = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


# Botão de avanço = qualquer um
def pressione_tecla():
      input("Pressione qualquer tecla para continuar...")

# Menu Inicial/Loop
while True:
        menu = f"""

      =============== MENU ===============
     |      Selecione a Opção Desejada    |
     |               Saldo: R${saldo}     
     |    [d] - Depositar                 |
     |    [s] - Sacar                     |
     |    [e] - Extrato                   |
     |    [q] - Sair                      |
     |                                    |
     |====================================|
    => """
      
        opcao = input(menu)

            # DEPÓSITO
        if opcao == "d":
                valor = float(input("Informe o valor do Depósito: "))

                if valor > 0:
                    saldo += valor
                    print("\n Valor depositado com sucesso!")
                    extrato += f"Depósito: R$ {valor:.2f}\n" # Adiciona o registro (consutltavél EXTRATO)
                    time.sleep(1)
                else:
                    print("\n Operação não permitida. \n Depósitos devem ser positivos.")
                    time.sleep(2)

            # SAQUE
        elif opcao == "s":
            valor = float(input("Informe o valor do Saque: "))

            excedeu_saldo = valor > saldo
            
            excedeu_limite = valor > limite
            
            excedeu_saques = numero_saques >= LIMITE_SAQUES 
                
            if excedeu_saldo:
                  print("\n Operação recusada. \n Saldo insuficiente.")
                  time.sleep(2)
            
            elif excedeu_limite:
                  print(f"\n Operação recusada. \n O valor de saque limite é R${limite}")
                  time.sleep(2)
            
            elif excedeu_saques:
                  print(f"\n Operação não permitida. \n O número máximo de saques foi atingido ({numero_saques}/{LIMITE_SAQUES})")
                  time.sleep(2)
            
            elif valor > 0:
                  saldo -= valor
                  print("\n Saque realizado com sucesso!")
                  extrato += f"Saque: R$ {valor:.2f}\n"  # Adiciona o registro (consutltavél EXTRATO)
                  numero_saques += 1
                  time.sleep(1)

            else:
                  print("\n Operação recusada. Valor inválido.")
                  time.sleep(2)
            
            # EXTRATO
        elif opcao == "e":
            print("\n |============= EXTRATO =============|")
            print("Não há movimentações para serem vistas." if not extrato else extrato)
            print(f"            |Saldo: R${saldo:.2f}|")
            print(" |===================================|")
            pressione_tecla()

            # SAIR
        elif opcao =="q":
              print("Obrigado por utilizar nossos canais. Até a próxima!")
              break
        
        else:
            print("\n Operação inválida. \n Digite uma das Operações. -d -s -e -q")
            time.sleep(3)