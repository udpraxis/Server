__author__ = 'Darwin Subramaniam'


import serial
import time

class Udarduino:

    #function to make connection to the Arduino
    def connectserial(self, usbport, baud, timeout, sleeptime=int, debugmode=bool):
        try:
            arduino = serial.Serial(usbport, baud, timeout=timeout)
            time.sleep(sleeptime)
            if debugmode:
                print("The Arduino is connected")
        except:
            print("The Arduino could not be connect")
            print("1.This could be due to another serialCommunication is busy with Arduino")
            print("2.The Arduino is not connect to the given USB Port")

    #This function should deal with all the read function available in the pyserial library
    def recieve_messages_from_arduino(self, msgtype_byte1_string2 = int , lines1_line2_certainlength3 = int, iflength= int):
