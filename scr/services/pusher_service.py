from typing import Callable, Union
import pysher
import pusher
import sys

# Add a logging handler so we can see the raw communication data
import logging

from scr.config.enviroment import Enviroments

class PusherService: 
  _pusher_server = None
  _pusher_client = None

  def __init__(self, 
                onConnect: Callable
                ):
      self.onConnect = onConnect
      root = logging.getLogger()
      root.setLevel(logging.INFO)
      ch = logging.StreamHandler(sys.stdout)
      root.addHandler(ch)

      self._pusher_server = pysher.Pusher( key=Enviroments.pusherAppkey, 
                                          cluster=Enviroments.pusherCluster, 
                                          secret=Enviroments.pusherCluster)
      self._pusher_client = pusher.Pusher(app_id=Enviroments.pusherAppId,
                                          key=Enviroments.pusherAppkey,
                                          secret=Enviroments.pusherSecret,
                                          cluster=Enviroments.pusherCluster)

      self._pusher_server.connection.bind('pusher:connection_established', self.connect_handler)
      self._pusher_server.connect()

  # We can't subscribe until we've connected, so we use a callback handler
  # to subscribe when able
  def connect_handler(self,_):
    self.onConnect(self)
  

  def channel(self, channelName:str):
    channel = self._pusher_server.subscribe(channelName)
    return channel

  def trigger(self, channelName:str, event:str, data:Union[dict,str]):
    self._pusher_client.trigger(channelName, event, data)






    