import re
import json

from time import sleep

from courts.courts_list import COURTS
from courts.court_numbering import NUMBERING
from config.log.logger import logging
from messeger import messeger


def main():
    logging.debug('Starting taker...')
    supported_courts = define_supported_courts()
    
    while(True):
        logging.debug('Waiting for process number...')
        process_number = messeger.rpop('process_number')
        if not process_number:
            sleep(1) # turn into a lazy process
            continue
        process_number = process_number.decode('utf-8')
        logging.debug(f'Process number {process_number} received.')
        court = get_court_by_numbering(process_number)
        if court not in supported_courts:
            logging.debug('Court not supported.')
            sleep(1) # turn into a lazy process
            continue
        data = COURTS[court](process_number).get_process_data()
        for d in data:
            messeger.lpush(process_number, json.dumps(d).encode('utf-8'))
            logging.info(f'Process number {process_number} data pushed.')
        sleep(1) # turn into a lazy process


def define_supported_courts():
    messeger.delete('supported_courts')
    supported_courts = []
    for court in COURTS.keys():
        messeger.lpush('supported_courts', court)
        supported_courts.append(court)
    logging.debug(f'Defined supported courts: {supported_courts}')
    return supported_courts

def get_court_by_numbering(process_number):
    regex = r'\.\d\.\d{2}\.'
    court_number = re.search(regex, process_number)
    
    if court_number:
        court = NUMBERING.get(court_number.group(), '')
        return court
    return ''

main()
