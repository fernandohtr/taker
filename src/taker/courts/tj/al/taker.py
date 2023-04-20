from abstract_taker_tj import AbstractTakerTJ
from .first_instance import FirstInstance
from .second_instance import SecondInstance
from config.log.logger import logging

class TakerTJAL(AbstractTakerTJ):

    def __init__(self, process_number):
        self.process_number = process_number
        self.first_instance = FirstInstance(self.process_number)
        self.second_instance = SecondInstance(self.process_number)

    def get_process_data(self):
        process_data = []
        for instance in [
            self.get_first_instance,
            self.get_second_instance,
        ]:
            try:
                data = instance()
                process_data.append(data)
            except Exception as error:
                logging.error(f'[TJCE] Error in {instance}: {error}')
                continue
        return process_data

    def get_first_instance(self):
        return self.first_instance.get_process_data()
    
    def get_second_instance(self):
        return self.second_instance.get_process_data()