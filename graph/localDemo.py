# minimalistic client example from 
# https://github.com/seprich/py-bson-rpc/blob/master/README.md#quickstart

import socket
from bsonrpc import JSONRpc
from bsonrpc.exceptions import FramingError
from bsonrpc.framing import (
	JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)
from node import *
import json

# Cut-the-corners TCP Client:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50001))

rpc = JSONRpc(s,framing_cls=JSONFramingNone)
server = rpc.get_peer_proxy()

def recursiveUpdateRoot(rootStrObj, root):
	# update node value
	root.val = rootStrObj["val"]
	# iterate through children to update value
	for index, child in enumerate(root.children):
		recursiveUpdateRoot( rootStrObj["children"][index], child )

# Client Node demo
leaf1 = node("leaf1")
leaf2 = node("leaf2")

root = node("root", [leaf1, leaf2])

print("graph before increment:")
root.show()
print("\n")

rootStr = str(root) # make dict str out of dict/ class obj
rootStr = server.increment(rootStr)

rootStrObj = eval(rootStr) # evaluate str as python dict
recursiveUpdateRoot(rootStrObj, root) # update root w/ new values
print("graph after increment:")
root.show()

rpc.close() # Closes the socket 's' also