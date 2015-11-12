__author__ = 'udlab'
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import time
import RPi.GPIO as GPIO

#Server Initialization code
debugmode = False
loop = True
device_configured = bool
configure_now = True

GPIO.setmode(GPIO.BCM)



while loop:
    print("Hello Im the Tcp Client")
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

class Server(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print(" clients are ", self.factory.clients)


    def dataReceived(self, data):
        decodedata = bytes.decode(data, 'utf-8')
        a = decodedata.split(':')


        if len(a) > 1:
            dataX = a[0]
            dataY = a[1]
            dataZ = a[2]


    def message(self, message):
        # the transmission is in byte
        byteMessage = str.encode(message)
        self.transport.write(byteMessage)

    def dataAction(self,dataX,dataY,dataZ):



factory = Factory()
factory.clients = []
factory.protocol = Server
reactor.listenTCP(8000, factory)
time.sleep(0.5)
print("Darwin :server started")
reactor.run()