#
#  MiniTVDisplay - Converter
#
#  Coded by Dr.Best (c) 2010
#  Support: www.dreambox-tools.info
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.

#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#

from Components.Converter.Converter import Converter
from enigma import eServiceReference, eServiceCenter, getBestPlayableServiceReference, iServiceInformation

class KravenHDMiniTVDisplay(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.pipservice = None
		self.currentRunningService = None
		self.shown = False
		# check if we can use the PipServiceRelation plugin
		try:
			from Plugins.SystemPlugins.PiPServiceRelation.plugin import getRelationDict
			self.pipServiceRelation = getRelationDict()
		except ImportError:
			self.pipServiceRelation = None

	def setPiPService(self):
		if self.shown:
			service = self.source.getCurrentService()
			if self.currentRunningService is None or self.pipservice is None:
				self.currentRunningService = service
			# check, if tuner with the service is available
			service_center = eServiceCenter.getInstance()
			info = service_center.info(service)
			if info and info.isPlayable(service, self.currentRunningService):
				if service and (service.flags & eServiceReference.isGroup):
					ref = getBestPlayableServiceReference(service, eServiceReference())
				else:
					ref = service
				if ref and not (ref.flags & (eServiceReference.isMarker|eServiceReference.isDirectory)):
					if self.pipServiceRelation is not None:
						n_service = self.pipServiceRelation.get(ref.toString(),None)
						if n_service is not None:
							self.pipservice = eServiceCenter.getInstance().play(eServiceReference(n_service))
						else:
							self.pipservice = eServiceCenter.getInstance().play(ref)
					else:
						self.pipservice = eServiceCenter.getInstance().play(ref)
					if self.pipservice and not self.pipservice.setTarget(1):
						self.pipservice.start()
						return True
		self.pipservice = None
		return False

	def closePiPService(self):
		if self.pipservice:
			self.pipservice = None
