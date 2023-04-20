from abc import ABCMeta, abstractmethod

class AbstractInstance(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, process_number):
        self.process_number = process_number
    
    @abstractmethod
    def get_process_data(self):
        pass

    @abstractmethod
    def _get_classe(self, soup):
        pass

    @abstractmethod
    def _get_area(self, soup):
        pass

    @abstractmethod
    def _get_assunto(self, soup):
        pass

    @abstractmethod
    def _get_data_distribuicao(self, soup):
        pass

    @abstractmethod
    def _get_juiz(self, soup):
        pass

    @abstractmethod
    def _get_valor_acao(self, soup):
        pass

    @abstractmethod
    def _get_partes_processo(self, soup):
        pass

    @abstractmethod
    def _get_lista_movimentacao(self, soup):
        pass
    