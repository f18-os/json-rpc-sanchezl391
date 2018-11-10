# minimalistic server example from 
# https://github.com/seprich/py-bson-rpc/blob/master/README.md#quickstart

import socket
from bsonrpc import JSONRpc
from bsonrpc import request, service_class
from bsonrpc.exceptions import FramingError
from bsonrpc.framing import (
	JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)

dic = dict() # dictionary that will contain root

# Iterates through root's children and increases values
def recursiveIncrement(node):
	node['val'] += 1
	for child in node['children']:
		recursiveIncrement(child)

# Class providing functions for the client to use:
@service_class
class ServerServices(object):

  # handles making dictionary from string and returning updated 
  #   graph in string format
  @request
  def increment(self, graphStr):
    dic = eval(graphStr)
    recursiveIncrement(dic)
    return str(dic)

# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 50001))
ss.listen(10)

while True:
  s, _ = ss.accept()
  # JSONRpc object spawns internal thread to serve the connection.
  JSONRpc(s, ServerServices(),framing_cls=JSONFramingNone)
