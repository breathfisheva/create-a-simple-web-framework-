'''
add routers
input http://127.0.0.1:9000/goodbye/lucy/ will show goodbye lucy
input http://127.0.0.1:9000/hello/lucy/ will show hello lucy
'''

from wsgiref.simple_server import make_server
import urllib.parse

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ['PATH_INFO']

    @property
    def args(self):
        """ 把查询参数转成字典形式 """
        get_arguments = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
        return {k: v[0] for k, v in get_arguments.items()}


import http.client
from wsgiref.headers import Headers

class Response:
    def __init__(self, response=None, status=200, charset='utf-8', content_type='text/html'):
        self.response = [] if response is None else response
        self.charset = charset
        self.headers = Headers()
        content_type = '{content_type}; charset={charset}'.format(content_type=content_type, charset=charset)
        self.headers.add_header('content-type', content_type)
        self._status = status

    @property
    def status(self):
        status_string = http.client.responses.get(self._status, 'UNKNOWN')
        return '{status} {status_string}'.format(status=self._status, status_string=status_string)

    def __iter__(self):
        for val in self.response:
            if isinstance(val, bytes):
                yield val
            else:
                yield val.encode(self.charset)

import re
class NotFoundError(Exception):
    pass

class Router(object):
    def __init__(self):
        self.routing_table = []  # 保存url pattern，和对应的函数

    def add_route(self, pattern, callback):
        self.routing_table.append((pattern, callback))  # 求路径到可调用对象的 tuple 列表

    def match(self, path):
        for (pattern, callback) in self.routing_table:
            m = re.match(pattern, path)
            if m:
                return (callback, m.groups())
        raise NotFoundError()

def hello(request, name):
    return Response("<h1>Hello, {name}</h1>".format(name=name))

def goodbye(request, name):
    return Response("<h1>Goodbye, {name}</h1>".format(name=name))

routers = Router()
routers.add_route(r'/hello/(.*)/$', hello)
routers.add_route(r'/goodbye/(.*)/$', goodbye)


def request_response_application(func):
    def application(environ, start_response):
        try:
            request = Request(environ)

            callback, args = routers.match(request.path)
            response = callback(request, *args)

        except NotFoundError:
            response = Response("<h1>Not found</h1>", status=404)
        start_response(response.status,
                       response.headers.items())  # <class 'list'>: [('content-type', 'text/html; charset=utf-8')]
        return iter(response)

    return application


@request_response_application
def application(request):
    name = request.args.get('name', 'default_name')  # 获取查询字符串中的 name
    return Response(['<h1>hello {name}</h1>'.format(name=name)])


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 9000, application)
    print('Server HTTP on port 9000')
    httpd.serve_forever()