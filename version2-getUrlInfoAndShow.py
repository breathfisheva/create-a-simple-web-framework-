#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
获取url的信息，返回相应的内容
http://127.0.0.1:9000/?name=lucy， 输出为hello lucy
'''

from wsgiref.simple_server import make_server


def application(environ, start_response):
# print(environ)
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf8')]

    query_string = environ['QUERY_STRING']    # 这里是 "name=John"
    name = query_string.split("=")[1]    # 从查询字符串 "name=John" 里获取 "John"
    start_response(status, headers)
    return ["<h1>Hello, {}!</h1>".format(name).encode('utf-8')] #需要是一个可迭代对象，里面的元素需要是byte类型，所以encode成utf-8，返回是一个list


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 9000, application)
    httpd.serve_forever()