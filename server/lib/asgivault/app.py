import colorlog
import logging
import falcon.asgi
import getpass
import base64
import os

from ..crypto import encrypt_string_aes_256, decrypt_aes_256_cbc

# Utilities
def envget(key, default):
    tmp = os.environ.get(key, default=default)
    if tmp == "":
        return default
    return tmp

def clogger(name):
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
    '%(asctime)-15s %(log_color)s%(levelname)s:%(name)s:%(message)s'))

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)

    log_level = os.environ.get('STATION_LOG_LEVEL', default='INFO')
    if log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)

    return logger

logger = clogger(__name__)

def load_docker_secret(name):
    """Load a docker secret, registered as an ENV variable, from the filesystem."""
    location = os.environ.get(name, default=None)
    if not location or not os.path.exists(location):
        logger.warning(f"Could not find docker secret {name} at {location}")
        return None
    
    with open(location, 'r') as f:
        logger.info(f"Loaded docker secret {name}")
        tmp =  f.read().strip()
        if tmp.endswith('\n'):
            tmp = tmp[:-1]
        return tmp

password = load_docker_secret('ROOT_KEY') 

class EncryptResource:
    async def on_post(self, req, resp):
        """Handles GET requests"""
        data = await req.get_media()
        to_encrypt = data['to_encrypt']

        if not 'to_encrypt' in data:
            resp.status = falcon.HTTP_400
            resp.text = 'Bad Request'
            return

        resp.media = {
            "encrypted_string": base64.b64encode(encrypt_string_aes_256(to_encrypt, password)).decode()
        }

class DecryptResource:
    async def on_post(self, req, resp):
        print("on_post")
        print(req.params)
        """Handles GET requests"""
        data = await req.get_media()
        print(data)
        print(req.params)

        if not 'to_decrypt' in data:
            resp.status = falcon.HTTP_400
            resp.text = 'Bad Request'
            return

        to_decrypt = data['to_decrypt']

        resp.status = falcon.HTTP_200
        resp.media = {
            "raw_string": decrypt_aes_256_cbc(base64.b64decode(to_decrypt), password)        
        }

app = falcon.asgi.App(cors_enable=True)
app.add_route('/encrypt', EncryptResource())
app.add_route('/decrypt', DecryptResource())

#pip install httpie
#http POST http://localhost:8000/encrypt to_encrypt="John Doe"
#http POST http://localhost:8000/encrypt to_decrypt="bE0maisgTUmMijz+k0WoPWbxPUVVy8H39FUmVRPFHuC7WLM2pfDdn8NUVJRPqafH" # Jhon Doe with pwd="e"

# uvicorn asgivault.app:app