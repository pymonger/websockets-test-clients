import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList
from autobahn.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampClientProtocol
 
 
class SimpleClientProtocol(WampClientProtocol):
   """
   Demonstrates simple Remote Procedure Calls (RPC) with
   Autobahn WebSockets and Twisted Deferreds.
   """
 
   def show(self, result):
      print "SUCCESS:", result
 
   def logerror(self, e):
      erroruri, errodesc, errordetails = e.value.args
      print "ERROR: %s ('%s') - %s" % (erroruri, errodesc, errordetails)
 
   def done(self, *args):
      self.sendClose()
      reactor.stop()
 
   def onSessionOpen(self):
 
      self.prefix("calc", "http://example.com/simple/calc#")
 
      d1 = self.call("calc:square", 23).addCallback(self.show)
 
      d2 = self.call("calc:add", 23, 7).addCallback(self.show)
 
      d3 = self.call("calc:sum", [1, 2, 3, 4, 5]).addCallback(self.show)
 
      d4 = self.call("calc:square", 23).addCallback(lambda res: \
                         self.call("calc:sqrt", res)).addCallback(self.show)
 
      d5 = self.call("calc:sqrt", -1).addCallbacks(self.show,
                                                   self.logerror)
 
      d6 = self.call("calc:square", 1001).addCallbacks(self.show,
                                                       self.logerror)
 
      d7 = self.call("calc:asum", [1, 2, 3]).addCallback(self.show)
 
      d8 = self.call("calc:sum", [4, 5, 6]).addCallback(self.show)
 
      d9 = self.call("calc:pickySum", range(0, 30)).addCallbacks(self.show,
                                                                 self.logerror)
 
      ## we want to shutdown the client exactly when all deferreds are finished
      DeferredList([d1, d2, d3, d4, d5, d6, d7, d8, d9]).addCallback(self.done)
 
 
if __name__ == '__main__':
 
   log.startLogging(sys.stdout)
   factory = WampClientFactory("ws://mozart.kawigi.com:9000", debugWamp = True)
   factory.protocol = SimpleClientProtocol
   connectWS(factory)
   reactor.run()
