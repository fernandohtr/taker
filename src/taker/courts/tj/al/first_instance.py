import requests

from bs4 import BeautifulSoup as bs

from config.log.logger import logging
from config.log import message
from config.shared import USER_AGENT
from abstract_instance import AbstractInstance

class FirstInstance(AbstractInstance):

    @classmethod
    def get_process_data(cls, url, process_number):
        session = requests.Session()
        request = session.get(
            url,
            params={
                'processo.numero': process_number
            },
            headers={
                'User-Agent': USER_AGENT
            }
        )
        logging.debug(message.SEARCH_DATA.format(request.url), extra={'court': 'TJAL'})
        # if request.text.find('Não existem informações disponíveis para os parâmetros informados.'):
        #     logging.info(message.PROCESS_NOT_FOUND.format(process_number), extra={'court': 'TJAL'})
        #     raise AttributeError(message.PROCESS_NOT_FOUND.format(process_number))
        soup = bs(request.text, 'html.parser')
        process_data = {
            'classe': cls._get_classe(soup),
            'area': cls._get_area(soup),
            'assunto': cls._get_assunto(soup),
            'data_distribuicao': cls._get_data_distribuicao(soup),
            'juiz': cls._get_juiz(soup),
            'valor_acao': cls._get_valor_acao(soup),
            'partes_processo': cls._get_partes_processo(soup),
            'lista_movimentacao': cls._get_lista_movimentacao(soup),
        }
        logging.info(message.FIND_DATA.format(process_number), extra={'court': 'TJAL'})
        return process_data
    
    def _get_classe(soup):
        data = soup.find('span', id='classeProcesso')
        if not data:
            logging.error(message.CLASSE_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.CLASSE_NOT_FOUND, data)
        return data.text
        
    def _get_area(soup):
        data = soup.find('div', id='areaProcesso').span
        if not data:
            logging.error(message.AREA_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.AREA_NOT_FOUND)
        return data.text
    
    def _get_assunto(soup):
        data = soup.find('span', id='assuntoProcesso')
        if not data:
            logging.error(message.ASSUNTO_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.ASSUNTO_NOT_FOUND)
        return data.text
    
    def _get_data_distribuicao(soup):
        data = soup.find('div', id='dataHoraDistribuicaoProcesso')
        if not data:
            logging.error(message.DATA_DISTRIBUICAO_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.DATA_DISTRIBUICAO_NOT_FOUND)
        return data.text
    
    def _get_juiz(soup):
        data = soup.find('span', id='juizProcesso')
        if not data:
            logging.error(message.JUIZ_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.JUIZ_NOT_FOUND)
        return data.text
    
    def _get_valor_acao(soup):
        data = soup.find('div', id='valorAcaoProcesso')
        if not data:
            logging.error(message.VALOR_ACAO_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.VALOR_ACAO_NOT_FOUND)
        return data.text.replace('R$', '').strip()
    
    def _get_partes_processo(soup):
        partes = {}
        todas_partes_data = soup.find('table', id='tableTodasPartes')
        if not todas_partes_data:
            logging.error(message.PARTES_TABLE_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.PARTES_TABLE_NOT_FOUND)
        todas_partes = todas_partes_data.find_all('tr')

        for parte in todas_partes:
            parte_data = parte.find('td', class_='nomeParteEAdvogado')
            if not parte_data:
                logging.error(message.PARTES_NOT_FOUND, extra={'court': 'TJAL'})
                raise AttributeError(message.PARTES_NOT_FOUND)
            raw_parte = parte_data.text.strip().replace('\t', '').replace('\n \n', ',').replace('\n', '').replace('\xa0', ' ')
            list_partes = raw_parte.split(',')

            advogados = []
            for adv in list_partes[1:]:
                advogados.append(adv.replace('Advogado: ', '').replace('Advogada: ', ''))

            tipo_data = parte.find('span', class_='tipoDeParticipacao')
            if not tipo_data:
                logging.error(message.TIPO_PARTICIPACAO_NOT_FOUND, extra={'court': 'TJAL'})
                raise AttributeError(message.TIPO_PARTICIPACAO_NOT_FOUND)
            partes[tipo_data.text.lower().strip() ] = {
                'parte': list_partes[0],
                'advogados': advogados
            }
        return partes
    
    def _get_lista_movimentacao(soup):
        movimentacoes = []
        raw_movimentacoes_data = soup.find('tbody', id='tabelaTodasMovimentacoes')
        if not raw_movimentacoes_data:
            logging.error(message.MOVIMENTACOES_TABLE_NOT_FOUND, extra={'court': 'TJAL'})
            raise AttributeError(message.MOVIMENTACOES_TABLE_NOT_FOUND)
        raw_movimentacoes = raw_movimentacoes_data.find_all('tr')

        for movimentacao in raw_movimentacoes:
            data_data = movimentacao.find('td', class_='dataMovimentacao')
            if not data_data:
                logging.error(message.DATA_NOT_FOUND, extra={'court': 'TJAL'})
                raise AttributeError(message.DATA_NOT_FOUND)
            
            movimentacao_data = movimentacao.find('td', class_='descricaoMovimentacao')
            if not movimentacao_data:
                logging.error(message.MOVIMENTACAO_NOT_FOUND, extra={'court': 'TJAL'})
                raise AttributeError(message.MOVIMENTACAO_NOT_FOUND)
            movimentacoes.append({
                'data': data_data.text.replace('\n', '').replace('\t', ''),
                'movimento': movimentacao_data.text.replace('\n', '').replace('\t', '')
            })
        return movimentacoes
