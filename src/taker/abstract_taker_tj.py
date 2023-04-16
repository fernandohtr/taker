from abc import ABCMeta, abstractmethod

class AbstractTakerTJ(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, process_number):
        self.process_number = process_number

    @abstractmethod
    def get_process_data(self):
        pass
