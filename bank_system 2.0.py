import time

# FUNÇÕES DO CÓDIGO

def menu(saldo):
    return f"""
      =============== MENU ===============
     |      Selecione a opção Desejada    |
     |              Saldo: R${saldo:.2f}   
     |                                    |
     |    [d] - Depositar                 |
     |    [s] - Sacar                     |
     |    [e] - Extrato                   |
     |    [u] - Cadastrar Usuário         |
     |    [c] - Cadastrar Conta           |
     |    [l] - Lista de Contas           |
     |    [q] - Sair                      |
     |====================================|
    => """

def pressione_tecla():
    input("Pressione ENTER para continuar...") # Botão de avanço = enter

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
        time.sleep(1)
    else:
        print("Valor inválido para depósito.")
        time.sleep(1)
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    if valor > saldo:
        print("Saldo insuficiente")
        time.sleep(1)
    elif valor > limite:
        print(f"Valor excedeu o limite de saque. Limite: R$ {limite}")
        time.sleep(1)
    elif numero_saques >= LIMITE_SAQUES:
        print(f"Número máximo de saques atingido {numero_saques}/{LIMITE_SAQUES}.")
        time.sleep(1)
    else:
        saldo -= valor
        extrato += f"Saque: \t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
        time.sleep(1)
    # Sempre retornar saldo e extrato
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato):
    print("\n |============= EXTRATO =============|")
    print("Não há movimentações para serem vistas." if not extrato else extrato)
    print(f"           \t|Saldo: R${saldo:.2f}|")
    print(" |===================================|")
    pressione_tecla()

def cadastrar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    usuario = pesquisa_usuario(cpf, usuarios)

    if usuario:
        print("\n CPF já está vinculado a um usuário!")
        return None  # Adiciona o retorno aqui para evitar cadastrar o usuário novamente
    nome = input("Nome: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = {
        "estado": input("Estado: "),
        "cidade": input("Cidade: "),
        "bairro": input("Bairro: "),
        "rua": input("Rua: "),
        "numero": input("Número: ")
    }
    usuarios.append({"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco})
    print("\n Usuário Cadastrado com sucesso!")
    time.sleep(1)
    return nome  # Retorna o nome do usuário

def pesquisa_usuario(cpf, usuarios):
    usuarios_pesquisados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_pesquisados[0] if usuarios_pesquisados else None

def cadastrar_conta(agencia, numero_conta, usuarios):
    cpf = input("CPF do usuário: ")
    usuario = pesquisa_usuario(cpf, usuarios)

    if usuario:
        print("\n Sua conta foi criada com sucesso! ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n Usuário não foi encontrado. Conta não foi criada!")
    return None

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)
        print("=" * 100)

# Solicitar o nome de exibição temporário
usuario_temp = input("Como gostaria de ser chamado por agora?: ")

print(f"Olá, Bem vindo ao nosso Sistema {usuario_temp}!")
time.sleep(1)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []   # Nome do usuário e contas
    contas = []
    numero_saques = 0
    saldo = 0.0     # Váriaveis dos dados do Usuário
    limite = 500.0
    extrato = ""

    # Menu Inicial/Loop
    while True:
        opcao = input(menu(saldo))

        # DEPÓSITO
        if opcao == "d":
            valor = float(input("Informe o valor do Depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        
        # SAQUE
        elif opcao == "s":
            valor_saque = float(input("Informe o valor de Saque: "))
            if valor_saque > 0: # Verificando saque válido
                saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor_saque, extrato=extrato, limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)
            else:
                print("Valor não é válido para saque.")

        # EXTRATO
        elif opcao == "e":
            mostrar_extrato(saldo, extrato=extrato)

        # CADASTRAR USUÁRIO
        elif opcao == "u":
            usuario_temp = cadastrar_usuario(usuarios)
    
        # CADASTRAR CONTA
        elif opcao == "c":
            numero_conta = len(contas) + 1
            conta = cadastrar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        # LISTAR CONTAS
        elif opcao == "l":
            listar_contas(contas)

        # SAIR
        elif opcao == "q":
            print("Obrigado por utilizar nossos canais. Até a próxima!")
            break

        # OPÇÃO INVÁLIDA
        else:
            print("\n Operação inválida. \n Digite uma das Operações. -d -s -e -q")
            time.sleep(3)

main()
