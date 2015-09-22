"""
calibrateScanner.ino should be run after this is already running.
"""

import serial
import math
import string

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2);

use_stored_data = True

readings = []
run_flag = False

angles = [0, 30, 60, 90, 120, 150, 180]

angle_to_read_values = {}

if not use_stored_data:
	f = open('calibrateScanner.txt', 'w')

	print "running"

	while not run_flag:
		line = ser.readline()
		print run_flag, line,
		# print type(line)
		if line[:5] == "START":
			run_flag = True

	while run_flag:
		line = ser.readline()
		readings.append(line)
		print run_flag, line,
		if line[:3] == "END":
			run_flag = False

	for i in readings:
		if i[:3] == "@@@":
			current_index = int(string.strip(i, '@\n\r'))
			if current_index not in angle_to_read_values.keys():
				angle_to_read_values[current_index] = []
		elif i[:3] == "END":
			break
		else:
			angle_to_read_values[current_index].append(int(i))



	for i in readings:
		f.write(i)

	f.close()

else:
	f = open('calibrateScanner.txt', 'r')
	print "reading"
	f.seek(0)
	readings = f.readlines()
	for i in readings:
		if i[:3] == "@@@":
			current_index = int(string.strip(i, '@\n\r'))
			if current_index not in angle_to_read_values.keys():
				angle_to_read_values[current_index] = []
		elif i[:3] == "END":
			break
		else:
			angle_to_read_values[current_index].append(int(i))

	for i in angle_to_read_values.keys():
		print i, '\t', sorted(angle_to_read_values[i])

	f.close()