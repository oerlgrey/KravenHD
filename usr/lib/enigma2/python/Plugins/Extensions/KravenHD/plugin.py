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
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext
from enigma import ePicLoad, getDesktop, eConsoleAppContainer
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
config.plugins.KravenHD.weather_city = ConfigNumber(default="676757")

config.plugins.KravenHD.Image = ConfigSelection(default="main-custom-openatv", choices = [
				("main-custom-atemio4you", _("Atemio4You")),
				("main-custom-hdmu", _("HDMU")),
				("main-custom-openatv", _("openATV")),
				("main-custom-openhdf", _("openHDF")),
				("main-custom-openmips", _("openMIPS")),
				("main-custom-opennfr", _("openNFR"))
				])
				
config.plugins.KravenHD.Volume = ConfigSelection(default="volume-border", choices = [
				("volume-original", _("Original")),
				("volume-border", _("with Border")),
				("volume-left", _("left")),
				("volume-right", _("right")),
				("volume-top", _("top")),
				("volume-center", _("center"))
				])
				
config.plugins.KravenHD.BackgroundColorTrans = ConfigSelection(default="0A", choices = [
				("0A", _("low")),
				("4A", _("medium")),
				("8C", _("high"))
				])
				
config.plugins.KravenHD.Background = ConfigSelection(default="000000", choices = [
				("F0A30A", _("Amber")),
				("B27708", _("Amber Dark")),
				("000000", _("Black")),
				("1B1775", _("Blue")),
				("0E0C3F", _("Blue Dark")),
				("7D5929", _("Brown")),
				("3F2D15", _("Brown Dark")),
				("0050EF", _("Cobalt")),
				("001F59", _("Cobalt Dark")),
				("1BA1E2", _("Cyan")),
				("0F5B7F", _("Cyan Dark")),
				("999999", _("Grey")),
				("3F3F3F", _("Grey Dark")),
				("70AD11", _("Green")),
				("213305", _("Green Dark")),
				("28150B", _("Kraven")),
				("6D8764", _("Olive")),
				("313D2D", _("Olive Dark")),
				("C3461B", _("Orange")),
				("892E13", _("Orange Dark")),
				("F472D0", _("Pink")),
				("723562", _("Pink Dark")),
				("E51400", _("Red")),
				("330400", _("Red Dark")),
				("647687", _("Steel")),
				("262C33", _("Steel Dark")),
				("6C0AAB", _("Violet")),
				("1F0333", _("Violet Dark")),
				("ffffff", _("White"))
				])
				
config.plugins.KravenHD.SkinColorInfobar = ConfigSelection(default="4A1B1775", choices = [
				("4AF0A30A", _("Amber")),
				("4AB27708", _("Amber Dark")),
				("4A000000", _("Black")),
				("4A1B1775", _("Blue")),
				("4A0E0C3F", _("Blue Dark")),
				("4A7D5929", _("Brown")),
				("4A3F2D15", _("Brown Dark")),
				("4A999999", _("Grey")),
				("4A3F3F3F", _("Grey Dark")),
				("4A70AD11", _("Green")),
				("4A213305", _("Green Dark")),
				("4A28150B", _("Kraven")),
				("4AC3461B", _("Orange")),
				("4A892E13", _("Orange Dark")),
				("4AF472D0", _("Pink")),
				("4A723562", _("Pink Dark")),
				("4AE51400", _("Red")),
				("4A330400", _("Red Dark")),
				("4A6C0AAB", _("Violet")),
				("4A1F0333", _("Violet Dark")),
				("4Affffff", _("White"))
				])
				
config.plugins.KravenHD.SelectionBackground = ConfigSelection(default="000050EF", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00ffffff", _("White"))
				])
				
config.plugins.KravenHD.Font1 = ConfigSelection(default="00fffff3", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00fffff3", _("White"))
				])
				
config.plugins.KravenHD.Font2 = ConfigSelection(default="00fffff4", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00fffff4", _("White"))
				])
				
config.plugins.KravenHD.SelectionFont = ConfigSelection(default="00fffff7", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00fffff7", _("White"))
				])
				
config.plugins.KravenHD.ButtonText = ConfigSelection(default="00fffff2", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00fffff2", _("White"))
				])
				
