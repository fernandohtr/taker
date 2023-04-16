from time import sleep
from courts.courts_list import COURTS

court = 'TJAL'
process_number = '0802324-93.2023.8.02.0000'
# process_number = '0710802-55.2018.8.02.0001'

while(True):
    data = COURTS[court](process_number).get_process_data()
    print(data)
    sleep(5)
