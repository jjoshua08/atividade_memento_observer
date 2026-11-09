from .memento import Memento
from .tarefa import Tarefa
from .zelador import Zelador


class GerenciadorTarefas:
    # Originador: cria e restaura estados; delega o historico ao zelador.
    def __init__(self):
        self.__tarefas = []
        self.__zelador = Zelador()

    def criar_memento(self):
        return Memento(self.__tarefas)

    def restaurar(self, memento):
        self.__tarefas = memento.recuperar_tarefas()

    def listar_tarefas(self):
        return self.criar_memento().recuperar_tarefas()

    def adicionar(self, titulo, descricao):
        tarefa = Tarefa(titulo, descricao)
        self.__zelador.guardar(self.criar_memento())
        self.__tarefas.append(tarefa)

    def __validar_indice(self, indice):
        if type(indice) is not int or not 0 <= indice < len(self.__tarefas):
            raise IndexError("Indice de tarefa invalido.")

    def editar(self, indice, titulo, descricao):
        self.__validar_indice(indice)
        tarefa = Tarefa(titulo, descricao)
        atual = self.__tarefas[indice]
        if (atual.getTitulo(), atual.getDescricao()) == (titulo, descricao):
            return
        self.__zelador.guardar(self.criar_memento())
        self.__tarefas[indice] = tarefa

    def remover(self, indice):
        self.__validar_indice(indice)
        self.__zelador.guardar(self.criar_memento())
        self.__tarefas.pop(indice)

    def desfazer(self):
        memento = self.__zelador.retirar_ultimo()
        if memento is None:
            return False
        self.restaurar(memento)
        return True
