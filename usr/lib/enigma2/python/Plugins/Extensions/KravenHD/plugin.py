#######################################################################
#
#    MyMetrix
#    Coded by iMaxxx (c) 2013
#    KravenHD by Kraven
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
#
#######################################################################

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext
from enigma import ePicLoad
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS

#############################################################

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

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block


#############################################################

config.plugins.KravenHD = ConfigSubsection()

                 #Image

config.plugins.KravenHD.Image = ConfigSelection(default="main-custom-openatv", choices = [
				("main-custom-atemio4you", _("Atemio4You")),
				("main-custom-hdmu", _("HDMU")),
				("main-custom-openatv", _("openATV")),
				("main-custom-openhdf", _("openHDF")),
				("main-custom-openmips", _("openMIPS"))
				])

				#Color

config.plugins.KravenHD.SkinColor = ConfigSelection(default="00a19181", choices = [
				("00F0A30A", _("Amber")),
				("005696d2", _("Blue")),
				("00825A2C", _("Brown")),
				("000050EF", _("Cobalt")),
				("00911d10", _("Crimson")),
				("001BA1E2", _("Cyan")),
				("00a19181", _("Kraven")),
				("00a61d4d", _("Magenta")),
				("00A4C400", _("Lime")),
				("006A00FF", _("Indigo")),
				("0070ad11", _("Green")),
				("00008A00", _("Emerald")),
				("0076608A", _("Mauve")),
				("006D8764", _("Olive")),
				("00c3461b", _("Orange")),
				("00F472D0", _("Pink")),
				("00E51400", _("Red")),
				("007A3B3F", _("Sienna")),
				("00647687", _("Steel")),
				("00149baf", _("Teal")),
				("006c0aab", _("Violet")),
				("00bf9217", _("Yellow"))
				])
				
config.plugins.KravenHD.SkinColorProgress = ConfigSelection(default="05a19181", choices = [
				("05F0A30A", _("Amber")),
				("06F0A30A", _("Amber/White")),
				("055696d2", _("Blue")),
				("06007eff", _("Blue/White")),
				("05825A2C", _("Brown")),
				("06825A2C", _("Brown/White")),
				("050050EF", _("Cobalt")),
				("060050EF", _("Cobalt/White")),
				("05911d10", _("Crimson")),
				("06911d10", _("Crimson/White")),
				("051BA1E2", _("Cyan")),
				("061BA1E2", _("Cyan/White")),
				("060F6EB2", _("Dodger Blue/White")),
				("05a19181", _("Kraven")),
				("05352111", _("Colorfull")),
				("05a61d4d", _("Magenta")),
				("06a61d4d", _("Magenta/White")),
				("05A4C400", _("Lime")),
				("06A4C400", _("Lime/White")),
				("056A00FF", _("Indigo")),
				("066A00FF", _("Indigo/White")),
				("0570ad11", _("Green")),
				("0670ad11", _("Green/White")),
				("05008A00", _("Emerald")),
				("06008A00", _("Emerald/White")),
				("0576608A", _("Mauve")),
				("0676608A", _("Mauve/White")),
				("050047D4", _("Medium Blue")),
				("060047D4", _("Medium Blue/White")),
				("056D8764", _("Olive")),
				("066D8764", _("Olive/White")),
				("05c3461b", _("Orange")),
				("06c3461b", _("Orange/White")),
				("05F472D0", _("Pink")),
				("06F472D0", _("Pink/White")),
				("05E51400", _("Red")),
				("06E51400", _("Red/White")),
				("057A3B3F", _("Sienna")),
				("067A3B3F", _("Sienna/White")),
				("05647687", _("Steel")),
				("06647687", _("Steel/White")),
				("05149baf", _("Teal")),
				("06149baf", _("Teal/White")),
				("056c0aab", _("Violet")),
				("066c0aab", _("Violet/White")),
				("05ffffff", _("White")),
				("06000001", _("White/Grey")),
				("05bf9217", _("Yellow")),
				("06bf9217", _("Yellow/White"))
				])

