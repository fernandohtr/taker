import requests

from bs4 import BeautifulSoup as bs

from config.log.logger import logging
from config.log import message
from config.shared import USER_AGENT
from abstract_instance import AbstractInstance

class FirstInstance(AbstractInstance):

    URL = 'https://www2.tjal.jus.br/cpopg/show.do'

    def __init__(self, process_number):
        self.process_number = process_number

    def get_process_data(self):
        session = requests.Session()
        request = session.get(
            self.URL,
            params={
                'processo.numero': self.process_number
            },
            headers={
                'User-Agent': USER_AGENT
            }
        )
        logging.debug(f'[TJAL] {message.SEARCH_DATA.format(request.url)}')
        soup = bs(request.text, 'html.parser')
        process_data = {
            'classe': self._get_classe(soup),
            'area': self._get_area(soup),
            'assunto': self._get_assunto(soup),
            'data_distribuicao': self._get_data_distribuicao(soup),
            'juiz': self._get_juiz(soup),
            'valor_acao': self._get_valor_acao(soup),
            'partes_processo': self._get_partes_processo(soup),
            'lista_movimentacao': self._get_lista_movimentacao(soup),
        }
        logging.info(f'[TJAL] {message.FIND_DATA.format(self.process_number)}')
        return process_data
    
    def _get_classe(self, soup):
        data = soup.find('span', id='classeProcesso')
        if not data:
            logging.error(f'[TJAL] {message.CLASSE_NOT_FOUND}')
            raise AttributeError(message.CLASSE_NOT_FOUND, data)
        return data.text
        
    def _get_area(self, soup):
        data = soup.find('div', id='areaProcesso').span
        if not data:
            logging.error(f'[TJAL] {message.AREA_NOT_FOUND}')
            raise AttributeError(message.AREA_NOT_FOUND)
        return data.text
    
    def _get_assunto(self, soup):
        data = soup.find('span', id='assuntoProcesso')
        if not data:
            logging.error(f'[TJAL] {message.ASSUNTO_NOT_FOUND}')
            raise AttributeError(message.ASSUNTO_NOT_FOUND)
        return data.text
    
    def _get_data_distribuicao(self, soup):
        data = soup.find('div', id='dataHoraDistribuicaoProcesso')
        if not data:
            logging.error(f'[TJAL] {message.DATA_DISTRIBUICAO_NOT_FOUND}')
            raise AttributeError(message.DATA_DISTRIBUICAO_NOT_FOUND)
        return data.text
    
    def _get_juiz(self, soup):
        data = soup.find('span', id='juizProcesso')
        if not data:
            logging.error(f'[TJAL] {message.JUIZ_NOT_FOUND}')
            raise AttributeError(message.JUIZ_NOT_FOUND)
        return data.text
    
    def _get_valor_acao(self, soup):
        data = soup.find('div', id='valorAcaoProcesso')
        if not data:
            logging.error(f'[TJAL] {message.VALOR_ACAO_NOT_FOUND}')
            raise AttributeError(message.VALOR_ACAO_NOT_FOUND)
        return data.text.replace('R$', '').strip()
    
    def _get_partes_processo(self, soup):
        partes = {}
        todas_partes_data = soup.find('table', id='tableTodasPartes')
        if not todas_partes_data:
            logging.error(f'[TJAL] {message.PARTES_TABLE_NOT_FOUND}')
            raise AttributeError(message.PARTES_TABLE_NOT_FOUND)
        todas_partes = todas_partes_data.find_all('tr')

        for parte in todas_partes:
            parte_data = parte.find('td', class_='nomeParteEAdvogado')
            if not parte_data:
                logging.error(f'[TJAL] {message.PARTES_NOT_FOUND}')
                raise AttributeError(message.PARTES_NOT_FOUND)
            raw_parte = parte_data.text.strip().replace('\t', '').replace('\n \n', ',').replace('\n', '').replace('\xa0', ' ')
            list_partes = raw_parte.split(',')

            raw_advogados = list_partes[1].replace('Advogado: ', ',').replace('Advogada: ', ',').split(',')
            advogados = []
            for adv in raw_advogados[1:]:
                advogados.append(adv)

            tipo_data = parte.find('span', class_='tipoDeParticipacao')
            if not tipo_data:
                logging.error(f'[TJAL] {message.TIPO_PARTICIPACAO_NOT_FOUND}')
                raise AttributeError(message.TIPO_PARTICIPACAO_NOT_FOUND)
            partes[tipo_data.text.lower().strip() ] = {
                'parte': list_partes[0],
                'advogados': advogados
            }
        return partes
    
    def _get_lista_movimentacao(self, soup):
        movimentacoes = []
        raw_movimentacoes_data = soup.find('tbody', id='tabelaTodasMovimentacoes')
        if not raw_movimentacoes_data:
            logging.error(f'[TJAL] {message.MOVIMENTACOES_TABLE_NOT_FOUND}')
            raise AttributeError(message.MOVIMENTACOES_TABLE_NOT_FOUND)
        raw_movimentacoes = raw_movimentacoes_data.find_all('tr')

        for movimentacao in raw_movimentacoes:
            data_data = movimentacao.find('td', class_='dataMovimentacao')
            if not data_data:
                logging.error(f'[TJAL] {message.DATA_NOT_FOUND}')
                raise AttributeError(message.DATA_NOT_FOUND)
            
            movimentacao_data = movimentacao.find('td', class_='descricaoMovimentacao')
            if not movimentacao_data:
                logging.error(f'[TJAL] {message.MOVIMENTACAO_NOT_FOUND}')
                raise AttributeError(message.MOVIMENTACAO_NOT_FOUND)
            movimentacoes.append({
                'data': data_data.text.replace('\n', '').replace('\t', ''),
                'movimento': movimentacao_data.text.replace('\n', '').replace('\t', '')
            })
        return movimentacoes
