from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS
 
 
class EchoClientProtocol(WebSocketClientProtocol):
 
   def sendHello(self):
      self.sendMessage("Hello, world!")
 
   def onOpen(self):
      self.sendHello()
 
   def onMessage(self, msg, binary):
      print "Got echo: " + msg
      reactor.callLater(1, self.sendHello)
 
 
if __name__ == '__main__':
 
   factory = WebSocketClientFactory("ws://mozart.kawigi.com:9000", debug = False)
   factory.protocol = EchoClientProtocol
   connectWS(factory)
   reactor.run()
