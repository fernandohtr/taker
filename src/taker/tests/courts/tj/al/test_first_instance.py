import unittest

from bs4 import BeautifulSoup as bs

from courts.tj.al.first_instance import FirstInstance
from abstract_instance import AbstractInstance


class TestFirstInstance(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www2.tjal.jus.br/cpopg/show.do'
        self.process_number = '0800001-93.2017.8.02.0001'
        self.first_instance = FirstInstance()

        with open('src/taker/tests/courts/tj/al/fixtures/first_instance.html', 'r') as f:
            fixture = f.read()
        self.soup = bs(fixture, 'html.parser')
        self.fail_soup = bs('', 'html.parser')

    def test_instance(self):
        self.assertIsInstance(self.first_instance, FirstInstance)
        self.assertIsInstance(self.first_instance, AbstractInstance)

    def test_get_classe_successfully(self):
        expected = 'Procedimento Comum Cível'
        received = self.first_instance._get_classe(self.soup)
        self.assertEqual(expected, received)

    def test_classe_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_classe(self.fail_soup)

    def test_get_area_successfully(self):
        expected = 'Cível'
        received = self.first_instance._get_area(self.soup)
        self.assertEqual(expected, received)

    def test_area_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_area(self.fail_soup)

    def test_get_assunto_successfully(self):
        expected = 'Dano Material'
        received = self.first_instance._get_assunto(self.soup)
        self.assertEqual(expected, received)

    def test_assunto_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_assunto(self.fail_soup)

    def test_get_data_distribuicao_successfully(self):
        expected = '02/05/2018 às 19:01 - Sorteio'
        received = self.first_instance._get_data_distribuicao(self.soup)
        self.assertEqual(expected, received)

    def test_data_distribuicao_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_data_distribuicao(self.fail_soup)

    def test_get_juiz_successfully(self):
        expected = 'José Cícero Alves da Silva'
        received = self.first_instance._get_juiz(self.soup)
        self.assertEqual(expected, received)

    def test_juiz_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_juiz(self.fail_soup)

    def test_get_valor_acao_successfully(self):
        expected = '281.178,42'
        received = self.first_instance._get_valor_acao(self.soup)
        self.assertEqual(expected, received)

    def test_valor_acao_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_valor_acao(self.fail_soup)

    def test_get_partes_successfully(self):
        expected = {
			'autor': {
				'parte': 'José Carlos Cerqueira Souza Filho',
				'advogados': [
					'Vinicius Faria de Cerqueira'
				]
			},
			'autora': {
				'parte': 'Livia Nascimento da Rocha',
				'advogados': [
					'Vinicius Faria de Cerqueira'
				]
			},
			'ré': {
				'parte': 'Cony Engenharia Ltda.',
				'advogados': [
					'Carlos Henrique de Mendonça Brandão ',
					'Guilherme Freire Furtado ',
					'Maria Eugênia Barreiros de Mello ',
					'Vítor Reis de Araujo Carvalho'
				]
			},
			'réu': {
				'parte': 'Banco do Brasil S A',
				'advogados': [
					'Nelson Wilians Fratoni Rodrigues'
				]
			}
		}
        received = self.first_instance._get_partes_processo(self.soup)
        self.assertEqual(expected, received)

    def test_partes_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_partes_processo(self.fail_soup)

    def test_get_lista_movimentacao_successfully(self):
        excepted_first_movimentacao = {
            "data": "22/02/2021",
            "movimento": "Remetido recurso eletrônico ao Tribunal de Justiça/Turma de recurso"
		}
        excepted_last_movimentacao = {
            "data": "02/05/2018",
            "movimento": "Distribuído por Sorteio"
        }
        received = self.first_instance._get_lista_movimentacao(self.soup)
        self.assertEqual(excepted_first_movimentacao, received[0])
        self.assertEqual(excepted_last_movimentacao, received[-1])

    def test_lista_movimentacao_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_lista_movimentacao(self.fail_soup)
