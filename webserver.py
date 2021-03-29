from aiohttp import web


app = web.Application()
web.run_app(app, host='0.0.0.0', port=8080)