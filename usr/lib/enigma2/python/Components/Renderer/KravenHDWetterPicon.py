# -*- coding: utf-8 -*-

#  Wetter Picon Renderer
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
from Components.Renderer.Renderer import Renderer 
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, resolveFilename 

class KravenHDWetterPicon(Renderer):

	__module__ = __name__
	def __init__(self):
		Renderer.__init__(self)
		self.pngname = ''
		self.userpath = "/usr/share/enigma2/Kraven-user-icons/"

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
				if fileExists(self.userpath + '3200.png'):
					self.pngname = self.userpath + str(self.source.text) + '.png'
				else:
					self.pngname = '/usr/share/enigma2/KravenHD/' + self.path + '/' + str(self.source.text) + '.png'
				if not fileExists(self.pngname):
					self.pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
				self.instance.setScale(1)
				self.instance.setPixmapFromFile(self.pngname)
