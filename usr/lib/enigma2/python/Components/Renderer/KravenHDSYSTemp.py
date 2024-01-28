# -*- coding: utf-8 -*-

#  Sys Temp Renderer
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

from Components.VariableText import VariableText
from enigma import eLabel
from Components.Renderer.Renderer import Renderer
from os import path, popen

class KravenHDSYSTemp(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)

	GUI_WIDGET = eLabel

	def changed(self, what):
		if not self.suspended:
			systemp = "-- "
			try:
				if path.exists('/proc/stb/sensors/temp0/value'):
					out_line = popen("cat /proc/stb/sensors/temp0/value").readline()
					systemp = out_line.replace('\n', '')
				elif path.exists('/proc/stb/fp/temp_sensor'):
					out_line = popen("cat /proc/stb/fp/temp_sensor").readline()
					systemp = out_line.replace('\n', '')
				if not systemp == "-- " and len(systemp) > 2:
					systemp = systemp[:2]
			except:
				pass
			self.text = systemp + str('\xc2\xb0') + "C"

	def onShow(self):
		self.suspended = False
		self.changed(None)

	def onHide(self):
		self.suspended = True
