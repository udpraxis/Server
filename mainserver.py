__author__ = 'udlab'


from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import serial
import time

#Initializing the arduino Connection in mac change /dev/cu.usbmodem1441 to apprioprate
#arduino = serial.Serial('/dev/cu.usbmodem1441', 9600)
#time.sleep(2)

#if the connection is based in linux then uncomment this part 
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

#Server Side
class Server(Protocol):
        command = " "
        def connectionMade(self):
            self.factory.clients.append(self)
            print(" clients are ", self.factory.clients)

        def connectionLost(self, reason):
            self.factory.clients.remove(self)

        def dataReceived(self, data):
            decodedata = bytes.decode(data,'utf-8')
            a = decodedata.split(':')

            print(a)

            if len(a) > 1:
                command = a[0]
                content = a[1]

                msg = ""
                if command == "iam":
                    self.name = content
                    msg = self.name + " has joined "
                    bytemsg = str.encode(msg)

                elif command == "msg":
                    msg = self.name + " : " + content
                    bytemsg = str.encode(msg)
                    stringCommand = content
                    self.devicecommand(stringCommand)


                for c in self.factory.clients:
                    c.message(msg)



        def message(self, message):
            # the transmission is in byte
            byteMessage = str.encode(message)
            self.transport.write(byteMessage)

        def devicecommand(self, message):
            msg = message
            inByte = b''

            if msg == "Red\r\n":
                inByte = b'1\n'
            elif msg == "NRed\r\n":
                inByte = b'-1\n'
            elif msg == "Blue\r\n":
                inByte = b'2\n'
            elif msg == "NBlue\r\n":
                inByte = b'-2\n'
            elif msg == "Green\r\n":
                inByte = b'3\n'
            elif msg == "NGreen\r\n":
               inByte = b'-3\n'
            else:
                print("there is no command")

            arduino.write(inByte)
            time.sleep(0.2)
            print(inByte)


factory = Factory()
factory.clients = []
factory.protocol = Server
reactor.listenTCP(8000, factory)
time.sleep(0.5)
print("Darwin :server started")
reactor.run()









