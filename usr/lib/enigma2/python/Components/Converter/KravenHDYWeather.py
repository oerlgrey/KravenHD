# -*- coding: utf-8 -*-
# YWeather Converter
# xml from http://weather.yahooapis.com/forecastrss
# Copyright (c) 2boom 2013-14 (02.03.2014)
# v.1.5-r0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from Components.config import config
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Poll import Poll
import time, gettext, os
from Components.Language import language

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("KravenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/KravenHD/locale/"))

def _(txt):
	t = gettext.dgettext("KravenHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

time_update = 20
time_update_ms = 5000

class KravenHDYWeather(Poll, Converter, object):
	city = 0
	direction = 1
	speed = 2
	humidity = 3
	wtext = 4
	temp = 5
	picon = 6
	fweekday0 = 7
	fweekday1 = 8
	fweekday2 = 9
	fweekday3 = 10
	fweekday4 = 11
	ftemp_high0 = 12
	ftemp_low0 = 13
	ftemp_high1 = 14
	ftemp_low1 = 15
	ftemp_high2 = 16
	ftemp_low2 = 17
	ftemp_high3 = 18
	ftemp_low3 = 19
	ftemp_high4 = 20
	ftemp_low4 = 21
	ftext0 = 22
	ftext1 = 23
	ftext2 = 24
	ftext3 = 25
	ftext4 = 26
	fpicon0 = 27
	fpicon1 = 28
	fpicon2 = 29
	fpicon3 = 30
	fpicon4 = 31
	feels = 32
	cityid = 33
	wind = 34
	templang = 35
	klima = 36

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)

		if type == "city":
			self.type = self.city
		elif type == "direction":
			self.type = self.direction
		elif type == "speed":
			self.type = self.speed
		elif type == "humidity":
			self.type = self.humidity
		elif type == "feels":
			self.type = self.feels
		elif type == "text":
			self.type = self.wtext
		elif type == "temp":
			self.type = self.temp
		elif type == "picon":
			self.type = self.picon
		elif type == "fweekday0":
			self.type = self.fweekday0
		elif type == "fweekday1":
			self.type = self.fweekday1
		elif type == "fweekday2":
			self.type = self.fweekday2
		elif type == "fweekday3":
			self.type = self.fweekday3
		elif type == "fweekday4":
			self.type = self.fweekday4
		elif type == "ftemp_high0":
			self.type = self.ftemp_high0
		elif type == "ftemp_low0":
			self.type = self.ftemp_low0
		elif type == "ftemp_high1":
			self.type = self.ftemp_high1
		elif type == "ftemp_low1":
			self.type = self.ftemp_low1
		elif type == "ftemp_high2":
			self.type = self.ftemp_high2
		elif type == "ftemp_low2":
			self.type = self.ftemp_low2
		elif type == "ftemp_high3":
			self.type = self.ftemp_high3
		elif type == "ftemp_low3":
			self.type = self.ftemp_low3
		elif type == "ftemp_high4":
			self.type = self.ftemp_high4
		elif type == "ftemp_low4":
			self.type = self.ftemp_low4
		elif type == "ftext0":
			self.type = self.ftext0
		elif type == "ftext1":
			self.type = self.ftext1
		elif type == "ftext2":
			self.type = self.ftext2
		elif type == "ftext3":
			self.type = self.ftext3
		elif type == "ftext4":
			self.type = self.ftext4
		elif type == "fpicon0":
			self.type = self.fpicon0
		elif type == "fpicon1":
			self.type = self.fpicon1
		elif type == "fpicon2":
			self.type = self.fpicon2
		elif type == "fpicon3":
			self.type = self.fpicon3
		elif type == "fpicon4":
			self.type = self.fpicon4
		elif type == "cityid":
			self.type = self.cityid
		elif type == "wind":
			self.type = self.wind
		elif type == "templang":
			self.type = self.templang
		elif type == "klima":
			self.type = self.klima
		self.poll_interval = time_update_ms
		self.poll_enabled = True
		
	def write_none(self):
		os.popen("echo -e 'None' >> /tmp/KravenHDweather.xml")
		
	def get_xmlfile(self):
		os.popen("wget -P /tmp -T2 'http://xml.weather.yahoo.com/forecastrss?w=%s&u=c' -O /tmp/KravenHDweather.xml" % str(config.plugins.KravenHD.weather_city.value))
			
	@cached
	def getText(self):
		fweather, tweather = [], []
		xweather = {'ycity':"N/A", 'feels':"N/A", 'ydirection':"N/A", 'yspeed':"N/A", 'yhumidity':"N/A", 'ytext':"N/A", 'ytemp':"N/A", 'ypicon':"3200", 'ymetric':"N/A"}
		direct = 0
		info = ''
		if fileExists("/tmp/KravenHDweather.xml"):
			if int((time.time() - os.stat("/tmp/KravenHDweather.xml").st_mtime)/60) >= time_update:
				self.get_xmlfile()
		else:
			self.get_xmlfile()
			if not fileExists("/tmp/KravenHDweather.xml"):
				self.write_none()
				return 'N/A'
                if not fileExists("/tmp/KravenHDweather.xml"):
			self.write_none()
			return 'N/A'
		for line in open("/tmp/KravenHDweather.xml"):
			if "<yweather:location" in line:
				xweather['ycity'] = line.split('city')[1].split('"')[1]
			elif "<yweather:units" in line:
				xweather['ymetric'] = line.split('temperature')[1].split('"')[1]
			elif "<yweather:wind" in line:
				xweather['feels'] = line.split('chill')[1].split('"')[1]
				xweather['ydirection'] = line.split('direction')[1].split('"')[1]
				xweather['yspeed'] = line.split('speed')[1].split('"')[1]
			elif "<yweather:atmosphere" in line:
				xweather['yhumidity'] = line.split('humidity')[1].split('"')[1]
			elif "<yweather:condition" in line:
				xweather['ytext'] = line.split('text')[1].split('"')[1]
				xweather['ypicon'] = line.split('code')[1].split('"')[1]
				xweather['ytemp'] = line.split('temp')[1].split('"')[1]
			elif "<yweather:forecast" in line:
				fweather.append(line.split('<yweather:forecast')[-1].split('/>')[0].strip())
				
		if self.type == self.city:
			info = xweather['ycity']
		elif self.type == self.direction:
			if not xweather['ydirection'] is 'N/A':
				direct = int(xweather['ydirection'])
				if direct >= 0 and direct <= 20:
					info = _('N')
				elif direct >= 21 and direct <= 35:
					info = _('N-NE')
				elif direct >= 36 and direct <= 55:
					info = _('NE')
				elif direct >= 56 and direct <= 70:
					info = _('E-NE')
				elif direct >= 71 and direct <= 110:
					info = _('E')
				elif direct >= 111 and direct <= 125:
					info = _('E-SE')
				elif direct >= 126 and direct <= 145:
					info = _('SE')
				elif direct >= 146 and direct <= 160:
					info = _('S-SE')
				elif direct >= 161 and direct <= 200:
					info = _('S')
				elif direct >= 201 and direct <= 215:
					info = _('S-SW')
				elif direct >= 216 and direct <= 235:
					info = _('SW')
				elif direct >= 236 and direct <= 250:
					info = _('W-SW')
				elif direct >= 251 and direct <= 290:
					info = _('W')
				elif direct >= 291 and direct <= 305:
					info = _('W-NW')
				elif direct >= 306 and direct <= 325:
					info = _('NW')
				elif direct >= 326 and direct <= 340:
					info = _('N-NW')
				elif direct >= 341 and direct <= 360:
					info = _('N')
                                else:
					info = _('N/A')
		elif self.type == self.speed:
			info = xweather['yspeed'] + _(' km/h')
		elif self.type == self.humidity:
			info = xweather['yhumidity'] + '%'
		elif self.type == self.wtext:
			info = xweather['ytext']
		elif self.type == self.feels:
			if not info is "N/A":
				info = xweather['feels'] + '%s' % unichr(176).encode("latin-1") + xweather['ymetric']
		elif self.type == self.temp:
			if not info is "N/A":
				info = xweather['ytemp'] + '%s' % unichr(176).encode("latin-1") + xweather['ymetric']
		elif self.type == self.picon:
			info = xweather['ypicon']
