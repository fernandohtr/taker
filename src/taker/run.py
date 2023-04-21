import re
import json

from time import sleep

from courts.courts_list import COURTS
from courts.court_numbering import NUMBERING
from config.log.logger import logging
from messeger import messeger

TTL_PROCESS_NUMBER = 60 * 60 * 3 # 3 hours
LAZY_PROCESS = 1 # 1 second


def main():
    logging.debug('Starting taker...')
    supported_courts = define_supported_courts()
    
    while(True):
        logging.debug(f'Process number queue: {messeger.lrange("process_number", 0, -1)}')
        process_number = messeger.rpop('process_number')
        if not process_number:
            sleep(LAZY_PROCESS)
            continue
        process_number = process_number.decode('utf-8')
        logging.debug(f'Process number {process_number} received.')
        court = get_court_by_numbering(process_number)
        if court not in supported_courts:
            logging.debug('Court not supported.')
            sleep(LAZY_PROCESS)
            continue
        data = COURTS[court](process_number).get_process_data()
        for d in data:
            messeger.lpush(process_number, json.dumps(d).encode('utf-8'))
            messeger.expire(process_number, TTL_PROCESS_NUMBER)
            logging.info(f'Process number {process_number} data pushed.')
        messeger.lrange(process_number, 0, -1)
        sleep(LAZY_PROCESS)


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


if __name__ == '__main__':
    main()
