import unittest
from dataclasses import FrozenInstanceError

from questao_1_memento.gerenciador_tarefas import GerenciadorTarefas
from questao_1_memento.memento import Memento
from questao_1_memento.tarefa import Tarefa
from questao_1_memento.zelador import Zelador


class TesteMemento(unittest.TestCase):
    def setUp(self):
        self.gerenciador = GerenciadorTarefas()

    def estado(self):
        return [(t.getTitulo(), t.getDescricao())
                for t in self.gerenciador.listar_tarefas()]

    def test_acessores_tarefa(self):
        tarefa = Tarefa("A", "B")
        tarefa.setTitulo("C")
        tarefa.setDescricao("D")
        self.assertEqual((tarefa.getTitulo(), tarefa.getDescricao()), ("C", "D"))

    def test_adicao(self):
        self.gerenciador.adicionar("A", "B")
        self.gerenciador.adicionar("C", "D")
        self.assertEqual(self.estado(), [("A", "B"), ("C", "D")])

    def test_edicao(self):
        self.gerenciador.adicionar("A", "B")
        self.gerenciador.editar(0, "C", "D")
        self.assertEqual(self.estado(), [("C", "D")])

    def test_remocao(self):
        self.gerenciador.adicionar("A", "B")
        self.gerenciador.remover(0)
        self.assertEqual(self.estado(), [])

    def test_desfazer_adicao(self):
        self.gerenciador.adicionar("A", "B")
        self.assertTrue(self.gerenciador.desfazer())
        self.assertEqual(self.estado(), [])

    def test_desfazer_edicao(self):
        self.gerenciador.adicionar("A", "B")
        self.gerenciador.editar(0, "C", "D")
        self.gerenciador.desfazer()
        self.assertEqual(self.estado(), [("A", "B")])

    def test_desfazer_remocao_preserva_ordem(self):
        self.gerenciador.adicionar("A", "B")
        self.gerenciador.adicionar("C", "D")
        self.gerenciador.remover(0)
        self.gerenciador.desfazer()
        self.assertEqual(self.estado(), [("A", "B"), ("C", "D")])

    def test_multiplos_desfazeres(self):
        self.gerenciador.adicionar("A", "B")
        self.gerenciador.adicionar("C", "D")
        self.gerenciador.editar(0, "E", "F")
        self.gerenciador.remover(1)
        for esperado in ([("E", "F"), ("C", "D")],
                         [("A", "B"), ("C", "D")], [("A", "B")], []):
            self.assertTrue(self.gerenciador.desfazer())
            self.assertEqual(self.estado(), esperado)
        self.assertFalse(self.gerenciador.desfazer())

    def test_estado_independente_dos_objetos(self):
        tarefa = Tarefa("A", "B")
        memento = Memento([tarefa])
        tarefa.setTitulo("Alterado")
        copia = memento.recuperar_tarefas()
        copia[0].setDescricao("Alterada")
        self.gerenciador.restaurar(memento)
        self.assertEqual(self.estado(), [("A", "B")])
        self.gerenciador.editar(0, "C", "D")
        self.gerenciador.restaurar(memento)
        self.assertEqual(self.estado(), [("A", "B")])

    def test_listagem_nao_altera_originador(self):
        self.gerenciador.adicionar("A", "B")
        tarefas = self.gerenciador.listar_tarefas()
        tarefas[0].setTitulo("Outro")
        tarefas.clear()
        self.assertEqual(self.estado(), [("A", "B")])

    def test_memento_imutavel(self):
        memento = Memento([Tarefa("A", "B")])
        with self.assertRaises(FrozenInstanceError):
            memento._Memento__estado = ()

    def test_historico_vazio(self):
        self.assertFalse(self.gerenciador.desfazer())
        self.assertEqual(self.estado(), [])

    def test_operacoes_invalidas_nao_entram_no_historico(self):
        self.gerenciador.adicionar("A", "B")
        for indice in (-1, 1, "0", True):
            with self.assertRaises(IndexError):
                self.gerenciador.editar(indice, "C", "D")
            with self.assertRaises(IndexError):
                self.gerenciador.remover(indice)
        with self.assertRaises(TypeError):
            self.gerenciador.editar(0, "C", None)
        with self.assertRaises(TypeError):
            self.gerenciador.adicionar(None, "D")
        self.assertEqual(self.estado(), [("A", "B")])
        self.gerenciador.desfazer()
        self.assertEqual(self.estado(), [])
        self.assertFalse(self.gerenciador.desfazer())

    def test_edicao_sem_mudanca_nao_cria_historico(self):
        self.gerenciador.adicionar("A", "B")
        self.gerenciador.editar(0, "A", "B")
        self.gerenciador.desfazer()
        self.assertEqual(self.estado(), [])

    def test_zelador_ordem_inversa(self):
        zelador = Zelador()
        primeiro, segundo = Memento([]), Memento([Tarefa("A", "B")])
        zelador.guardar(primeiro)
        zelador.guardar(segundo)
        self.assertIs(zelador.retirar_ultimo(), segundo)
        self.assertIs(zelador.retirar_ultimo(), primeiro)
        self.assertIsNone(zelador.retirar_ultimo())
