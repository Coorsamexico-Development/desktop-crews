
from dotenv import load_dotenv
import os
class Enviroments:
    
    @staticmethod
    def init_environment():
        load_dotenv()


    def __init__(self):
        
        self.pusherAppId = os.environ['PUSHER_APP_ID']
        self.pusherAppkey = os.environ['PUSHER_APP_KEY']
        self.pusherCluster = os.environ['PUSHER_CLUSTER']
        self.pusherSecret = os.environ['PUSHER_SECRET']
        self.pusherMesa = os.environ['MESA']