config.plugins.KravenHD.SelectionBackground = ConfigSelection(default="00200E04", choices = [
				("30F0A30A", _("Amber transparency")),
                ("00F0A30A", _("Amber")),				
				("30007eff", _("Blue transparency")),
				("00007eff", _("Blue")),
				("30825A2C", _("Brown transparency")),
				("00825A2C", _("Brown")),
				("300050EF", _("Cobalt transparency")),
				("000050EF", _("Cobalt")),
				("30911d10", _("Crimson transparency")),
				("00911d10", _("Crimson")),
				("301BA1E2", _("Cyan transparency")),
				("001BA1E2", _("Cyan")),
				("300F6EB2", _("Dodger Blue transparency")),
				("000F6EB2", _("Dodger Blue")),
				("30a61d4d", _("Magenta transparency")),
				("00a61d4d", _("Magenta")),
				("30200E04", _("KravenHD transparency")),
				("00200E04", _("KravenHD")),
				("30A4C400", _("Lime transparency")),
				("00A4C400", _("Lime")),
				("306A00FF", _("Indigo transparency")),
				("006A00FF", _("Indigo")),
				("3070ad11", _("Green transparency")),
				("0070ad11", _("Green")),
				("30008A00", _("Emerald transparency")),
				("00008A00", _("Emerald")),
				("3076608A", _("Mauve transparency")),
				("0076608A", _("Mauve")),
				("300047D4", _("Medium Blue transparency")),
				("000047D4", _("Medium Blue")),
				("306D8764", _("Olive transparency")),
				("006D8764", _("Olive")),
				("30c3461b", _("Orange transparency")),
				("00c3461b", _("Orange")),
				("30F472D0", _("Pink transparency")),
				("00F472D0", _("Pink")),
				("30E51400", _("Red transparency")),
				("00E51400", _("Red")),
				("307A3B3F", _("Sienna transparency")),
				("007A3B3F", _("Sienna")),
				("30647687", _("Steel transparency")),
				("00647687", _("Steel")),
				("30149baf", _("Teal transparency")),
				("00149baf", _("Teal")),
				("306c0aab", _("Violet transparency")),
				("006c0aab", _("Violet")),
				("30bf9217", _("Yellow transparency")),
				("00bf9217", _("Yellow"))
				])
				
config.plugins.KravenHD.SkinBackgroundColor = ConfigSelection(default="2028150B", choices = [
				("00000338", _("Blue 0%")),
				("0D000338", _("Blue 5%")),
				("1A000338", _("Blue 10%")),
				("20000338", _("Blue 15%")),
				("00000000", _("Black 0%")),
				("0D000000", _("Black 5%")),
				("1A000000", _("Black 10%")),
				("20000000", _("Black 15%")),
				("00011600", _("Green 0%")),
				("0D011600", _("Green 5%")),
				("1A011600", _("Green 10%")),
				("20011600", _("Green 15%")),
				("00210038", _("Violet 0%")),
				("0D210038", _("Violet 5%")),
				("1A210038", _("Violet 10%")),
				("20210038", _("Violet 15%")),
				("00330500", _("Red 0%")),
				("0D330500", _("Red 5%")),
				("1A330500", _("Red 10%")),
				("20330500", _("Red 15%")),
				("0028150B", _("Kraven 0%")),
				("0D28150B", _("Kraven 5%")),
				("1A28150B", _("Kraven 10%")),
				("2028150B", _("Kraven 15%"))
				])
				
config.plugins.KravenHD.SkinColorInfobar = ConfigSelection(default="11000000", choices = [
				("11000338", _("Blue")),
				("11000000", _("Black")),
				("11011600", _("Green")),
				("11210038", _("Violet")),
				("11330500", _("Red")),
				("1128150B", _("Kraven"))
				])
				
	            #General
							
config.plugins.KravenHD.VolumeStyle = ConfigSelection(default="volume-classic", choices = [
				("volume-classic", _("Classic")),
				("volume-cycle-center", _("CycleMod center")),
				("volume-cycle-left", _("CycleMod left")),
				("volume-army", _("Army")),
				("volume-stony", _("Stony")),
				("volume-concinnity", _("Concinnity"))
				])
				
config.plugins.KravenHD.SecondInfobarStyle = ConfigSelection(default="secondinfobar-style-xpicon", choices = [
				("secondinfobar-style-zpicon", _("ZPicons")),
				("secondinfobar-style-xpicon", _("XPicons")),
				("secondinfobar-style-zzpicon", _("ZZPicons")),
				("secondinfobar-style-zzzpicon", _("ZZZPicons"))
				])
				
