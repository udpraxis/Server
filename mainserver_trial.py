__author__ = 'udlab'

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import serial
import time


#Server Initialization code
debugmode = False
loop = True


while loop:
    print(" Hello Darwin the Server will be starting soon")
    print(" please initialize certian parameters before running the server")
    print(" Setting the Server in debugmode? yes = y/Y or no  = n/N")
    x = input()
    print()

    if x == 'y' or x == 'Y':
        debugmode = True
        print("Server is running in a debugging mode")
        print(debugmode)
        loop = False
    elif x == 'n' or x == 'N':
        debugmode = False
        print("Server is in none debugging mode ")
        loop = False
    else:
        print("The answer is not acceptable")

time.sleep(1)

print()

# Server Side
class Server(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print(" clients are ", self.factory.clients)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        decodedata = bytes.decode(data, 'utf-8')
        a = decodedata.split(':')

        if debugmode:
            print(a)

        if len(a) > 1:
            datax = a[0]
            datay = a[1]
            dataz = a[2]

            print(datax)
            print(datay)
            print(dataz)


factory = Factory()
factory.clients = []
factory.protocol = Server
reactor.listenTCP(8000, factory)
time.sleep(0.5)
print("Darwin :server started")


reactor.run()
