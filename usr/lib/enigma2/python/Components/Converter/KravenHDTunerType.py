# -*- coding: utf-8 -*-

#  Tuner Type Converter
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

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll
from enigma import iServiceInformation

class KravenHDTunerType(Poll, Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.poll_interval = 1000
		self.poll_enabled = True

	@cached
	def getBoolean(self):
	
		if self.type == "IsStream" and self.getServiceType() == "STREAM":
			return True
		
		return False
		
	boolean = property(getBoolean)
	
	@cached
	def getText(self):
	
		return self.getServiceType()
		
	text = property(getText)

	def getServiceType(self):
	
		type = "N/A"
		stream = False

		service = self.source.service
		info = service and service.info()

		if info:
			stream = service.streamed() is not None
			
		if stream:
			type = "STREAM"
		elif info:
			tpdata = info.getInfoObject(iServiceInformation.sTransponderData)
			if tpdata:
				type = tpdata.get("tuner_type", "")
			else:
				type = "STREAM"
			
			if type == "DVB-S" and tpdata.get("system", 0) == 1:
				type = "DVB-S2"

		return type
