import RPi.GPIO as gpio
import pymysql
import time
from time import sleep
from datetime import datetime
import mysql.connector as mysql
import yagmail

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

pirM = 40
ledR = 38
ledV = 36

gpio.setup(pirM, gpio.IN)
gpio.setup(ledV, gpio.OUT)
gpio.setup(ledR, gpio.OUT)


config = {
	'host': '82.197.82.133',
	'user': 'u670852162_Edaa',
	'password': 'Sonora2234',
	'database': 'u670852162_Edy_PIRMOTION',
	'port': 3306,
}

class MYSQL:

    def Insert(self, Fecha, Hora, Estado, conexion):
        conector = conexion.cursor()
        try:
            conector.execute(f"INSERT INTO PirMotion VALUES(0, '{Fecha}', '{Hora}', {Estado});")
            # print(f"Insertado correctamente")
        except  Exception as e:
            print("Error Al Insertar ", e)
    
    def showdata(self, luz):
	    fecha = datetime.today().strftime('%d/%m/%Y')
	    hora =  datetime.today().strftime('%H:%M:%S')
	    print('|', fecha, '|', hora, '|', 'NO HAY MOVIMIENTO')
    
    def showdataM(self, luz):
	    fecha = datetime.today().strftime('%d/%m/%Y')
	    hora =  datetime.today().strftime('%H:%M:%S')
	    print('|', fecha, '|', hora, '|', 'MOVIMIENTO DETECTADO!')


print("\n")
print("         MOVIMIENTO          ")
print("------------------------------")
print(" |  Fecha   |   Hora    | Movimiento  |")
print("------------------------------")





try:
	while True:
		Estado = gpio.input(pirM)
		start = time.time()
		conn = pymysql.connect(**config)

		BD = MYSQL()
		
		fecha = datetime.today().strftime('%d/%m/%Y')
		hora =  datetime.today().strftime('%H:%M:%S')
		
		if Estado == 1:
			BD.showdataM(Estado)
			BD.Insert(datetime.today().strftime('%Y-%m-%d'), datetime.today().strftime('%H:%M:%S'),Estado, conn)
			gpio.output(ledR, gpio.HIGH)
			gpio.output(ledV, gpio.LOW)
			conn.commit()
			try:
			    yag = yagmail.SMTP(user='edyparrautslrc@gmail.com',password='wydq kfke qxlx xprw')
			    yag.send(to = 'edyparra0@gmail.com', subject = 'Monitoreo de Presencia - Edy Parra TI5-3', contents = f'Se ha detectado movimiento el {fecha} a las {hora}')
			    print("Correo enviado exitosamente")
	

			except Exception as e:
			    print(f"Error, correo no se envio", e)
		else:
		    BD.showdata(Estado)
		    gpio.output(ledR, gpio.LOW)
		    gpio.output(ledV, gpio.HIGH)
		sleep(1)

		
except KeyboardInterrupt:
	gpio.cleanup()