config.plugins.KravenHD.NumberZapExtStyle = ConfigSelection(default="numberzapext-none", choices = [
				("numberzapext-none", _("Off")),
				("numberzapext-zpicon", _("ZPicons")),
				("numberzapext-xpicon", _("XPicons")),
				("numberzapext-zzpicon", _("ZZPicons")),
				("numberzapext-zzzpicon", _("ZZZPicons"))
				])
				
config.plugins.KravenHD.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("MiniTV")),
				("cooltv-picon", _("Picon"))
				])
							
config.plugins.KravenHD.ChannelSelectionStyle = ConfigSelection(default="channelselection-style-nopicon", choices = [
				("channelselection-style-nopicon", _("No Picon")),
				("channelselection-style-zpicon", _("ZPicons")),
				("channelselection-style-xpicon", _("XPicons")),
				("channelselection-style-zzpicon", _("ZZPicons")),
				("channelselection-style-zzzpicon", _("ZZZPicons")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-minitv", _("MiniTV")),
				("channelselection-style-minitv2", _("MiniTV/PIP")),
				("channelselection-style-minitv22", _("MiniTV/PIP 2")),
				("channelselection-style-minitv3", _("PIP"))
				])
				
config.plugins.KravenHD.EMCStyle = ConfigSelection(default="emc-nocover", choices = [
				("emc-nocover", _("No Cover")),
				("emc-smallcover", _("Small Cover")),				
				("emc-bigcover", _("Big Cover")),
				("emc-verybigcover", _("Very Big Cover"))	,
				("emc-minitv", _("MiniTV"))
				])	
				
				#InfoBar
config.plugins.KravenHD.InfobarStyle = ConfigSelection(default="infobar-style-x3", choices = [
				("infobar-style-z1", _("Z1")),
				("infobar-style-z2", _("Z2")),
				("infobar-style-x1", _("X1")),
				("infobar-style-x2", _("X2")),
				("infobar-style-x3", _("X3")),
				("infobar-style-zz1", _("ZZ1")),
				("infobar-style-zz2", _("ZZ2")),
				("infobar-style-zz3", _("ZZ3")),
				("infobar-style-zz4", _("ZZ4")),
				("infobar-style-zzz1", _("ZZZ1"))
				])	

config.plugins.KravenHD.InfobarShowChannelname = ConfigSelection(default="infobar-channelname-none", choices = [
				("infobar-channelname-none", _("Off")),	
				("infobar-channelname-z1", _("Name for Z1+Z2 Infobar")),
				("infobar-channelname-small-z1", _("Name small for Z1+Z2 Infobar")),
                ("infobar-channelname-number-z1", _("Name and Number for Z1+Z2 Infobar")),	
                ("infobar-channelname-number-small-z1", _("Name and Number small for Z1+Z2 Infobar")),				
				("infobar-channelname-x1", _("Name for X1 Infobar")),
				("infobar-channelname-small-x1", _("Name small for X1 Infobar")),
				("infobar-channelname-number-x1", _("Name and Number for X1 Infobar")),	
				("infobar-channelname-number-small-x1", _("Name and Number small for X1 Infobar")),	
				("infobar-channelname-x2", _("Name for X2+X3 Infobar")),
                ("infobar-channelname-small-x2", _("Name small for X2+X3 Infobar")),				
				("infobar-channelname-number-x2", _("Name and Number for X2+X3 Infobar")),	
                ("infobar-channelname-number-small-x2", _("Name and Number small for X2+X3 Infobar")),				
				("infobar-channelname-zz1", _("Name for ZZ1 Infobar")),
				("infobar-channelname-small-zz1", _("Name small for ZZ1 Infobar")),
				("infobar-channelname-number-zz1", _("Name and Number for ZZ1 Infobar")),	
				("infobar-channelname-number-small-zz1", _("Name and Number small for ZZ1 Infobar")),
                ("infobar-channelname-zz2", _("Name for ZZ2+ZZ3 Infobar")),
				("infobar-channelname-number-zz2", _("Name and Number for ZZ2+ZZ3 Infobar")),
				("infobar-channelname-zz4", _("Name for ZZ4 Infobar")),
				("infobar-channelname-small-zz4", _("Name small for ZZ4 Infobar")),
				("infobar-channelname-number-zz4", _("Name and Number for ZZ4 Infobar")),
				("infobar-channelname-number-small-zz4", _("Name and Number small for ZZ4 Infobar")),
				("infobar-channelname-zzz1", _("Name for ZZZ1 Infobar")),
				("infobar-channelname-number-zzz1", _("Name and Number for ZZZ1 Infobar"))
				])				

config.plugins.KravenHD.InfobarWeatherWidget = ConfigSelection(default="infobar-weather-none", choices = [
				("infobar-weather-none", _("Off")),				
				("infobar-weather-classic", _("Classic not for Z1+X2 Infobar")),				
				("infobar-weather-original", _("Original")),
				("infobar-weather-big", _("Big not for Z1+X2 Infobar"))
				])	
			
config.plugins.KravenHD.InfobarClockWidget = ConfigSelection(default="infobar-clock-classic", choices = [
				("infobar-clock-android", _("Android")),
				("infobar-clock-analog", _("Analog")),
				("infobar-clock-classic", _("Classic")),
				("infobar-clock-classic-big", _("Classic Big")),
				("infobar-clock-color", _("Classic colored")),
				("infobar-clock-none", _("Off for ZZ4 Infobar"))
				])
				
config.plugins.KravenHD.InfobarSatInfo = ConfigSelection(default="infobar-satinfo-off", choices = [
				("infobar-satinfo-on", _("On")),
				("infobar-satinfo-off", _("Off"))
				])
				
config.plugins.KravenHD.InfobarSystemInfo = ConfigSelection(default="infobar-systeminfo-off", choices = [
				("infobar-systeminfo-big", _("Big")),
				("infobar-systeminfo-small", _("Small")),
				("infobar-systeminfo-off", _("Off"))
				])
				
config.plugins.KravenHD.InfobarECMInfo = ConfigSelection(default="infobar-ecminfo-none", choices = [
				("infobar-ecminfo-small-z1", _("Small for Z1+Z2 Infobar")),
				("infobar-ecminfo-z1", _("Big for Z1+Z2 Infobar")),
				("infobar-ecminfo-small-x1", _("Small for X1 Infobar")),
				("infobar-ecminfo-x1", _("Big for X1 Infobar")),
				("infobar-ecminfo-small-x2", _("Small for X2+X3 Infobar")),
				("infobar-ecminfo-x2", _("Big for X2+X3 Infobar")),	
				("infobar-ecminfo-small-zz1", _("Small for ZZ1 Infobar")),
				("infobar-ecminfo-zz1", _("Big for ZZ1 Infobar")),
				("infobar-ecminfo-small-zz2", _("Small for ZZ2+ZZ3 Infobar")),
				("infobar-ecminfo-zz2", _("Big for ZZ2+ZZ3 Infobar")),
				("infobar-ecminfo-small-zz4", _("Small for ZZ4 Infobar")),
				("infobar-ecminfo-zz4", _("Big for ZZ4 Infobar")),
				("infobar-ecminfo-small-zzz1", _("Small for ZZZ1 Infobar")),
				("infobar-ecminfo-zzz1", _("Big for ZZZ1 Infobar")),
				("infobar-ecminfo-none", _("Off"))				
                ])
#######################################################################

class KravenHD(ConfigListScreen, Screen):
	skin = """
<screen name="KravenHD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
  <eLabel font="Regular; 20" foregroundColor="foreground" backgroundColor="KravenPreBlack2" halign="left" position="37,667" size="250,24" text="Cancel" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="foreground" backgroundColor="KravenPreBlack2" halign="left" position="335,667" size="250,24" text="Save" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="foreground" backgroundColor="KravenPreBlack2" halign="left" position="643,667" size="250,24" text="Reboot" transparent="1" />
  <widget name="config" position="29,14" scrollbarMode="showOnDemand" size="590,632" transparent="1" />
  <eLabel position="738,15" size="349,43" text="KravenHD" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="KravenPreBlack2" />
  <eLabel position="738,58" size="349,43" text="Version: 5.7.4" foregroundColor="foreground" font="Regular; 35" valign="center" backgroundColor="KravenPreBlack2" transparent="1" halign="center" />
  <widget name="helperimage" position="635,173" size="550,309" zPosition="1" backgroundColor="KravenPreBlack2" />
  <eLabel backgroundColor="BackgroundKraven" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
  <ePixmap position="0,0" size="1280,149" zPosition="-9" pixmap="KravenHD/infobar/ibaro.png" alphatest="blend" />
  <ePixmap position="0,555" size="1280,170" zPosition="-9" pixmap="KravenHD/infobar/ibar.png" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_red1.png" position="32,692" size="200,5" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_green1.png" position="330,692" size="200,5" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_yellow1.png" position="638,692" size="200,5" alphatest="blend" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.datei = "/usr/share/enigma2/KravenHD/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/"
		self.komponente = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/comp/"
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		list = []
		list.append(getConfigListEntry(_("----------------------------- Image  --------------------------------"), ))
		list.append(getConfigListEntry(_("Image"), config.plugins.KravenHD.Image))
		list.append(getConfigListEntry(_("----------------------------- Color  --------------------------------"), ))
		list.append(getConfigListEntry(_("Font"), config.plugins.KravenHD.SkinColor))
		list.append(getConfigListEntry(_("Listselection"), config.plugins.KravenHD.SelectionBackground))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.KravenHD.SkinColorProgress))
		list.append(getConfigListEntry(_("Background-/Transparency"), config.plugins.KravenHD.SkinBackgroundColor))
		list.append(getConfigListEntry(_("Infobar"), config.plugins.KravenHD.SkinColorInfobar))
		list.append(getConfigListEntry(_("----------------------------- General  --------------------------------"), ))
		list.append(getConfigListEntry(_("Channel Selection"), config.plugins.KravenHD.ChannelSelectionStyle))
		list.append(getConfigListEntry(_("EMC"), config.plugins.KravenHD.EMCStyle))		
		list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenHD.SecondInfobarStyle))
		list.append(getConfigListEntry(_("ExtNumberZap"), config.plugins.KravenHD.NumberZapExtStyle))
		list.append(getConfigListEntry(_("Volume"), config.plugins.KravenHD.VolumeStyle))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.KravenHD.CoolTVGuide))
		list.append(getConfigListEntry(_("----------------------------- InfoBar  --------------------------------"), ))
		list.append(getConfigListEntry(_("InfobarStyle"), config.plugins.KravenHD.InfobarStyle))
		list.append(getConfigListEntry(_("ECM Info"), config.plugins.KravenHD.InfobarECMInfo))
		list.append(getConfigListEntry(_("Sat Info"), config.plugins.KravenHD.InfobarSatInfo))
		list.append(getConfigListEntry(_("System Info"), config.plugins.KravenHD.InfobarSystemInfo))
		list.append(getConfigListEntry(_("Channel Name"), config.plugins.KravenHD.InfobarShowChannelname))
		list.append(getConfigListEntry(_("Clock"), config.plugins.KravenHD.InfobarClockWidget))
		list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.InfobarWeatherWidget))

		ConfigListScreen.__init__(self, list)
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)
		self.onLayoutFinish.append(self.UpdatePicture)

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/" + returnValue + ".jpg"
			return path
		except:
			return "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/Kravenweather.jpg"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#002C2C39"])
		self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["helperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.ShowPicture()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.ShowPicture()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.ShowPicture()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.ShowPicture()

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def showInfo(self):
		self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

	def getDataByKey(self, list, key):
		for item in list:
			if item["key"] == key:
				return item
		return list[0]

	def getFontStyleData(self, key):
		return self.getDataByKey(channelselFontStyles, key)

	def getFontSizeData(self, key):
		return self.getDataByKey(channelInfoFontSizes, key)

	def save(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		try:
			#global tag search and replace in all skin elements
			self.skinSearchAndReplace = []
			self.skinSearchAndReplace.append(["2028150B", config.plugins.KravenHD.SkinBackgroundColor.value])
			self.skinSearchAndReplace.append(["005696d2", config.plugins.KravenHD.SkinColor.value])
			self.skinSearchAndReplace.append(["00200E04", config.plugins.KravenHD.SelectionBackground.value])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbarv2 = ("p_barv2_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_barv2.png", self.pbarv2])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbarv3 = ("p_barv3_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_barv3.png", self.pbarv3])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbarv1 = ("p_barv1_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_barv1.png", self.pbarv1])
			
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbar153 = ("p_bar153_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_bar153.png", self.pbar153])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbar220 = ("p_bar220_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_bar220.png", self.pbar220])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbar355 = ("p_bar355_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_bar355.png", self.pbar355])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbar410 = ("p_bar410_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_bar410.png", self.pbar410])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbar581 = ("p_bar581_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_bar581.png", self.pbar581])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbar750 = ("p_bar750_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_bar750.png", self.pbar750])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbar990 = ("p_bar990_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_bar990.png", self.pbar990])
			
			self.skincolorprogresscolor = config.plugins.KravenHD.SkinColorProgress.value
			self.pbarv = ("p_barv_" + self.skincolorprogresscolor + ".png")
			self.skinSearchAndReplace.append(["p_barv.png", self.pbarv])
			
			self.skincolorinfobarcolor = config.plugins.KravenHD.SkinColorInfobar.value
			self.ibar = ("ibar_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibar.png", self.ibar])
			
			self.skincolorinfobarcolor = config.plugins.KravenHD.SkinColorInfobar.value
			self.ibar2 = ("ibar2_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibar2.png", self.ibar2])
			
			self.skincolorinfobarcolor = config.plugins.KravenHD.SkinColorInfobar.value
			self.ibar3 = ("ibar3_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibar3.png", self.ibar3])
			
			self.skincolorinfobarcolor = config.plugins.KravenHD.SkinColorInfobar.value
			self.ibaro = ("ibaro_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibaro.png", self.ibaro])
			
			self.skincolorinfobarcolor = config.plugins.KravenHD.SkinColorInfobar.value
			self.ibaro2 = ("ibaro2_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibaro2.png", self.ibaro2])
			
			
				
		  
			###Header XML
			self.appendSkinFile(self.daten + "header.xml")
			
			###InfoBar
			self.appendSkinFile(self.daten + "infobar-header.xml")

			#InfobarStyle
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarStyle.value + ".xml")
			
			#WeatherWidget
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarWeatherWidget.value + ".xml")
			
			#ClockWidget
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarClockWidget.value + ".xml")
			#Sat Info
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarSatInfo.value + ".xml")
			#System Info
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarSystemInfo.value + ".xml")
            #ECMInfo
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarECMInfo.value + ".xml")			
			#ChannelName
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarShowChannelname.value + ".xml")		
			#Footer
			self.appendSkinFile(self.daten + "screen-footer.xml")				
			
			#EMCSTYLE
			self.appendSkinFile(self.daten + config.plugins.KravenHD.EMCStyle.value +".xml")			
			
			#SecondInfobarStyle
			self.appendSkinFile(self.daten + config.plugins.KravenHD.SecondInfobarStyle.value + ".xml")
			
            #NumberZapExtStyle
			self.appendSkinFile(self.daten + config.plugins.KravenHD.NumberZapExtStyle.value + ".xml")
			
			#VolumeStyle
			self.appendSkinFile(self.daten + config.plugins.KravenHD.VolumeStyle.value + ".xml")
			
            #Channel Selection
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ChannelSelectionStyle.value +".xml")	
		
			
			###Main XML
			self.appendSkinFile(self.daten + "main.xml")
			
			###plugins XML
			self.appendSkinFile(self.daten + "plugins.xml")
			
			###custom-main XML
			self.appendSkinFile(self.daten + config.plugins.KravenHD.Image.value + ".xml")
			
			###cooltv XML
			self.appendSkinFile(self.daten + config.plugins.KravenHD.CoolTVGuide.value + ".xml")
			
			###skin-user
			try:
				self.appendSkinFile(self.daten + "skin-user.xml")
			except:
				pass
			###skin-end
			self.appendSkinFile(self.daten + "skin-end.xml")

			xFile = open(self.dateiTMP, "w")
			for xx in self.skin_lines:
				xFile.writelines(xx)
			xFile.close()

			move(self.dateiTMP, self.datei)

			#system('rm -rf ' + self.dateiTMP)
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None):
		"""
		add skin file to main skin content

		appendFileName:
		 xml skin-part to add

		skinPartSearchAndReplace:
		 (optional) a list of search and replace arrays. first element, search, second for replace
		"""
		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()

		tmpSearchAndReplace = []

		if skinPartSearchAndReplace is not None:
			tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
		else:
			tmpSearchAndReplace = self.skinSearchAndReplace

		for skinLine in file_lines:
			for item in tmpSearchAndReplace:
				skinLine = skinLine.replace(item[0], item[1])
			self.skin_lines.append(skinLine)

	def restartGUI(self, answer):
		if answer is True:
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
					pass
		self.close()

#############################################################

def main(session, **kwargs):
	session.open(KravenHD,"/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/kravencolors.jpg")

def Plugins(**kwargs):
	return PluginDescriptor(name="KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)