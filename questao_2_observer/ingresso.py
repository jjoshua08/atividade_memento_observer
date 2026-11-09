from math import isfinite


class Ingresso:
    # Subject: conhece apenas o contrato atualizar dos observadores.
    def __init__(self, tipo, preco):
        self.__validar_preco(preco)
        self.__tipo = tipo
        self.__preco = preco
        self.__observadores = []
        self.__descontos = []

    @property
    def tipo(self):
        return self.__tipo

    @property
    def preco(self):
        return self.__preco

    @staticmethod
    def __validar_preco(preco):
        if not isfinite(preco) or preco < 0:
            raise ValueError("Preco deve ser finito e nao negativo.")

    def registrar_observador(self, observador):
        if observador not in self.__observadores:
            self.__observadores.append(observador)

    def __notificar(self, alteracao):
        for observador in tuple(self.__observadores):
            observador.atualizar(f"{self.tipo}: {alteracao}")

    def atualizar_preco(self, preco):
        self.__validar_preco(preco)
        if preco == self.preco:
            return
        anterior = self.preco
        self.__preco = preco
        self.__notificar(f"preco alterado de R$ {anterior:.2f} para R$ {preco:.2f}")

    def adicionar_desconto(self, desconto):
        if desconto not in self.__descontos:
            self.__descontos.append(desconto)
            self.__notificar(f"novo desconto — {desconto}")

    def calcular_total(self, quantidade=1, estudante=False):
        if type(quantidade) is not int or quantidade < 1:
            raise ValueError("Quantidade deve ser um inteiro positivo.")
        # Regra do exemplo: descontos nao cumulativos, usando o maior elegivel.
        percentual = max((desconto.percentual for desconto in self.__descontos
                          if desconto.aplicavel(estudante, quantidade)), default=0)
        return round(self.preco * quantidade * (1 - percentual / 100), 2)


class CadeiraPremium(Ingresso):
    def __init__(self, preco):
        super().__init__("Cadeira premium", preco)


class Arquibancada(Ingresso):
    def __init__(self, preco):
        super().__init__("Arquibancada", preco)


class Camarote(Ingresso):
    def __init__(self, preco):
        super().__init__("Camarote", preco)
