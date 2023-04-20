import unittest

from unittest.mock import patch

from bs4 import BeautifulSoup as bs

from courts.tj.ce.first_instance import FirstInstance
from abstract_instance import AbstractInstance


class TestFirstInstance(unittest.TestCase):

    def setUp(self):
        process_number = '0070337-91.2008.8.06.0001'
        self.first_instance = FirstInstance(process_number)

        with open('src/taker/tests/courts/tj/ce/fixtures/first_instance.html', 'r') as f:
            fixture = f.read()
        self.soup = bs(fixture, 'html.parser')
        self.fail_soup = bs('', 'html.parser')

    def test_instance(self):
        self.assertIsInstance(self.first_instance, FirstInstance)
        self.assertIsInstance(self.first_instance, AbstractInstance)

    def test_get_classe_successfully(self):
        expected = 'Ação Penal - Procedimento Ordinário'
        received = self.first_instance._get_classe(self.soup)
        self.assertEqual(expected, received)

    def test_classe_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_classe(self.fail_soup)

    def test_get_area_successfully(self):
        expected = 'Criminal'
        received = self.first_instance._get_area(self.soup)
        self.assertEqual(expected, received)

    def test_area_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_area(self.fail_soup)

    def test_get_assunto_successfully(self):
        expected = 'Crimes de Trânsito'
        received = self.first_instance._get_assunto(self.soup)
        self.assertEqual(expected, received)

    def test_assunto_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_assunto(self.fail_soup)

    def test_get_data_distribuicao_successfully(self):
        expected = '02/05/2018 às 09:13 - Sorteio'
        received = self.first_instance._get_data_distribuicao(self.soup)
        self.assertEqual(expected, received)

    def test_data_distribuicao_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_data_distribuicao(self.fail_soup)

    def test_get_juiz_successfully(self):
        received = self.first_instance._get_juiz(self.soup)
        self.assertIsNone(received)

    def test_get_valor_acao_successfully(self):
        received = self.first_instance._get_valor_acao(self.soup)
        self.assertIsNone(received)

    def test_get_partes_successfully(self):
        expected = {
            'vítima': 'G. de O. C., A. S. F.',
            'autor': 'Ministério Público do Estado do Ceará',
            'terceiro': 'Departamento de Tecnologia da Informação e Comunicação - DETIC (Polícia Civil)',
            'testemunha': 'M. L. S. I.'
        }
        received = self.first_instance._get_partes_processo(self.soup)
        self.assertEqual(expected, received)

    def test_partes_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_partes_processo(self.fail_soup)

    def test_get_lista_movimentacao_successfully(self):
        excepted_first_movimentacao = {
            'data': '16/08/2022',
            'movimento': 'Juntada de OfícioNº Protocolo: WEB1.22.02299977-0Tipo da Petição: OfícioData: 16/08/2022 12:49'
        }
        excepted_last_movimentacao = {
            'data': '10/07/2008',
            'movimento': 'ProtocoladoPROTOCOLADO - Local: SERVIÇO DE PORTARIA DOS FEITOS JUDICIAIS DA COMARCA DE FORTALEZA'
        }
        received = self.first_instance._get_lista_movimentacao(self.soup)
        self.assertEqual(excepted_first_movimentacao, received[0])
        self.assertEqual(excepted_last_movimentacao, received[-1])

    def test_lista_movimentacao_not_found(self):
        with self.assertRaises(AttributeError):
            self.first_instance._get_lista_movimentacao(self.fail_soup)

    @patch('courts.tj.ce.first_instance.requests.Session.get')
    @patch('courts.tj.ce.first_instance.bs')
    @patch('courts.tj.ce.first_instance.FirstInstance.get_process_data')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_classe')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_area')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_assunto')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_data_distribuicao')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_juiz')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_valor_acao')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_partes_processo')
    @patch('courts.tj.ce.first_instance.FirstInstance._get_lista_movimentacao')
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

        self.first_instance.get_process_data()

        mock_get_process_data.assert_called_once()
