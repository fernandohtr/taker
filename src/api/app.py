from wsgiref.simple_server import make_server

import falcon

from routes.api import Api

app = falcon.App()

api = Api()

app.add_route('/api', api)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
