# -*- coding: utf-8 -*-

#  pstrRndr Renderer
#
#  Coded/Modified/Adapted by örlgrey
#  Based on OpenATV image source code
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

# by digiteng...12-2019

from Components.Renderer.Renderer import Renderer 
from enigma import ePixmap, loadJPG
import os, re

class KravenHDpstrRndr(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.path = ""
		self.pstrNm = ""
		self.scale = "0"

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
				if value.endswith("/"):
					self.path = value
				else:
					self.path = value + "/"
			elif attrib == 'noscale':
				self.scale = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		try:
			eventName = self.source.text
			if eventName :
				posterNm = re.sub('\s+', '+', eventName)
				pstrNm = "/media/hdd/" + self.path + posterNm + ".jpg"

				if os.path.exists(pstrNm):
					if self.scale == '0':
						self.instance.setScale(1)
					self.instance.setPixmap(loadJPG(pstrNm))
					self.instance.show()
				else:
					self.instance.hide()
			else:
				self.instance.hide()
		except:
			pass
