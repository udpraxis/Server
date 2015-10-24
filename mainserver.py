__author__ = 'udlab'

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import serial
import time


# Server Initialization code
debugmode = False
loop = True
device_configured = True

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


class deviceConnection():
    def connectionConfigure(self, nameoftheport, baudrate=int, timeout=int):
        configure_now = True

        while configure_now:

            print("Connecting Device in serial port...")
            try:
                # Initializing the arduino Connection in mac change /dev/cu.usbmodem1441 to apprioprate '/dev/cu.usbmodem1431'
                self.connected(nameoftheport,baudrate,timeout)
                # time.sleep(2)
                # arduino = serial.Serial('/dev/ttyACM0', 9600)
                time.sleep(2)
                print("Arduino initialization Complete")
                return device_configured = True
                configure_now = False
                print()
            except:
                print("The Arduino could not be connected!")
                print("1.This could be due to another serialCommunication is busy with Arduino")
                print("2.The Arduino is not connect to the given USB Port")
                print()

                # Configure Arduino later
                print("Do you want to connect the device now?")
                x_1 = input()
                if x_1 == 'y' or x_1 == 'Y':
                    print("Connect the Device to the server")

                    print("Reconnect by pressing c ")
                    connect_now = input()
                    if connect_now == 'c' or connect_now == 'C':
                        pass

                if x_1 == 'n' or x_1 == 'N':
                    device_configured = False
                    configure_now = False

    print()

    def connected(self, nameoftheport, baud, timeout):
        return serial.Serial(nameoftheport, baud, timeout)


# while configure_now:
#     print("Connecting Device in serial port...")
#     try:
#         # Initializing the arduino Connection in mac change /dev/cu.usbmodem1441 to apprioprate '/dev/cu.usbmodem1431'
#         device_connected = serial.Serial('/dev/cu.usbmodem1431', 9600, timeout=1) #timeout is important action
#         # time.sleep(2)
#         # arduino = serial.Serial('/dev/ttyACM0', 9600)
#         time.sleep(2)
#         print("Arduino initialization Complete")
#         device_configured = True
#         configure_now = False
#         print()
#     except:
#         print("The Arduino could not be connected!")
#         print("1.This could be due to another serialCommunication is busy with Arduino")
#         print("2.The Arduino is not connect to the given USB Port")
#         print()
#
#         #Configure Arduino later
#         print("Do you want to connect the device now?")
#         x_1 = input()
#         if x_1 == 'y' or x_1 == 'Y':
#             print("Connect the Device to the server")
#
#             print("Reconnect by pressing c ")
#             connect_now = input()
#             if connect_now == 'c' or connect_now == 'C':
#                 connect_now = True
#
#         if x_1 == 'n' or x_1 == 'N':
#             device_configured = False
#             configure_now = False
#
#
# print()



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

            elif command == "configure":
                pass

            for c in self.factory.clients:
                c.message(msg)

    def message(self, message):
        # the transmission is in byte
        byteMessage = str.encode(message)
        self.transport.write(byteMessage)

    def devicecommand(self, message):
        if device_configured:
            devicemsg = deviceConnected_sent_msg()
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

            device_connected.write(inByte)
            time.sleep(0.2)
            devicemsg.device_send_msg()
            time.sleep(.2)
        else:
            print("The Device is not properly configured")
            self.message("The Server is not configured properly to the server")
            print("Do you want to reconfigure the server to the device?")
            nameoftheport = input("Name of the port ")
            s_baudrate = input("What is the baudrate")
            baudrate = s_baudrate.encode('utf-8')
            print(int(baudrate))
            s_timeout = input("What is the timeout?")
            timeout = s_timeout.encode('utf-8')
            print(int(timeout))


class deviceConnected_sent_msg():
    def device_send_msg(self):

        if debugmode:
            print("Iam currently in the waiting for device send msg function")

        devicemsg_byte = device_connected.readline()

        if debugmode:
            print("msg from device is read")
            print("This is the msg:", devicemsg_byte)

        devicemsg_string = str(devicemsg_byte.decode('utf-8'))
        print(devicemsg_string)


port = '/dev/cu.usbmodem1431'
baud = 9600
timeout = 1

factory = Factory()
factory.clients = []
factory.protocol = Server
reactor.listenTCP(8000, factory)
time.sleep(0.5)
print("Darwin :server started")

if debugmode:
    print("Device is connected", device_configured)

reactor.run()
