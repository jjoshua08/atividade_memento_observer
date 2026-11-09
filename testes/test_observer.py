import unittest
from contextlib import redirect_stdout
from io import StringIO

from questao_2_observer.desconto import DescontoEstudante, DescontoQuantidade
from questao_2_observer.ingresso import Arquibancada, CadeiraPremium, Camarote
from questao_2_observer.observador import Administrador, Cliente, Observador


class TesteObserver(unittest.TestCase):
    def setUp(self):
        saida = redirect_stdout(StringIO())
        saida.__enter__()
        self.addCleanup(saida.__exit__, None, None, None)
        self.ingresso = Arquibancada(100)
        self.cliente = Cliente("Ana")
        self.administrador = Administrador("Bruno")
        self.ingresso.registrar_observador(self.cliente)
        self.ingresso.registrar_observador(self.administrador)

    def test_tres_tipos(self):
        ingressos = [CadeiraPremium(200), self.ingresso, Camarote(300)]
        self.assertEqual([(i.tipo, i.preco) for i in ingressos],
                         [("Cadeira premium", 200), ("Arquibancada", 100), ("Camarote", 300)])

    def test_alteracao_preco_notifica_todos(self):
        self.ingresso.atualizar_preco(120)
        self.assertEqual(self.ingresso.preco, 120)
        esperado = ["Arquibancada: preco alterado de R$ 100.00 para R$ 120.00"]
        for observador in (self.cliente, self.administrador):
            self.assertIsInstance(observador, Observador)
            self.assertEqual(observador.notificacoes, esperado)

    def test_inclusao_descontos_notifica_todos(self):
        self.ingresso.adicionar_desconto(DescontoEstudante(50))
        self.ingresso.adicionar_desconto(DescontoQuantidade(10, 3))
        for observador in (self.cliente, self.administrador):
            self.assertEqual(observador.notificacoes, [
                "Arquibancada: novo desconto — estudante: 50%",
                "Arquibancada: novo desconto — quantidade: 10% a partir de 3 ingressos",
            ])

    def test_calculos_demonstrados(self):
        self.ingresso.atualizar_preco(120)
        self.ingresso.adicionar_desconto(DescontoEstudante(50))
        self.ingresso.adicionar_desconto(DescontoQuantidade(10, 3))
        self.assertEqual(self.ingresso.calcular_total(), 120)
        self.assertEqual(self.ingresso.calcular_total(estudante=True), 60)
        self.assertEqual(self.ingresso.calcular_total(3), 324)
        self.assertEqual(self.ingresso.calcular_total(3, True), 180)

    def test_limite_quantidade(self):
        self.ingresso.adicionar_desconto(DescontoQuantidade(10, 3))
        self.assertEqual(self.ingresso.calcular_total(2), 200)
        self.assertEqual(self.ingresso.calcular_total(3), 270)
        self.assertEqual(self.ingresso.calcular_total(4), 360)

    def test_estudante_sem_desconto_cadastrado(self):
        self.assertEqual(self.ingresso.calcular_total(estudante=True), 100)

    def test_observador_desacoplado(self):
        class ObservadorTeste(Observador):
            def atualizar(self, mensagem):
                self.mensagem = mensagem

        observador = ObservadorTeste()
        self.ingresso.registrar_observador(observador)
        self.ingresso.atualizar_preco(80)
        self.assertIn("Arquibancada", observador.mensagem)
        self.assertIn("80.00", observador.mensagem)

    def test_registro_repetido_nao_duplica_notificacoes(self):
        self.ingresso.registrar_observador(self.cliente)
        self.ingresso.atualizar_preco(120)
        self.assertEqual(len(self.cliente.notificacoes), 1)

    def test_preco_igual_nao_notifica(self):
        self.ingresso.atualizar_preco(100)
        self.assertEqual(self.cliente.notificacoes, [])

    def test_preco_invalido_nao_modifica_nem_notifica(self):
        for preco in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                self.ingresso.atualizar_preco(preco)
            with self.assertRaises(ValueError):
                Camarote(preco)
        self.assertEqual(self.ingresso.preco, 100)
        self.assertEqual(self.cliente.notificacoes, [])

    def test_percentuais_invalidos(self):
        for percentual in (-10, 0, 101, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                DescontoEstudante(percentual)

    def test_quantidades_invalidas(self):
        for quantidade in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                self.ingresso.calcular_total(quantidade)
        for quantidade in (1, 0, 2.5, True):
            with self.assertRaises(ValueError):
                DescontoQuantidade(10, quantidade)

    def test_notificacoes_restritas_ao_ingresso_observado(self):
        Camarote(300).atualizar_preco(350)
        self.assertEqual(self.cliente.notificacoes, [])
