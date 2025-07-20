import RPi.GPIO as gpio
import os
import glob
from time import sleep
import pymysql
from datetime import datetime
import time

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

luzVerde = 40
luzRoja = 38
Buzzer = 36

base_dir='/sys/bus/w1/devices/'
device_folder=glob.glob(base_dir + '28*')[0]
device_file=device_folder+'/w1_slave'

gpio.setup(luzVerde, gpio.OUT)
gpio.setup(luzRoja, gpio.OUT)
gpio.setup(Buzzer, gpio.OUT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

config = {
	'host': '82.197.82.133',
	'user': 'u670852162_Edaa',
	'password': 'Sonora2234',
	'database': 'u670852162_Edy_PIRMOTION',
	'port': 3306,
}

gpio.output(luzVerde, gpio.LOW)
gpio.output(luzRoja, gpio.LOW)
gpio.output(Buzzer, gpio.LOW)


class MYSQL:
    def Insert(self, Fecha, Hora, Estado, conexion):
        conector = conexion.cursor()
        try:
            sql = "INSERT INTO sumergible (id, Fecha, Hora, Temperatura) VALUES(%s, %s, %s, %s);"
            conector.execute(sql, (0, Fecha, Hora, Estado))
            conexion.commit() 
        except Exception as e:
            # Rollback in case of error
            conexion.rollback()
            print("Error Al Insertar ", e)
        finally:
            conector.close() 

    def showdata(self, Temp): 
        fecha = datetime.today().strftime('%d/%m/%Y')
        hora = datetime.today().strftime('%H:%M:%S')
        print(f'| {fecha} |  {hora}  | {Temp}   ')

def read_temp_raw():
	f = open(device_file,'r')
	lines=f.readlines()
	f.close()
	return lines
	
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		
		temp_c = float(temp_string)/1000.0
		temp_f= temp_c * 9.0 / 5.0 + 32.0
		
		return temp_c #, temp_f
		
print("\n")
print("                  TEMPERATURA           ")
print("---------------------------------------------------------")
print(" |   Fecha   |   Hora     | Temperatura  |")
print("--------------------------------------------------------")

		
try:
	conn = pymysql.connect(**config)
	BD = MYSQL()
	while True:
		temp = read_temp()
		if temp > 30:
			BD.showdata(temp)
			current_date = datetime.today().strftime('%Y-%m-%d')
			current_time = datetime.today().strftime('%H:%M:%S')
			BD.Insert(current_date, current_time, temp, conn)
			gpio.output(luzVerde, gpio.LOW)
			gpio.output(luzRoja, gpio.HIGH)
			gpio.output(Buzzer, gpio.LOW)
			sleep(0.3)
			gpio.output(luzRoja, gpio.LOW)
			gpio.output(Buzzer, gpio.HIGH)
			sleep(0.3)
		else:
			BD.showdata(temp)
			gpio.output(luzVerde, gpio.HIGH)
			gpio.output(Buzzer, gpio.LOW)
			gpio.output(luzRoja, gpio.LOW)
			sleep(1)
		sleep(1)
		
except KeyboardInterrupt:
	gpio.cleanup()