config.plugins.KravenHD.Border = ConfigSelection(default="00fffff1", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00fffff1", _("White")),
				("ff000000", _("Off"))
				])
				
config.plugins.KravenHD.Progress = ConfigSelection(default="00fffff6", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00fffff6", _("White"))
				])
				
config.plugins.KravenHD.Line = ConfigSelection(default="00fffff5", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00fffff5", _("White"))
				])
				
config.plugins.KravenHD.SelectionBorder = ConfigSelection(default="00ffffff", choices = [
				("00F0A30A", _("Amber")),
				("00B27708", _("Amber Dark")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("000E0C3F", _("Blue Dark")),
				("007D5929", _("Brown")),
				("003F2D15", _("Brown Dark")),
				("000050EF", _("Cobalt")),
				("00001F59", _("Cobalt Dark")),
				("001BA1E2", _("Cyan")),
				("000F5B7F", _("Cyan Dark")),
				("00999999", _("Grey")),
				("003F3F3F", _("Grey Dark")),
				("0070AD11", _("Green")),
				("00213305", _("Green Dark")),
				("0028150B", _("Kraven")),
				("006D8764", _("Olive")),
				("00313D2D", _("Olive Dark")),
				("00C3461B", _("Orange")),
				("00892E13", _("Orange Dark")),
				("00F472D0", _("Pink")),
				("00723562", _("Pink Dark")),
				("00E51400", _("Red")),
				("00330400", _("Red Dark")),
				("00647687", _("Steel")),
				("00262C33", _("Steel Dark")),
				("006C0AAB", _("Violet")),
				("001F0333", _("Violet Dark")),
				("00ffffff", _("White"))
				])
				
config.plugins.KravenHD.AnalogStyle = ConfigSelection(default="00999999", choices = [
				("00F0A30A", _("Amber")),
				("00000000", _("Black")),
				("001B1775", _("Blue")),
				("007D5929", _("Brown")),
				("000050EF", _("Cobalt")),
				("001BA1E2", _("Cyan")),
				("00999999", _("Grey")),
				("0070AD11", _("Green")),
				("00C3461B", _("Orange")),
				("00F472D0", _("Pink")),
				("00E51400", _("Red")),
				("00647687", _("Steel")),
				("006C0AAB", _("Violet")),
				("00ffffff", _("White"))
				])
				
config.plugins.KravenHD.InfobarStyle = ConfigSelection(default="infobar-style-x3", choices = [
				("infobar-style-x1", _("X1")),
				("infobar-style-x2", _("X2")),
				("infobar-style-x3", _("X3")),
				("infobar-style-z1", _("Z1")),
				("infobar-style-z2", _("Z2")),
				("infobar-style-zz1", _("ZZ1")),
				("infobar-style-zz2", _("ZZ2")),
				("infobar-style-zz3", _("ZZ3")),
				("infobar-style-zz4", _("ZZ4")),
				("infobar-style-zzz1", _("ZZZ1"))
				])
				
config.plugins.KravenHD.InfobarChannelName = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-channelname-small-x1", _("Name small")),
				("infobar-channelname-number-small-x1", _("Name & Number small")),
				("infobar-channelname-x1", _("Name big")),
				("infobar-channelname-number-x1", _("Name & Number big"))
				])
				
config.plugins.KravenHD.InfobarChannelName2 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-channelname-small-x2", _("Name small")),
				("infobar-channelname-number-small-x2", _("Name & Number small")),
				("infobar-channelname-x2", _("Name big")),
				("infobar-channelname-number-x2", _("Name & Number big"))
				])
				
config.plugins.KravenHD.InfobarChannelName3 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-channelname-small-z1", _("Name small")),
				("infobar-channelname-number-small-z1", _("Name & Number small")),
				("infobar-channelname-z1", _("Name big")),
				("infobar-channelname-number-z1", _("Name & Number big"))
				])
				
config.plugins.KravenHD.InfobarChannelName4 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-channelname-small-zz1", _("Name small")),
				("infobar-channelname-number-small-zz1", _("Name & Number small")),
				("infobar-channelname-zz1", _("Name big")),
				("infobar-channelname-number-zz1", _("Name & Number big"))
				])
				
config.plugins.KravenHD.InfobarChannelName5 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-channelname-zz2", _("Name")),
				("infobar-channelname-number-zz2", _("Name & Number"))
				])
				
