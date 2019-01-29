'''
 抽象 Request 和 Response 对象
 创建一个Request类处理request
 创建一个Response类处理response信息

 输入 http://127.0.0.1:9000/?name=lily ， 获取问号后面的内容，获取name后面的信息。返回hello lily
'''


from wsgiref.simple_server import make_server

import urllib.parse



class Request:

    def __init__(self, environ):
        self.environ = environ
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

def request_response_application(func):

    def application(environ, start_response):

        request = Request(environ)

        response = func(request)

        start_response(response.status, response.headers.items())

        return iter(response)

    return application



@request_response_application

def application(request):

    name = request.args.get('name', 'default_name')


    return Response(['<h1>hello {name}</h1>'.format(name=name)])



if __name__ == '__main__':

    httpd = make_server('127.0.0.1', 9000, application)

    print('Server HTTP on port 9000')

    httpd.serve_forever()