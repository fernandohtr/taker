from abstract_taker_tj import AbstractTakerTJ
from .first_instance import FirstInstance
from .second_instance import SecondInstance

class TakerTJAL(AbstractTakerTJ):

    URL_FIRST_INSTANCE = 'https://www2.tjal.jus.br/cpopg/show.do'
    URL_SECOND_INSTANCE = 'https://www2.tjal.jus.br/cposg5/search.do'

    def __init__(self, process_number):
        self.process_number = process_number

    def get_process_data(self):
        process_data = []
        for instance in [
            self.get_first_instance,
            self.get_second_instance,
        ]:
            try:
                data = instance()
                process_data.append(data)
            except:
                continue
        return process_data

    def get_first_instance(self):
        return FirstInstance.get_process_data(self.URL_FIRST_INSTANCE, self.process_number)
    
    def get_second_instance(self):
        return SecondInstance.get_process_data(self.URL_SECOND_INSTANCE, self.process_number)