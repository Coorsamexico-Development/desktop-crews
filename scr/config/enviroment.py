
from dotenv import load_dotenv, dotenv_values
import os
class Enviroments:
    
    pusherAppId = ''
    pusherAppkey = ''
    pusherCluster = ''
    pusherSecret = ''
    pusherMesa = ''
    @staticmethod
    def init_environment():
        load_dotenv()
        config = dotenv_values(".env")
        Enviroments.pusherAppId = config['PUSHER_APP_ID']
        Enviroments.pusherAppkey = config['PUSHER_APP_KEY']
        Enviroments.pusherCluster = config['PUSHER_CLUSTER']
        Enviroments.pusherSecret = config['PUSHER_SECRET']
        Enviroments.pusherMesa = config['MESA']


    



