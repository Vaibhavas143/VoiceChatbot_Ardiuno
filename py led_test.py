import serial
import time

# Connect to Arduino
arduino = serial.Serial('COM5', 9600)
time.sleep(2)

arduino.write(b'1')  # Turn LED on
time.sleep(5)
arduino.write(b'0')  # Turn LED off

arduino.close()      # Close the serial connection properly
