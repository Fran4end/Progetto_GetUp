#!/usr/bin/python
# -*- coding:utf-8 -*-
from pickle import TRUE
import serial
import time
import json

ser = serial.Serial('/dev/ttyUSB2',115200)
ser.flushInput()

power_key = 6
rec_buff = ''
rec_buff2 = ''
time_count = 0

def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			return 0
		else:
			cord = rec_buff.decode().replace(back, '').replace('OK', '').replace(' ','').replace('\r\n','')
			#if ',,,,' not in cord:
			try:
				latitude = int(cord[0:2]) + ((float(cord[2:11]))/60);
				longitude = int(cord[14:17]) + ((float(cord[17:26]))/60);
				co = str(latitude) + ' ' + str(longitude)
				return 1, co
			except ValueError:
			#else:
				return 1, ',,,,,,'

def get_gps_position():
	answer = 0
	send_at('AT+CGPS=1,1','OK',1)
	time.sleep(0.5)

	answer, cord = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
	
	if 1 == answer:
		if ',,,,,,' in cord:
			print('GPS is not ready')
			time.sleep(1)
		else:
			return cord
	else:
		print('error %d'%answer)
		send_at('AT+CGPS=0','OK',1)
		return False

while True:
    info = get_gps_position()
    file = open('info.json', 'w')
    json.dump(info, file)
    file.close()
    time.sleep(0.2)

