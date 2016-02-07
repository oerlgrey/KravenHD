# -*- coding: utf-8 -*-

#######################################################################
#
# KravenHD by Team-Kraven
# 
# Thankfully inspired by:
# MyMetrix
# Coded by iMaxxx (c) 2013
#
# This plugin is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
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
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigClock, ConfigSlider
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system, popen
from shutil import move, rmtree
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from Components.SystemInfo import SystemInfo
from PIL import Image, ImageFilter
import gettext, time, subprocess, re, requests
from enigma import ePicLoad, getDesktop, eConsoleAppContainer, eTimer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from lxml import etree
from xml.etree.cElementTree import fromstring

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

ColorList = []
ColorList.append(("00F0A30A", _("amber")))
ColorList.append(("00B27708", _("amber dark")))
ColorList.append(("001B1775", _("blue")))
ColorList.append(("000E0C3F", _("blue dark")))
ColorList.append(("007D5929", _("brown")))
ColorList.append(("003F2D15", _("brown dark")))
ColorList.append(("000050EF", _("cobalt")))
ColorList.append(("00001F59", _("cobalt dark")))
ColorList.append(("001BA1E2", _("cyan")))
ColorList.append(("000F5B7F", _("cyan dark")))
ColorList.append(("00FFEA04", _("yellow")))
ColorList.append(("00999999", _("grey")))
ColorList.append(("003F3F3F", _("grey dark")))
ColorList.append(("0070AD11", _("green")))
ColorList.append(("00213305", _("green dark")))
ColorList.append(("00A19181", _("Kraven")))
ColorList.append(("0028150B", _("Kraven dark")))
ColorList.append(("006D8764", _("olive")))
ColorList.append(("00313D2D", _("olive dark")))
ColorList.append(("00C3461B", _("orange")))
ColorList.append(("00892E13", _("orange dark")))
ColorList.append(("00F472D0", _("pink")))
ColorList.append(("00723562", _("pink dark")))
ColorList.append(("00E51400", _("red")))
ColorList.append(("00330400", _("red dark")))
ColorList.append(("00000000", _("black")))
ColorList.append(("00647687", _("steel")))
ColorList.append(("00262C33", _("steel dark")))
ColorList.append(("006C0AAB", _("violet")))
ColorList.append(("001F0333", _("violet dark")))
ColorList.append(("00ffffff", _("white")))

LanguageList = []
LanguageList.append(("de", _("Deutsch")))
LanguageList.append(("en", _("English")))
LanguageList.append(("ru", _("Russian")))
LanguageList.append(("it", _("Italian")))
LanguageList.append(("es", _("Spanish (es)")))
LanguageList.append(("sp", _("Spanish (sp)")))
LanguageList.append(("uk", _("Ukrainian (uk)")))
LanguageList.append(("ua", _("Ukrainian (ua)")))
LanguageList.append(("pt", _("Portuguese")))
LanguageList.append(("ro", _("Romanian")))
LanguageList.append(("pl", _("Polish")))
LanguageList.append(("fi", _("Finnish")))
LanguageList.append(("nl", _("Dutch")))
LanguageList.append(("fr", _("French")))
LanguageList.append(("bg", _("Bulgarian")))
LanguageList.append(("sv", _("Swedish (sv)")))
LanguageList.append(("se", _("Swedish (se)")))
LanguageList.append(("zh_tw", _("Chinese Traditional")))
LanguageList.append(("zh", _("Chinese Simplified (zh)")))
LanguageList.append(("zh_cn", _("Chinese Simplified (zh_cn)")))
LanguageList.append(("tr", _("Turkish")))
LanguageList.append(("hr", _("Croatian")))
LanguageList.append(("ca", _("Catalan")))

config.plugins.KravenHD = ConfigSubsection()
config.plugins.KravenHD.Primetime = ConfigClock(default=time.mktime((0, 0, 0, 20, 15, 0, 0, 0, 0)))
config.plugins.KravenHD.InfobarSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenHD.InfobarSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenHD.InfobarSelfColorB = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenHD.BackgroundSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenHD.BackgroundSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenHD.BackgroundSelfColorB = ConfigSlider(default=75, increment=15, limits=(0,255))
config.plugins.KravenHD.InfobarAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))
config.plugins.KravenHD.ECMLineAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))
config.plugins.KravenHD.ScreensAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))

config.plugins.KravenHD.customProfile = ConfigSelection(default="1", choices = [
				("1", _("1")),
				("2", _("2")),
				("3", _("3")),
				("4", _("4")),
				("5", _("5"))
				])

profList = [("default", _("0 (hardcoded)"))]
for i in range(1,21):
	n=name=str(i)
	if fileExists("/etc/enigma2/kraven_default_"+n):
		if i==1:
			name="1 (@tomele)"
		elif i==2:
			name="2 (@örlgrey)"
		elif i==3:
			name="3 (@stony272)"
		elif i==4:
			name="4 (@Linkstar)"
		elif i==5:
			name="5 (@Rene67)"
		elif i==6:
			name="6 (@Mister-T)"
		profList.append((n,_(name)))
config.plugins.KravenHD.defaultProfile = ConfigSelection(default="default", choices = profList)
				
config.plugins.KravenHD.refreshInterval = ConfigSelection(default="15", choices = [
				("0", _("0")),
				("15", _("15")),
				("30", _("30")),
				("60", _("60")),
				("120", _("120")),
				("240", _("240")),
				("480", _("480"))
				])
				
config.plugins.KravenHD.Image = ConfigSelection(default="main-custom-openatv", choices = [
				("main-custom-atemio4you", _("Atemio4You")),
				("main-custom-openatv", _("openATV")),
				("main-custom-openhdf", _("openHDF")),
				("main-custom-openmips", _("openMIPS")),
				("main-custom-opennfr", _("openNFR"))
				])
				
config.plugins.KravenHD.Volume = ConfigSelection(default="volume-top", choices = [
				("volume-original", _("original")),
				("volume-border", _("with Border")),
				("volume-left", _("left")),
				("volume-right", _("right")),
				("volume-top", _("top")),
				("volume-center", _("center"))
				])

config.plugins.KravenHD.MenuColorTrans = ConfigSelection(default="32", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])

config.plugins.KravenHD.MenuColorTransNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for MiniTV"))
				])

config.plugins.KravenHD.BackgroundColorTrans = ConfigSelection(default="32", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])

config.plugins.KravenHD.InfobarColorTrans = ConfigSelection(default="00", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])
				
config.plugins.KravenHD.BackgroundColor = ConfigSelection(default="000000", choices = [
				("F0A30A", _("amber")),
				("B27708", _("amber dark")),
				("665700", _("amber very dark")),
				("1B1775", _("blue")),
				("0E0C3F", _("blue dark")),
				("03001E", _("blue very dark")),
				("7D5929", _("brown")),
				("3F2D15", _("brown dark")),
				("180B00", _("brown very dark")),
				("0050EF", _("cobalt")),
				("001F59", _("cobalt dark")),
				("000E2B", _("cobalt very dark")),
				("1BA1E2", _("cyan")),
				("0F5B7F", _("cyan dark")),
				("01263D", _("cyan very dark")),
				("FFEA04", _("yellow")),
				("999999", _("grey")),
				("3F3F3F", _("grey dark")),
				("1C1C1C", _("grey very dark")),
				("70AD11", _("green")),
				("213305", _("green dark")),
				("001203", _("green very dark")),
				("A19181", _("Kraven")),
				("28150B", _("Kraven dark")),
				("1D130B", _("Kraven very dark")),
				("6D8764", _("olive")),
				("313D2D", _("olive dark")),
				("161C12", _("olive very dark")),
				("C3461B", _("orange")),
				("892E13", _("orange dark")),
				("521D00", _("orange very dark")),
				("F472D0", _("pink")),
				("723562", _("pink dark")),
				("2F0029", _("pink very dark")),
				("E51400", _("red")),
				("330400", _("red dark")),
				("240004", _("red very dark")),
				("000000", _("black")),
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("131619", _("steel very dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("11001E", _("violet very dark")),
				("ffffff", _("white")),
				("self", _("self"))
				])

config.plugins.KravenHD.InfobarColor = ConfigSelection(default="self", choices = [
				("F0A30A", _("amber")),
				("B27708", _("amber dark")),
				("665700", _("amber very dark")),
				("1B1775", _("blue")),
				("0E0C3F", _("blue dark")),
				("03001E", _("blue very dark")),
				("7D5929", _("brown")),
				("3F2D15", _("brown dark")),
				("180B00", _("brown very dark")),
				("0050EF", _("cobalt")),
				("001F59", _("cobalt dark")),
				("000E2B", _("cobalt very dark")),
				("1BA1E2", _("cyan")),
				("0F5B7F", _("cyan dark")),
				("01263D", _("cyan very dark")),
				("FFEA04", _("yellow")),
				("999998", _("grey")),
				("3F3F3E", _("grey dark")),
				("1C1C1C", _("grey very dark")),
				("70AD11", _("green")),
				("213305", _("green dark")),
				("001203", _("green very dark")),
				("A19181", _("Kraven")),
				("28150B", _("Kraven dark")),
				("1D130B", _("Kraven very dark")),
				("6D8764", _("olive")),
				("313D2D", _("olive dark")),
				("161C12", _("olive very dark")),
				("C3461B", _("orange")),
				("892E13", _("orange dark")),
				("521D00", _("orange very dark")),
				("F472D0", _("pink")),
				("723562", _("pink dark")),
				("2F0029", _("pink very dark")),
				("E51400", _("red")),
				("330400", _("red dark")),
				("240004", _("red very dark")),
				("000000", _("black")),
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("131619", _("steel very dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("11001E", _("violet very dark")),
				("ffffff", _("white")),
				("self", _("self"))
				])
				
config.plugins.KravenHD.SelectionBackground = ConfigSelection(default="000050EF", choices = ColorList)
				
config.plugins.KravenHD.Font1 = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.Font2 = ConfigSelection(default="00F0A30A", choices = ColorList)

config.plugins.KravenHD.IBFont1 = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenHD.IBFont2 = ConfigSelection(default="00F0A30A", choices = ColorList)
				
config.plugins.KravenHD.SelectionFont = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.MarkedFont = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.ECMFont = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.ChannelnameFont = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.PrimetimeFont = ConfigSelection(default="0070AD11", choices = ColorList)
				
config.plugins.KravenHD.ButtonText = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.Android = ConfigSelection(default="00000000", choices = ColorList)
				
config.plugins.KravenHD.Border = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.Progress = ConfigSelection(default="progress", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("progress", _("colorfull")),
				("progress2", _("colorfull2")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("00A19181", _("Kraven")),
				("0028150B", _("Kraven dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
config.plugins.KravenHD.Line = ConfigSelection(default="00ffffff", choices = ColorList)
				
config.plugins.KravenHD.SelectionBorder = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("00A19181", _("Kraven")),
				("0028150B", _("Kraven dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])

config.plugins.KravenHD.MiniTVBorder = ConfigSelection(default="003F3F3F", choices = ColorList)
				
config.plugins.KravenHD.AnalogStyle = ConfigSelection(default="00999999", choices = [
				("00F0A30A", _("amber")),
				("001B1775", _("blue")),
				("007D5929", _("brown")),
				("000050EF", _("cobalt")),
				("001BA1E2", _("cyan")),
				("00999999", _("grey")),
				("0070AD11", _("green")),
				("00C3461B", _("orange")),
				("00F472D0", _("pink")),
				("00E51400", _("red")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("006C0AAB", _("violet")),
				("00ffffff", _("white"))
				])
				
config.plugins.KravenHD.InfobarStyle = ConfigSelection(default="infobar-style-x2", choices = [
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
				("none", _("off")),
				("infobar-channelname-small", _("Name small")),
				("infobar-channelname-number-small", _("Name & Number small")),
				("infobar-channelname", _("Name big")),
				("infobar-channelname-number", _("Name & Number big"))
				])

config.plugins.KravenHD.InfobarChannelName2 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small", _("Name")),
				("infobar-channelname-number-small", _("Name & Number"))
				])
							
config.plugins.KravenHD.ChannelSelectionStyle = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right")),
				("channelselection-style-minitv3", _("Preview")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-nobile-minitv3", _("Nobile Preview"))
				])
							
config.plugins.KravenHD.ChannelSelectionStyle2 = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right")),
				("channelselection-style-minitv3", _("Preview")),
				("channelselection-style-minitv33", _("Extended Preview")),
				("channelselection-style-minitv2", _("Dual TV")),
				("channelselection-style-minitv22", _("Dual TV 2")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-nobile-minitv3", _("Nobile Preview")),
				("channelselection-style-nobile-minitv33", _("Nobile Extended Preview"))
				])

config.plugins.KravenHD.ChannelSelectionMode = ConfigSelection(default="zap", choices = [
				("zap", _("Zap (1xOK)")),
				("preview", _("Preview (2xOK)"))
				])

config.plugins.KravenHD.ChannelSelectionModeNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for this channellist style"))
				])

config.plugins.KravenHD.ChannelSelectionTrans = ConfigSelection(default="32", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])

config.plugins.KravenHD.ChannelSelectionTransNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for this channellist style"))
				])

config.plugins.KravenHD.ChannelSelectionServiceNA = ConfigSelection(default="00FFEA04", choices = ColorList)
				
config.plugins.KravenHD.NumberZapExt = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("numberzapext-xpicon", _("X-Picons")),
				("numberzapext-zpicon", _("Z-Picons")),
				("numberzapext-zzpicon", _("ZZ-Picons")),
				("numberzapext-zzzpicon", _("ZZZ-Picons"))
				])
				
config.plugins.KravenHD.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("MiniTV")),
				("cooltv-picon", _("Picon"))
				])
				
