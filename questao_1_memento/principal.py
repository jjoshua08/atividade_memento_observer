from .gerenciador_tarefas import GerenciadorTarefas


def exibir(gerenciador, mensagem):
    print(f"\n{mensagem}")
    for indice, tarefa in enumerate(gerenciador.listar_tarefas()):
        print(f"{indice}: {tarefa.getTitulo()} — {tarefa.getDescricao()}")


def principal():
    gerenciador = GerenciadorTarefas()
    gerenciador.adicionar("Estudar", "Ler sobre Memento")
    gerenciador.adicionar("Praticar", "Implementar Observer")
    gerenciador.editar(0, "Estudar padroes", "Revisar Memento e Observer")
    gerenciador.remover(1)
    exibir(gerenciador, "Lista atual:")
    for acao in ("remocao", "edicao", "adicao"):
        gerenciador.desfazer()
        exibir(gerenciador, f"Apos desfazer {acao}:")


if __name__ == "__main__":
    principal()
