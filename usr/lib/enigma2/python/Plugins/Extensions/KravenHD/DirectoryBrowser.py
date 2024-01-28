# -*- coding: utf-8 -*-

#  Directory Browser
#
#  Coded/Modified/Adapted by oerlgrey
#  Based on openATV image source code
#  Thankfully inspired by MyMetrix by iMaxxx
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

from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.FileList import FileList
from Components.Sources.StaticText import StaticText
import gettext
from enigma import getDesktop
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Language import language
from os import environ

#############################################################

DESKTOP_WIDTH = getDesktop(0).size().width()

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("KravenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/KravenHD/locale/"))

def _(txt):
	t = gettext.dgettext("KravenHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

#############################################################

class KravenHDBrowser(Screen):
	if DESKTOP_WIDTH <= 1280:
		skin = """
<screen name="KravenHDBrowser" position="center,center" size="800,600" backgroundColor="#00000000">
  <widget backgroundColor="#00000000" source="info" render="Label" font="Regular;24" foregroundColor="#00f0a30a" position="14,14" size="772,30" transparent="1" />
  <widget backgroundColor="#00000000" name="list" font="Regular;22" foregroundColor="#00ffffff" itemHeight="30" position="14,58" size="772,390" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="instruction" render="Label" font="Regular;22" foregroundColor="#00f0a30a" position="14,460" size="772,60" halign="center" valign="center" transparent="1" />
  <widget backgroundColor="#00000000" source="key_red" render="Label" font="Regular;20" foregroundColor="#00ffffff" position="19,546" size="220,26" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_green" render="Label" font="Regular;20" foregroundColor="#00ffffff" position="269,546" size="220,26" valign="center" transparent="1" zPosition="1" />
  <eLabel backgroundColor="#00E61805" position="14,573" size="150,5" />
  <eLabel backgroundColor="#005FE500" position="264,573" size="150,5" />
</screen>
"""
	else:
		skin = """
<screen name="KravenHDBrowser" position="center,center" size="1200,900" backgroundColor="#00000000">
  <widget backgroundColor="#00000000" source="info" render="Label" font="Regular;35" foregroundColor="#00f0a30a" position="21,21" size="1158,45" transparent="1" />
  <widget backgroundColor="#00000000" name="list" font="Regular;32" foregroundColor="#00ffffff" itemHeight="45" position="21,87" size="1158,585" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="instruction" render="Label" font="Regular;32" foregroundColor="#00f0a30a" position="21,690" size="1158,90" halign="center" valign="center" transparent="1" />
  <widget backgroundColor="#00000000" source="key_red" render="Label" font="Regular;30" foregroundColor="#00ffffff" position="29,818" size="330,39" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_green" render="Label" font="Regular;30" foregroundColor="#00ffffff" position="404,818" size="330,39" valign="center" transparent="1" zPosition="1" />
  <eLabel backgroundColor="#00E61805" position="21,859" size="225,7" />
  <eLabel backgroundColor="#005FE500" position="396,859" size="225,7" />
</screen>
"""

	def __init__(self, session, title):
		Screen.__init__(self, session)
		Screen.setTitle(self, title)

		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"],
		{
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"green": self.save,
			"ok": self.keyOK,
			"red": self.exit,
			"cancel": self.exit
		}, -2)

		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText()
		self["list"] = FileList("/media/", showFiles=False, matchingPattern="")
		self["info"] = StaticText()
		self["instruction"] = StaticText(_("The full path can be seen in the preview text."))
		self.showInfo()

	def showInfo(self):
		try:
			folder = self["list"].getSelection()[0].rsplit("/", 1)[0]
			if folder:
				if self["list"].canDescent():
					self["info"].setText(folder)
					self["key_green"].setText(_("apply path"))
				else:
					self["info"].setText(_("The path is not available"))
					self["key_green"].setText("")
			else:
				self["info"].setText(_("The path is not available"))
				self["key_green"].setText("")
		except:
			self["info"].setText(_("The path is not available"))
			self["key_green"].setText("")

	def keyLeft(self):
		self["list"].pageUp()
		self.showInfo()

	def keyRight(self):
		self["list"].pageDown()
		self.showInfo()

	def keyUp(self):
		self["list"].up()
		self.showInfo()

	def keyDown(self):
		self["list"].down()
		self.showInfo()

	def keyOK(self):
		if self["list"].canDescent():
			self["list"].descent()
		self.showInfo()

	def save(self):
		if not self["info"].text == _("The path is not available"):
			try:
				folder = self["list"].getSelection()[0].rsplit('/', 1)[0]
				if self["list"].canDescent():
					self.close(folder)
				return
			except:
				return

	def exit(self):
		self.close(None)
		return