config.plugins.KravenHD.MovieSelection = ConfigSelection(default="movieselection-no-cover", choices = [
				("movieselection-no-cover", _("no Cover")),
				("movieselection-small-cover", _("small Cover")),
				("movieselection-big-cover", _("big Cover")),
				("movieselection-minitv", _("MiniTV")),
				("movieselection-minitv-cover", _("MiniTV + Cover"))
				])
				
config.plugins.KravenHD.EMCStyle = ConfigSelection(default="emc-minitv", choices = [
				("emc-nocover", _("no Cover")),
				("emc-nocover2", _("no Cover2")),
				("emc-smallcover", _("small Cover")),
				("emc-smallcover2", _("small Cover2")),
				("emc-bigcover", _("big Cover")),
				("emc-bigcover2", _("big Cover2")),
				("emc-verybigcover", _("very big Cover")),
				("emc-verybigcover2", _("very big Cover2")),
				("emc-minitv", _("MiniTV")),
				("emc-minitv2", _("MiniTV2"))
				])
				
config.plugins.KravenHD.RunningText = ConfigSelection(default="startdelay=4000", choices = [
				("none", _("off")),
				("startdelay=2000", _("2 sec")),
				("startdelay=4000", _("4 sec")),
				("startdelay=6000", _("6 sec")),
				("startdelay=8000", _("8 sec")),
				("startdelay=10000", _("10 sec")),
				("startdelay=15000", _("15 sec")),
				("startdelay=20000", _("20 sec"))
				])

config.plugins.KravenHD.RunningTextSpeed = ConfigSelection(default="steptime=100", choices = [
				("steptime=200", _("5 px/sec")),
				("steptime=100", _("10 px/sec")),
				("steptime=66", _("15 px/sec")),
				("steptime=50", _("20 px/sec"))
				])
				
config.plugins.KravenHD.ScrollBar = ConfigSelection(default="showOnDemand", choices = [
				("showOnDemand", _("on")),
				("showNever", _("off"))
				])
				
config.plugins.KravenHD.IconStyle = ConfigSelection(default="icons-light", choices = [
				("icons-light", _("light")),
				("icons-dark", _("dark"))
				])
				
config.plugins.KravenHD.IconStyle2 = ConfigSelection(default="icons-light2", choices = [
				("icons-light2", _("light")),
				("icons-dark2", _("dark"))
				])

config.plugins.KravenHD.ClockStyle = ConfigSelection(default="clock-classic", choices = [
				("clock-classic", _("standard")),
				("clock-classic-big", _("standard big")),
				("clock-analog", _("analog")),
				("clock-android", _("android")),
				("clock-color", _("colored")),
				("clock-flip", _("flip"))
				])

config.plugins.KravenHD.ClockStyle2 = ConfigSelection(default="clock-classic2", choices = [
				("clock-classic2", _("standard")),
				("clock-classic-big2", _("standard big")),
				("clock-analog", _("analog")),
				("clock-android", _("android")),
				("clock-color2", _("colored")),
				("clock-flip2", _("flip"))
				])

config.plugins.KravenHD.ClockStyle3 = ConfigSelection(default="clock-classic3", choices = [
				("clock-classic3", _("standard")),
				("clock-classic-big3", _("standard big")),
				("clock-analog", _("analog")),
				("clock-android", _("android")),
				("clock-color3", _("colored")),
				("clock-flip3", _("flip"))
				])
				
config.plugins.KravenHD.WeatherStyle = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-big", _("big")),
				("weather-small", _("small"))
				])
				
config.plugins.KravenHD.WeatherStyle2 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-left", _("on"))
				])

config.plugins.KravenHD.ECMLine1 = ConfigSelection(default="ShortReader", choices = [
				("none", _("off")),
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact"))
				])

config.plugins.KravenHD.ECMLine2 = ConfigSelection(default="ShortReader", choices = [
				("none", _("off")),
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact")),
				("Normal", _("balanced")),
				("Long", _("extensive")),
				("VeryLong", _("complete"))
				])

config.plugins.KravenHD.ECMLine3 = ConfigSelection(default="ShortReader", choices = [
				("none", _("off")),
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact")),
				("Normal", _("balanced")),
				("Long", _("extensive")),
				])

config.plugins.KravenHD.FTA = ConfigSelection(default="FTAVisible", choices = [
				("FTAVisible", _("on")),
				("none", _("off"))
				])

config.plugins.KravenHD.SystemInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("systeminfo-small", _("small")),
				("systeminfo-big", _("big")),
				("systeminfo-bigsat", _("big + Sat"))
				])

config.plugins.KravenHD.SIB = ConfigSelection(default="sib4", choices = [
				("sib1", _("top/bottom")),
				("sib2", _("left/right")),
				("sib3", _("single")),
				("sib4", _("MiniTV")),
				("sib5", _("MiniTV2")),
				("sib6", _("Weather")),
				("sib7", _("Weather2"))
				])
				
config.plugins.KravenHD.IBtop = ConfigSelection(default="infobar-x2-z1_top", choices = [
				("infobar-x2-z1_top", _("4 Tuner")),
				("infobar-x2-z1_top2", _("REC + 2 Tuner"))
				])
				
config.plugins.KravenHD.Infobox = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("db", _("Tuner/Satellite + dB")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])
				
config.plugins.KravenHD.IBColor = ConfigSelection(default="all-screens", choices = [
				("all-screens", _("in all Screens")),
				("only-infobar", _("only Infobar, SecondInfobar & Players"))
				])
				
config.plugins.KravenHD.About = ConfigSelection(default="about", choices = [
				("about", _(" "))
				])

config.plugins.KravenHD.About2 = ConfigSelection(default="about", choices = [
				("about", _("press OK for the FAQs"))
				])
				
config.plugins.KravenHD.ClockStyleNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available in this style"))
				])
				
config.plugins.KravenHD.IBtopNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available in this style"))
				])
				
config.plugins.KravenHD.InfoboxNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available in this style"))
				])
				
config.plugins.KravenHD.Logo = ConfigSelection(default="logo", choices = [
				("logo", _("Logo")),
				("minitv", _("MiniTV")),
				("metrix-icons", _("Icons")),
				("minitv-metrix-icons", _("MiniTV + Icons"))
				])

config.plugins.KravenHD.MenuIcons = ConfigSelection(default="stony272", choices = [
				("stony272", _("stony272")),
				("rennmaus-kleinerteufel", _("rennmaus-kleiner.teufel"))
				])

config.plugins.KravenHD.MenuIconsNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for Menu with Icons"))
				])
				
config.plugins.KravenHD.DebugNames = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("screennames-on", _("on"))
				])
				
config.plugins.KravenHD.WeatherView = ConfigSelection(default="meteo", choices = [
				("icon", _("Icon")),
				("meteo", _("Meteo"))
				])
				
config.plugins.KravenHD.MeteoColor = ConfigSelection(default="meteo-light", choices = [
				("meteo-light", _("light")),
				("meteo-dark", _("dark"))
				])
				
config.plugins.KravenHD.MeteoColorNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for Meteo-Style"))
				])
				
config.plugins.KravenHD.Primetimeavailable = ConfigSelection(default="primetime-on", choices = [
				("none", _("off")),
				("primetime-on", _("on"))
				])
				
config.plugins.KravenHD.PrimetimeNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when Primetime is activated"))
				])
				
config.plugins.KravenHD.PrimetimeFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when Primetime is activated"))
				])

config.plugins.KravenHD.ChannelnameFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when activated"))
				])

config.plugins.KravenHD.FTANA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when ECM-Infos are activated"))
				])

config.plugins.KravenHD.ECMFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when ECM-Infos are activated"))
				])

config.plugins.KravenHD.RunningTextSpeedNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when Running Text is activated"))
				])

config.plugins.KravenHD.EMCSelectionColors = ConfigSelection(default="emc-colors-on", choices = [
				("none", _("off")),
				("emc-colors-on", _("on"))
				])

config.plugins.KravenHD.EMCSelectionBackground = ConfigSelection(default="00213305", choices = ColorList)

config.plugins.KravenHD.EMCSelectionBackgroundNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for 'Custom EMC-Selection-Colors'"))
				])

config.plugins.KravenHD.EMCSelectionFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenHD.EMCSelectionFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for 'Custom EMC-Selection-Colors'"))
				])

config.plugins.KravenHD.ColorNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for self-colors"))
				])

config.plugins.KravenHD.SerienRecorder = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("serienrecorder", _("on"))
				])

config.plugins.KravenHD.MediaPortal = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("mediaportal", _("on"))
				])

config.plugins.KravenHD.MediaPortalNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("MediaPortal not installed"))
				])

config.plugins.KravenHD.PVRState = ConfigSelection(default="pvrstate-center-big", choices = [
				("pvrstate-center-big", _("center big")),
				("pvrstate-center-small", _("center small")),
				("pvrstate-left-small", _("left small")),
				("pvrstate-off", _("off"))
				])

config.plugins.KravenHD.PigStyle=ConfigText(default="")
config.plugins.KravenHD.PigMenuActive=ConfigYesNo(default=False)

config.plugins.KravenHD.weather_gmcode = ConfigText(default="GM")
config.plugins.KravenHD.weather_cityname = ConfigText(default = "")
config.plugins.KravenHD.weather_language = ConfigSelection(default="de", choices = LanguageList)
config.plugins.KravenHD.weather_server = ConfigSelection(default="_owm", choices = [
				("_owm", _("OpenWeatherMap")),
				("_accu", _("Accuweather")),
				("_realtek", _("RealTek"))
				])
config.plugins.KravenHD.weather_search_over = ConfigSelection(default="ip", choices = [
				("ip", _("Auto (IP)")),
				("name", _("Search String")),
				("gmcode", _("GM Code"))
				])

config.plugins.KravenHD.weather_owm_latlon = ConfigText(default = "")
config.plugins.KravenHD.weather_accu_latlon = ConfigText(default = "")
config.plugins.KravenHD.weather_realtek_latlon = ConfigText(default = "")
config.plugins.KravenHD.weather_accu_id = ConfigNumber(default = "")
config.plugins.KravenHD.weather_foundcity = ConfigText(default = "")
				
#######################################################################

