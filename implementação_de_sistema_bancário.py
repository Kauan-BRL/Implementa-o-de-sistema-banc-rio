from abc import ABC, abstractmethod
from datetime import datetime, date

class Transação(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transação):
    def __init__(self, valor:float):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso = conta.depositar(self._valor)
        if sucesso:
            conta.historico.adicionar_transação(self)

class Saque(Transação):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transação(self)

class Historico:
    def __init__(self):
        self._transações = []

    @property
    def transações(self):
        return self._transações
    
    def adicionar_transação(self, transação:Transação):
        self._transações.append(transação)

    def extrato(self):
        print(f'\n{20* '='} EXTRATO {20* '='}\n')
        if not self._transações:
            print('Sem movimentações bancárias')
        else:
            for transação in self._transações:
                tipo = transação.__class__.__name__
                data_formatada = transação.data.strftime('%d/%m/%Y %H:%M:%S')
                print(f'{data_formatada}\t{tipo} : R${transação.valor:.2f}\n')
        print(f'{49*'='}')

class Conta:
    def __init__(self, numero:int, agencia:str, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero:int):
        return cls(cliente, numero)
    
    def sacar(self, valor:float):
        if valor > self._saldo:
            print('\nSaque falhou!\n')
            return False
        elif valor > 0:
            self._saldo -= valor
            print('\nSaque concluído!\n')
            return True
    
    def depositar(self, valor:float):
        if valor > 0:
            self._saldo += valor
            print('\nDepósito concluído!\n')
            return True
        else:
            print('\nDepósito falhou!\n')
            return False


class ContaCorrente(Conta):
    def __init__(self, numero:int, agencia:str, cliente, limite:float, limite_saques:int):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor:float):
        q_saques = len([t for t in self._historico.transações if isinstance(t, Saque)])
        if valor > self._limite:
            print('\nSaque falhou, limite excedido!')
        elif q_saques >= self._limite_saques:
            print('\nSaque falhou, limite de saques excedido!')
        else:
            return super().sacar(valor)
        
        return False

class Cliente:
    def __init__(self, endereço:str):
        self._endereço = endereço
        self._contas = []

    def realizar_transação(self, conta:Conta, transação:Transação):
        transação.registrar(conta)

    def adicionar_conta(self, conta:Conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf:str, nome:str, data_nascimento:date, endereço = str):
        super().__init__(endereço)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

#Exemplo

cliente = PessoaFisica(nome = 'Jonas', cpf = '11345235674', data_nascimento = date(2007,11,27), endereço = 'Rua A n°1437, Brooklyn')

conta = ContaCorrente(cliente = cliente, numero = 1, agencia = '3658', limite = 30000, limite_saques = 30)
cliente.adicionar_conta(conta)

cliente.realizar_transação(conta = conta, transação = Deposito(50000.0))
print(conta.saldo)

cliente.realizar_transação(conta = conta, transação = Saque(1000.0))
print(conta.saldo)

conta.historico.extrato()
