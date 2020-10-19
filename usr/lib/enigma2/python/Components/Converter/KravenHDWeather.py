# -*- coding: utf-8 -*-
#
#  KravenHDMSNWeather Converter
#
#  Coded by örlgrey
#  Based on openATV and/or teamBlue image source code
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

from __future__ import print_function

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from enigma import eTimer
import requests, time, os, gettext
from Components.Converter.Poll import Poll
from Plugins.Extensions.KravenHD import ping
from lxml import etree
from xml.etree.cElementTree import fromstring
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
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

WEATHER_DATA = None
WEATHER_LOAD = True

class KravenHDWeather(Poll, Converter, object):
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.poll_interval = 60000
		self.poll_enabled = True
		self.type = type
		self.timer = eTimer()
		self.timer.callback.append(self.reset)
		self.timer.callback.append(self.get_Data)
		self.data = None
		self.get_Data()

	@cached
	def getText(self):
		global WEATHER_DATA
		self.data = WEATHER_DATA
		if self.type == "temp_cur":
			return self.getTemperature_current()
		elif self.type == "feels_like":
			return self.getTemperature_feelslike()
		elif self.type == "humidity":
			return self.getHumidity()
		elif self.type == "wind":
			return self.getWind()
		elif self.type == "city":
			return str(config.plugins.KravenHD.msn_cityfound.value)
		elif self.type in ("meteo_cur","meteo1","meteo2","meteo3"):
			return self.getMeteoFont()
		elif self.type in ("icon_cur","icon1","icon2","icon3"):
			return self.getMeteoIcon()
		elif self.type in ("text_cur","text1","text2","text3"):
			return self.getMeteoText()
		elif self.type in ("high0","high1","high2","high3"):
			return self.getTemperature_high()
		elif self.type in ("low0","low1","low2","low3"):
			return self.getTemperature_low()
		elif self.type in ("minmax0","minmax1","minmax2","minmax3"):
			return self.getMinMax()
		elif self.type in ("shortday0","shortday1","shortday2","shortday3"):
			return self.getShortday()
		else:
			return ""

	text = property(getText)

	def reset(self):
		global WEATHER_LOAD
		WEATHER_LOAD = True
		self.timer.stop()

	def get_Data(self):
		global WEATHER_DATA
		global WEATHER_LOAD
		if WEATHER_LOAD == True:
			try:
				r = ping.doOne("8.8.8.8",1.5)
				if r != None and r <= 1.5:
					print ("KravenHD: download from URL")
					res = requests.get('http://weather.service.msn.com/data.aspx?src=windows&weadegreetype=C&culture=' + str(config.plugins.KravenHD.msn_language.value) + '&wealocations=wc:' + str(config.plugins.KravenHD.msn_code.value), timeout=1.5)
					self.data = fromstring(res.text)
					WEATHER_DATA = self.data
					WEATHER_LOAD = False
			except:
				pass
			timeout = max(15,int(config.plugins.KravenHD.refreshInterval.value)) * 1000.0 * 60.0
			self.timer.start(int(timeout), True)
		else:
			self.data = WEATHER_DATA

	def getTemperature_current(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						value = items.attrib.get("temperature").encode("utf-8", 'ignore')
						return str(value) + "°C"
		except:
			return ''

	def getTemperature_feelslike(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						cur_temp = items.attrib.get("temperature").encode("utf-8", 'ignore')
						feels_temp = items.attrib.get("feelslike").encode("utf-8", 'ignore')
						return str(cur_temp) + '°C' + _(", feels ") + str(feels_temp) + '°C'
		except:
			return ''

	def getHumidity(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						value = items.attrib.get("humidity").encode("utf-8", 'ignore')
						return str(value) + _('% humidity')
		except:
			return ''

	def getWind(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						value = items.attrib.get("winddisplay").encode("utf-8", 'ignore')
						return str(value)
		except:
			return ''

	def getTemperature_high(self):
		try:
			if self.type == "high0":
				for items in self.data.findall(".//forecast[2]"):
					value = items.get("high").encode("utf-8", 'ignore')
					return str(value) + "°C"
			if self.type == "high1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("high").encode("utf-8", 'ignore')
					return str(value) + "°C"
			if self.type == "high2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("high").encode("utf-8", 'ignore')
					return str(value) + "°C"
			if self.type == "high3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("high").encode("utf-8", 'ignore')
					return str(value) + "°C"
		except:
			return ''

	def getTemperature_low(self):
		try:
			if self.type == "low0":
				for items in self.data.findall(".//forecast[2]"):
					value = items.get("low").encode("utf-8", 'ignore')
					return str(value) + "°C"
			if self.type == "low1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("low").encode("utf-8", 'ignore')
					return str(value) + "°C"
			if self.type == "low2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("low").encode("utf-8", 'ignore')
					return str(value) + "°C"
			if self.type == "low3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("low").encode("utf-8", 'ignore')
					return str(value) + "°C"
		except:
			return ''

	def getMinMax(self):
		try:
			if self.type == "minmax0":
				for items in self.data.findall(".//forecast[2]"):
					min = items.get("low").encode("utf-8", 'ignore')
					max = items.get("high").encode("utf-8", 'ignore')
					return str(min) + "° / " + str(max) + "°"
			if self.type == "minmax1":
				for items in self.data.findall(".//forecast[3]"):
					min = items.get("low").encode("utf-8", 'ignore')
					max = items.get("high").encode("utf-8", 'ignore')
					return str(min) + "° / " + str(max) + "°"
			if self.type == "minmax2":
				for items in self.data.findall(".//forecast[4]"):
					min = items.get("low").encode("utf-8", 'ignore')
					max = items.get("high").encode("utf-8", 'ignore')
					return str(min) + "° / " + str(max) + "°"
			if self.type == "minmax3":
				for items in self.data.findall(".//forecast[5]"):
					min = items.get("low").encode("utf-8", 'ignore')
					max = items.get("high").encode("utf-8", 'ignore')
					return str(min) + "° / " + str(max) + "°"
		except:
			return ''

	def getShortday(self):
		try:
			if self.type == "shortday0":
				for items in self.data.findall(".//forecast[2]"):
					value = items.get("shortday").encode("utf-8", 'ignore')
					return str(value)
			if self.type == "shortday1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("shortday").encode("utf-8", 'ignore')
					return str(value)
			if self.type == "shortday2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("shortday").encode("utf-8", 'ignore')
					return str(value)
			if self.type == "shortday3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("shortday").encode("utf-8", 'ignore')
					return str(value)
		except:
			return ''

	def getMeteoIcon(self):
		try:
			if self.type == "icon_cur":
				for childs in self.data:
					for items in childs:
						if items.tag == "current":
							value = items.attrib.get("skycode").encode("utf-8", 'ignore')
							return str(value)
			if self.type == "icon1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("skycodeday").encode("utf-8", 'ignore')
					return str(value)
			if self.type == "icon2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("skycodeday").encode("utf-8", 'ignore')
					return str(value)
			if self.type == "icon3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("skycodeday").encode("utf-8", 'ignore')
					return str(value)
		except:
			return "3200"

	def getMeteoText(self):
		try:
			if self.type == "text_cur":
				for childs in self.data:
					for items in childs:
						if items.tag == "current":
							value = items.attrib.get("skytext").encode("utf-8", 'ignore')
							return str(value)
			if self.type == "text1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("skytextday").encode("utf-8", 'ignore')
					return str(value)
			if self.type == "text2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("skytextday").encode("utf-8", 'ignore')
					return str(value)
			if self.type == "text3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("skytextday").encode("utf-8", 'ignore')
					return str(value)
		except:
			return ''

	def getMeteoFont(self):
		try:
			if self.type == "meteo_cur":
				for childs in self.data:
					for items in childs:
						if items.tag == "current":
							value = items.attrib.get("skycode").encode("utf-8", 'ignore')
			if self.type == "meteo1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("skycodeday").encode("utf-8", 'ignore')
			if self.type == "meteo2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("skycodeday").encode("utf-8", 'ignore')
			if self.type == "meteo3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("skycodeday").encode("utf-8", 'ignore')
		except:
			return ''

		if value in ("0","1","2","23","24"):
			return "S"
		elif value in ("3","4"):
			return "Z"
		elif value in ("5","6","7","18"):
			return "U"
		elif value in ("8","10","25"):
			return "G"
		elif value == "9":
			return "Q"
		elif value in ("11","12","40"):
			return "R"
		elif value in ("13","14","15","16","41","42","43","46"):
			return "W"
		elif value in ("17","35"):
			return "X"
		elif value == "19":
			return "F"
		elif value in ("20","21","22"):
			return "L"
		elif value in ("26","44"):
			return "N"
		elif value in ("27","29"):
			return "I"
		elif value in ("28","30"):
			return "H"
		elif value in ("31","33"):
			return "C"
		elif value in ("32","34","36"):
			return "B"
		elif value in ("37","38","39","45","47"):
			return "0"
		else:
			return ")"
