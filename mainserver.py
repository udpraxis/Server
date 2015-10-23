__author__ = 'udlab'


from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import serial
import time

#Initializing the arduino Connection in mac change /dev/cu.usbmodem1441 to apprioprate
#arduino = serial.Serial('/dev/cu.usbmodem1441', 9600)
#time.sleep(2)

debugmode = False
loop = True
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



#if the connection is based in linux then uncomment this part
print()
print("Initalizing Serial port...")
try:
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)
    print ("Arduino initialization Complete")
    print()
except:
    print("The Arduino could not be connected!")
    print("1.This could be due to another serialCommunication is busy with Arduino")
    print("2.The Arduino is not connect to the given USB Port")
    print()


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

        def device_send_msg(self):
            seq = []

            for c in arduino.read():
                seq.append(c)

                if(c == '\n'):
                    self.message(seq)
                    print(seq)




factory = Factory()
factory.clients = []
factory.protocol = Server
reactor.listenTCP(8000, factory)
time.sleep(0.5)
print("Darwin :server started")
reactor.run()









