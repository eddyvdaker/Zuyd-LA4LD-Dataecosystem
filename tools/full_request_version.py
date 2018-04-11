# -*- coding: utf-8 -*-
"""
    tools.full_request_version
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    A wrapper around the flask application that provides insight in the
    exact HTTP requests going en and coming out of the application. Used
    for debugging purposes.
"""
import pprint

from app import create_app

app = create_app()


class LoggingWrapper(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, resp):
        errorlog = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(environ, log_response)


if __name__ == '__main__':
    app.wsgi_app = LoggingWrapper(app.wsgi_app)
    app.run()
