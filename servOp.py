# -*- coding: utf-8 -*-
import requests
import RPi.GPIO as GPIO
import time
import bluetooth
import sys
GPIO.setwarnings(False)
hostMACAddress = 'b8:27:eb:d0:dd:86' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
#time.sleep.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(7,GPIO.OUT)

p = GPIO.PWM(7,50)
p.start(7.5) #выствляем в  исходно  положение лепесток

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data) # Echo back to client
            rp = data.encode("ascii") # отправим методо POST параметр z, равный 555
			      print(sys.version_info) # запрашиваем версию
			      response = requests.POST('url', data=rp)
			      html = response.text.decode("utf-8") # utf-8 чтобы принять русские буквы
			if (html==true):
				print("open the door") 
				p.ChangeDutyCycle(1.5) #если ответ  с сервера тру то поворачиваем серво на 90  градусов
				time.sleep(1)# ДАТЧик движения не тестил,но впринципе он вроде не сложно работает, его можно прикрутить
def RCtome(RCpin):    #датчик  движения, который  по идее будет закрывать дверцу ,после того как  единица сменится на ноль в  датчике
	GPIO.setmode(GPIO.BCM)#BCM -pin 16
	GPIO.setup(RCpin,GPIO.IN)
	GPIO.wait_for_edge(RCpin,GPIO.FALLING)
	signal = 1
	while(signal==true):
		signal=GPIO.input(RCpin)
		p.ChangeDuttyCycle(0.5)
		

GPIO.cleanup()
except:	
    print("Closing socket")
    client.close()
    s.close()
