from wsgiref.simple_server import make_server

import falcon

from routes.api import Api
from config.log.logger import logging

app = falcon.App()

api = Api()

app.add_route('/api', api)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        logging.info('Serving on port 8000...')
        httpd.serve_forever()
