from abc import ABC, abstractmethod
from math import isfinite


class Desconto(ABC):
    def __init__(self, percentual):
        if not isfinite(percentual) or not 0 < percentual <= 100:
            raise ValueError("Percentual deve estar entre 0 (exclusivo) e 100.")
        self.percentual = percentual

    @abstractmethod
    def aplicavel(self, estudante, quantidade):
        pass


class DescontoEstudante(Desconto):
    def aplicavel(self, estudante, quantidade):
        return estudante

    def __str__(self):
        return f"estudante: {self.percentual}%"


class DescontoQuantidade(Desconto):
    def __init__(self, percentual, quantidade_minima):
        super().__init__(percentual)
        if type(quantidade_minima) is not int or quantidade_minima < 2:
            raise ValueError("Quantidade minima deve ser um inteiro maior que 1.")
        self.quantidade_minima = quantidade_minima

    def aplicavel(self, estudante, quantidade):
        return quantidade >= self.quantidade_minima

    def __str__(self):
        return f"quantidade: {self.percentual}% a partir de {self.quantidade_minima} ingressos"
