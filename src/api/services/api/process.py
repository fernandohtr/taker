import re
import json
from time import sleep

from messeger import messeger
from court_numbering import NUMBERING
from config.log.logger import logging

import falcon

class Process:

    def __init__(self, process_number, response):
        self.process_number = process_number
        self.response = response

    def get_data(self):
        logging.info(f'Process number {self.process_number} received.')

        self._check_existence_process_number(self.process_number)
        self._validate_process_number(self.process_number)
        self._validate_court(self.process_number)

        result = []

        if messeger.exists(self.process_number):
            result = [
                json.loads(data.decode('utf-8')) for data in messeger.lrange(self.process_number, 0, -1)
            ]
        if result:
            self.response.status = falcon.HTTP_200
            self.response.body = json.dumps(result)
            return

        messeger.lpush('process_number', self.process_number)
        logging.info(f'Process number {self.process_number} pushed: {messeger.lrange("process_number", 0, -1)}')
        check_times = 1
        timeout = 5
        while not result:
            sleep(1)
            result = [
                json.loads(data.decode('utf-8')) for data in messeger.lrange(self.process_number, 0, -1)
            ]
            check_times += 1
            if check_times > timeout:
                break
        if not result:
            self.response.status = falcon.HTTP_404
            self.response.body = json.dumps({'message': f'Process {self.process_number} not found.'})
            return

        self.response.status = falcon.HTTP_200
        self.response.body = json.dumps(result)

    def _check_existence_process_number(self, process_number):
        if process_number is None:
            logging.debug('A \'process number\' is required.')
            raise falcon.HTTPBadRequest(
                description='A \'process number\' is required.'
            )

    def _validate_process_number(self, process_number):
        regex = r'^\d{6,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$'
        if not re.match(regex, process_number):
            logging.debug('The process number must be in the format: NNNNNNN-DD.AAAA.J.TR.OOOO')
            raise falcon.HTTPBadRequest(
                description='The process number must be in the format: NNNNNNN-DD.AAAA.J.TR.OOOO'
            )
        
    def _validate_court(self, process_number):
        court = self._get_court_by_numbering(process_number)
        supported_courts = [c.decode('utf-8') for c in messeger.lrange('supported_courts', 0, -1)]
        if court not in supported_courts:
            logging.debug('Court not supported.')
            raise falcon.HTTPBadRequest(
                description='Court not supported.'
            )
    
    def _get_court_by_numbering(self, process_number):
        regex = r'\.\d\.\d{2}\.'
        court_number = re.search(regex, process_number)
        if court_number:
            court = NUMBERING.get(court_number.group(), '')
            return court
        return ''
