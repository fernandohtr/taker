import re
import json
from time import sleep

from wsgiref.simple_server import make_server
from messeger import messeger

import falcon


class Api(object):

    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.body = ('Hello World!')

    def on_post(self, request, response):
        body = request.media

        process_number = body.get('process_number')
        
        self._check_existence_process_number(process_number)
        self._validate_process_number(process_number)
        # TODO
        # self._validate_court(process_number)

        # 0710802-55.2018.8.02.0001
        # \d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}

        messeger.rpush('process_number', process_number)
        result = None
        check_times = 0
        while result is None:
            sleep(1)
            result = messeger.get(process_number)
            check_times += 1
            if check_times > 5:
                break
        messeger.delete(process_number)

        response.status = falcon.HTTP_200
        response.body = json.dumps(result)

    def _check_existence_process_number(self, process_number):
        if process_number is None:
            raise falcon.HTTPBadRequest(
                'A \'process number\' is required.'
            )

    def _validate_process_number(self, process_number):
        regex = r'^\d{6,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$'
        if not re.match(regex, process_number):
            raise falcon.HTTPBadRequest(
                'The process number must be in the format: NNNNNNN-DD.AAAA.J.TR.OOOO'
            )


app = falcon.App()

api = Api()

app.add_route('/api', api)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
