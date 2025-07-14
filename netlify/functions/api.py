from serverless_wsgi import WsgiHandler
from system import app


handler = WsgiHandler(app)