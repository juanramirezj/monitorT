from influxdb import InfluxDBClient
import serial
import struct
import time
from datetime import datetime
import pytz

# Open the serial port connection
ser = serial.Serial('/dev/ttyAMA0', 9600)  # Replace '/dev/ttyUSB0' with the appropriate port
eof = struct.pack('B', 0xff)

# InfluxDB connection details
host = '192.168.0.236'
port = 8086
username = 'dba'
password = 'supremo'
database = 'sensors'
client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

def convert_rfc3339_to_custom_format(rfc3339_date_str):
    # Parse the RFC3339 date string
    dt = datetime.fromisoformat(rfc3339_date_str.replace('Z', '+00:00'))
    
    # Define the target timezone
    target_timezone = pytz.timezone('America/Santiago')
    
    # Convert to the target timezone
    dt_santiago = dt.astimezone(target_timezone)
    
    # Format the date in the desired format "DD-MM-YYYY HH:MM:SS"
    formatted_date = dt_santiago.strftime("%d-%m-%Y %H:%M:%S")
    
    return formatted_date


def get_last_value(measurement):
    # Connect to InfluxDB

    # Query the last value from the measurement
    query = f'SELECT last(*) FROM "{measurement}"'
    query = query + " tz('America/Santiago')"
    # print(f'Query={query}')
    result = client.query(query)
    # print(result)

    # Extract the last value from the result
    last_date = list(result.get_points())[0]['time']
     
    # Convert last_date to the desired format
    last_date = convert_rfc3339_to_custom_format(last_date)
      
    last_value = list(result.get_points())[0]['last_value']
    
    # print(f'last_date = {last_date}')
    # print(f'last_value = {last_value}')
    # Convert last_value to string with 1 decimal and append "C"
    last_value = "{:.1f} C".format(last_value)
    # Return the last value
    return last_date, last_value

def display_text(field, text):
    command = f'{field}.txt="{text}"'
    # print(f'Command={command}')
    ser.write(command.encode())
    ser.write(eof)
    ser.write(eof)
    ser.write(eof)
    
def display_ht(room, hourfield, hourvalue, temperaturefield, temperaturevalue ):
    display_text(hourfield, room+" "+hourvalue)
    display_text(temperaturefield, temperaturevalue)

    
# Measurement details
mtpiezajuan = 'monitoring/vecinal/rbpico/piezajuan/temperaturaC'
mtescalera = 'monitoring/vecinal/rbpico/escalera/temperaturaC'
mtliving = 'monitoring/vecinal/rbpico/living/temperaturaC'
mtpiezamami = 'monitoring/vecinal/rbpico/piezamami/temperaturaC'
mtventana = 'monitoring/vecinal/rbpico/ventana/temperaturaC'

while True:
    hpiezajuan, tpiezajuan = get_last_value(mtpiezajuan)
    hescalera, tescalera = get_last_value(mtescalera)
    hliving, tliving = get_last_value(mtliving)
    hpiezamami,tpiezamami = get_last_value(mtpiezamami)
    hventana, tventana = get_last_value(mtventana)

    if False:
        print(f'Pieza juan: {hpiezajuan}:  {tpiezajuan}°C')
        print(f'Escalera: {hescalera}:  {tescalera}°C')
        print(f'Living: {hliving}:  {tliving}')
        print(f'Pieza mami {hpiezamami}:  {tpiezamami}')
        print(f'Ventana: {hventana}:  {tventana}')

    display_ht('Pieza Juan', 'hpiezajuan', hpiezajuan, 'tpiezajuan', tpiezajuan)
    display_ht('Escalera', 'hescalera', hescalera, 'tescalera', tescalera)
    display_ht('Living', 'hliving', hliving, 'tliving', tliving)
    display_ht('Pieza mami','hpiezamami', hpiezamami, 'tpiezamami', tpiezamami)
    display_ht('Ventana', 'hventana', hventana, 'tventana', tventana)

    time.sleep(60)
# Close the serial port connection


ser.close()