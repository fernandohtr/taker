import requests

from bs4 import BeautifulSoup as bs

from config.log.logger import logging
from config.log import message
from config.shared import USER_AGENT
from abstract_instance import AbstractInstance

class FirstInstance(AbstractInstance):

    URL = 'https://esaj.tjce.jus.br/cpopg/show.do'

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
                'Host': 'esaj.tjce.jus.br',
                'Referer': 'https://esaj.tjce.jus.br/cpopg/open.do',
                'User-Agent': USER_AGENT
            },
            verify=False
        )
        logging.debug(f'[TJCE] {message.SEARCH_DATA.format(request.url)}: Status code {request.status_code}')
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
        logging.info(f'[TJCE] {message.FIND_DATA.format(self.process_number)}')
        return process_data
    
    def _get_classe(self, soup):
        data = soup.find('span', id='classeProcesso')
        if not data:
            logging.error(f'[TJCE] {message.CLASSE_NOT_FOUND}')
            raise AttributeError(message.CLASSE_NOT_FOUND, data)
        return data.text
        
    def _get_area(self, soup):
        data = soup.find('div', id='areaProcesso').span
        if not data:
            logging.error(f'[TJCE] {message.AREA_NOT_FOUND}')
            raise AttributeError(message.AREA_NOT_FOUND)
        return data.text
    
    def _get_assunto(self, soup):
        data = soup.find('span', id='assuntoProcesso')
        if not data:
            logging.error(f'[TJCE] {message.ASSUNTO_NOT_FOUND}')
            raise AttributeError(message.ASSUNTO_NOT_FOUND)
        return data.text
    
    def _get_data_distribuicao(self, soup):
        data = soup.find('div', id='dataHoraDistribuicaoProcesso')
        if not data:
            logging.error(f'[TJCE] {message.DATA_DISTRIBUICAO_NOT_FOUND}')
            raise AttributeError(message.DATA_DISTRIBUICAO_NOT_FOUND)
        return data.text
    
    def _get_juiz(self, soup):
        return None
    
    def _get_valor_acao(self, soup):
       return None
    
    def _get_partes_processo(self, soup):
        partes = {}
        todas_partes_data = soup.find('table', id='tableTodasPartes')
        if not todas_partes_data:
            logging.error(f'[TJCE] {message.PARTES_TABLE_NOT_FOUND}')
            raise AttributeError(message.PARTES_TABLE_NOT_FOUND)
        todas_partes = todas_partes_data.find_all('tr')

        for parte in todas_partes:
            parte_data = parte.find('td', class_='nomeParteEAdvogado')
            if not parte_data:
                logging.error(f'[TJCE] {message.PARTES_NOT_FOUND}')
                raise AttributeError(message.PARTES_NOT_FOUND)
            raw_parte = parte_data.text.strip().replace('\t', '').replace('\n \n', ',').replace('\n', '').replace('\xa0', ' ')
            list_partes = raw_parte.split(',')

            tipo_data_raw = parte.find('span', class_='tipoDeParticipacao')
            tipo_data = tipo_data_raw.text.lower().strip()
            if not tipo_data_raw:
                logging.error(f'[TJCE] {message.TIPO_PARTICIPACAO_NOT_FOUND}')
                raise AttributeError(message.TIPO_PARTICIPACAO_NOT_FOUND)
            if tipo_data in partes:
                partes[tipo_data] += f', {list_partes[0]}'
            else:
                partes[tipo_data] = list_partes[0]
        return partes
    
    def _get_lista_movimentacao(self, soup):
        movimentacoes = []
        raw_movimentacoes_data = soup.find('tbody', id='tabelaTodasMovimentacoes')
        if not raw_movimentacoes_data:
            logging.error(f'[TJCE] {message.MOVIMENTACOES_TABLE_NOT_FOUND}')
            raise AttributeError(message.MOVIMENTACOES_TABLE_NOT_FOUND)
        raw_movimentacoes = raw_movimentacoes_data.find_all('tr')

        for movimentacao in raw_movimentacoes:
            data_data = movimentacao.find('td', class_='dataMovimentacao')
            if not data_data:
                logging.error(f'[TJCE] {message.DATA_NOT_FOUND}')
                raise AttributeError(message.DATA_NOT_FOUND)
            
            movimentacao_data = movimentacao.find('td', class_='descricaoMovimentacao')
            if not movimentacao_data:
                logging.error(f'[TJCE] {message.MOVIMENTACAO_NOT_FOUND}')
                raise AttributeError(message.MOVIMENTACAO_NOT_FOUND)
            movimentacoes.append({
                'data': data_data.text.replace('\n', '').replace('\t', ''),
                'movimento': movimentacao_data.text.replace('\n', '').replace('\t', '')
            })
        return movimentacoes
