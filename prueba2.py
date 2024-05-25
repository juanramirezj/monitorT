from influxdb import InfluxDBClient
import serial
import struct
import time
from datetime import datetime
import pytz
import random

# Open the serial port connection
ser = serial.Serial('/dev/ttyAMA0', 9600)  # Replace /dev/ttyUSB0 with the appropriate port
eof = struct.pack('B', 0xff)

# InfluxDB connection details
host = '192.168.0.236'
port = 8086
username = 'dba'
password = 'supremo'
database = 'sensors'
client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

cred = 63488
cwhite = 65535
cgreen = 2016
cblack = 0
cblue = 31
cyellow = 65504
ccyan = 34815
cmagenta = 63519
corange = 64480
cpurple = 49152
cpink = 65280
cgray = 33840
cbrown = 48192
clightblue = 2047
clime = 2016
cdarkgreen = 480
cteal = 2047
cnavy = 31
cgold = 64480
csilver = 33840
cindigo = 31
colive = 480
cmaroon = 48192
caqua = 34815
ccoral = 64480
csalmon = 65280
cviolet = 49152
ctan = 33840
corchid = 63519
cslategray = 33840
cturquoise = 34815
cchocolate = 48192
cplum = 49152
cdarkslategray = 33840
ccrimson = 63488
cdarkorange = 64480
cperu = 48192
cdarkviolet = 49152

color_pairs = [
    (cred, cwhite),
    (cgreen, cblack),
    (cblue, cyellow),
    (ccyan, cmagenta),
    (corange, cpurple),
    (cpink, cgray),
    (cbrown, clightblue),
    (clime, cdarkgreen),
    (cteal, cnavy),
    (cgold, csilver),
    (cindigo, colive),
    (cmaroon, caqua),
    (ccoral, csalmon),
    (cviolet, ctan),
    (cnavy, cgray),
    (corchid, cslategray),
    (cturquoise, cchocolate),
    (cplum, cdarkslategray),
    (ccrimson, cdarkorange),
    (cperu, cdarkviolet)
]




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
    
    # TEMPERATURE
    try:
        result = client.query(query)
    except Exception as e:
        print(f"An error occurred while querying InfluxDB: {e}")
    # print(result)

    # Extract the last value from the result
    last_date = list(result.get_points())[0]['time']
     
    # Convert last_date to the desired format
    last_date = convert_rfc3339_to_custom_format(last_date)     
    last_value = list(result.get_points())[0]['last_value']
    
    # print(flast_date = {last_date})
    # print(flast_value = {last_value})
    # Convert last_value to string with 1 decimal and append "C"
    last_value = "{:.1f}".format(last_value)
    
      
    # Return the last value
    return last_date, last_value

def display_text(field, text, fore, back):
    command = f'{field}.txt="{text}"'
    # print(f'Command={command}')
    ser.write(command.encode())
    ser.write(eof)
    ser.write(eof)
    ser.write(eof)
    
    # Assign random foreground and background colors from color_pairs
    command = f'{field}.bco={back}'
    # print(fCommand={command})
    ser.write(command.encode())
    ser.write(eof)
    ser.write(eof)
    ser.write(eof)
    
    command = f'{field}.pco={fore}'
    # print(fCommand={command})
    ser.write(command.encode())
    ser.write(eof)
    ser.write(eof)
    ser.write(eof)

    
def display_ht(room, hourfield, hourvalue, temperaturefield, temperaturevalue, humfield, humvalue ):
    fore,back = (cwhite, cblack)
    display_text(hourfield, room+" "+hourvalue, fore, back)
    
    fore,back = random.choice(color_pairs)  
    display_text(temperaturefield, temperaturevalue+"C", fore, back)
    
    fore,back = random.choice(color_pairs)  
    display_text(humfield, humvalue+"%", fore, back)

    
# Measurement details
mtpiezajuan = 'monitoring/vecinal/rbpico/piezajuan/temperaturaC'
mtescalera = 'monitoring/vecinal/rbpico/escalera/temperaturaC'
mtliving = 'monitoring/vecinal/rbpico/living/temperaturaC'
mtpiezamami = 'monitoring/vecinal/rbpico/piezamami/temperaturaC'
mtventana = 'monitoring/vecinal/rbpico/ventana/temperaturaC'

mhpiezajuan = 'monitoring/vecinal/rbpico/piezajuan/humedad'
mhescalera = 'monitoring/vecinal/rbpico/escalera/humedad'
mhliving = 'monitoring/vecinal/rbpico/living/humedad'
mhpiezamami = 'monitoring/vecinal/rbpico/piezamami/humedad'
mhventana = 'monitoring/vecinal/rbpico/ventana/humedad'

while True:
    hpiezajuan, tpiezajuan = get_last_value(mtpiezajuan)
    hescalera, tescalera  = get_last_value(mtescalera)
    hliving, tliving = get_last_value(mtliving)
    hpiezamami,tpiezamami = get_last_value(mtpiezamami)
    hventana, tventana = get_last_value(mtventana)
    
    _ , humpiezajuan = get_last_value(mhpiezajuan)
    _ , humescalera  = get_last_value(mhescalera)
    _ , humliving = get_last_value(mhliving)
    _ , humpiezamami = get_last_value(mhpiezamami)
    _ , humventana = get_last_value(mhventana)

    
    if False:
        print(f'Pieza juan: {hpiezajuan}:  {tpiezajuan}°C')
        print(f'Escalera: {hescalera}:  {tescalera}°C')
        print(f'Living: {hliving}:  {tliving}')
        print(f'Pieza mami {hpiezamami}:  {tpiezamami}')
        print(f'Ventana: {hventana}:  {tventana}')

    display_ht('Pieza Juan', 'hpiezajuan', hpiezajuan, 'tpiezajuan', tpiezajuan, 'humpiezajuan', humpiezajuan)
    display_ht('Escalera', 'hescalera', hescalera, 'tescalera', tescalera, 'humescalera', humescalera )
    display_ht('Living', 'hliving', hliving, 'tliving', tliving, 'humliving', humliving )
    display_ht('Pieza mami','hpiezamami', hpiezamami, 'tpiezamami', tpiezamami, 'humpiezamami', humpiezamami)
    display_ht('Ventana', 'hventana', hventana, 'tventana', tventana, 'humventana', humventana )

    time.sleep(60)
# Close the serial port connection


ser.close()
