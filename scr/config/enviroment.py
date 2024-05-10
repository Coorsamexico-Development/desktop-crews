
from dotenv import load_dotenv
import os
class Enviroments:
    pusherAppId = os.environ['PUSHER_APP_ID']
    pusherAppkey = os.environ['PUSHER_APP_KEY']
    pusherCluster = os.environ['PUSHER_CLUSTER']
    pusherSecret = os.environ['PUSHER_SECRET']
    pusherMesa = os.environ['MESA']
    @staticmethod
    def init_environment():
        load_dotenv()



