import serial
import time

print("Initalizing Serial port...")
arduino = serial.Serial('/dev/cu.usbmodem1431', 9600,
                        timeout=1)  # 2=Com3 on windows always a good idea to sepcify a timeout incase we send bad data
time.sleep(2)  # wait for initialize
print("Initialization Complete")

command = b'1\n'

arduino.write(command)

time.sleep(0.2)



devicemsg = arduino.readlines()
currentCondition = devicemsg[1]
print(type(currentCondition))
print(str(currentCondition.decode('utf-8')))
print(currentCondition)
