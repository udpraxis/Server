import  serial
import time

print("Initalizing Serial port...")
arduino = serial.Serial('/dev/cu.usbmodem1441',9600,timeout = 1) # 2=Com3 on windows always a good idea to sepcify a timeout incase we send bad data
time.sleep(2) #wait for initialize
print ("Initialization Complete")

command = b'1\n'
print(command)
print(type(command))

arduino.write(command)

time.sleep(2)
arduino.write(b'-1\n')