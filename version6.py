'''
处理异步 使用aiohttp，因为使用了aiohttp，我们可以直接用它的router属性，所以相比之前的版本5少了很多代码
需要等待的都要用async，await写成异步，同时注意不是每个方法都支持异步的，对于不支持异步的即使用async它也不是异步，
比如下面的asyncio是异步（如果要看出异步效果，可以把sleep时间延长，然后多个请求就可以看出来了。），可是time.sleep方法就不是异步。

http://127.0.0.1:9000/goodbye/lucy （注意现在的代码还没有处理lucy后面有/的情况。）  显示goodbye lucy
http://127.0.0.1:9000/hello/lucy  显示 hello lucy
'''

import asyncio
from aiohttp import web

async def goodbye(request):
    await asyncio.sleep(0.5)
    text = '<h1>goodbye, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'), content_type='text/html')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'), content_type='text/html')

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/goodbye/{name}', goodbye)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    print('Server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()