config.plugins.KravenHD.InfobarChannelName6 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-channelname-small-zz4", _("Name small")),
				("infobar-channelname-number-small-zz4", _("Name & Number small")),
				("infobar-channelname-zz4", _("Name big")),
				("infobar-channelname-number-zz4", _("Name & Number big"))
				])
				
config.plugins.KravenHD.InfobarChannelName7 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-channelname-zzz1", _("Name")),
				("infobar-channelname-number-zzz1", _("Name & Number"))
				])
							
config.plugins.KravenHD.ChannelSelectionStyle = ConfigSelection(default="channelselection-style-minitv", choices = [
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
				
config.plugins.KravenHD.NumberZapExt = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("numberzapext-zpicon", _("ZPicons")),
				("numberzapext-xpicon", _("XPicons")),
				("numberzapext-zzpicon", _("ZZPicons")),
				("numberzapext-zzzpicon", _("ZZZPicons"))
				])
				
config.plugins.KravenHD.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("MiniTV")),
				("cooltv-picon", _("Picon"))
				])
				
config.plugins.KravenHD.EMCStyle = ConfigSelection(default="emc-minitv", choices = [
				("emc-nocover", _("No Cover")),
				("emc-smallcover", _("Small Cover")),
				("emc-bigcover", _("Big Cover")),
				("emc-verybigcover", _("Very Big Cover")),
				("emc-minitv", _("MiniTV"))
				])
				
config.plugins.KravenHD.RunningText = ConfigSelection(default="movetype=running", choices = [
				("movetype=running", _("On")),
				("movetype=none", _("Off"))
				])
# .:TBX:.
config.plugins.KravenHD.ClockStyle = ConfigSelection(default="clock-classic", choices = [
				("clock-classic", _("Standard")),
				("clock-classic-big", _("Standard big")),
				("clock-analog", _("Analog")),
				("clock-android", _("Android")),
				("clock-color", _("Color"))
				])
				
config.plugins.KravenHD.WeatherStyle = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("weather-big", _("Big")),
				("weather-small", _("Small"))
				])
				
config.plugins.KravenHD.WeatherStyle2 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("weather-left", _("On"))
				])
				
config.plugins.KravenHD.SatInfo = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("satinfo", _("On"))
				])
				
config.plugins.KravenHD.ECMInfo = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-ecminfo-x1", _("Bottom")),
				("ecminfo", _("Right"))
				])
				
config.plugins.KravenHD.ECMInfo2 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-ecminfo-x2", _("Bottom")),
				("ecminfo", _("Right"))
				])
				
config.plugins.KravenHD.ECMInfo3 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-ecminfo-zz1", _("Bottom")),
				("ecminfo", _("Right"))
				])
				
config.plugins.KravenHD.ECMInfo4 = ConfigSelection(default="none", choices = [
				("none", _("Off")),
				("infobar-ecminfo-zz2", _("Bottom")),
				("ecminfo", _("Right"))
				])
				
config.plugins.KravenHD.ButtonStyle = ConfigSelection(default="buttons_light", choices = [
				("buttons_light", _("Light")),
				("buttons_dark", _("Dark"))
				])
				
config.plugins.KravenHD.ButtonStyleFont = ConfigSelection(default="00fffff8", choices = [
				("00fffff8", _("Light")),
				("00373737", _("Dark"))
				])
				
config.plugins.KravenHD.FontStyle = ConfigSelection(default="NotoSans", choices = [
				("NotoSans", _("NotoSans")),
				("OpenSans", _("OpenSans"))
				])
				
#######################################################################