class KravenHD(ConfigListScreen, Screen):
	skin = """
<screen name="KravenHD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#00000000">
  <widget font="Regular; 20" halign="left" valign="center" source="key_red" position="70,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_green" position="320,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_yellow" position="570,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_blue" position="820,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget name="config" position="70,85" size="708,540" itemHeight="30" font="Regular;24" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="70,12" size="708,46" text="KravenHD - Konfigurationstool" font="Regular; 35" valign="center" halign="left" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" />
  <eLabel position="847,208" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="847,417" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="845,208" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel position="1215,208" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
  <ePixmap pixmap="KravenHD/buttons/key_red1.png" position="65,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_green1.png" position="315,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_yellow1.png" position="565,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenHD/buttons/key_blue1.png" position="815,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1138,22" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
	<convert type="KravenHDClockToText">Default</convert>
  </widget>
  <eLabel position="830,80" size="402,46" text="KravenHD" font="Regular; 36" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" />
  <eLabel position="845,139" size="372,40" text="Version: 7.1.0" font="Regular; 30" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
  <widget name="helperimage" position="847,210" size="368,207" zPosition="1" backgroundColor="#00000000" />
  <widget source="Canvas" render="Canvas" position="847,210" size="368,207" zPosition="-1" backgroundColor="#00000000" />
  <widget source="help" render="Label" position="847,440" size="368,196" font="Regular;20" backgroundColor="#00000000" foregroundColor="#00f0a30a" halign="left" valign="top" transparent="1" />
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
		self.picPath = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/"
		self.profiles = "/etc/enigma2/"
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		self["Canvas"] = CanvasSource()
		self["help"] = StaticText()
		
		list = []
		ConfigListScreen.__init__(self, list)

		self["actions"] = ActionMap(["KravenHDConfigActions", "OkCancelActions", "DirectionActions", "ColorActions", "InputActions"],
		{
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"red": self.exit,
			"green": self.save,
			"yellow": self.saveProfile,
			"blue": self.reset,
			"cancel": self.exit,
			"pageup": self.pageUp,
			"papedown": self.pageDown,
			"ok": self.faq
		}, -1)

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save skin"))
		self["key_yellow"] = StaticText(_("Save profile"))
		self["key_blue"] = StaticText(_("Reset profile"))

		self.UpdatePicture()

		self.timer = eTimer()
		self.timer.callback.append(self.updateMylist)
		self.onLayoutFinish.append(self.updateMylist)

		self.lastProfile="0"

		self.actClockstyle=""
		self.actWeatherstyle=""
		self.actChannelselectionstyle=""
		self.actCity=""

	def mylist(self):
		self.timer.start(100, True)

	def updateMylist(self):		
		list = []
		list.append(getConfigListEntry(_("About"), config.plugins.KravenHD.About2, _("The KravenHD skin will be generated by this plugin according to your preferences. Make your settings and watch the changes in the preview window above. When finished, save your skin by pressing the green button and restart the GUI.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("PROFILES _____________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Active Profile"), config.plugins.KravenHD.customProfile, _("Select the profile you want to work with. Profiles are saved automatically on switching them or by pressing the yellow button. New profiles will be generated based on the actual one. Profiles are interchangeable between boxes.")))
		list.append(getConfigListEntry(_("Default Profile for Reset"), config.plugins.KravenHD.defaultProfile, _("Select the default profile you want to use when resetting the active profile (blue button). You can add your own default profiles under /etc/enigma2/kraven_default_n (n<=20).")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("SYSTEM _______________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Image"), config.plugins.KravenHD.Image, _(" ")))
		list.append(getConfigListEntry(_("Icons (except Infobar)"), config.plugins.KravenHD.IconStyle2, _("Choose between light and dark icons in system screens. The icons in the infobars are not affected.")))
		list.append(getConfigListEntry(_("Running Text (Delay)"), config.plugins.KravenHD.RunningText, _("Choose the start delay for running text.")))
		if config.plugins.KravenHD.RunningText.value in ("startdelay=2000","startdelay=4000","startdelay=6000","startdelay=8000","startdelay=10000","startdelay=15000","startdelay=20000"):
			list.append(getConfigListEntry(_("Running Text (Speed)"), config.plugins.KravenHD.RunningTextSpeed, _("Choose the speed for running text.")))
		elif config.plugins.KravenHD.RunningText.value == "none":
			list.append(getConfigListEntry(_("Running Text (Speed)"), config.plugins.KravenHD.RunningTextSpeedNA, _("This option is not available because running text is deactivated.")))
		list.append(getConfigListEntry(_("Scrollbars"), config.plugins.KravenHD.ScrollBar, _("Choose the width of scrollbars in lists or deactivate scrollbars completely.")))
		list.append(getConfigListEntry(_("Show Infobar-Background"), config.plugins.KravenHD.IBColor, _("Choose whether you want to see the infobar background in all screens (bicolored background).")))
		list.append(getConfigListEntry(_("Menus"), config.plugins.KravenHD.Logo, _("Choose from different options to display the system menus. Press OK for the FAQs with details on installing menu icons.")))
		if config.plugins.KravenHD.Logo.value in ("metrix-icons","minitv-metrix-icons"):
			list.append(getConfigListEntry(_("Menu-Icons"), config.plugins.KravenHD.MenuIcons, _("Choose from different icon sets for the menu screens.")))
		else:
			list.append(getConfigListEntry(_("Menu-Icons"), config.plugins.KravenHD.MenuIconsNA, _("This option is not available for the selected menu style.")))
		if config.plugins.KravenHD.Logo.value in ("logo","metrix-icons"):
			list.append(getConfigListEntry(_("Menu-Transparency"), config.plugins.KravenHD.MenuColorTrans, _("Choose the degree of background transparency for system menu screens.")))
		else:
			list.append(getConfigListEntry(_("Menu-Transparency"), config.plugins.KravenHD.MenuColorTransNA, _("This option is not available because MiniTV for system menus is activated.")))
		list.append(getConfigListEntry(_("GLOBAL COLORS ________________________________________________________"), config.plugins.KravenHD.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Background"), config.plugins.KravenHD.BackgroundColor, _("Choose the background color for all screens. You can choose from a list of predefined colors or create your own color using RGB sliders.")))
		if config.plugins.KravenHD.BackgroundColor.value == "self":
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenHD.BackgroundSelfColorR, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenHD.BackgroundSelfColorG, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenHD.BackgroundSelfColorB, _("Set the intensity of this basic color with the slider.")))
		else:
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenHD.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenHD.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenHD.ColorNA, _(" ")))
		list.append(getConfigListEntry(_("Background-Transparency"), config.plugins.KravenHD.BackgroundColorTrans, _("Choose the degree of background transparency for all screens except system menus and channellists.")))
		list.append(getConfigListEntry(_("Listselection"), config.plugins.KravenHD.SelectionBackground, _("Choose the background color of selection bars.")))
		list.append(getConfigListEntry(_("Listselection-Border"), config.plugins.KravenHD.SelectionBorder, _("Choose the border color of selection bars or deactivate borders completely.")))
		list.append(getConfigListEntry(_("Listselection-Font"), config.plugins.KravenHD.SelectionFont, _("Choose the color of the font in selection bars.")))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.KravenHD.Progress, _("Choose the color of progress bars.")))
		list.append(getConfigListEntry(_("Progress-Border"), config.plugins.KravenHD.Border, _("Choose the border color of progress bars.")))
		list.append(getConfigListEntry(_("MiniTV-Border"), config.plugins.KravenHD.MiniTVBorder, _("Choose the border color of MiniTV's.")))
		list.append(getConfigListEntry(_("Lines"), config.plugins.KravenHD.Line, _("Choose the color of all lines. This affects dividers as well as the line in the center of some progress bars.")))
		list.append(getConfigListEntry(_("Primary-Font"), config.plugins.KravenHD.Font1, _("Choose the color of the primary font. The primary font is used for list items, textboxes and other important information.")))
		list.append(getConfigListEntry(_("Secondary-Font"), config.plugins.KravenHD.Font2, _("Choose the color of the secondary font. The secondary font is used for headers, labels and other additional information.")))
		list.append(getConfigListEntry(_("Marking-Font"), config.plugins.KravenHD.MarkedFont, _("Choose the font color of marked list items.")))
		list.append(getConfigListEntry(_("Colorbutton-Font"), config.plugins.KravenHD.ButtonText, _("Choose the font color of the color button labels.")))
		list.append(getConfigListEntry(_("INFOBAR ______________________________________________________________"), config.plugins.KravenHD.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Infobar-Style"), config.plugins.KravenHD.InfobarStyle, _("Choose from different infobar styles. Please note that not every style provides every feature. Therefore some features might be unavailable for the chosen style.")))
		list.append(getConfigListEntry(_("Infobar-Background"), config.plugins.KravenHD.InfobarColor, _("Choose the background color of the infobars. You can choose from a list of predefined colors or create your own color using RGB sliders.")))
		if config.plugins.KravenHD.InfobarColor.value == "self":
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenHD.InfobarSelfColorR, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenHD.InfobarSelfColorG, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenHD.InfobarSelfColorB, _("Set the intensity of this basic color with the slider.")))
		else:
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenHD.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenHD.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenHD.ColorNA, _(" ")))
		list.append(getConfigListEntry(_("Infobar-Transparency"), config.plugins.KravenHD.InfobarColorTrans, _("Choose the degree of background transparency for the infobars.")))
		list.append(getConfigListEntry(_("Primary-Infobar-Font"), config.plugins.KravenHD.IBFont1, _("Choose the color of the primary infobar font.")))
		list.append(getConfigListEntry(_("Secondary-Infobar-Font"), config.plugins.KravenHD.IBFont2, _("Choose the color of the secondary infobar font.")))
		list.append(getConfigListEntry(_("Infobar-Icons"), config.plugins.KravenHD.IconStyle, _("Choose between light and dark infobar icons.")))
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			list.append(getConfigListEntry(_("Tuner number/Record"), config.plugins.KravenHD.IBtop, _("Choose from different options to display tuner and recording state.")))
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Tuner number/Record"), config.plugins.KravenHD.IBtopNA, _("This option is not available for the selected infobar style.")))
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x1","infobar-style-x2","infobar-style-z1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenHD.Infobox, _("Choose which informations will be shown in the info box.")))
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenHD.InfoboxNA, _("This option is not available for the selected infobar style.")))
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x1","infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz1","infobar-style-zz4"):
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenHD.InfobarChannelName, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenHD.InfobarChannelName.value == "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenHD.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenHD.ChannelnameFont, _("Choose the font color of channel name and number")))
		else:
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenHD.InfobarChannelName2, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenHD.InfobarChannelName2.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenHD.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenHD.ChannelnameFont, _("Choose the font color of channel name and number")))
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenHD.ClockStyle, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenHD.ClockStyle.value
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenHD.ClockStyle2, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenHD.ClockStyle2.value
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenHD.ClockStyle3, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenHD.ClockStyle3.value
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenHD.ClockStyleNA, _("This option is not available for the selected infobar style.")))
			self.actClockstyle="none"
		if self.actClockstyle == "clock-analog":
			list.append(getConfigListEntry(_("Analog-Clock-Color"), config.plugins.KravenHD.AnalogStyle, _("Choose from different colors for the analog type clock in the infobar.")))
		if self.actClockstyle == "clock-android":
			list.append(getConfigListEntry(_("Android-Temp-Color"), config.plugins.KravenHD.Android, _("Choose the font color of android-clock temperature.")))
		list.append(getConfigListEntry(_("System-Infos"), config.plugins.KravenHD.SystemInfo, _("Choose from different additional windows with system informations or deactivate them completely.")))
		if not self.actClockstyle in ("clock-analog","clock-android"):
			list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("ECM INFOS ____________________________________________________________"), config.plugins.KravenHD.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("ECM-Infos"), config.plugins.KravenHD.ECMLine1, _("Choose from different options to display the ECM informations.")))
			if config.plugins.KravenHD.ECMLine1.value == "none":
				list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTANA, _("This option is not available because displaying ECM information is deactivated.")))
				list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFontNA, _("This option is not available because displaying ECM information is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
				list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFont, _("Choose the font color of the ECM information.")))
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			list.append(getConfigListEntry(_("ECM-Infos"), config.plugins.KravenHD.ECMLine2, _("Choose from different options to display the ECM informations.")))
			if config.plugins.KravenHD.ECMLine2.value == "none":
				list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTANA, _("This option is not available because displaying ECM information is deactivated.")))
				list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFontNA, _("This option is not available because displaying ECM information is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
				list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFont, _("Choose the font color of the ECM information.")))
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("ECM-Infos"), config.plugins.KravenHD.ECMLine3, _("Choose from different options to display the ECM informations.")))
			if config.plugins.KravenHD.ECMLine3.value == "none":
				list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTANA, _("This option is not available because displaying ECM information is deactivated.")))
				list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFontNA, _("This option is not available because displaying ECM information is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
				list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFont, _("Choose the font color of the ECM information.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("WEATHER ______________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyle, _("Choose from different options to show the weather in the infobar.")))
			self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle.value
		else:
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyle2, _("Activate or deactivate displaying the weather in the infobar.")))
			self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle2.value
		list.append(getConfigListEntry(_("Search by"), config.plugins.KravenHD.weather_search_over, _("Choose from different options to specify your location.")))
		if config.plugins.KravenHD.weather_search_over.value == 'name':
			list.append(getConfigListEntry(_("Search String"), config.plugins.KravenHD.weather_cityname, _("Specify any search string for your location (zip/city/district/state single or combined). Press OK to use the virtual keyboard. Step up or down in the menu to start the search.")))
		elif config.plugins.KravenHD.weather_search_over.value == 'gmcode':
			list.append(getConfigListEntry(_("GM Code"), config.plugins.KravenHD.weather_gmcode, _("Specify the GM code for your location. You can find it at https://weather.codes. Press OK to use the virtual keyboard. Step up or down in the menu to start the search.")))
		list.append(getConfigListEntry(_("Server"), config.plugins.KravenHD.weather_server, _("Choose from different servers for the weather data.")))
		list.append(getConfigListEntry(_("Language"), config.plugins.KravenHD.weather_language, _("Specify the language for the weather output.")))
		list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.KravenHD.refreshInterval, _("Choose the frequency of loading weather data from the internet.")))
		list.append(getConfigListEntry(_("Weather-Style"), config.plugins.KravenHD.WeatherView, _("Choose between graphical weather symbols and Meteo symbols.")))
		if config.plugins.KravenHD.WeatherView.value == "meteo":
			list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenHD.MeteoColor, _("Choose between light and dark Meteo symbols.")))
		elif config.plugins.KravenHD.WeatherView.value == "icon":
			list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenHD.MeteoColorNA, _("This option is not available because Meteo symbols are not selected.")))
		if config.plugins.KravenHD.weather_search_over.value == "ip":
			list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("CHANNELLIST __________________________________________________________"), config.plugins.KravenHD.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		if SystemInfo.get("NumVideoDecoders",1) > 1:
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenHD.ChannelSelectionStyle2, _("Choose from different styles for the channel selection screen.")))
			self.actChannelselectionstyle=config.plugins.KravenHD.ChannelSelectionStyle2.value
		else:
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenHD.ChannelSelectionStyle, _("Choose from different styles for the channel selection screen.")))
			self.actChannelselectionstyle=config.plugins.KravenHD.ChannelSelectionStyle.value
		if self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv22","channelselection-style-minitv33","channelselection-style-minitv4","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv33"):
			list.append(getConfigListEntry(_("Channellist-Mode"), config.plugins.KravenHD.ChannelSelectionMode, _("Choose between direct zapping (1xOK) and zapping after preview (2xOK).")))
		else:
			list.append(getConfigListEntry(_("Channellist-Mode"), config.plugins.KravenHD.ChannelSelectionModeNA, _("This option is only available for MiniTV, Extended Preview and DualTV channellist styles.")))
		if not self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv3","channelselection-style-minitv4","channelselection-style-minitv22","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3"):
			list.append(getConfigListEntry(_("Channellist-Transparenz"), config.plugins.KravenHD.ChannelSelectionTrans, _("Choose the degree of background transparency for the channellists.")))
		else:
			list.append(getConfigListEntry(_("Channellist-Transparenz"), config.plugins.KravenHD.ChannelSelectionTransNA, _("This option is not available for MiniTV, Preview and DualTV channellist styles.")))
		list.append(getConfigListEntry(_("'not available'-Font"), config.plugins.KravenHD.ChannelSelectionServiceNA, _("Choose the font color of channels that are unavailable at the moment.")))
		list.append(getConfigListEntry(_("Primetime"), config.plugins.KravenHD.Primetimeavailable, _("Choose whether primetime program information is displayed or not.")))
		if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on":
			list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenHD.Primetime, _("Specify the time for your primetime.")))
			list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenHD.PrimetimeFont, _("Choose the font color of the primetime information.")))
		elif config.plugins.KravenHD.Primetimeavailable.value == "none":
			list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenHD.PrimetimeNA, _("This option is not available because displaying primetime information is deactivated.")))
			list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenHD.PrimetimeFontNA, _("This option is not available because displaying primetime information is deactivated.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("ENHANCED MOVIE CENTER ________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("EMC-Style"), config.plugins.KravenHD.EMCStyle, _("Choose from different styles for EnhancedMovieCenter.")))
		list.append(getConfigListEntry(_("Custom EMC-Selection-Colors"), config.plugins.KravenHD.EMCSelectionColors, _("Choose whether you want to customize the selection-colors for EnhancedMovieCenter.")))
		if config.plugins.KravenHD.EMCSelectionColors.value == "emc-colors-on":
			list.append(getConfigListEntry(_("EMC-Listselection"), config.plugins.KravenHD.EMCSelectionBackground, _("Choose the background color of selection bars for EnhancedMovieCenter.")))
			list.append(getConfigListEntry(_("EMC-Selection-Font"), config.plugins.KravenHD.EMCSelectionFont, _("Choose the color of the font in selection bars for EnhancedMovieCenter.")))
		elif config.plugins.KravenHD.EMCSelectionColors.value == "none":
			list.append(getConfigListEntry(_("EMC-Listselection"), config.plugins.KravenHD.EMCSelectionBackgroundNA, _("This option is not available because 'Custom EMC-Selection-Colors' is deactivated.")))
			list.append(getConfigListEntry(_("EMC-Selection-Font"), config.plugins.KravenHD.EMCSelectionFontNA, _("This option is not available because 'Customize EMC-Selection-Colors' is deactivated.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("VIEWS ________________________________________________________________"), config.plugins.KravenHD.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Volume"), config.plugins.KravenHD.Volume, _("Choose from different styles for the volume display.")))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.KravenHD.CoolTVGuide, _("Choose from different styles for CoolTVGuide.")))
		list.append(getConfigListEntry(_("MovieSelection"), config.plugins.KravenHD.MovieSelection, _("Choose from different styles for MovieSelection.")))
		list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenHD.SIB, _("Choose from different styles for SecondInfobar.")))
		list.append(getConfigListEntry(_("SerienRecorder"), config.plugins.KravenHD.SerienRecorder, _("Choose whether you want the Kraven skin to be applied to 'Serienrecorder' or not. Activation of this option prohibits the skin selection in the SR-plugin.")))
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py"):
			list.append(getConfigListEntry(_("MediaPortal"), config.plugins.KravenHD.MediaPortal, _("Choose whether you want the Kraven skin to be applied to 'MediaPortal' or not. To remove it again, you must deactivate it here and activate another skin in 'MediaPortal'.")))
		else:
			list.append(getConfigListEntry(_("MediaPortal"), config.plugins.KravenHD.MediaPortalNA, _("This option is not available because 'MediaPortal' is not installed.")))
		list.append(getConfigListEntry(_("ExtNumberZap"), config.plugins.KravenHD.NumberZapExt, _("Choose from different styles for ExtNumberZap.")))
		list.append(getConfigListEntry(_("PVRState"), config.plugins.KravenHD.PVRState, _("Choose from different options to display the PVR state.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("ANTIALIASING BRIGHTNESS ________________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Infobar"), config.plugins.KravenHD.InfobarAntialias, _("Reduce distortions (faint/blurry) or color frames around fonts in the infobar and widgets by adjusting the antialiasing brightness.")))
		list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenHD.ECMLineAntialias, _("Reduce distortions (faint/blurry) or color frames around the ecm information in the infobar by adjusting the antialiasing brightness.")))
		list.append(getConfigListEntry(_("Screens"), config.plugins.KravenHD.ScreensAntialias, _("Reduce distortions (faint/blurry) or color frames around fonts at top and bottom of screens by adjusting the antialiasing brightness.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("DEBUG ________________________________________________________________"), config.plugins.KravenHD.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Screennames"), config.plugins.KravenHD.DebugNames, _("Activate or deactivate small screen names for debugging purposes.")))

		self["config"].list = list
		self["config"].l.setList(list)
		self.updateHelp()
		self["helperimage"].hide()
		self.ShowPicture()

		option = self["config"].getCurrent()[1]

		if option == config.plugins.KravenHD.customProfile:
			if config.plugins.KravenHD.customProfile.value==self.lastProfile:
				self.saveProfile(msg=False)
			else:
				self.loadProfile()
				self.lastProfile=config.plugins.KravenHD.customProfile.value
		if option.value == "none":
			self.showText(50,_("Off"))
		elif option == config.plugins.KravenHD.customProfile:
			self.showText(25,"/etc/enigma2/kraven_profile_"+str(config.plugins.KravenHD.customProfile.value))
		elif option == config.plugins.KravenHD.defaultProfile:
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/"+str(config.plugins.KravenHD.defaultProfile.value)+".jpg"):
				self["helperimage"].show()
			else:
				self.showText(25,"/etc/enigma2/kraven_default_"+str(config.plugins.KravenHD.defaultProfile.value))
		elif option == config.plugins.KravenHD.IBtop:
			if option.value == "infobar-x2-z1_top":
				self.showText(50,_("4 Tuner"))
			elif option.value == "infobar-x2-z1_top2":
				self.showText(50,_("REC + 2 Tuner"))
		elif option in (config.plugins.KravenHD.InfobarChannelName,config.plugins.KravenHD.InfobarChannelName2):
			if option.value == "infobar-channelname-small":
				self.showText(40,_("RTL"))
			elif option.value == "infobar-channelname-number-small":
				self.showText(40,_("5 - RTL"))
			elif option.value == "infobar-channelname":
				self.showText(76,_("RTL"))
			elif option.value == "infobar-channelname-number":
				self.showText(76,_("5 - RTL"))
		elif option in (config.plugins.KravenHD.ECMLine1,config.plugins.KravenHD.ECMLine2,config.plugins.KravenHD.ECMLine3):
			if option.value == "VeryShortCaid":
				self.showText(17,"CAID - Time")
			elif option.value == "VeryShortReader":
				self.showText(17,"Reader - Time")
			elif option.value == "ShortReader":
				self.showText(17,"CAID - Reader - Time")
			elif option.value == "Normal":
				self.showText(17,"CAID - Reader - Hops - Time")
			elif option.value == "Long":
				self.showText(17,"CAID - System - Reader - Hops - Time")
			elif option.value == "VeryLong":
				self.showText(17,"CAM - CAID - System - Reader - Hops - Time")
		elif option == config.plugins.KravenHD.FTA and option.value == "FTAVisible":
			self.showText(17,_("free to air"))
		elif option in (config.plugins.KravenHD.weather_gmcode,config.plugins.KravenHD.weather_cityname,config.plugins.KravenHD.weather_server,config.plugins.KravenHD.weather_search_over):
			self.get_weather_data()
			self.showText(20,self.actCity)
		elif option == config.plugins.KravenHD.weather_language:
			self.showText(60,option.value)
		elif option == config.plugins.KravenHD.refreshInterval:
			if option.value == "0":
				self.showText(50,_("Off"))
			elif option.value == "15":
				self.showText(50,"00:15")
			elif option.value == "30":
				self.showText(50,"00:30")
			elif option.value == "60":
				self.showText(50,"01:00")
			elif option.value == "120":
				self.showText(50,"02:00")
			elif option.value == "240":
				self.showText(50,"04:00")
			elif option.value == "480":
				self.showText(50,"08:00")
		elif option == config.plugins.KravenHD.ChannelSelectionMode:
			if option.value == "zap":
				self.showText(50,"1 x OK")
			elif option.value == "preview":
				self.showText(50,"2 x OK")
		elif option == config.plugins.KravenHD.PVRState:
			if option.value == "pvrstate-center-big":
				self.showText(44,">> 8x")
			elif option.value == "pvrstate-center-small":
				self.showText(22,">> 8x")
			else:
				self["helperimage"].show()
		elif option in (config.plugins.KravenHD.InfobarAntialias,config.plugins.KravenHD.ECMLineAntialias,config.plugins.KravenHD.ScreensAntialias):
			if option.value == 10:
				self.showText(50,"+/- 0%")
			elif option.value in range(0,10):
				self.showText(50,"- "+str(100-option.value*10)+"%")
			elif option.value in range(11,21):
				self.showText(50,"+ "+str(option.value*10-100)+"%")
		elif option == config.plugins.KravenHD.DebugNames and option.value == "screennames-on":
			self.showText(50,"Debug")
		elif option in (config.plugins.KravenHD.MenuColorTrans,config.plugins.KravenHD.BackgroundColorTrans,config.plugins.KravenHD.InfobarColorTrans,config.plugins.KravenHD.ChannelSelectionTrans) and option.value == "00":
			self.showText(50,_("Off"))
		elif option == config.plugins.KravenHD.BackgroundColor:
			if config.plugins.KravenHD.BackgroundColor.value == "self":
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.BackgroundColor.value))
		elif option in (config.plugins.KravenHD.BackgroundSelfColorR,config.plugins.KravenHD.BackgroundSelfColorG,config.plugins.KravenHD.BackgroundSelfColorB):
			self.showColor(self.RGB(int(config.plugins.KravenHD.BackgroundSelfColorR.value), int(config.plugins.KravenHD.BackgroundSelfColorG.value), int(config.plugins.KravenHD.BackgroundSelfColorB.value)))
		elif option == config.plugins.KravenHD.SelectionBackground:
			self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionBackground.value))
		elif option == config.plugins.KravenHD.SelectionBorder:
			self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionBorder.value))
		elif option == config.plugins.KravenHD.EMCSelectionBackground:
			self.showColor(self.hexRGB(config.plugins.KravenHD.EMCSelectionBackground.value))
		elif option == config.plugins.KravenHD.Progress:
			if config.plugins.KravenHD.Progress.value in ("progress", "progress2"):
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.Progress.value))
		elif option == config.plugins.KravenHD.Border:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Border.value))
		elif option == config.plugins.KravenHD.MiniTVBorder:
			self.showColor(self.hexRGB(config.plugins.KravenHD.MiniTVBorder.value))
		elif option == config.plugins.KravenHD.Line:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Line.value))
		elif option == config.plugins.KravenHD.Font1:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Font1.value))
		elif option == config.plugins.KravenHD.Font2:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Font2.value))
		elif option == config.plugins.KravenHD.IBFont1:
			self.showColor(self.hexRGB(config.plugins.KravenHD.IBFont1.value))
		elif option == config.plugins.KravenHD.IBFont2:
			self.showColor(self.hexRGB(config.plugins.KravenHD.IBFont2.value))
		elif option == config.plugins.KravenHD.SelectionFont:
			self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionFont.value))
		elif option == config.plugins.KravenHD.EMCSelectionFont:
			self.showColor(self.hexRGB(config.plugins.KravenHD.EMCSelectionFont.value))
		elif option == config.plugins.KravenHD.MarkedFont:
			self.showColor(self.hexRGB(config.plugins.KravenHD.MarkedFont.value))
		elif option == config.plugins.KravenHD.ButtonText:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ButtonText.value))
		elif option == config.plugins.KravenHD.Android:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Android.value))
		elif option == config.plugins.KravenHD.ChannelSelectionServiceNA:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ChannelSelectionServiceNA.value))
		elif option == config.plugins.KravenHD.InfobarColor:
			if config.plugins.KravenHD.InfobarColor.value == "self":
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.InfobarColor.value))
		elif option in (config.plugins.KravenHD.InfobarSelfColorR,config.plugins.KravenHD.InfobarSelfColorG,config.plugins.KravenHD.InfobarSelfColorB):
			self.showColor(self.RGB(int(config.plugins.KravenHD.InfobarSelfColorR.value), int(config.plugins.KravenHD.InfobarSelfColorG.value), int(config.plugins.KravenHD.InfobarSelfColorB.value)))
		elif option == config.plugins.KravenHD.ChannelnameFont:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ChannelnameFont.value))
		elif option == config.plugins.KravenHD.ECMFont:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ECMFont.value))
		elif option == config.plugins.KravenHD.PrimetimeFont:
			self.showColor(self.hexRGB(config.plugins.KravenHD.PrimetimeFont.value))
		else:
			self["helperimage"].show()

	def updateHelp(self):
		cur = self["config"].getCurrent()
		if cur:
			self["help"].text = cur[2]

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			if returnValue in ("clock-classic2","clock-classic3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-classic.jpg"
			elif returnValue in ("clock-classic-big2","clock-classic-big3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-classic-big.jpg"
			elif returnValue in ("clock-color2","clock-color3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-color.jpg"
			elif returnValue in ("clock-flip2","clock-flip3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-flip.jpg"
			elif returnValue in ("startdelay=2000","startdelay=4000","startdelay=6000","startdelay=8000","startdelay=10000","startdelay=15000","startdelay=20000"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/running-delay.jpg"
			elif returnValue in ("steptime=200","steptime=100","steptime=66","steptime=50"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/running-speed.jpg"
			elif returnValue in ("about","about2"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/about.png"
			elif returnValue == ("meteo-light"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/meteo.jpg"
			elif returnValue in ("progress"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/colorfull.jpg"
			elif returnValue == ("progress2"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/colorfull2.jpg"
			elif returnValue in ("self","emc-colors-on"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/colors.jpg"
			elif returnValue == ("channelselection-style-minitv3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/channelselection-style-minitv.jpg"
			elif returnValue == ("channelselection-style-nobile-minitv3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/channelselection-style-nobile-minitv.jpg"
			elif returnValue == "all-screens":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/emc-smallcover.jpg"
			elif returnValue in ("infobar-style-x3","only-infobar"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/2.jpg"
			elif returnValue in ("0C","18","32","58","7E"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/transparent.jpg"
			else:
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/" + returnValue + ".jpg"
			if fileExists(path):
				return path
			else:
				return "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/black.jpg"
		except:
			return "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/fb.jpg"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
		if self.picPath is not None:
			self.picPath = None
			self.PicLoad.startDecode(self.picPath)
		else:
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

	def pageUp(self):
		self["config"].instance.moveSelection(self["config"].instance.pageUp)
		self.mylist()

	def pageDown(self):
		self["config"].instance.moveSelection(self["config"].instance.pageDown)
		self.mylist()

	def keyVirtualKeyBoardCallBack(self, callback):
		try:
			if callback:  
				self["config"].getCurrent()[1].value = callback
			else:
				pass
		except:
			pass

	def faq(self):
		if isinstance(self["config"].getCurrent()[1],ConfigText):
			from Screens.VirtualKeyBoard import VirtualKeyBoard
			text = self["config"].getCurrent()[1].value
			if config.plugins.KravenHD.weather_search_over.value == 'name':
				title = _("Enter the city name of your location:")
			elif config.plugins.KravenHD.weather_search_over.value == 'gmcode':
				title = _("Enter the GM code for your location:")
			self.session.openWithCallback(self.keyVirtualKeyBoardCallBack, VirtualKeyBoard, title = title, text = text)
		else:
			from Plugins.SystemPlugins.MPHelp import PluginHelp, XMLHelpReader
			reader = XMLHelpReader(resolveFilename(SCOPE_PLUGINS, "Extensions/KravenHD/faq.xml"))
			KravenHDFaq = PluginHelp(*reader)
			KravenHDFaq.open(self.session)

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

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
		
		self.saveProfile(msg=False)
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		self.skinSearchAndReplace = []

		### Background
		if config.plugins.KravenHD.BackgroundColor.value == "self":
			self.skincolorbackgroundcolor = str(hex(config.plugins.KravenHD.BackgroundSelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenHD.BackgroundSelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenHD.BackgroundSelfColorB.value)[2:4]).zfill(2)
		else:
			self.skincolorbackgroundcolor = config.plugins.KravenHD.BackgroundColor.value
		self.skinSearchAndReplace.append(['name="Kravenbg" value="#00000000', 'name="Kravenbg" value="#00' + self.skincolorbackgroundcolor])

		### Background Transparency (global)
		self.skinSearchAndReplace.append(['name="Kravenbg" value="#00', 'name="Kravenbg" value="#' + config.plugins.KravenHD.BackgroundColorTrans.value])

		### Background2 (non-transparent)
		if config.plugins.KravenHD.BackgroundColor.value == "self":
			self.skinSearchAndReplace.append(['name="Kravenbg2" value="#00000000', 'name="Kravenbg2" value="#00' + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg2" value="#00000000', 'name="Kravenbg2" value="#00' + config.plugins.KravenHD.BackgroundColor.value])

		### Background3 (Menus Transparency)
		if config.plugins.KravenHD.Logo.value in ("logo","metrix-icons"):
			if config.plugins.KravenHD.BackgroundColor.value == "self":
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#' + config.plugins.KravenHD.MenuColorTrans.value + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#' + config.plugins.KravenHD.MenuColorTrans.value + config.plugins.KravenHD.BackgroundColor.value])
		else:
			if config.plugins.KravenHD.BackgroundColor.value == "self":
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#00' + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#00' + config.plugins.KravenHD.BackgroundColor.value])

		### Background4 (Channellist)
		if config.plugins.KravenHD.BackgroundColor.value == "self":
			self.skinSearchAndReplace.append(['name="Kravenbg4" value="#00000000', 'name="Kravenbg4" value="#' + config.plugins.KravenHD.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg4" value="#00000000', 'name="Kravenbg4" value="#' + config.plugins.KravenHD.ChannelSelectionTrans.value + config.plugins.KravenHD.BackgroundColor.value])

		### Background5 (Radio Channellist)
		if config.plugins.KravenHD.BackgroundColor.value == "self":
			self.skinSearchAndReplace.append(['name="Kravenbg5" value="#00000000', 'name="Kravenbg5" value="#' + "60" + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg5" value="#00000000', 'name="Kravenbg5" value="#' + "60" + config.plugins.KravenHD.BackgroundColor.value])

		### Infobar Backgrounds
		if config.plugins.KravenHD.InfobarColor.value == "self":
			self.skincolorinfobarcolor = str(hex(config.plugins.KravenHD.InfobarSelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenHD.InfobarSelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenHD.InfobarSelfColorB.value)[2:4]).zfill(2)
		else:
			self.skincolorinfobarcolor = config.plugins.KravenHD.InfobarColor.value

		##### Channelname. Transparency 50%, color always grey
		self.skinSearchAndReplace.append(['name="KravenNamebg" value="#A01B1775', 'name="KravenNamebg" value="#7F7F7F7F'])

		##### ECM. Transparency of infobar, color of text
		self.skinSearchAndReplace.append(['name="KravenECMbg" value="#F1325698', 'name="KravenECMbg" value="#' + config.plugins.KravenHD.InfobarColorTrans.value + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenHD.ECMLineAntialias.value)])

		##### Infobar. Transparency of infobar, color of infobar
		self.skinSearchAndReplace.append(['name="KravenIBbg" value="#001B1775', 'name="KravenIBbg" value="#' + config.plugins.KravenHD.InfobarColorTrans.value + self.skincolorinfobarcolor])

		##### CoolTV. color of infobar or color of background, if ibar invisible
		if config.plugins.KravenHD.IBColor.value == "all-screens":
			self.skinSearchAndReplace.append(['name="KravenIBCoolbg" value="#00000000', 'name="KravenIBCoolbg" value="#00' + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenHD.ScreensAntialias.value)])
		else:
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBCoolbg"', 'backgroundColor="Kravenbg2"'])

		##### Screens. Lower Transparency of infobar and background, color of infobar or color of background, if ibar invisible
		if config.plugins.KravenHD.IBColor.value == "all-screens":
			self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#' + self.calcTransparency(config.plugins.KravenHD.InfobarColorTrans.value,config.plugins.KravenHD.BackgroundColorTrans.value) + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenHD.ScreensAntialias.value)])
			self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#' + self.calcTransparency(config.plugins.KravenHD.InfobarColorTrans.value,config.plugins.KravenHD.MenuColorTrans.value) + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenHD.ScreensAntialias.value)])
			self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#' + self.calcTransparency(config.plugins.KravenHD.InfobarColorTrans.value,config.plugins.KravenHD.ChannelSelectionTrans.value) + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenHD.ScreensAntialias.value)])
		else:
			self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#00' + config.plugins.KravenHD.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#00' + config.plugins.KravenHD.MenuColorTrans.value + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#00' + config.plugins.KravenHD.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])
			
		### Selection Background
		if config.plugins.KravenHD.EMCSelectionColors.value == "none":
			self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#' + config.plugins.KravenHD.SelectionBackground.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#' + config.plugins.KravenHD.SelectionBackground.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#' + config.plugins.KravenHD.SelectionBackground.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#' + config.plugins.KravenHD.EMCSelectionBackground.value])

		### Menu (Logo/MiniTV)
		if config.plugins.KravenHD.Logo.value == "minitv":
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo" />', '<panel name="template_menu_minitv" />'])
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo2" />', '<panel name="template_menu_minitv2" />'])
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo3" />', '<panel name="template_menu_minitv" />'])
		elif config.plugins.KravenHD.Logo.value == "metrix-icons":
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo" />', '<panel name="template_menu_metrix-icons" />'])
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo2" />', '<panel name="template_menu_metrix-icons2" />'])
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo3" />', '<panel name="template_menu_metrix-icons3" />'])
		elif config.plugins.KravenHD.Logo.value == "minitv-metrix-icons":
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo" />', '<panel name="template_menu_minitv-metrix-icons" />'])
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo2" />', '<panel name="template_menu_minitv-metrix-icons2" />'])
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo3" />', '<panel name="template_menu_minitv-metrix-icons3" />'])
		elif config.plugins.KravenHD.Logo.value == "logo":
			self.skinSearchAndReplace.append(['<panel name="template_menu_logo3" />', '<panel name="template_menu_logo" />'])

		### Font Colors
		self.skinSearchAndReplace.append(['name="KravenFont1" value="#00ffffff', 'name="KravenFont1" value="#' + config.plugins.KravenHD.Font1.value])
		self.skinSearchAndReplace.append(['name="KravenFont2" value="#00F0A30A', 'name="KravenFont2" value="#' + config.plugins.KravenHD.Font2.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont1" value="#00ffffff', 'name="KravenIBFont1" value="#' + config.plugins.KravenHD.IBFont1.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont2" value="#00F0A30A', 'name="KravenIBFont2" value="#' + config.plugins.KravenHD.IBFont2.value])
		if config.plugins.KravenHD.EMCSelectionColors.value == "none":
			self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#' + config.plugins.KravenHD.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#' + config.plugins.KravenHD.SelectionFont.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#' + config.plugins.KravenHD.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#' + config.plugins.KravenHD.EMCSelectionFont.value])
		self.skinSearchAndReplace.append(['name="selectedFG" value="#00ffffff', 'name="selectedFG" value="#' + config.plugins.KravenHD.SelectionFont.value])
		self.skinSearchAndReplace.append(['name="KravenMarked" value="#00ffffff', 'name="KravenMarked" value="#' + config.plugins.KravenHD.MarkedFont.value])
		self.skinSearchAndReplace.append(['name="KravenECM" value="#00ffffff', 'name="KravenECM" value="#' + config.plugins.KravenHD.ECMFont.value])
		self.skinSearchAndReplace.append(['name="KravenName" value="#00ffffff', 'name="KravenName" value="#' + config.plugins.KravenHD.ChannelnameFont.value])
		self.skinSearchAndReplace.append(['name="KravenButton" value="#00ffffff', 'name="KravenButton" value="#' + config.plugins.KravenHD.ButtonText.value])
		self.skinSearchAndReplace.append(['name="KravenAndroid" value="#00ffffff', 'name="KravenAndroid" value="#' + config.plugins.KravenHD.Android.value])

		### ChannelSelection 'not available' Font
		self.skinSearchAndReplace.append(['name="KravenNotAvailable" value="#00FFEA04', 'name="KravenNotAvailable" value="#' + config.plugins.KravenHD.ChannelSelectionServiceNA.value])

		### Primetime
		if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on":
			self.skinSearchAndReplace.append(['<!--<widget', '<widget'])
			self.skinSearchAndReplace.append(['</widget>-->', '</widget>'])
			self.skinSearchAndReplace.append(['name="KravenPrime" value="#0070AD11', 'name="KravenPrime" value="#' + config.plugins.KravenHD.PrimetimeFont.value])
		else:
			self.skinSearchAndReplace.append(['render="KravenHDSingleEpgList" size="362,54"', 'render="KravenHDSingleEpgList" size="362,81"'])
			self.skinSearchAndReplace.append(['render="KravenHDSingleEpgList" size="400,54"', 'render="KravenHDSingleEpgList" size="400,81"'])
			self.skinSearchAndReplace.append(['render="KravenHDSingleEpgList" size="505,27"', 'render="KravenHDSingleEpgList" size="505,54"'])
			self.skinSearchAndReplace.append(['render="KravenHDSingleEpgList" size="778,81"', 'render="KravenHDSingleEpgList" size="778,108"'])
			self.skinSearchAndReplace.append(['render="KravenHDSingleEpgListNobile" size="339,572"', 'render="KravenHDSingleEpgListNobile" size="339,594"'])
			self.skinSearchAndReplace.append(['render="KravenHDSingleEpgList" size="474,308"', 'render="KravenHDSingleEpgList" size="474,330"'])

		### Debug-Names
		if config.plugins.KravenHD.DebugNames.value == "screennames-on":
			self.skinSearchAndReplace.append(['<!--<text', '<eLabel backgroundColor="#00000000" font="Regular;15" foregroundColor="white" text'])
			self.skinSearchAndReplace.append(['<!-- KravenHDMenuEntryID-Converter -->', '<widget backgroundColor="#00000000" font="Regular;15" foregroundColor="white" render="Label" source="menu" position="70,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9"><convert type="KravenHDMenuEntryID"></convert></widget><eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />'])
			self.skinSearchAndReplace.append(['" position="70,0" />-->', ' " position="70,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9" /><eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />'])
			self.skinSearchAndReplace.append(['" position="42,0" />-->', ' " position="42,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9" /><eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />'])
			self.skinSearchAndReplace.append(['" position="40,0" />-->', ' " position="40,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9" /><eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />'])

		### Icons
		if config.plugins.KravenHD.IBColor.value == "only-infobar":
			if config.plugins.KravenHD.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-dark/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-dark/"])
			elif config.plugins.KravenHD.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-light/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-light/"])
			if config.plugins.KravenHD.IconStyle.value == "icons-dark":
				self.skinSearchAndReplace.append(['name="KravenIcon" value="#00fff0e0"', 'name="KravenIcon" value="#00000000"'])
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-dark/"])
			elif config.plugins.KravenHD.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-light/"])
		elif config.plugins.KravenHD.IBColor.value == "all-screens":
			if config.plugins.KravenHD.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-dark/"])
			elif config.plugins.KravenHD.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-light/"])
			if config.plugins.KravenHD.IconStyle.value == "icons-dark":
				self.skinSearchAndReplace.append(['name="KravenIcon" value="#00fff0e0"', 'name="KravenIcon" value="#00000000"'])
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-dark/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-dark/"])
			elif config.plugins.KravenHD.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-light/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-light/"])

		### Weather-Server
		if config.plugins.KravenHD.weather_server.value == "_owm":
			self.skinSearchAndReplace.append(['KravenHDWeather', 'KravenHDWeather_owm'])
			if config.plugins.KravenHD.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo2; 40" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenHDWetterPicon" alphatest="blend"', 'size="50,50" render="Label" font="Meteo2; 45" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo2; 70" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])
		elif config.plugins.KravenHD.weather_server.value == "_accu":
			self.skinSearchAndReplace.append(['KravenHDWeather', 'KravenHDWeather_accu'])
			if config.plugins.KravenHD.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo3; 40" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenHDWetterPicon" alphatest="blend"', 'size="50,50" render="Label" font="Meteo3; 45" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo3; 70" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])
		elif config.plugins.KravenHD.weather_server.value == "_realtek":
			self.skinSearchAndReplace.append(['KravenHDWeather', 'KravenHDWeather_realtek'])
			if config.plugins.KravenHD.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo3; 40" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenHDWetterPicon" alphatest="blend"', 'size="50,50" render="Label" font="Meteo3; 45" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo3; 70" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])

		### Meteo-Font
		if config.plugins.KravenHD.MeteoColor.value == "meteo-dark":
			self.skinSearchAndReplace.append(['name="KravenMeteo" value="#00fff0e0"', 'name="KravenMeteo" value="#00000000"'])

		### Progress
		if config.plugins.KravenHD.Progress.value == "progress2":
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress18.png"',' pixmap="KravenHD/progress/progress18_2.png"'])
			self.skinSearchAndReplace.append([' picServiceEventProgressbar="KravenHD/progress/progress52.png"',' picServiceEventProgressbar="KravenHD/progress/progress52_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress170.png"',' pixmap="KravenHD/progress/progress170_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress220.png"',' pixmap="KravenHD/progress/progress220_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress248.png"',' pixmap="KravenHD/progress/progress248_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress300.png"',' pixmap="KravenHD/progress/progress300_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress328.png"',' pixmap="KravenHD/progress/progress328_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress370.png"',' pixmap="KravenHD/progress/progress370_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress380.png"',' pixmap="KravenHD/progress/progress380_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress410.png"',' pixmap="KravenHD/progress/progress410_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress420.png"',' pixmap="KravenHD/progress/progress420_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress535.png"',' pixmap="KravenHD/progress/progress535_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress581.png"',' pixmap="KravenHD/progress/progress581_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress599.png"',' pixmap="KravenHD/progress/progress599_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress640.png"',' pixmap="KravenHD/progress/progress640_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress665.png"',' pixmap="KravenHD/progress/progress665_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress708.png"',' pixmap="KravenHD/progress/progress708_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress749.png"',' pixmap="KravenHD/progress/progress749_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress858.png"',' pixmap="KravenHD/progress/progress858_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress990.png"',' pixmap="KravenHD/progress/progress990_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress1265.png"',' pixmap="KravenHD/progress/progress1265_2.png"'])
		elif not config.plugins.KravenHD.Progress.value == "progress":
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress18.png"'," "])
			self.skinSearchAndReplace.append([' picServiceEventProgressbar="KravenHD/progress/progress52.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress170.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress220.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress248.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress300.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress328.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress370.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress380.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress410.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress420.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress535.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress581.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress599.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress640.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress665.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress708.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress749.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress858.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress990.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress1265.png"'," "])
			self.skinSearchAndReplace.append(['name="KravenProgress" value="#00C3461B', 'name="KravenProgress" value="#' + config.plugins.KravenHD.Progress.value])

		### Border
		self.skinSearchAndReplace.append(['name="KravenBorder" value="#00ffffff', 'name="KravenBorder" value="#' + config.plugins.KravenHD.Border.value])

		### MiniTV Border
		self.skinSearchAndReplace.append(['name="KravenBorder2" value="#003F3F3F', 'name="KravenBorder2" value="#' + config.plugins.KravenHD.MiniTVBorder.value])

		### Line
		self.skinSearchAndReplace.append(['name="KravenLine" value="#00ffffff', 'name="KravenLine" value="#' + config.plugins.KravenHD.Line.value])

		### Runningtext
		if config.plugins.KravenHD.RunningText.value == "none":
			self.skinSearchAndReplace.append(["movetype=running", "movetype=none"])
		if not config.plugins.KravenHD.RunningText.value == "none":
			self.skinSearchAndReplace.append(["startdelay=5000", config.plugins.KravenHD.RunningText.value])
			self.skinSearchAndReplace.append(["steptime=90", config.plugins.KravenHD.RunningTextSpeed.value])
			if config.plugins.KravenHD.RunningTextSpeed.value == "steptime=200":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=66"])
			elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=100":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=33"])
			elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=66":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=22"])
			elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=50":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=17"])

		### Scrollbar
		if config.plugins.KravenHD.ScrollBar.value == "showOnDemand":
			self.skinSearchAndReplace.append(['scrollbarMode="showNever"', 'scrollbarMode="showOnDemand"'])
		else:
			self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])

		### Selectionborder
		if not config.plugins.KravenHD.SelectionBorder.value == "none":
			self.selectionbordercolor = config.plugins.KravenHD.SelectionBorder.value
			self.borset = ("borset_" + self.selectionbordercolor + ".png")
			self.skinSearchAndReplace.append(["borset.png", self.borset])

		### IB Color visible
		if not config.plugins.KravenHD.IBColor.value == "all-screens":
			self.skinSearchAndReplace.append(['backgroundColor="KravenMbg"', 'backgroundColor="Kravenbg"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont1"', 'foregroundColor="KravenFont1"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont2"', 'foregroundColor="KravenFont2"'])
			self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenHD/ibar.png" position="0,550" size="1280,310" alphatest="blend" zPosition="-9" />'," "])
			self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenHD/ibar.png" position="0,570" size="1280,310" alphatest="blend" zPosition="-9" />'," "])
			self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenHD/ibaro2.png" position="0,0" size="1280,125" alphatest="blend" zPosition="-9" />'," "])
			self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenHD/ibar.png" position="0,550" size="380,310" alphatest="blend" zPosition="-9" />'," "])
			self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenHD/ibaro2.png" position="0,0" size="380,125" alphatest="blend" zPosition="-9" />'," "])
		else:
			self.skinSearchAndReplace.append(['backgroundColor="KravenMbg"', 'backgroundColor="KravenIBbg2"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont1"', 'foregroundColor="KravenIBFont1"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont2"', 'foregroundColor="KravenIBFont2"'])
		self.skinSearchAndReplace.append(['backgroundColor="KravenSIBbg2"', 'backgroundColor="KravenIBbg2"'])
		self.skinSearchAndReplace.append(['foregroundColor="KravenSIBFont1"', 'foregroundColor="KravenIBFont1"'])
		self.skinSearchAndReplace.append(['foregroundColor="KravenSIBFont2"', 'foregroundColor="KravenIBFont2"'])

		### Clock Analog Style
		self.analogstylecolor = config.plugins.KravenHD.AnalogStyle.value
		self.analog = ("analog_" + self.analogstylecolor + ".png")
		self.skinSearchAndReplace.append(["analog.png", self.analog])

		### Header
		self.appendSkinFile(self.daten + "header_begin.xml")
		if not config.plugins.KravenHD.SelectionBorder.value == "none":
			self.appendSkinFile(self.daten + "header_middle.xml")
		self.appendSkinFile(self.daten + "header_end.xml")
			
		### Image
		self.appendSkinFile(self.daten + config.plugins.KravenHD.Image.value + ".xml")

		### Volume
		self.appendSkinFile(self.daten + config.plugins.KravenHD.Volume.value + ".xml")

		### ChannelSelection
		self.appendSkinFile(self.daten + self.actChannelselectionstyle + ".xml")
			
		if self.actChannelselectionstyle in ("channelselection-style-nopicon","channelselection-style-xpicon","channelselection-style-zpicon","channelselection-style-zzpicon","channelselection-style-zzzpicon","channelselection-style-minitv3","channelselection-style-nobile-minitv3") or config.plugins.KravenHD.ChannelSelectionMode.value=="zap": 
			config.usage.servicelistpreview_mode.value=False
		else:
			config.usage.servicelistpreview_mode.value=True
		config.usage.servicelistpreview_mode.save()

		if self.actChannelselectionstyle in ("channelselection-style-minitv2","channelselection-style-minitv22"): #DualTV
			config.plugins.KravenHD.PigStyle.value="DualTV"
		elif self.actChannelselectionstyle in ("channelselection-style-minitv33","channelselection-style-nobile-minitv33"): #ExtPreview
			config.plugins.KravenHD.PigStyle.value="ExtPreview"
		elif self.actChannelselectionstyle in ("channelselection-style-minitv3","channelselection-style-nobile-minitv3"): #Preview
			config.plugins.KravenHD.PigStyle.value="Preview"
		config.plugins.KravenHD.PigStyle.save()

		### Infobox
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x1","infobar-style-x2","infobar-style-z1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			if config.plugins.KravenHD.Infobox.value == "cpu":
				self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="  L:"'])
				self.skinSearchAndReplace.append(['foregroundColor="KravenIcon" />-->', 'foregroundColor="KravenIcon" />'])
				self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
				self.skinSearchAndReplace.append(['convert  type="KravenHDFrontendInfo">SNR', 'convert type="KravenHDLayoutInfo">LoadAvg'])
				self.skinSearchAndReplace.append(['convert  type="KravenHDExtServiceInfo">OrbitalPosition', 'convert  type="KravenHDCpuUsage">$0'])
			elif config.plugins.KravenHD.Infobox.value == "temp":
				self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="U:"'])
				self.skinSearchAndReplace.append(['foregroundColor="KravenIcon" />-->', 'foregroundColor="KravenIcon" />'])
				self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
				self.skinSearchAndReplace.append(['convert  type="KravenHDFrontendInfo">SNR', 'convert type="KravenHDTempFanInfo">FanInfo'])
				self.skinSearchAndReplace.append(['convert  type="KravenHDExtServiceInfo">OrbitalPosition', 'convert  type="KravenHDTempFanInfo">TempInfo'])
			elif config.plugins.KravenHD.Infobox.value == "db":
				self.skinSearchAndReplace.append(['convert  type="KravenHDFrontendInfo">SNR', 'convert  type="KravenHDFrontendInfo">SNRdB'])

		### Infobar_begin
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + "infobar-begin-x1.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			self.appendSkinFile(self.daten + "infobar-begin-zz1.xml")
		else:
			self.appendSkinFile(self.daten + "infobar-begin.xml")

		### Infobar_main
		self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarStyle.value + "_main.xml")

		### Infobar_top
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if config.plugins.KravenHD.IBtop.value == "infobar-x2-z1_top":
				self.appendSkinFile(self.daten + "infobar-x2-z1_top.xml")
			elif config.plugins.KravenHD.IBtop.value == "infobar-x2-z1_top2":
				self.appendSkinFile(self.daten + "infobar-x2-z1_top2.xml")

		### Channelname
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.skinSearchAndReplace.append(['"KravenName" position="20,527"', '"KravenName" position="20,510"'])
			self.skinSearchAndReplace.append(['"KravenName" position="20,452"', '"KravenName" position="20,450"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
			self.skinSearchAndReplace.append(['"KravenName" position="20,527"', '"KravenName" position="20,474"'])
			self.skinSearchAndReplace.append(['"KravenName" position="20,452"', '"KravenName" position="20,414"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
			self.skinSearchAndReplace.append(['"KravenName" position="20,527" size="1240,60"', '"KravenName" position="435,534" size="565,50"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName2.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
			self.skinSearchAndReplace.append(['"KravenName" position="20,527" size="1240,60"', '"KravenName" position="446,464" size="754,50"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName2.value + ".xml")

		### clock-style_ib
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle2.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle3.value + ".xml")

		### FTA
		if config.plugins.KravenHD.FTA.value == "none":
			self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

		### ecm-contents
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			if not config.plugins.KravenHD.ECMLine1.value == "none":
				self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine1.value])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			if not config.plugins.KravenHD.ECMLine2.value == "none":
				self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine2.value])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine3.value])

		### ecm-info
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			if not config.plugins.KravenHD.ECMLine1.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if not config.plugins.KravenHD.ECMLine2.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2"):
			if not config.plugins.KravenHD.ECMLine2.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2":
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3":
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

		### system-info
		self.appendSkinFile(self.daten + config.plugins.KravenHD.SystemInfo.value + ".xml")

		### weather-style
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle.value
		else:
			self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle2.value
		self.appendSkinFile(self.daten + self.actWeatherstyle + ".xml")
		if self.actWeatherstyle == "none" and self.actClockstyle != "clock-android" and config.plugins.KravenHD.SIB.value != "sib6" and config.plugins.KravenHD.SIB.value != "sib7":
			config.plugins.KravenHD.refreshInterval.value = "0"
			config.plugins.KravenHD.refreshInterval.save()
		elif config.plugins.KravenHD.refreshInterval.value == "0":
			config.plugins.KravenHD.refreshInterval.value = config.plugins.KravenHD.refreshInterval.default
			config.plugins.KravenHD.refreshInterval.save()

		### Infobar_end - SIB_begin
		self.appendSkinFile(self.daten + "infobar-style_middle.xml")

		### clock-style - SIB
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle2.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1""infobar-style-zzz1"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle3.value + ".xml")

		### SIB_main
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + "infobar-style-x1_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x2":
			self.appendSkinFile(self.daten + "infobar-style-x2_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x3":
			self.appendSkinFile(self.daten + "infobar-style-x3_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z1":
			self.appendSkinFile(self.daten + "infobar-style-z1_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-z2":
			self.appendSkinFile(self.daten + "infobar-style-z2_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1":
			self.skinSearchAndReplace.append(['size="1199,186">', 'size="1199,155">'])
			self.skinSearchAndReplace.append(['size="297">', 'size="264">'])
			self.appendSkinFile(self.daten + "infobar-style-zz1_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2":
			self.skinSearchAndReplace.append(['size="1199,186">', 'size="1199,155">'])
			self.skinSearchAndReplace.append(['size="297">', 'size="264">'])
			self.appendSkinFile(self.daten + "infobar-style-zz2_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3":
			self.skinSearchAndReplace.append(['size="1199,186">', 'size="1199,155">'])
			self.skinSearchAndReplace.append(['size="297">', 'size="264">'])
			self.appendSkinFile(self.daten + "infobar-style-zz3_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz4":
			self.skinSearchAndReplace.append(['size="1199,186">', 'size="1199,155">'])
			self.skinSearchAndReplace.append(['size="297">', 'size="264">'])
			self.appendSkinFile(self.daten + "infobar-style-zz4_main.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
			self.skinSearchAndReplace.append(['size="570,396">', 'size="570,330">'])
			self.skinSearchAndReplace.append(['size="1199,186">', 'size="1199,124">'])
			self.skinSearchAndReplace.append(['size="297">', 'size="231">'])
			self.appendSkinFile(self.daten + "infobar-style-zzz1_main.xml")
		self.appendSkinFile(self.daten + config.plugins.KravenHD.SIB.value + ".xml")

		### Main XML
		self.appendSkinFile(self.daten + "main.xml")

		### Timeshift_begin
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + "timeshift-begin-x1.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zz4", "infobar-style-zzz1"):
			self.appendSkinFile(self.daten + "timeshift-begin-zz1.xml")
		else:
			self.appendSkinFile(self.daten + "timeshift-begin.xml")

		if self.actWeatherstyle in ("weather-big","weather-left"):
			if config.plugins.KravenHD.SystemInfo.value == "systeminfo-bigsat":
				self.appendSkinFile(self.daten + "timeshift-begin-leftlow.xml")
			else:
				self.appendSkinFile(self.daten + "timeshift-begin-low.xml")
		elif self.actWeatherstyle == "weather-small":
			self.appendSkinFile(self.daten + "timeshift-begin-left.xml")
		else:
			self.appendSkinFile(self.daten + "timeshift-begin-high.xml")

		### Timeshift_Infobar_main
		self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarStyle.value + "_main.xml")

		### Timeshift_Infobar_top
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if config.plugins.KravenHD.IBtop.value == "infobar-x2-z1_top":
				self.appendSkinFile(self.daten + "infobar-x2-z1_top.xml")
			elif config.plugins.KravenHD.IBtop.value == "infobar-x2-z1_top2":
				self.appendSkinFile(self.daten + "infobar-x2-z1_top2.xml")

		### Timeshift_Channelname
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.skinSearchAndReplace.append(['"KravenName" position="20,527"', '"KravenName" position="20,510"'])
			self.skinSearchAndReplace.append(['"KravenName" position="20,452"', '"KravenName" position="20,450"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
			self.skinSearchAndReplace.append(['"KravenName" position="20,527"', '"KravenName" position="20,474"'])
			self.skinSearchAndReplace.append(['"KravenName" position="20,452"', '"KravenName" position="20,414"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
			self.skinSearchAndReplace.append(['"KravenName" position="20,527" size="1240,60"', '"KravenName" position="435,534" size="565,50"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName2.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
			self.skinSearchAndReplace.append(['"KravenName" position="20,527" size="1240,60"', '"KravenName" position="446,464" size="754,50"'])
			self.appendSkinFile(self.daten + config.plugins.KravenHD.InfobarChannelName2.value + ".xml")

		### Timeshift_clock-style_ib
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle2.value + ".xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1""infobar-style-zzz1"):
			self.appendSkinFile(self.daten + config.plugins.KravenHD.ClockStyle3.value + ".xml")

		### Timeshift_FTA
		if config.plugins.KravenHD.FTA.value == "none":
			self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

		### Timeshift_ecm-contents
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			if not config.plugins.KravenHD.ECMLine1.value == "none":
				self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine1.value])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			if not config.plugins.KravenHD.ECMLine2.value == "none":
				self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine2.value])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine3.value])

		### Timeshift_ecm-info
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			if not config.plugins.KravenHD.ECMLine1.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if not config.plugins.KravenHD.ECMLine2.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2"):
			if not config.plugins.KravenHD.ECMLine2.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz2":
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz3":
			if not config.plugins.KravenHD.ECMLine3.value == "none":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

		### Timeshift_system-info
		self.appendSkinFile(self.daten + config.plugins.KravenHD.SystemInfo.value + ".xml")

		### Timeshift_weather-style
		self.appendSkinFile(self.daten + self.actWeatherstyle + ".xml")

		### Timeshift_end
		self.appendSkinFile(self.daten + "timeshift-end.xml")

		### Plugins XML
		self.appendSkinFile(self.daten + "plugins.xml")

		### MSNWeatherPlugin XML
		console1 = eConsoleAppContainer()
		if fileExists("/usr/lib/enigma2/python/Components/Converter/MSNWeather.pyo"):
			self.appendSkinFile(self.daten + "MSNWeatherPlugin.xml")
			if not fileExists("/usr/share/enigma2/KravenHD/msn_weather_icons/1.png"):
				console1.execute("wget -q https://raw.githubusercontent.com/KravenHD/SevenHD-Daten/master/SevenHD/msn/msn-icon.tar.gz -O /tmp/msn-icon.tar.gz; tar xf /tmp/msn-icon.tar.gz -C /usr/share/enigma2/KravenHD/")
		else:
			self.appendSkinFile(self.daten + "MSNWeatherPlugin2.xml")

		### InfobarTunerState
		if self.actWeatherstyle in ("weather-big","weather-left"):
			if config.plugins.KravenHD.SystemInfo.value == "systeminfo-bigsat":
				self.appendSkinFile(self.daten + "infobartunerstate-low.xml")
			else:
				self.appendSkinFile(self.daten + "infobartunerstate-mid.xml")
		else:
			self.appendSkinFile(self.daten + "infobartunerstate-high.xml")

		### EMCSTYLE
		self.appendSkinFile(self.daten + config.plugins.KravenHD.EMCStyle.value + ".xml")

		### NumberZapExtStyle
		self.appendSkinFile(self.daten + config.plugins.KravenHD.NumberZapExt.value + ".xml")

		### PVRState
		self.appendSkinFile(self.daten + config.plugins.KravenHD.PVRState.value + ".xml")

		### cooltv XML
		self.appendSkinFile(self.daten + config.plugins.KravenHD.CoolTVGuide.value + ".xml")

		### MovieSelection XML
		self.appendSkinFile(self.daten + config.plugins.KravenHD.MovieSelection.value + ".xml")

		### SerienRecorder XML
		self.appendSkinFile(self.daten + config.plugins.KravenHD.SerienRecorder.value + ".xml")

		### MediaPortal
		console = eConsoleAppContainer()
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py"):
			if config.plugins.KravenHD.MediaPortal.value == "mediaportal":
				if config.plugins.KravenHD.IBColor.value == "all-screens" and config.plugins.KravenHD.IconStyle.value == "icons-light":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/MediaPortal_IB_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/")
				elif config.plugins.KravenHD.IBColor.value == "only-infobar" and config.plugins.KravenHD.IconStyle.value == "icons-light":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/")
				elif config.plugins.KravenHD.IBColor.value == "all-screens" and config.plugins.KravenHD.IconStyle.value == "icons-dark":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/MediaPortal_IB_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/")
				elif config.plugins.KravenHD.IBColor.value == "only-infobar" and config.plugins.KravenHD.IconStyle.value == "icons-dark":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/MediaPortal_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/")
				config.mediaportal.skin.value = "KravenHD"
				config.mediaportal.skin.save()

		### skin-user
		try:
			self.appendSkinFile(self.daten + "skin-user.xml")
		except:
			pass
		### skin-end
		self.appendSkinFile(self.daten + "skin-end.xml")

		xFile = open(self.dateiTMP, "w")
		for xx in self.skin_lines:
			xFile.writelines(xx)
		xFile.close()

		move(self.dateiTMP, self.datei)

		### Menu icons download - we do it here to give it some time
		if config.plugins.KravenHD.Logo.value in ("metrix-icons","minitv-metrix-icons"):
			self.installIcons(config.plugins.KravenHD.MenuIcons.value)

		### Get weather data to make sure the helper config values are not empty
		self.get_weather_data()
			
		# Make ibar graphics
		self.makeIbarpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value) # ibars

		if config.plugins.KravenHD.SystemInfo.value == "systeminfo-small":
			self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 185, "info") # sysinfo small
		elif config.plugins.KravenHD.SystemInfo.value == "systeminfo-big":
			self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 275, "info") # sysinfo big
		else:
			self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 375, "info") # sysinfo bigsat

		self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 905, 170, "shift") # timeshift bar

		self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 200, "wsmall") # weather small

		# Thats it
		self.restart()

	def restart(self):
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
			config.skin.primary_skin.setValue("KravenHD/skin.xml")
			config.skin.save()
			configfile.save()
			if fileExists("/usr/share/enigma2/KravenHD/icons-dark/icons/key_ok.png"):
				rmtree("/usr/share/enigma2/KravenHD/icons-dark/icons")
				rmtree("/usr/share/enigma2/KravenHD/icons-dark/infobar")
				rmtree("/usr/share/enigma2/KravenHD/icons-dark/message")
				rmtree("/usr/share/enigma2/KravenHD/icons-light/icons")
				rmtree("/usr/share/enigma2/KravenHD/icons-light/infobar")
				rmtree("/usr/share/enigma2/KravenHD/icons-light/message")
			if fileExists("/usr/share/enigma2/KravenHD/header-kraven/ibar_000000.png"):
				rmtree("/usr/share/enigma2/KravenHD/header-kraven")
			if fileExists("/usr/share/enigma2/KravenHD-menu-icons/setup.png"):
				rmtree("/usr/share/enigma2/KravenHD-menu-icons")
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		askExit = self.session.openWithCallback(self.doExit,MessageBox,_("Do you really want to exit without saving?"), MessageBox.TYPE_YESNO)
		askExit.setTitle(_("Exit"))

	def doExit(self,answer):
		if answer is True:
			for x in self["config"].list:
				if len(x) > 1:
						x[1].cancel()
				else:
						pass
			self.close()
		else:
			self.mylist()

	def reset(self):
		askReset = self.session.openWithCallback(self.doReset,MessageBox,_("Do you really want to reset all values to the selected default profile?"), MessageBox.TYPE_YESNO)
		askReset.setTitle(_("Reset profile"))

	def doReset(self,answer):
		if answer is True:
			if config.plugins.KravenHD.defaultProfile.value == "0":
				for name in config.plugins.KravenHD.dict():
					if not name in ("customProfile","DebugNames"):
						item=(getattr(config.plugins.KravenHD,name))
						item.value=item.default
			else:
				self.loadProfile(loadDefault=True)
		self.mylist()

	def showColor(self,actcolor):
		c = self["Canvas"]
		c.fill(0,0,368,207,actcolor)
		c.flush()

	def showText(self,fontsize,text):
		from enigma import gFont,RT_HALIGN_CENTER,RT_VALIGN_CENTER
		c = self["Canvas"]
		c.fill(0,0,368,207,self.RGB(0,0,0))
		c.writeText(0,0,368,207,self.RGB(255,255,255),self.RGB(0,0,0),gFont("Regular",fontsize),text,RT_HALIGN_CENTER+RT_VALIGN_CENTER)
		c.flush()

	def loadProfile(self,loadDefault=False):
		if loadDefault:
			profile=config.plugins.KravenHD.defaultProfile.value
			fname=self.profiles+"kraven_default_"+profile
		else:
			profile=config.plugins.KravenHD.customProfile.value
			fname=self.profiles+"kraven_profile_"+profile
		if profile and fileExists(fname):
			print ("KravenPlugin: Load profile "+fname)
			pFile=open(fname,"r")
			for line in pFile:
				try:
					line=line.split("|")
					name=line[0]
					value=line[1]
					type=line[2].strip('\n')
					if not (name in ("customProfile","DebugNames","weather_owm_latlon","weather_accu_latlon","weather_realtek_latlon","weather_accu_id","weather_foundcity","weather_gmcode","weather_cityname","weather_language","weather_server") or (loadDefault and name == "defaultProfile")):
						if type == "<type 'int'>":
							getattr(config.plugins.KravenHD,name).value=int(value)
						elif type == "<type 'hex'>":
							getattr(config.plugins.KravenHD,name).value=hex(value)
						elif type == "<type 'list'>":
							getattr(config.plugins.KravenHD,name).value=eval(value)
						else:
							getattr(config.plugins.KravenHD,name).value=str(value)
				except:
					pass
			pFile.close()
			# fix possible inconsistencies between boxes
			if SystemInfo.get("NumVideoDecoders",1)>1:
				if config.plugins.KravenHD.ChannelSelectionStyle.value!=config.plugins.KravenHD.ChannelSelectionStyle.default:
					config.plugins.KravenHD.ChannelSelectionStyle2.value=config.plugins.KravenHD.ChannelSelectionStyle.value
					config.plugins.KravenHD.ChannelSelectionStyle.value=config.plugins.KravenHD.ChannelSelectionStyle.default
			else:
				if config.plugins.KravenHD.ChannelSelectionStyle2.value!=config.plugins.KravenHD.ChannelSelectionStyle2.default:
					if config.plugins.KravenHD.ChannelSelectionStyle2.value in ("channelselection-style-minitv33","channelselection-style-minitv2","channelselection-style-minitv22"):
						config.plugins.KravenHD.ChannelSelectionStyle.value="channelselection-style-minitv3"
					elif config.plugins.KravenHD.ChannelSelectionStyle2.value == "channelselection-style-nobile-minitv33":
						config.plugins.KravenHD.ChannelSelectionStyle.value="channelselection-style-nobile-minitv3"
					else:
						config.plugins.KravenHD.ChannelSelectionStyle.value=config.plugins.KravenHD.ChannelSelectionStyle2.value
					config.plugins.KravenHD.ChannelSelectionStyle2.value=config.plugins.KravenHD.ChannelSelectionStyle2.default
		elif not loadDefault:
			print ("KravenPlugin: Create profile "+fname)
			self.saveProfile(msg=False)

	def saveProfile(self,msg=True):
		profile=config.plugins.KravenHD.customProfile.value
		if profile:
			try:
				fname=self.profiles+"kraven_profile_"+profile
				print ("KravenPlugin: Save profile "+fname)
				pFile=open(fname,"w")
				for name in config.plugins.KravenHD.dict():
					if not name in ("customProfile","DebugNames","weather_owm_latlon","weather_accu_latlon","weather_realtek_latlon","weather_accu_id","weather_foundcity","weather_gmcode","weather_cityname","weather_language","weather_server"):
						value=getattr(config.plugins.KravenHD,name).value
						pFile.writelines(name+"|"+str(value)+"|"+str(type(value))+"\n")
				pFile.close()
				if msg:
					self.session.open(MessageBox,_("Profile ")+str(profile)+_(" saved successfully."), MessageBox.TYPE_INFO, timeout=5)
			except:
				self.session.open(MessageBox,_("Profile ")+str(profile)+_(" could not be saved!"), MessageBox.TYPE_INFO, timeout=15)

	def installIcons(self,author):

		pathname="http://coolskins.de/downloads/kraven/"
		instname="/usr/share/enigma2/Kraven-menu-icons/iconpackname"
		versname="Kraven-Menu-Icons-by-"+author+".packname"
		
		# Read iconpack version on box
		packinstalled = "not installed"
		if fileExists(instname):
			pFile=open(instname,"r")
			for line in pFile:
				packinstalled=line.strip('\n')
			pFile.close()
		print ("KravenPlugin: Iconpack on box is "+packinstalled)
		
		# Read iconpack version on server
		packonserver = "unknown"
		fullversname=pathname+versname
		sub=subprocess.Popen("wget -q "+fullversname+" -O /tmp/"+versname,shell=True)
		sub.wait()
		if fileExists("/tmp/"+versname):
			pFile=open("/tmp/"+versname,"r")
			for line in pFile:
				packonserver=line.strip('\n')
			pFile.close()
			popen("rm /tmp/"+versname)
			print ("KravenPlugin: Iconpack on server is "+packonserver)

			# Download an install icon pack, if needed
			if packinstalled != packonserver:
				packname=packonserver
				fullpackname=pathname+packname
				sub=subprocess.Popen("rm -rf /usr/share/enigma2/Kraven-menu-icons/*.*; rm -rf /usr/share/enigma2/Kraven-menu-icons; wget -q "+fullpackname+" -O /tmp/"+packname+"; tar xf /tmp/"+packname+" -C /usr/share/enigma2/",shell=True)
				sub.wait()
				popen("rm /tmp/"+packname)
				print ("KravenPlugin: Installed iconpack "+fullpackname)
			else:
				print ("KravenPlugin: No need to install other iconpack")

	def makeIbarpng(self, newcolor, newtrans):

		width = 1280 # width of the png file
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder

		ibarheight = 310 # height of ibar
		ibargradientstart = 50 # start of ibar gradient (from top)
		ibargradientsize = 100 # size of ibar gradient

		ibaroheight = 165 # height of ibaro
		ibarogradientstart = 65 # start of ibaro gradient (from top)
		ibarogradientsize = 100 # size of ibaro gradient

		ibaro2height = 125 # height of ibaro2
		ibaro2gradientstart = 25 # start of ibaro2 gradient (from top)
		ibaro2gradientsize = 100 # size of ibaro2 gradient

		ibaro3height = 145 # height of ibaro3
		ibaro3gradientstart = 45 # start of ibaro3 gradient (from top)
		ibaro3gradientsize = 100 # size of ibaro3 gradient

		newcolor = newcolor[-6:]
		r = int(newcolor[0:2], 16)
		g = int(newcolor[2:4], 16)
		b = int(newcolor[4:6], 16)

		trans = (255-int(newtrans,16))/255.0

		img = Image.new("RGBA",(width,ibarheight),(r,g,b,0))
		gradient = Image.new("L",(1,ibarheight),int(255*trans))
		for pos in range(0,ibargradientstart):
			gradient.putpixel((0,pos),0)
		for pos in range(0,ibargradientsize):
			gradient.putpixel((0,ibargradientstart+pos),int(self.dexpGradient(ibargradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenHD/ibar.png")

		img = Image.new("RGBA",(width,ibaroheight),(r,g,b,0))
		gradient = Image.new("L",(1,ibaroheight),0)
		for pos in range(0,ibarogradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibarogradientsize):
			gradient.putpixel((0,ibarogradientstart+ibarogradientsize-pos-1),int(self.dexpGradient(ibarogradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenHD/ibaro.png")

		img = Image.new("RGBA",(width,ibaro2height),(r,g,b,0))
		gradient = Image.new("L",(1,ibaro2height),0)
		for pos in range(0,ibaro2gradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibaro2gradientsize):
			gradient.putpixel((0,ibaro2gradientstart+ibaro2gradientsize-pos-1),int(self.dexpGradient(ibaro2gradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenHD/ibaro2.png")

		img = Image.new("RGBA",(width,ibaro3height),(r,g,b,0))
		gradient = Image.new("L",(1,ibaro3height),0)
		for pos in range(0,ibaro3gradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibaro3gradientsize):
			gradient.putpixel((0,ibaro3gradientstart+ibaro3gradientsize-pos-1),int(self.dexpGradient(ibaro3gradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenHD/ibaro3.png")

	def makeRectpng(self, newcolor, newtrans, width, height, pngname):

		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder
		gradientsize = 80 # size of gradient

		newcolor = newcolor[-6:]
		r = int(newcolor[0:2], 16)
		g = int(newcolor[2:4], 16)
		b = int(newcolor[4:6], 16)

		trans = (255-int(newtrans,16))/255.0

		img = Image.new("RGBA",(width,height),(r,g,b,int(255*trans)))

		gradient = Image.new("RGBA",(1,gradientsize),(r,g,b,0))
		for pos in range(0,gradientsize):
			gradient.putpixel((0,pos),(r,g,b,int((self.dexpGradient(gradientsize,gradientspeed,pos))*trans)))

		hgradient = gradient.resize((width-2*gradientsize, gradientsize))
		img.paste(hgradient, (gradientsize,0,width-gradientsize,gradientsize))
		hgradient = hgradient.transpose(Image.ROTATE_180)
		img.paste(hgradient, (gradientsize,height-gradientsize,width-gradientsize,height))

		vgradient = gradient.transpose(Image.ROTATE_90)
		vgradient = vgradient.resize((gradientsize,height-2*gradientsize))
		img.paste(vgradient, (0,gradientsize,gradientsize,height-gradientsize))
		vgradient = vgradient.transpose(Image.ROTATE_180)
		img.paste(vgradient, (width-gradientsize,gradientsize,width,height-gradientsize))

		corner = Image.new("RGBA",(gradientsize,gradientsize),(r,g,b,0))
		for xpos in range(0,gradientsize):
			for ypos in range(0,gradientsize):
				dist = int(round((xpos**2+ypos**2)**0.503))
				corner.putpixel((xpos,ypos),(r,g,b,int((self.dexpGradient(gradientsize,gradientspeed,gradientsize-dist-1))*trans)))
		corner = corner.filter(ImageFilter.BLUR)
		img.paste(corner, (width-gradientsize,height-gradientsize,width,height))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (width-gradientsize,0,width,gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (0,0,gradientsize,gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (0,height-gradientsize,gradientsize,height))

		img.save("/usr/share/enigma2/KravenHD/"+pngname+".png")

	def dexpGradient(self,len,spd,pos):
		if pos < 0:
			pos = 0
		if pos > len-1:
			pos = len-1
		a = ((len/2)**spd)*2.0
		if pos <= len/2:
			f = (pos**spd)
		else:
			f = a-((len-pos)**spd)
		e = int((f/a)*255)
		return e

	def makeBackpng(self):
		# this makes a transparent png
		# not needed above, use it manually
		width = 1280 # width of the png file
		height = 720 # height of the png file
		img = Image.new("RGBA",(width,height),(0,0,0,0))
		img.save("/usr/share/enigma2/KravenHD/backg.png")

	def calcBrightness(self,color,factor):
		f = int(int(factor)*25.5-255)
		color = color[-6:]
		r = int(color[0:2],16)+f
		g = int(color[2:4],16)+f
		b = int(color[4:6],16)+f
		if r<0:
			r=0
		if g<0:
			g=0
		if b<0:
			b=0
		if r>255:
			r=255
		if g>255:
			g=255
		if b>255:
			b=255
		return str(hex(r)[2:4]).zfill(2)+str(hex(g)[2:4]).zfill(2)+str(hex(b)[2:4]).zfill(2)

	def calcTransparency(self,trans1,trans2):
		t1 = int(trans1,16)
		t2 = int(trans2,16)
		return str(hex(min(t1,t2))[2:4]).zfill(2)
		
	def hexRGB(self,color):
		color = color[-6:]
		r = int(color[0:2],16)
		g = int(color[2:4],16)
		b = int(color[4:6],16)
		return (r<<16)|(g<<8)|b

	def RGB(self,r,g,b):
		return (r<<16)|(g<<8)|b

	def get_weather_data(self):
			
			self.city = ''
			self.lat = ''
			self.lon = ''
			self.zipcode = ''
			self.accu_id = ''
			self.woe_id = ''
			self.gm_code = ''
			self.preview_text = ''
			self.preview_warning = ''
			
			if config.plugins.KravenHD.weather_search_over.value == 'ip':
			  self.get_latlon_by_ip()
			elif config.plugins.KravenHD.weather_search_over.value == 'name':
			  self.get_latlon_by_name()
			elif config.plugins.KravenHD.weather_search_over.value == 'gmcode':
			  self.get_latlon_by_gmcode()
			
			self.generate_owm_accu_realtek_string()
			if config.plugins.KravenHD.weather_server.value == '_accu':
			  self.get_accu_id_by_latlon()
	
			self.actCity=self.preview_text+self.preview_warning
			config.plugins.KravenHD.weather_foundcity.value=self.city
			config.plugins.KravenHD.weather_foundcity.save()
	
	def get_latlon_by_ip(self):
		try:
			res = requests.request('get', 'http://api.wunderground.com/api/2b0d6572c90d3e4a/geolookup/q/autoip.json')
			data = res.json()
			
			self.city = data['location']['city']
			self.lat = data['location']['lat'] 
			self.lon = data['location']['lon']
			
			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
		except:
			self.preview_text = _('No data for IP')
			
	def get_latlon_by_name(self):
		try:
			name = config.plugins.KravenHD.weather_cityname.getValue()
			res = requests.request('get', 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true' % str(name))
			data = res.json()
			
			for info in data['results'][0]['address_components'][0]['types']:
			  if 'locality' in info:
				 self.city = data['results'][0]['address_components'][0]['long_name']
			
			self.lat = data['results'][0]['geometry']['location']['lat']
			self.lon = data['results'][0]['geometry']['location']['lng']
			
			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
		except:
			self.get_latlon_by_ip()
			self.preview_warning = _('\n\nNo data for search string,\nfallback to IP')
	
	def get_latlon_by_gmcode(self):
		try:		  
			gmcode = config.plugins.KravenHD.weather_gmcode.value
			res = requests.request('get', 'http://wxdata.weather.com/wxdata/weather/local/%s?cc=*' % str(gmcode))
			data = fromstring(res.text)
			
			self.city = data[1][0].text.split(',')[0]
			self.lat = data[1][2].text
			self.lon = data[1][3].text
			
			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
		except:
			self.get_latlon_by_ip()
			self.preview_warning = _('\n\nNo data for GM code,\nfallback to IP')
			
	def get_accu_id_by_latlon(self):
		try:
			res = requests.request('get', 'http://realtek.accu-weather.com/widget/realtek/weather-data.asp?%s' % config.plugins.KravenHD.weather_realtek_latlon.value)
			
			cityId = re.search('cityId>(.+?)</cityId', str(res.text)).groups(1)
			city = re.search('city>(.+?)</city', str(res.text)).groups(1)
			lat = re.search('lat>(.+?)</lat', str(res.text)).groups(1)
			lon = re.search('lon>(.+?)</lon', str(res.text)).groups(1)
			
			self.city = str(city[0])
			self.accu_id = str(cityId[0])
			self.lat = str(lat[0])
			self.lon = str(lon[0])
			
			config.plugins.KravenHD.weather_accu_id.value = str(self.accu_id)
			config.plugins.KravenHD.weather_accu_id.save()
			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
		except:
			self.preview_text = _('No Accu ID found')
			
	def generate_owm_accu_realtek_string(self):
		config.plugins.KravenHD.weather_owm_latlon.value = 'lat=%s&lon=%s&units=metric&lang=%s' % (str(self.lat),str(self.lon),str(config.plugins.KravenHD.weather_language.value))
		config.plugins.KravenHD.weather_accu_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenHD.weather_language.value))
		config.plugins.KravenHD.weather_realtek_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenHD.weather_language.value))
		config.plugins.KravenHD.weather_owm_latlon.save()
		config.plugins.KravenHD.weather_accu_latlon.save()
		config.plugins.KravenHD.weather_realtek_latlon.save()
