from abc import ABC, abstractmethod


class Observador(ABC):
    @abstractmethod
    def atualizar(self, mensagem):
        pass


class Cliente(Observador):
    def __init__(self, nome):
        self.nome = nome
        self.notificacoes = []

    def atualizar(self, mensagem):
        self.notificacoes.append(mensagem)
        print(f"Cliente {self.nome}: {mensagem}")


class Administrador(Observador):
    def __init__(self, nome):
        self.nome = nome
        self.notificacoes = []

    def atualizar(self, mensagem):
        self.notificacoes.append(mensagem)
        print(f"Administrador {self.nome}: {mensagem}")
