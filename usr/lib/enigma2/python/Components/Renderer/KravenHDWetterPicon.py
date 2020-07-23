# -*- coding: utf-8 -*-

#  Wetter Picon Renderer
#
#  Coded/Modified/Adapted by örlgrey
#  Based on VTi and/or OpenATV image source code
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

from Renderer import Renderer 
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, resolveFilename 

class KravenHDWetterPicon(Renderer):

	__module__ = __name__
	def __init__(self):
		Renderer.__init__(self)
		self.pngname = ''
		self.userpath = "/usr/share/enigma2/Kraven-user-icons/"
		self.usericons = [
		("1","32"),
		("2","34"),
		("3","30"),
		("4","30"),
		("5","21"),
		("6","28"),
		("7","26"),
		("8","26"),
		("11","20"),
		("12","40"),
		("13","39"),
		("14","39"),
		("15","4"),
		("16","4"),
		("17","4"),
		("18","4"),
		("19","13"),
		("20","13"),
		("21","13"),
		("22","16"),
		("23","16"),
		("24","25"),
		("25","18"),
		("26","10"),
		("29","5"),
		("30","36"),
		("31","25"),
		("32","24"),
		("33","31"),
		("34","33"),
		("35","29"),
		("36","29"),
		("37","33"),
		("38","27"),
		("39","12"),
		("40","12"),
		("41","4"),
		("42","4"),
		("43","13"),
		("44","16")
		]

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			if self.path:
				for pair in self.usericons:
					if pair[0] == str(self.source.text):
						break
				self.pngname = self.userpath + pair[1] + '.png'
				if not fileExists(self.pngname):
					self.pngname = '/usr/share/enigma2/KravenHD/' + self.path + '/' + str(self.source.text) + '.png'
					if not fileExists(self.pngname):
						self.pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
				self.instance.setScale(1)
				self.instance.setPixmapFromFile(self.pngname)
