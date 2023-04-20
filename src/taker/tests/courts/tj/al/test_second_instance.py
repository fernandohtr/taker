import unittest

from unittest.mock import patch

from bs4 import BeautifulSoup as bs

from courts.tj.al.second_instance import SecondInstance
from abstract_instance import AbstractInstance


class TestFirstInstance(unittest.TestCase):

    def setUp(self):
        process_number = '0710802-55.2018.8.02.0001'
        self.second_instance = SecondInstance(process_number)

        with open('src/taker/tests/courts/tj/al/fixtures/second_instance.html', 'r') as f:
            fixture = f.read()
        self.soup = bs(fixture, 'html.parser')
        self.fail_soup = bs('', 'html.parser')

    def test_instance(self):
        self.assertIsInstance(self.second_instance, SecondInstance)
        self.assertIsInstance(self.second_instance, AbstractInstance)

    def test_get_classe_successfully(self):
        expected = 'Apelação Cível'
        received = self.second_instance._get_classe(self.soup)
        self.assertEqual(expected, received)

    def test_classe_not_found(self):
        with self.assertRaises(AttributeError):
            self.second_instance._get_classe(self.fail_soup)

    def test_get_area_successfully(self):
        expected = 'Cível'
        received = self.second_instance._get_area(self.soup)
        self.assertEqual(expected, received)

    def test_area_not_found(self):
        with self.assertRaises(AttributeError):
            self.second_instance._get_area(self.fail_soup)

    def test_get_assunto_successfully(self):
        expected = 'Obrigações'
        received = self.second_instance._get_assunto(self.soup)
        self.assertEqual(expected, received)

    def test_assunto_not_found(self):
        with self.assertRaises(AttributeError):
            self.second_instance._get_assunto(self.fail_soup)

    def test_get_data_distribuicao_successfully(self):
        expected = None
        received = self.second_instance._get_data_distribuicao(self.soup)
        self.assertEqual(expected, received)

    def test_get_juiz_successfully(self):
        expected = 'VICE PRESIDENTE DO TRIBUNAL DE JUSTIÇA DE ALAGOAS'
        received = self.second_instance._get_juiz(self.soup)
        self.assertEqual(expected, received)

    def test_juiz_not_found(self):
        with self.assertRaises(AttributeError):
            self.second_instance._get_juiz(self.fail_soup)

    def test_get_valor_acao_successfully(self):
        expected = '281.178,42'
        received = self.second_instance._get_valor_acao(self.soup)
        self.assertEqual(expected, received)

    def test_valor_acao_not_found(self):
        with self.assertRaises(AttributeError):
            self.second_instance._get_valor_acao(self.fail_soup)

    def test_get_partes_successfully(self):
        expected = {
            'apelante:': {
                'parte': 'Cony Engenharia Ltda.',
                'advogados': [
                    'Carlos Henrique de Mendonça Brandão',
                    'Guilherme Freire Furtado',
                    'Maria Eugênia Barreiros de Mello',
                    'Vítor Reis de Araujo Carvalho'
                ]
            },
            'apelado:': {
                'parte': 'José Carlos Cerqueira Souza Filho',
                'advogados': [
                    'Vinicius Faria de Cerqueira'
                ]
            }
        }
        received = self.second_instance._get_partes_processo(self.soup)
        self.assertEqual(expected, received)

    def test_partes_not_found(self):
        with self.assertRaises(AttributeError):
            self.second_instance._get_partes_processo(self.fail_soup)

    def test_get_lista_movimentacao_successfully(self):
        excepted_first_movimentacao = {
            'data': '12/04/2023',
            'movimento': 'Publicado'
        }
        excepted_last_movimentacao = {
            'data': '22/02/2021',
            'movimento': 'Recebidos os Autos pela Entrada de Recursos Foro de origem: Foro de Maceió\nVara de origem: 4ª Vara Cível da Capital'
        }
        received = self.second_instance._get_lista_movimentacao(self.soup)
        self.assertEqual(excepted_first_movimentacao, received[0])
        self.assertEqual(excepted_last_movimentacao, received[-1])

    def test_lista_movimentacao_not_found(self):
        with self.assertRaises(AttributeError):
            self.second_instance._get_lista_movimentacao(self.fail_soup)

    @patch('courts.tj.al.second_instance.requests.Session.get')
    @patch('courts.tj.al.second_instance.bs')
    @patch('courts.tj.al.second_instance.SecondInstance.get_process_data')
    @patch('courts.tj.al.second_instance.SecondInstance._get_classe')
    @patch('courts.tj.al.second_instance.SecondInstance._get_area')
    @patch('courts.tj.al.second_instance.SecondInstance._get_assunto')
    @patch('courts.tj.al.second_instance.SecondInstance._get_data_distribuicao')
    @patch('courts.tj.al.second_instance.SecondInstance._get_juiz')
    @patch('courts.tj.al.second_instance.SecondInstance._get_valor_acao')
    @patch('courts.tj.al.second_instance.SecondInstance._get_partes_processo')
    @patch('courts.tj.al.second_instance.SecondInstance._get_lista_movimentacao')
    def test_get_process_data(
            self,
            mock_get_lista_movimentacao,
            mock_get_partes_processo,
            mock_get_valor_acao,
            mock_get_juiz,
            mock_get_data_distribuicao,
            mock_get_assunto,
            mock_get_area,
            mock_get_classe,
            mock_get_process_data,
            mock_bs,
            mock_get):

        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = '<html><body><span id="classeProcesso">Test Class</span></body></html>'

        mock_bs.return_value = bs(mock_response.text, 'html.parser')

        mock_get_classe.return_value = 'Test Class'
        mock_get_area.return_value
        mock_get_assunto.return_value
        mock_get_data_distribuicao.return_value
        mock_get_juiz.return_value
        mock_get_valor_acao.return_value
        mock_get_partes_processo.return_value
        mock_get_lista_movimentacao.return_value

        self.second_instance.get_process_data()

        mock_get_process_data.assert_called_once()