class KravenHD(ConfigListScreen, Screen):
	skin = """
<screen name="KravenHD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="70,665" size="220,26" text="Cancel" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="320,665" size="220,26" text="Save" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="570,665" size="220,26" text="Reboot" transparent="1" />
  <widget name="config" position="18,78" size="816,560" itemHeight="28" transparent="1" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="70,15" size="708,46" text="KravenHD - Konfigurationstool" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" name="," />
  <eLabel position="875,657" size="372,46" text="Thanks to http://www.gigablue-support.org/" font="Regular; 12" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" name="," />
  <eLabel position="877,278" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="877,487" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="875,278" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel position="1245,278" size="2,211" backgroundColor="#00f0a30a" />
  <widget name="helperimage" position="877,280" size="368,207" zPosition="1" valign="bottom" backgroundColor="#00000000" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
  <widget backgroundColor="#00000000" font="Regular2; 34" foregroundColor="#00ffffff" position="70,12" render="Label" size="708,46" source="Title" transparent="1" halign="center" valign="center" noWrap="1" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" foregroundColor="#00ffffff" />
  <ePixmap pixmap="KravenHD/buttons/key_red1.png" position="65,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_green1.png" position="315,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_yellow1.png" position="565,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <eLabel position="875,96" size="372,46" text="KravenHD" font="Regular2; 34" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" name="," />
  <eLabel position="875,156" size="372,46" text="Version: 6.0" font="Regular; 30" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
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
		ConfigListScreen.__init__(self, list)
		
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)
		self.UpdatePicture()
		self.onLayoutFinish.append(self.mylist)

	def mylist(self):
		list = []
		list.append(getConfigListEntry(_("______________________ System __________________________________"), ))
		list.append(getConfigListEntry(_("Image"), config.plugins.KravenHD.Image))
		list.append(getConfigListEntry(_("Font Style"), config.plugins.KravenHD.FontStyle))
		list.append(getConfigListEntry(_("Button Style"), config.plugins.KravenHD.ButtonStyle))
		list.append(getConfigListEntry(_("Background Transparency"), config.plugins.KravenHD.BackgroundColorTrans))
		list.append(getConfigListEntry(_("Running Text"), config.plugins.KravenHD.RunningText))
		list.append(getConfigListEntry(_("Weather ID"), config.plugins.KravenHD.weather_city))
		list.append(getConfigListEntry(_("______________________ Colors __________________________________"), ))
		list.append(getConfigListEntry(_("Line"), config.plugins.KravenHD.Line))
		list.append(getConfigListEntry(_("Infobar"), config.plugins.KravenHD.SkinColorInfobar))
		list.append(getConfigListEntry(_("Background"), config.plugins.KravenHD.Background))
		list.append(getConfigListEntry(_("Border"), config.plugins.KravenHD.Border))
		list.append(getConfigListEntry(_("Listselection"), config.plugins.KravenHD.SelectionBackground))
		list.append(getConfigListEntry(_("Listselection Border"), config.plugins.KravenHD.SelectionBorder))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.KravenHD.Progress))
		list.append(getConfigListEntry(_("Font 1"), config.plugins.KravenHD.Font1))
		list.append(getConfigListEntry(_("Font 2"), config.plugins.KravenHD.Font2))
		list.append(getConfigListEntry(_("Selection Font"), config.plugins.KravenHD.SelectionFont))
		list.append(getConfigListEntry(_("Button Text"), config.plugins.KravenHD.ButtonText))
		list.append(getConfigListEntry(_("______________________ Infobar __________________________________"), ))
		list.append(getConfigListEntry(_("Style"), config.plugins.KravenHD.InfobarStyle))
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("Channelname"), config.plugins.KravenHD.InfobarChannelName))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2":
			list.append(getConfigListEntry(_("Channelname"), config.plugins.KravenHD.InfobarChannelName2))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("Channelname"), config.plugins.KravenHD.InfobarChannelName3))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1":
			list.append(getConfigListEntry(_("Channelname"), config.plugins.KravenHD.InfobarChannelName4))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2":
			list.append(getConfigListEntry(_("Channelname"), config.plugins.KravenHD.InfobarChannelName5))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("Channelname"), config.plugins.KravenHD.InfobarChannelName6))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Channelname"), config.plugins.KravenHD.InfobarChannelName7))
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Clock"), config.plugins.KravenHD.ClockStyle))
		if config.plugins.KravenHD.ClockStyle.value == "clock-analog":
			list.append(getConfigListEntry(_("Clock Analog Color"), config.plugins.KravenHD.AnalogStyle))
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyle))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyle2))
		list.append(getConfigListEntry(_("Sat-Info"), config.plugins.KravenHD.SatInfo))
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("ECM-Info"), config.plugins.KravenHD.ECMInfo))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2":
			list.append(getConfigListEntry(_("ECM-Info"), config.plugins.KravenHD.ECMInfo2))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("ECM-Info"), config.plugins.KravenHD.ECMInfo3))
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3":
			list.append(getConfigListEntry(_("ECM-Info"), config.plugins.KravenHD.ECMInfo4))
		list.append(getConfigListEntry(_("______________________ General __________________________________"), ))
		list.append(getConfigListEntry(_("Channel Selection"), config.plugins.KravenHD.ChannelSelectionStyle))
		list.append(getConfigListEntry(_("EMC"), config.plugins.KravenHD.EMCStyle))
		list.append(getConfigListEntry(_("ExtNumberZap"), config.plugins.KravenHD.NumberZapExt))
		list.append(getConfigListEntry(_("Volume Style"), config.plugins.KravenHD.Volume))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.KravenHD.CoolTVGuide))
		
		self["config"].list = list
		self["config"].l.setList(list)
		
		self.ShowPicture()

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/" + returnValue + ".jpg"
			if fileExists(path):
				return path
			else:
				## colors
				return "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/colors.jpg"
		except:
			## weather
			return "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/676757.jpg"

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
		self.mylist()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.mylist()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.mylist()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.mylist()

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
		if fileExists("/tmp/KravenHDweather.xml"):
			remove('/tmp/KravenHDweather.xml')

		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		try:
			#global tag search and replace in all skin elements
			self.skinSearchAndReplace = []
			self.skinSearchAndReplace.append(["0A", config.plugins.KravenHD.BackgroundColorTrans.value])
			self.skinSearchAndReplace.append(["000000", config.plugins.KravenHD.Background.value])
			self.skinSearchAndReplace.append(["4A1B1775", config.plugins.KravenHD.SkinColorInfobar.value])
			self.skinSearchAndReplace.append(["000050EF", config.plugins.KravenHD.SelectionBackground.value])
			self.skinSearchAndReplace.append(["00fffff3", config.plugins.KravenHD.Font1.value])
			self.skinSearchAndReplace.append(["00fffff4", config.plugins.KravenHD.Font2.value])
			self.skinSearchAndReplace.append(["00fffff7", config.plugins.KravenHD.SelectionFont.value])
			self.skinSearchAndReplace.append(["00fffff2", config.plugins.KravenHD.ButtonText.value])
			self.skinSearchAndReplace.append(["00fffff6", config.plugins.KravenHD.Progress.value])
			self.skinSearchAndReplace.append(["00fffff1", config.plugins.KravenHD.Border.value])
			self.skinSearchAndReplace.append(["00fffff5", config.plugins.KravenHD.Line.value])
			self.skinSearchAndReplace.append(["buttons_light", config.plugins.KravenHD.ButtonStyle.value])
			self.skinSearchAndReplace.append(["NotoSans", config.plugins.KravenHD.FontStyle.value])
			
			### ButtonStyleFont
			if config.plugins.KravenHD.ButtonStyle.value == "buttons_light":
				config.plugins.KravenHD.ButtonStyleFont.value = "00fffff8"
			elif config.plugins.KravenHD.ButtonStyle.value == "buttons_dark":
				config.plugins.KravenHD.ButtonStyleFont.value = "00373737"
			
			self.skinSearchAndReplace.append(["00fffff8", config.plugins.KravenHD.ButtonStyleFont.value])
			
			self.skinSearchAndReplace.append(["movetype=running", config.plugins.KravenHD.RunningText.value])
			
			self.selectionbordercolor = config.plugins.KravenHD.SelectionBorder.value
			self.borset = ("borset_" + self.selectionbordercolor + ".png")
			self.skinSearchAndReplace.append(["borset.png", self.borset])
			
			self.skincolorinfobarcolor = config.plugins.KravenHD.SkinColorInfobar.value
			self.ibar = ("ibar_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibar.png", self.ibar])
			
			self.skincolorinfobarcolor = config.plugins.KravenHD.SkinColorInfobar.value
			self.ibar = ("ibaro_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibaro.png", self.ibar])
			
			self.analogstylecolor = config.plugins.KravenHD.AnalogStyle.value
			self.analog = ("analog_" + self.analogstylecolor + ".png")
			self.skinSearchAndReplace.append(["analog.png", self.analog])
			
			### Header
			self.appendSkinFile(self.daten + "header.xml")
			
			### Volume
			self.appendSkinFile(self.daten + config.plugins.KravenHD.Volume.value + ".xml")
			
			###ChannelSelection
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ChannelSelectionStyle.value + ".xml")

			###Infobar_main
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarStyle.value + "_main.xml")

			###Channelname
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName2.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName3.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName4.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName5.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName6.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName7.value + ".xml")

			###clock-style_ib
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle.value + ".xml")

			###sat-info
			self.appendSkinFile(self.daten + config.plugins.KravenHD.SatInfo.value + ".xml")

			###ecm-info
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.ECMInfo.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.ECMInfo2.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.ECMInfo3.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.ECMInfo4.value + ".xml")

			###weather-style
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.WeatherStyle.value + ".xml")
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.WeatherStyle2.value + ".xml")

			###Infobar_middle
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarStyle.value + "_middle.xml")

			###clock-style_sib
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle.value + ".xml")

			###Infobar_end
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarStyle.value + "_end.xml")

			###Main XML
			self.appendSkinFile(self.daten + "main.xml")

			###Plugins XML
			self.appendSkinFile(self.daten + "plugins.xml")

			#EMCSTYLE
			self.appendSkinFile(self.daten + config.plugins.KravenHD.EMCStyle.value +".xml")			

			#NumberZapExtStyle
			self.appendSkinFile(self.daten + config.plugins.KravenHD.NumberZapExt.value + ".xml")

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
			
			console1 = eConsoleAppContainer()
			console2 = eConsoleAppContainer()
			console3 = eConsoleAppContainer()
			console4 = eConsoleAppContainer()
			console5 = eConsoleAppContainer()
			
			#volume
			console1.execute("rm -rf /usr/share/enigma2/KravenHD/volume/*.*; rm -rf /usr/share/enigma2/KravenHD/volume; wget -q http://www.gigablue-support.org/skins/KravenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/KravenHD/" % (str(config.plugins.KravenHD.Volume.value), str(config.plugins.KravenHD.Volume.value), str(config.plugins.KravenHD.Volume.value)))
			#buttons
			console2.execute("rm -rf /usr/share/enigma2/KravenHD/buttons/*.*; rm -rf /usr/share/enigma2/KravenHD/buttons; wget -q http://www.gigablue-support.org/skins/KravenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/KravenHD/" % (str(config.plugins.KravenHD.ButtonStyle.value), str(config.plugins.KravenHD.ButtonStyle.value), str(config.plugins.KravenHD.ButtonStyle.value)))
			#weather-big
			console3.execute("rm -rf /usr/share/enigma2/KravenHD/WetterIcons/*.*; rm -rf /usr/share/enigma2/KravenHD/WetterIcons; wget -q http://www.gigablue-support.org/skins/KravenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/KravenHD/" % (str(config.plugins.KravenHD.WeatherStyle.value), str(config.plugins.KravenHD.WeatherStyle.value), str(config.plugins.KravenHD.WeatherStyle.value)))
			#weather-left
			console4.execute("rm -rf /usr/share/enigma2/KravenHD/WetterIcons/*.*; rm -rf /usr/share/enigma2/KravenHD/WetterIcons; wget -q http://www.gigablue-support.org/skins/KravenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/KravenHD/" % (str(config.plugins.KravenHD.WeatherStyle2.value), str(config.plugins.KravenHD.WeatherStyle2.value), str(config.plugins.KravenHD.WeatherStyle2.value)))
			#clock
			console5.execute("rm -rf /usr/share/enigma2/KravenHD/clock/*.*; rm -rf /usr/share/enigma2/KravenHD/clock; wget -q http://www.gigablue-support.org/skins/KravenHD/%s.tar.gz -O /tmp/%s.tar.gz; tar xf /tmp/%s.tar.gz -C /usr/share/enigma2/KravenHD/" % (str(config.plugins.KravenHD.ClockStyle.value), str(config.plugins.KravenHD.ClockStyle.value), str(config.plugins.KravenHD.ClockStyle.value)))
						
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

		self.restart()

	def restart(self):
		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to download files and apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
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
			config.skin.primary_skin.setValue("KravenHD/skin.xml")
			config.skin.save()
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
	screenwidth = getDesktop(0).size().width()
	if screenwidth and screenwidth == 1920:
		return [PluginDescriptor(name="KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
	else:
		return [PluginDescriptor(name="KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]