class Tarefa:
    def __init__(self, titulo: str, descricao: str):
        self.setTitulo(titulo)
        self.setDescricao(descricao)

    def getTitulo(self):
        return self.titulo

    def setTitulo(self, titulo):
        if not isinstance(titulo, str):
            raise TypeError("O titulo deve ser uma string.")
        self.titulo = titulo

    def getDescricao(self):
        return self.descricao

    def setDescricao(self, descricao):
        if not isinstance(descricao, str):
            raise TypeError("A descricao deve ser uma string.")
        self.descricao = descricao
