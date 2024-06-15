from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    @abstractmethod
    def valor(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido")
        else:
            conta.depositar(self.valor)
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    LIMITE_VALOR_SAQUE = 500

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido")
        elif conta.saldo < self.valor:
            print("Saldo insuficiente")
        elif self.valor > self.LIMITE_VALOR_SAQUE:
            print(f"Valor do saque excede o limite, seu valor por saque é {self.LIMITE_VALOR_SAQUE}")
        else:
            if conta.sacar(self.valor):  # Verifica se o saque foi realizado com sucesso
                conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": type(transacao).__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido")
            return False
        
        elif self._saldo >= valor:
            self._saldo -= valor
            return True
        
        else:
            print("Saldo insuficiente")
            return False

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido")
            return False
        else:
            self._saldo += valor
            return True

    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
C/C:\t{self.numero}
Titular:\t{self.cliente.nome}
Saldo:\t\tR${self.saldo:.2f}
"""

class ContaCorrente(Conta):
    LIMITE_DIARIO_SAQUE = 1500

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0
        self._total_sacado_hoje = 0.0
        self._data_ultimo_saque = datetime.min.date()

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    @property
    def saques_realizados(self):
        return self._saques_realizados

    @property
    def total_sacado_hoje(self):
        return self._total_sacado_hoje

    @property
    def data_ultimo_saque(self):
        return self._data_ultimo_saque

    def sacar(self, valor):
        hoje = datetime.now().date()

        if hoje != self._data_ultimo_saque:
            self._total_sacado_hoje = 0.0
            self._data_ultimo_saque = hoje

        if self._saques_realizados >= self._limite_saques:
            print("Limite de saques atingido")
            return False
        elif valor > (self._saldo + self._limite):
            print("Saldo insuficiente, incluindo limite")
            return False
        elif (self._total_sacado_hoje + valor) > self.LIMITE_DIARIO_SAQUE:
            print(f"Limite diário de saque atingido, seu limite é {self.LIMITE_DIARIO_SAQUE}")
            return False
        else:
            self._total_sacado_hoje += valor
            self._saques_realizados += 1
            if not super().sacar(valor):
                return False
            
            print("Saque realizado")
            return True

    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
C/C:\t{self.numero}
Titular:\t{self.cliente.nome}
Saldo:\t\tR${self.saldo:.2f}
"""

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    def __str__(self):
        return f"""\
Nome:\t\t{self.nome}
CPF:\t\t{self.cpf}
Nascimento:\t{self.data_nascimento}
Endereço:\t{self.endereco}
"""

def menu():
    menu = """\n
      =============== MENU ===============
     |                                    |
     |             Bem vindo!             |                       
     |                                    |
     |      Selecione a opção Desejada    |
     |                                    |
     |    [d] - Depositar                 |
     |    [s] - Sacar                     |
     |    [e] - Extrato                   |
     |    [u] - Cadastrar Usuário         |
     |    [c] - Cadastrar Conta           |
     |    [l] - Lista de Contas           |
     |    [q] - Sair                      |
     |                                    |
     |====================================|
    => """
    return input(menu)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Cliente sem conta registrada")
        return None
    
    return cliente.contas[0]  # Sempre vai retornar a primeira conta

def depositar(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não localizado, verifique a escritura")
        return
    
    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    print("Depósito realizado")

def sacar(clientes):
    cpf = input("Seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Não conseguimos localizar o cliente")
        return
    
    valor = float(input("Valor do saque: \n"))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def show_extrato(clientes):
    cpf = input("Seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n\tCliente não localizado")
        return 
    
    conta = recuperar_conta(cliente)
    if not conta:
        print("Conta não registrada")
        return

    print("\n |============= EXTRATO =============|")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não há movimentações para serem vistas"
    else:
        for transacao in transacoes:
            if transacao["tipo"] == "Deposito":
                extrato += f"\n Depósito: +R${transacao['valor']:.2f}"
            elif transacao["tipo"] == "Saque":
                extrato += f"\n Saque: -R${transacao['valor']:.2f}"

    extrato += f"\n\n Saldo: R${conta.saldo:.2f}"
    print(f"{extrato}\n")
    print(" |===================================|\n")

def cad_usuario(clientes):
    cpf = input("Seu CPF [Somente números]: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já existente")
        return
    
    nome = input("Qual seu nome? ")
    data_nasc = input("Quando você nasceu? [dd/mm/aaaa] ")
    endereco = input("Onde fica sua residência? [Estado, cidade, bairro, numero] ")

    cliente = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nascimento=data_nasc)
    clientes.append(cliente)
    print("Usuário criado")

def criar_conta(clientes, numero_conta, contas):
    cpf = input("Seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não localizado")
        return 
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f"Sua conta foi criada:\nCliente\n{cliente}\nConta\n{conta}")

def listar_contas(contas):
    if not contas:
        print("Ainda não há registro de contas")
    
    else:
        for conta in contas:
            print(">" * 100)
            print(str(conta))        

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            show_extrato(clientes)

        elif opcao == "u":
            cad_usuario(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(clientes, numero_conta, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break
        else:
            print("Operação não encontrada")


if __name__ == "__main__":
    main()

