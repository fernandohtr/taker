import falcon

from services.api.process import Process

class Api:

    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.body = ('Hello World!')

    def on_post(self, request, response):
        body = request.media
        process_number = body.get('process_number')
        process = Process(process_number, response)
        process.get_data()
