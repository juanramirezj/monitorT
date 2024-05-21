import serial
import struct

# Open the serial port connection
ser = serial.Serial('/dev/ttyAMA0', 9600)  # Replace '/dev/ttyUSB0' with the appropriate port
eof = struct.pack('B', 0xff)

def display_text(field, text):
    command = f'{field}.txt="{text}"'
    ser.write(command.encode())
    ser.write(eof)
    ser.write(eof)
    ser.write(eof)
              
              
display_text('t1', 'DIO OK 22')


# Close the serial port connection
ser.close()