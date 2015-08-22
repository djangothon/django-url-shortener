from god.common_settings import *
DEBUG = True

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DATA_CONNECTION_URL = "redis://{host}:{port}".format(
        host=REDIS_HOST,
        port=REDIS_PORT)
