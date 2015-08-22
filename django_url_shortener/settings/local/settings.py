import redisco

from god.common_settings import *
DEBUG = True

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
redisco.connectionsetup(host=REDIS_HOST, port=REDIS_PORT, db=0)
