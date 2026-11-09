from dataclasses import dataclass

from .tarefa import Tarefa


@dataclass(frozen=True, init=False)
class Memento:
    # Tuplas de strings preservam o estado sem guardar tarefas mutaveis.
    __estado: tuple

    def __init__(self, tarefas):
        object.__setattr__(self, "_Memento__estado", tuple(
            (tarefa.getTitulo(), tarefa.getDescricao()) for tarefa in tarefas
        ))

    def recuperar_tarefas(self):
        return [Tarefa(titulo, descricao) for titulo, descricao in self.__estado]
