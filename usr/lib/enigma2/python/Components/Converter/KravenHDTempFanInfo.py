# -*- coding: utf-8 -*-

#  Temp Fan Info Converter
#
#  Coded/Modified/Adapted by oerlgrey
#  Based on openATV image source code
#
#  This code is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan
#  Abbott Way, Stanford, California 94305, USA.
#
#  If you think this license infringes any rights,
#  please contact me at ochzoetna@gmail.com

from __future__ import absolute_import
from Components.config import config
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import iServiceInformation, iPlayableService
from Components.Converter.Poll import Poll
from os import path

class KravenHDTempFanInfo(Poll, Converter, object):
	TEMPINFO = 0
	FANINFO = 1

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.type = type
		self.poll_interval = 2000
		self.poll_enabled = True
		if type == 'TempInfo':
			self.type = self.TEMPINFO
		elif type == 'FanInfo':
			self.type = self.FANINFO

	@cached
	def getText(self):
		textvalue = ''
		if self.type == self.TEMPINFO:
			textvalue = self.tempfile()
		elif self.type == self.FANINFO:
			textvalue = self.fanfile()
		return textvalue

	text = property(getText)

	def tempfile(self):
		systemp = "N/A"
		try:
			if path.exists('/proc/stb/sensors/temp0/value'):
				f = open('/proc/stb/sensors/temp0/value', 'r')
				systemp = f.readline()
				f.close()
			elif path.exists('/proc/stb/fp/temp_sensor'):
				f = open('/proc/stb/fp/temp_sensor', 'r')
				systemp = f.readline()
				f.close()
			elif path.exists('/proc/stb/sensors/temp/value'):
				f = open('/proc/stb/sensors/temp/value', 'r')
				systemp = f.readline()
				f.close()
			elif path.exists('/proc/stb/fp/temp_sensor_avs'):
				f = open('/proc/stb/fp/temp_sensor_avs', 'r')
				systemp = f.readline()
				f.close()
			elif path.exists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
				f = open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r')
				systemp = f.readline()
				systemp = systemp[:-3]
				f.close()
			elif path.exists('/proc/stb/power/avs'):
				f = open('/proc/stb/power/avs', 'r')
				systemp = f.readline()
				f.close()
			elif path.exists('/proc/hisi/msp/pm_cpu'):
				for line in open('/proc/hisi/msp/pm_cpu').readlines():
					line = [x.strip() for x in line.strip().split(":")]
					if line[0] in ("Tsensor"):
						systemp = line[1].split("=")
						systemp = line[1].split(" ")
						systemp = systemp[2]
		except:
			pass
		if systemp != "N/A":
			if int(systemp.replace('\n', '')) > 2:
				systemp = systemp[:2]
			systemp = systemp.replace('\n', '').replace(' ', '') + "°C"
		return systemp

	def fanfile(self):
		faninfo = "N/A"
		try:
			if path.exists('/proc/stb/fp/fan_speed'):
				f = open('/proc/stb/fp/fan_speed', 'r')
				faninfo = f.readline()
				f.close()
		except:
			pass
		if faninfo != "N/A":
			faninfo = faninfo[:-4]
		return faninfo
