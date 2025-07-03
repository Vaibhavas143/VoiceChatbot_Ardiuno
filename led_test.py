import serial
import time

# Make sure the correct COM port is selected
arduino = serial.Serial('COM5', 9600)
time.sleep(2)  # Let Arduino initialize

while True:
    cmd = input("Type 1 to turn ON LED, 0 to turn OFF: ").strip()
    if cmd == '1' or cmd == '0':
        arduino.write(cmd.encode())
        print(f"Sent: {cmd}")
    else:
        print("Invalid input. Type 1 or 0.")
