import RPi.GPIO as gpio
from time import sleep
import time
from datetime import datetime
import mysql.connector as mysql

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

trig = 8
echo = 10
buzzer = 12
red = 40
green = 38
blue = 36
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.setup(buzzer, gpio.OUT)

gpio.setup(red, gpio.OUT)
gpio.setup(green, gpio.OUT)
gpio.setup(blue, gpio.OUT)

gpio.output(red, gpio.LOW)
gpio.output(green, gpio.LOW)
gpio.output(blue, gpio.LOW)

class DatabaseMySQL:
    def insertdb(self, distancia):
        miConexion = mysql.connect(user='root', password='1234', host='localhost', db='sensores')
        cur = miConexion.cursor()
        sql = "INSERT INTO ultrasonico(id, fecha, hora, distancia) VALUES (%s, %s, %s, %s)"
        val = (0, datetime.today().strftime('%Y-%m-%d'), datetime.today().strftime('%H:%M:%S'), distancia)
        cur.execute(sql, val)
        miConexion.commit()
        miConexion.close()
        
    def showdata(self, distancia):
        Fecha = datetime.today().strftime('%d/%m/%Y')
        Hora = datetime.today().strftime('%H:%M:%S')
        Distancia = distancia
        print('|   ' , Fecha, '|', Hora, '      |', Distancia, '           |')

print("\n")
print("                  Sensor de distancia                ")
print("-----------------------------------------------------")
print("|     Fecha     |      Hora      |     Distancia    |")
print("-----------------------------------------------------")

try:
	while True:
		gpio.output(trig, gpio.LOW)
		sleep(0.5)
		
		gpio.output(trig, gpio.HIGH)
		sleep(0.00001)
		gpio.output(trig, gpio.LOW)
		
		inicio = time.time()
		while gpio.input(echo) == 0:
			inicio = time.time()
		
		while gpio.input(echo) == 1:
			final = time.time()
			
		tiempo_transcurrido = final-inicio
		duracion = tiempo_transcurrido*34000
		distancia = round(duracion/2,2)
		
		DatabaseMySQL().showdata(distancia)
		if distancia >= 0 and distancia <= 5:
			#encender luz magenta aqui
			gpio.output(red, gpio.HIGH)
			gpio.output(green, gpio.LOW)
			gpio.output(blue, gpio.HIGH)
			DatabaseMySQL().insertdb(distancia)
		elif distancia >=6 and distancia <= 10:
			#encender luz cian
			gpio.output(red, gpio.LOW)
			gpio.output(green, gpio.HIGH)
			gpio.output(blue, gpio.HIGH)
		elif distancia >=11 and distancia <= 15:
			#encender luz blanco
			gpio.output(red, gpio.HIGH)
			gpio.output(green, gpio.HIGH)
			gpio.output(blue, gpio.HIGH)
			DatabaseMySQL().insertdb(distancia)
		elif distancia >=16 and distancia <= 20:
			#encender luz verde
			gpio.output(red, gpio.LOW)
			gpio.output(green, gpio.HIGH)
			gpio.output(blue, gpio.LOW)
			
		elif distancia >=21 and distancia <= 25:
			#encender luz azul 
			gpio.output(red, gpio.LOW)
			gpio.output(green, gpio.LOW)
			gpio.output(blue, gpio.HIGH)
			DatabaseMySQL().insertdb(distancia)
		elif distancia >=26:
			#gpio.output(red, gpio.HIGH)
			#gpio.output(green, gpio.LOW)
			#gpio.output(blue, gpio.LOW)
			gpio.output(buzzer,gpio.HIGH)
		sleep(1)

except KeyboardInterrupt:
	gpio.cleanup()
