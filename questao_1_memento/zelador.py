class Zelador:
    # O zelador armazena mementos sem inspecionar seu conteudo.
    def __init__(self):
        self.__historico = []

    def guardar(self, memento):
        self.__historico.append(memento)

    def retirar_ultimo(self):
        if not self.__historico:
            return None
        return self.__historico.pop()
