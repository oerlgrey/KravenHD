# -*- coding: utf-8 -*-

#  Color Info Converter
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
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Components.Converter.Poll import Poll

class KravenHDColorInfo(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)

		self.type = str(type)

		self.poll_interval = 1000
		self.poll_enabled = True
	
	@cached
	def getText(self):
		hexcolor = str(hex(config.plugins.KravenHD.SelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenHD.SelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenHD.SelfColorB.value)[2:4]).zfill(2)
		return "#" + hexcolor
	
	text = property(getText)

	def changed(self, what):
		if what[0] is self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] is self.CHANGED_POLL:
			self.downstream_elements.changed(what)
