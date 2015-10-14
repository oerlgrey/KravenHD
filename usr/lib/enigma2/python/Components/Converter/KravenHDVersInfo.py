#
#  Version Converter
#
#  Coded by tomele for Kraven Skins
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#

from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class KravenHDVersInfo(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = str(type)
	
	@cached
	def getText(self):
		line=""
		version=""
		os.popen("opkg info enigma2-plugin-skins-kravenhd > /tmp/KravenVersion")
		for line in open("/tmp/KravenVersion"):
			if "Version:" in line:
				version=line
		return version
	
	text = property(getText)
