from wsgiref.simple_server import make_server

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf8')]
    start_response(status, headers)
    return [b"<h1>Hello, World!</h1>"]  #需要返回一个可迭代的对象，里面的元素需要是byte类型，所以是一个list

if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 9000, application)
    print('Serving HTTP on port 9000...')
    httpd.serve_forever()


#visit url http://127.0.0.1:9000/ can see Hello world