#####################################################
		elif self.type == self.fweekday0:
			if len(fweather) >= 1:
				if fweather[0].split('"')[1] == 'Mon':
					info = _('Mon')
				elif fweather[0].split('"')[1] == 'Tue':
					info = _('Tue')
				elif fweather[0].split('"')[1] == 'Wed':
					info = _('Wed')
				elif fweather[0].split('"')[1] == 'Thu':
					info = _('Thu')
				elif fweather[0].split('"')[1] == 'Fri':
					info = _('Fri')
				elif fweather[0].split('"')[1] == 'Sat':
					info = _('Sat')
				elif fweather[0].split('"')[1] == 'Sun':
					info = _('Sun')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.fweekday1:
			if len(fweather) >= 2:
				if fweather[1].split('"')[1] == 'Mon':
					info = _('Mon')
				elif fweather[1].split('"')[1] == 'Tue':
					info = _('Tue')
				elif fweather[1].split('"')[1] == 'Wed':
					info = _('Wed')
				elif fweather[1].split('"')[1] == 'Thu':
					info = _('Thu')
				elif fweather[1].split('"')[1] == 'Fri':
					info = _('Fri')
				elif fweather[1].split('"')[1] == 'Sat':
					info = _('Sat')
				elif fweather[1].split('"')[1] == 'Sun':
					info = _('Sun')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.fweekday2:
			if len(fweather) >= 3:
				if fweather[2].split('"')[1] == 'Mon':
					info = _('Mon')
				elif fweather[2].split('"')[1] == 'Tue':
					info = _('Tue')
				elif fweather[2].split('"')[1] == 'Wed':
					info = _('Wed')
				elif fweather[2].split('"')[1] == 'Thu':
					info = _('Thu')
				elif fweather[2].split('"')[1] == 'Fri':
					info = _('Fri')
				elif fweather[2].split('"')[1] == 'Sat':
					info = _('Sat')
				elif fweather[2].split('"')[1] == 'Sun':
					info = _('Sun')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.fweekday3:
			if len(fweather) >= 4:
				if fweather[3].split('"')[1] == 'Mon':
					info = _('Mon')
				elif fweather[3].split('"')[1] == 'Tue':
					info = _('Tue')
				elif fweather[3].split('"')[1] == 'Wed':
					info = _('Wed')
				elif fweather[3].split('"')[1] == 'Thu':
					info = _('Thu')
				elif fweather[3].split('"')[1] == 'Fri':
					info = _('Fri')
				elif fweather[3].split('"')[1] == 'Sat':
					info = _('Sat')
				elif fweather[3].split('"')[1] == 'Sun':
					info = _('Sun')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.fweekday4:
			if len(fweather) >= 5:
				if fweather[4].split('"')[1] == 'Mon':
					info = _('Mon')
				elif fweather[4].split('"')[1] == 'Tue':
					info = _('Tue')
				elif fweather[4].split('"')[1] == 'Wed':
					info = _('Wed')
				elif fweather[4].split('"')[1] == 'Thu':
					info = _('Thu')
				elif fweather[4].split('"')[1] == 'Fri':
					info = _('Fri')
				elif fweather[4].split('"')[1] == 'Sat':
					info = _('Sat')
				elif fweather[4].split('"')[1] == 'Sun':
					info = _('Sun')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.ftemp_high0:
			if len(fweather) >= 1:
				info = fweather[0].split('"')[7] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_low0:
			if len(fweather) >= 1:
				info = fweather[0].split('"')[5] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_high1:
			if len(fweather) >= 2:
				info = fweather[1].split('"')[7] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_low1:
			if len(fweather) >= 2:
				info = fweather[1].split('"')[5] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_high2:
			if len(fweather) >= 3:
				info = fweather[2].split('"')[7] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_low2:
			if len(fweather) >= 3:
				info = fweather[2].split('"')[5] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_high3:
			if len(fweather) >= 4:
				info = fweather[3].split('"')[7] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_low3:
			if len(fweather) >= 4:
				info = fweather[3].split('"')[5] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_high4:
			if len(fweather) >= 5:
				info = fweather[4].split('"')[7] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.ftemp_low4:
			if len(fweather) >= 5:
				info = fweather[4].split('"')[5] + '%s' % unichr(176).encode("latin-1")
			else:
				info = "N/A"
		elif self.type == self.fpicon0:
			if len(fweather) >= 1:
				info = fweather[0].split('"')[-2]
			else:
				info = "3200"
		elif self.type == self.fpicon1:
			if len(fweather) >= 2:
				info = fweather[1].split('"')[-2]
			else:
				info = "3200"
		elif self.type == self.fpicon2:
			if len(fweather) >= 3:
				info = fweather[2].split('"')[-2]
			else:
				info = "3200"
		elif self.type == self.fpicon3:
			if len(fweather) >= 4:
				info = fweather[3].split('"')[-2]
			else:
				info = "3200"
		elif self.type == self.fpicon4:
			if len(fweather) >= 5:
				info = fweather[4].split('"')[-2]
			else:
				info = "3200"
		elif self.type == self.ftext0:
			if len(fweather) >= 1:
				if fweather[0].split('"')[-2] == '0':
					info = _('Tornado')
				elif fweather[0].split('"')[-2] == '1':
					info = _('Tropical\n storm')
				elif fweather[0].split('"')[-2] == '2':
					info = _('Hurricane')
				elif fweather[0].split('"')[-2] == '3':
					info = _('Severe\n thunderstorms')
				elif fweather[0].split('"')[-2] == '4':
					info = _('Thunderstorms')
				elif fweather[0].split('"')[-2] == '5':
					info = _('Mixed rain\n and snow')
				elif fweather[0].split('"')[-2] == '6':
					info = _('Mixed rain\n and sleet')
				elif fweather[0].split('"')[-2] == '7':
					info = _('Mixed snow\n and sleet')
				elif fweather[0].split('"')[-2] == '8':
					info = _('Freezing\n drizzle')
				elif fweather[0].split('"')[-2] == '9':
					info = _('Drizzle')
				elif fweather[0].split('"')[-2] == '10':
					info = _('Freezing\n rain')
				elif fweather[0].split('"')[-2] == '11':
					info = _('Showers')
				elif fweather[0].split('"')[-2] == '12':
					info = _('Rain')
				elif fweather[0].split('"')[-2] == '13':
					info = _('Snow\n flurries')
				elif fweather[0].split('"')[-2] == '14':
					info = _('Light\n snow showers')
				elif fweather[0].split('"')[-2] == '15':
					info = _('Blowing\n snow')
				elif fweather[0].split('"')[-2] == '16':
					info = _('Snow')
				elif fweather[0].split('"')[-2] == '17':
					info = _('Hail')
				elif fweather[0].split('"')[-2] == '18':
					info = _('Sleet')
				elif fweather[0].split('"')[-2] == '19':
					info = _('Dust')
				elif fweather[0].split('"')[-2] == '20':
					info = _('Foggy')
				elif fweather[0].split('"')[-2] == '21':
					info = _('Haze')
				elif fweather[0].split('"')[-2] == '22':
					info = _('Smoky')
				elif fweather[0].split('"')[-2] == '23':
					info = _('Blustery')
				elif fweather[0].split('"')[-2] == '24':
					info = _('Windy')
				elif fweather[0].split('"')[-2] == '25':
					info = _('Cold')
				elif fweather[0].split('"')[-2] == '26':
					info = _('Cloudy')
				elif fweather[0].split('"')[-2] == '27':
					info = _('Mostly\n cloudy')
				elif fweather[0].split('"')[-2] == '28':
					info = _('Mostly\n cloudy')
				elif fweather[0].split('"')[-2] == '29':
					info = _('Partly\n cloudy')
				elif fweather[0].split('"')[-2] == '30':
					info = _('Partly\n cloudy')
				elif fweather[0].split('"')[-2] == '31':
					info = _('Clear')
				elif fweather[0].split('"')[-2] == '32':
					info = _('Sunny')
				elif fweather[0].split('"')[-2] == '33':
					info = _('Fair')
				elif fweather[0].split('"')[-2] == '34':
					info = _('Fair')
				elif fweather[0].split('"')[-2] == '35':
					info = _('Mixed rain\n and hail')
				elif fweather[0].split('"')[-2] == '36':
					info = _('Hot')
				elif fweather[0].split('"')[-2] == '37':
					info = _('Isolated\n thunderstorms')
				elif fweather[0].split('"')[-2] == '38':
					info = _('Scattered\n thunderstorms')
				elif fweather[0].split('"')[-2] == '39':
					info = _('Scattered\n thunderstorms')
				elif fweather[0].split('"')[-2] == '40':
					info = _('Scattered\n showers')
				elif fweather[0].split('"')[-2] == '41':
					info = _('Heavy snow')
				elif fweather[0].split('"')[-2] == '42':
					info = _('Scattered\n snow showers')
				elif fweather[0].split('"')[-2] == '43':
					info = _('Heavy snow')
				elif fweather[0].split('"')[-2] == '44':
					info = _('Partly\n cloudy')
				elif fweather[0].split('"')[-2] == '45':
					info = _('Thundershowers')
				elif fweather[0].split('"')[-2] == '46':
					info = _('Snow showers')
				elif fweather[0].split('"')[-2] == '47':
					info = _('Isolated\n thundershowers')
				elif fweather[0].split('"')[-2] == '3200':
					info = _('Not\n available')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.ftext1:
			if len(fweather) >= 2:
				if fweather[1].split('"')[-2] == '0':
					info = _('Tornado')
				elif fweather[1].split('"')[-2] == '1':
					info = _('Tropical\n storm')
				elif fweather[1].split('"')[-2] == '2':
					info = _('Hurricane')
				elif fweather[1].split('"')[-2] == '3':
					info = _('Severe\n thunderstorms')
				elif fweather[1].split('"')[-2] == '4':
					info = _('Thunderstorms')
				elif fweather[1].split('"')[-2] == '5':
					info = _('Mixed rain\n and snow')
				elif fweather[1].split('"')[-2] == '6':
					info = _('Mixed rain\n and sleet')
				elif fweather[1].split('"')[-2] == '7':
					info = _('Mixed snow\n and sleet')
				elif fweather[1].split('"')[-2] == '8':
					info = _('Freezing\n drizzle')
				elif fweather[1].split('"')[-2] == '9':
					info = _('Drizzle')
				elif fweather[1].split('"')[-2] == '10':
					info = _('Freezing\n rain')
				elif fweather[1].split('"')[-2] == '11':
					info = _('Showers')
				elif fweather[1].split('"')[-2] == '12':
					info = _('Rain')
				elif fweather[1].split('"')[-2] == '13':
					info = _('Snow\n flurries')
				elif fweather[1].split('"')[-2] == '14':
					info = _('Light\n snow showers')
				elif fweather[1].split('"')[-2] == '15':
					info = _('Blowing\n snow')
				elif fweather[1].split('"')[-2] == '16':
					info = _('Snow')
				elif fweather[1].split('"')[-2] == '17':
					info = _('Hail')
				elif fweather[1].split('"')[-2] == '18':
					info = _('Sleet')
				elif fweather[1].split('"')[-2] == '19':
					info = _('Dust')
				elif fweather[1].split('"')[-2] == '20':
					info = _('Foggy')
				elif fweather[1].split('"')[-2] == '21':
					info = _('Haze')
				elif fweather[1].split('"')[-2] == '22':
					info = _('Smoky')
				elif fweather[1].split('"')[-2] == '23':
					info = _('Blustery')
				elif fweather[1].split('"')[-2] == '24':
					info = _('Windy')
				elif fweather[1].split('"')[-2] == '25':
					info = _('Cold')
				elif fweather[1].split('"')[-2] == '26':
					info = _('Cloudy')
				elif fweather[1].split('"')[-2] == '27':
					info = _('Mostly\n cloudy')
				elif fweather[1].split('"')[-2] == '28':
					info = _('Mostly\n cloudy')
				elif fweather[1].split('"')[-2] == '29':
					info = _('Partly\n cloudy')
				elif fweather[1].split('"')[-2] == '30':
					info = _('Partly\n cloudy')
				elif fweather[1].split('"')[-2] == '31':
					info = _('Clear')
				elif fweather[1].split('"')[-2] == '32':
					info = _('Sunny')
				elif fweather[1].split('"')[-2] == '33':
					info = _('Fair')
				elif fweather[1].split('"')[-2] == '34':
					info = _('Fair')
				elif fweather[1].split('"')[-2] == '35':
					info = _('Mixed rain\n and hail')
				elif fweather[1].split('"')[-2] == '36':
					info = _('Hot')
				elif fweather[1].split('"')[-2] == '37':
					info = _('Isolated\n thunderstorms')
				elif fweather[1].split('"')[-2] == '38':
					info = _('Scattered\n thunderstorms')
				elif fweather[1].split('"')[-2] == '39':
					info = _('Scattered\n thunderstorms')
				elif fweather[1].split('"')[-2] == '40':
					info = _('Scattered\n showers')
				elif fweather[1].split('"')[-2] == '41':
					info = _('Heavy snow')
				elif fweather[1].split('"')[-2] == '42':
					info = _('Scattered\n snow showers')
				elif fweather[1].split('"')[-2] == '43':
					info = _('Heavy snow')
				elif fweather[1].split('"')[-2] == '44':
					info = _('Partly\n cloudy')
				elif fweather[1].split('"')[-2] == '45':
					info = _('Thundershowers')
				elif fweather[1].split('"')[-2] == '46':
					info = _('Snow showers')
				elif fweather[1].split('"')[-2] == '47':
					info = _('Isolated\n thundershowers')
				elif fweather[1].split('"')[-2] == '3200':
					info = _('Not\n available')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.ftext2:
			if len(fweather) >= 3:
				if fweather[2].split('"')[-2] == '0':
					info = _('Tornado')
				elif fweather[2].split('"')[-2] == '1':
					info = _('Tropical\n storm')
				elif fweather[2].split('"')[-2] == '2':
					info = _('Hurricane')
				elif fweather[2].split('"')[-2] == '3':
					info = _('Severe\n thunderstorms')
				elif fweather[2].split('"')[-2] == '4':
					info = _('Thunderstorms')
				elif fweather[2].split('"')[-2] == '5':
					info = _('Mixed rain\n and snow')
				elif fweather[2].split('"')[-2] == '6':
					info = _('Mixed rain\n and sleet')
				elif fweather[2].split('"')[-2] == '7':
					info = _('Mixed snow\n and sleet')
				elif fweather[2].split('"')[-2] == '8':
					info = _('Freezing\n drizzle')
				elif fweather[2].split('"')[-2] == '9':
					info = _('Drizzle')
				elif fweather[2].split('"')[-2] == '10':
					info = _('Freezing\n rain')
				elif fweather[2].split('"')[-2] == '11':
					info = _('Showers')
				elif fweather[2].split('"')[-2] == '12':
					info = _('Rain')
				elif fweather[2].split('"')[-2] == '13':
					info = _('Snow\n flurries')
				elif fweather[2].split('"')[-2] == '14':
					info = _('Light\n snow showers')
				elif fweather[2].split('"')[-2] == '15':
					info = _('Blowing\n snow')
				elif fweather[2].split('"')[-2] == '16':
					info = _('Snow')
				elif fweather[2].split('"')[-2] == '17':
					info = _('Hail')
				elif fweather[2].split('"')[-2] == '18':
					info = _('Sleet')
				elif fweather[2].split('"')[-2] == '19':
					info = _('Dust')
				elif fweather[2].split('"')[-2] == '20':
					info = _('Foggy')
				elif fweather[2].split('"')[-2] == '21':
					info = _('Haze')
				elif fweather[2].split('"')[-2] == '22':
					info = _('Smoky')
				elif fweather[2].split('"')[-2] == '23':
					info = _('Blustery')
				elif fweather[2].split('"')[-2] == '24':
					info = _('Windy')
				elif fweather[2].split('"')[-2] == '25':
					info = _('Cold')
				elif fweather[2].split('"')[-2] == '26':
					info = _('Cloudy')
				elif fweather[2].split('"')[-2] == '27':
					info = _('Mostly\n cloudy')
				elif fweather[2].split('"')[-2] == '28':
					info = _('Mostly\n cloudy')
				elif fweather[2].split('"')[-2] == '29':
					info = _('Partly\n cloudy')
				elif fweather[2].split('"')[-2] == '30':
					info = _('Partly\n cloudy')
				elif fweather[2].split('"')[-2] == '31':
					info = _('Clear')
				elif fweather[2].split('"')[-2] == '32':
					info = _('Sunny')
				elif fweather[2].split('"')[-2] == '33':
					info = _('Fair')
				elif fweather[2].split('"')[-2] == '34':
					info = _('Fair')
				elif fweather[2].split('"')[-2] == '35':
					info = _('Mixed rain\n and hail')
				elif fweather[2].split('"')[-2] == '36':
					info = _('Hot')
				elif fweather[2].split('"')[-2] == '37':
					info = _('Isolated\n thunderstorms')
				elif fweather[2].split('"')[-2] == '38':
					info = _('Scattered\n thunderstorms')
				elif fweather[2].split('"')[-2] == '39':
					info = _('Scattered\n thunderstorms')
				elif fweather[2].split('"')[-2] == '40':
					info = _('Scattered\n showers')
				elif fweather[2].split('"')[-2] == '41':
					info = _('Heavy snow')
				elif fweather[2].split('"')[-2] == '42':
					info = _('Scattered\n snow showers')
				elif fweather[2].split('"')[-2] == '43':
					info = _('Heavy snow')
				elif fweather[2].split('"')[-2] == '44':
					info = _('Partly\n cloudy')
				elif fweather[2].split('"')[-2] == '45':
					info = _('Thundershowers')
				elif fweather[2].split('"')[-2] == '46':
					info = _('Snow showers')
				elif fweather[2].split('"')[-2] == '47':
					info = _('Isolated\n thundershowers')
				elif fweather[2].split('"')[-2] == '3200':
					info = _('Not\n available')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.ftext3:
			if len(fweather) >= 4:
				if fweather[3].split('"')[-2] == '0':
					info = _('Tornado')
				elif fweather[3].split('"')[-2] == '1':
					info = _('Tropical\n storm')
				elif fweather[3].split('"')[-2] == '2':
					info = _('Hurricane')
				elif fweather[3].split('"')[-2] == '3':
					info = _('Severe\n thunderstorms')
				elif fweather[3].split('"')[-2] == '4':
					info = _('Thunderstorms')
				elif fweather[3].split('"')[-2] == '5':
					info = _('Mixed rain\n and snow')
				elif fweather[3].split('"')[-2] == '6':
					info = _('Mixed rain\n and sleet')
				elif fweather[3].split('"')[-2] == '7':
					info = _('Mixed snow\n and sleet')
				elif fweather[3].split('"')[-2] == '8':
					info = _('Freezing\n drizzle')
				elif fweather[3].split('"')[-2] == '9':
					info = _('Drizzle')
				elif fweather[3].split('"')[-2] == '10':
					info = _('Freezing\n rain')
				elif fweather[3].split('"')[-2] == '11':
					info = _('Showers')
				elif fweather[3].split('"')[-2] == '12':
					info = _('Rain')
				elif fweather[3].split('"')[-2] == '13':
					info = _('Snow\n flurries')
				elif fweather[3].split('"')[-2] == '14':
					info = _('Light\n snow showers')
				elif fweather[3].split('"')[-2] == '15':
					info = _('Blowing\n snow')
				elif fweather[3].split('"')[-2] == '16':
					info = _('Snow')
				elif fweather[3].split('"')[-2] == '17':
					info = _('Hail')
				elif fweather[3].split('"')[-2] == '18':
					info = _('Sleet')
				elif fweather[3].split('"')[-2] == '19':
					info = _('Dust')
				elif fweather[3].split('"')[-2] == '20':
					info = _('Foggy')
				elif fweather[3].split('"')[-2] == '21':
					info = _('Haze')
				elif fweather[3].split('"')[-2] == '22':
					info = _('Smoky')
				elif fweather[3].split('"')[-2] == '23':
					info = _('Blustery')
				elif fweather[3].split('"')[-2] == '24':
					info = _('Windy')
				elif fweather[3].split('"')[-2] == '25':
					info = _('Cold')
				elif fweather[3].split('"')[-2] == '26':
					info = _('Cloudy')
				elif fweather[3].split('"')[-2] == '27':
					info = _('Mostly\n cloudy')
				elif fweather[3].split('"')[-2] == '28':
					info = _('Mostly\n cloudy')
				elif fweather[3].split('"')[-2] == '29':
					info = _('Partly\n cloudy')
				elif fweather[3].split('"')[-2] == '30':
					info = _('Partly\n cloudy')
				elif fweather[3].split('"')[-2] == '31':
					info = _('Clear')
				elif fweather[3].split('"')[-2] == '32':
					info = _('Sunny')
				elif fweather[3].split('"')[-2] == '33':
					info = _('Fair')
				elif fweather[3].split('"')[-2] == '34':
					info = _('Fair')
				elif fweather[3].split('"')[-2] == '35':
					info = _('Mixed rain\n and hail')
				elif fweather[3].split('"')[-2] == '36':
					info = _('Hot')
				elif fweather[3].split('"')[-2] == '37':
					info = _('Isolated\n thunderstorms')
				elif fweather[3].split('"')[-2] == '38':
					info = _('Scattered\n thunderstorms')
				elif fweather[3].split('"')[-2] == '39':
					info = _('Scattered\n thunderstorms')
				elif fweather[3].split('"')[-2] == '40':
					info = _('Scattered\n showers')
				elif fweather[3].split('"')[-2] == '41':
					info = _('Heavy snow')
				elif fweather[3].split('"')[-2] == '42':
					info = _('Scattered\n snow showers')
				elif fweather[3].split('"')[-2] == '43':
					info = _('Heavy snow')
				elif fweather[3].split('"')[-2] == '44':
					info = _('Partly\n cloudy')
				elif fweather[3].split('"')[-2] == '45':
					info = _('Thundershowers')
				elif fweather[3].split('"')[-2] == '46':
					info = _('Snow showers')
				elif fweather[3].split('"')[-2] == '47':
					info = _('Isolated\n thundershowers')
				elif fweather[3].split('"')[-2] == '3200':
					info = _('Not\n available')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.ftext4:
			if len(fweather) >= 5:
				if fweather[4].split('"')[-2] == '0':
					info = _('Tornado')
				elif fweather[4].split('"')[-2] == '1':
					info = _('Tropical\n storm')
				elif fweather[4].split('"')[-2] == '2':
					info = _('Hurricane')
				elif fweather[4].split('"')[-2] == '3':
					info = _('Severe\n thunderstorms')
				elif fweather[4].split('"')[-2] == '4':
					info = _('Thunderstorms')
				elif fweather[4].split('"')[-2] == '5':
					info = _('Mixed rain\n and snow')
				elif fweather[4].split('"')[-2] == '6':
					info = _('Mixed rain\n and sleet')
				elif fweather[4].split('"')[-2] == '7':
					info = _('Mixed snow\n and sleet')
				elif fweather[4].split('"')[-2] == '8':
					info = _('Freezing\n drizzle')
				elif fweather[4].split('"')[-2] == '9':
					info = _('Drizzle')
				elif fweather[4].split('"')[-2] == '10':
					info = _('Freezing\n rain')
				elif fweather[4].split('"')[-2] == '11':
					info = _('Showers')
				elif fweather[4].split('"')[-2] == '12':
					info = _('Rain')
				elif fweather[4].split('"')[-2] == '13':
					info = _('Snow\n flurries')
				elif fweather[4].split('"')[-2] == '14':
					info = _('Light\n snow showers')
				elif fweather[4].split('"')[-2] == '15':
					info = _('Blowing\n snow')
				elif fweather[4].split('"')[-2] == '16':
					info = _('Snow')
				elif fweather[4].split('"')[-2] == '17':
					info = _('Hail')
				elif fweather[4].split('"')[-2] == '18':
					info = _('Sleet')
				elif fweather[4].split('"')[-2] == '19':
					info = _('Dust')
				elif fweather[4].split('"')[-2] == '20':
					info = _('Foggy')
				elif fweather[4].split('"')[-2] == '21':
					info = _('Haze')
				elif fweather[4].split('"')[-2] == '22':
					info = _('Smoky')
				elif fweather[4].split('"')[-2] == '23':
					info = _('Blustery')
				elif fweather[4].split('"')[-2] == '24':
					info = _('Windy')
				elif fweather[4].split('"')[-2] == '25':
					info = _('Cold')
				elif fweather[4].split('"')[-2] == '26':
					info = _('Cloudy')
				elif fweather[4].split('"')[-2] == '27':
					info = _('Mostly\n cloudy')
				elif fweather[4].split('"')[-2] == '28':
					info = _('Mostly\n cloudy')
				elif fweather[4].split('"')[-2] == '29':
					info = _('Partly\n cloudy')
				elif fweather[4].split('"')[-2] == '30':
					info = _('Partly\n cloudy')
				elif fweather[4].split('"')[-2] == '31':
					info = _('Clear')
				elif fweather[4].split('"')[-2] == '32':
					info = _('Sunny')
				elif fweather[4].split('"')[-2] == '33':
					info = _('Fair')
				elif fweather[4].split('"')[-2] == '34':
					info = _('Fair')
				elif fweather[4].split('"')[-2] == '35':
					info = _('Mixed rain\n and hail')
				elif fweather[4].split('"')[-2] == '36':
					info = _('Hot')
				elif fweather[4].split('"')[-2] == '37':
					info = _('Isolated\n thunderstorms')
				elif fweather[4].split('"')[-2] == '38':
					info = _('Scattered\n thunderstorms')
				elif fweather[4].split('"')[-2] == '39':
					info = _('Scattered\n thunderstorms')
				elif fweather[4].split('"')[-2] == '40':
					info = _('Scattered\n showers')
				elif fweather[4].split('"')[-2] == '41':
					info = _('Heavy snow')
				elif fweather[4].split('"')[-2] == '42':
					info = _('Scattered\n snow showers')
				elif fweather[4].split('"')[-2] == '43':
					info = _('Heavy snow')
				elif fweather[4].split('"')[-2] == '44':
					info = _('Partly\n cloudy')
				elif fweather[4].split('"')[-2] == '45':
					info = _('Thundershowers')
				elif fweather[4].split('"')[-2] == '46':
					info = _('Snow showers')
				elif fweather[4].split('"')[-2] == '47':
					info = _('Isolated\n thundershowers')
				elif fweather[4].split('"')[-2] == '3200':
					info = _('Not\n available')
				else:
					info = "N/A"
			else:
				info = "N/A"
		elif self.type == self.cityid:
			info = config.plugins.KravenHD.weather_city.value
		elif self.type == self.wind:
			wspeed = xweather['yspeed'][:-3] + _(' km/h')
			if not xweather['ydirection'] is 'N/A':
				direct = int(xweather['ydirection'])
				if direct >= 0 and direct <= 20:
					wdirect = _('N')
				elif direct >= 21 and direct <= 35:
					wdirect = _('N-NE')
				elif direct >= 36 and direct <= 55:
					wdirect = _('NE')
				elif direct >= 56 and direct <= 70:
					wdirect = _('E-NE')
				elif direct >= 71 and direct <= 110:
					wdirect = _('E')
				elif direct >= 111 and direct <= 125:
					wdirect = _('E-SE')
				elif direct >= 126 and direct <= 145:
					wdirect = _('SE')
				elif direct >= 146 and direct <= 160:
					wdirect = _('S-SE')
				elif direct >= 161 and direct <= 200:
					wdirect = _('S')
				elif direct >= 201 and direct <= 215:
					wdirect = _('S-SW')
				elif direct >= 216 and direct <= 235:
					wdirect = _('SW')
				elif direct >= 236 and direct <= 250:
					wdirect = _('W-SW')
				elif direct >= 251 and direct <= 290:
					wdirect = _('W')
				elif direct >= 291 and direct <= 305:
					wdirect = _('W-NW')
				elif direct >= 306 and direct <= 325:
					wdirect = _('NW')
				elif direct >= 326 and direct <= 340:
					wdirect = _('N-NW')
				elif direct >= 341 and direct <= 360:
					wdirect = _('N')
				else:
					wdirect = _('N/A')
			info = wspeed + _(' from ') + wdirect
		elif self.type == self.templang:
			if not info is "N/A":
				temp1 = xweather['ytemp'] + '%s' % unichr(176).encode("latin-1") + xweather['ymetric']
				temp2 = xweather['feels'] + '%s' % unichr(176).encode("latin-1") + xweather['ymetric']
				info = temp1 + _(', feels ') + temp2
		elif self.type == self.klima:
			info = xweather['yhumidity'] + _('% humidity')
		return info
######################################################
	text = property(getText)

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))
