#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wsgiref.simple_server import make_server


def application(environ, start_response):
    # 1.处理request
    query_string = environ['QUERY_STRING']  # 这里是 "name=lucy"
    name = query_string.split("=")[1]  # 从查询字符串 "name=lucy" 里获取 "lucy"

    # 2.定义response信息
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf8')]

    # 3.调用start_response方法，生成response
    start_response(status, headers)

    # 4.返回body
    return [b"<h1>Hello, {}!</h1>".format(name)]


# 5.启动server
if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 9000, application)
    httpd.serve_forever()