#
#  MiniTV - Renderer
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

from Renderer import Renderer
from enigma import eVideoWidget, getDesktop, eTimer
from Components.SystemInfo import SystemInfo

class KravenHDMiniTV(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.Position = self.Size = None
		self.pipavailable = (SystemInfo.get("NumVideoDecoders", 1) > 1)
		self.timer = eTimer()	        
		try:
			self.timer_connection = self.timer.timeout.connect(self.activatePiP)
		except AttributeError:
			self.timer.callback.append(self.activatePiP)
		self.currentPiPService = None
		self.currentPiPServicePath = None

	GUI_WIDGET = eVideoWidget

	def postWidgetCreate(self, instance):
		desk = getDesktop(0)
		instance.setFBSize(desk.size())

	def changed(self, what):
		if self.pipavailable:
			self.timer.stop()
			self.source.closePiPService()
			if self.instance:
				self.instance.hide()
			self.timer.start(500)

	def activatePiP(self):
		self.timer.stop()
		if self.source.setPiPService():
			self.instance.show()
		else:
			self.instance.hide()

	def applySkin(self, desktop, parent):
		ret = Renderer.applySkin(self, desktop, parent)
		if ret:
			self.Position = self.instance.position()
			self.Size = self.instance.size()
		return ret

	def onShow(self):
		self.source.shown = True
		if self.instance:
			if self.pipavailable:
				from Screens.InfoBar import InfoBar
				infobarinstance = InfoBar.instance
				if infobarinstance.session.pipshown: # check if PiP is already shown
					self.currentPiPService = infobarinstance.session.pip.getCurrentService() # need current service
					self.currentPiPServicePath = infobarinstance.session.pip.servicePath # and current service path for reactivating
					infobarinstance.showPiP() # it is, close it!
				if self.Size:
					self.instance.resize(self.Size)
				if self.Position:
					self.instance.move(self.Position)
				self.timer.start(500)
			else:
				self.instance.hide()

	def onHide(self):
		self.timer.stop()
		self.source.shown = False
		self.source.closePiPService()
		if self.instance:
			self.preWidgetRemove(self.instance)
		# check if PiP was runnung before
		if self.currentPiPService is not None and self.currentPiPServicePath is not None:
			# PiP was running, so enabled it 
			from Screens.InfoBar import InfoBar
			from Screens.PictureInPicture import PictureInPicture
			infobarinstance = InfoBar.instance
			infobarinstance.session.pip = infobarinstance.session.instantiateDialog(PictureInPicture)
			infobarinstance.session.pip.show()
			if infobarinstance.session.pip.playService(self.currentPiPService):
				infobarinstance.session.pipshown = True
				infobarinstance.session.pip.servicePath = self.currentPiPServicePath
			else:
				infobarinstance.session.pipshown = False
				del infobarinstance.session.pip
		self.currentPiPService = None
		self.currentPiPServicePath = None
