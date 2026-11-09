from .desconto import DescontoEstudante, DescontoQuantidade
from .ingresso import Arquibancada, CadeiraPremium, Camarote
from .observador import Administrador, Cliente


def principal():
    print("Valores ficticios. Descontos nao cumulativos: aplica-se o maior elegivel.")
    ingressos = [CadeiraPremium(200), Arquibancada(100), Camarote(300)]
    cliente = Cliente("Ana")
    administrador = Administrador("Bruno")
    for ingresso in ingressos:
        print(f"{ingresso.tipo}: R$ {ingresso.preco:.2f}")
        ingresso.registrar_observador(cliente)
        ingresso.registrar_observador(administrador)

    ingresso = ingressos[1]
    ingresso.atualizar_preco(120)
    ingresso.adicionar_desconto(DescontoEstudante(50))
    ingresso.adicionar_desconto(DescontoQuantidade(10, 3))
    print(f"1 arquibancada sem desconto: R$ {ingresso.calcular_total():.2f}")
    print(f"1 arquibancada para estudante: R$ {ingresso.calcular_total(estudante=True):.2f}")
    print(f"3 arquibancadas por quantidade: R$ {ingresso.calcular_total(3):.2f}")
    print(f"3 arquibancadas para estudante: R$ {ingresso.calcular_total(3, True):.2f}")


if __name__ == "__main__":
    principal()
