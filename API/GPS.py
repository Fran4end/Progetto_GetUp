#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

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
			cord = rec_buff.decode().replace(back, '').replace('OK', '').replace(' ','')#.replace('\r\n','')
			co=',,,,,,'
			if ',,,,,,' not in cord:	
				inputDegrees = int(cord[2:4]);
				inputMinutes = float(cord[4:13]);
				latitude = inputDegrees + (inputMinutes/60);
				inputDegrees = int(cord[16:19]);
				inputMinutes = float(cord[19:28]);
				longitude = inputDegrees + (inputMinutes/60);
				co = str(latitude) + ' ' + str(longitude)
				return 1, co
			else:
				return 0

def get_gps_position():
	rec_null = True
	answer = 0
	rec_buff = ''
	send_at('AT+CGPS=1,1','OK',1)
	time.sleep(2)
	while rec_null:
		answer, cord = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
		if 1 == answer:
			answer = 0
			if ',,' in cord:
				print('GPS is not ready')
				time.sleep(1)
			else:
				return cord
		else:
			print('error %d'%answer)
			rec_buff = ''
			send_at('AT+CGPS=0','OK',1)
			return False
		time.sleep(1.5)

info = get_gps_position()
file = open('info.json', 'w')
json.dump(info, file)
file.close()
print(get_gps_position())
