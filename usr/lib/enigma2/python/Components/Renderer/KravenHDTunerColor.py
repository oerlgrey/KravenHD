# -*- coding: utf-8 -*-

#  Tuner Color Renderer
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
from Components.Renderer.Renderer import Renderer
from enigma import eLabel
from skin import parseColor

class KravenHDTunerColor(VariableText, Renderer):
	GUI_WIDGET = eLabel

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'text':
				value = self.text
				attribs.append((attrib, value))
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what):
		tunertext = self.source.text
		if tunertext.split("_")[1] == "B":
			color = "KravenTunerBusy"
		elif tunertext.split("_")[1] == "L":
			color = "KravenTunerLive"
		elif tunertext.split("_")[1] == "R":
			color = "KravenTunerRecord"
		elif tunertext.split("_")[1] == "X":
			color = "KravenTunerXtremeBusy"
		else:
			color = "KravenIcon"
		self.text = tunertext.split("_")[0]
		if self.instance:
			self.instance.clearForegroundColor()
			self.instance.setForegroundColor(parseColor(color))
