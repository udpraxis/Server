import serial
import time

loop = True
print("Initalizing Serial port...")
arduino = serial.Serial('/dev/cu.usbmodem1431', 9600,
                        timeout=1)  # 2=Com3 on windows always a good idea to sepcify a timeout incase we send bad data
time.sleep(2)  # wait for initialize
print("Initialization Complete")

while loop:
    command = b'0.19,0.19,0.19\n'

    arduino.write(command)

    time.sleep(1)
    


