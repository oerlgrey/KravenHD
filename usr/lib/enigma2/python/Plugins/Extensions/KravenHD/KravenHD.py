# -*- coding: utf-8 -*-

#  Kraven Plugin
#
#  Coded/Modified/Adapted by örlgrey
#  Based on VTi and/or OpenATV image source code
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

from __future__ import absolute_import
from __future__ import print_function
from .ColorSelection import KravenHDColorSelection
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from copy import deepcopy
from Components.config import config, configfile, getConfigListEntry, ConfigYesNo, ConfigSubsection, ConfigSelection, ConfigText, ConfigClock, ConfigSlider
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, system, popen, path
from shutil import move
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from Components.SystemInfo import SystemInfo
from PIL import Image, ImageFilter, ImageDraw
import gettext, time, subprocess, requests
from enigma import ePicLoad, getDesktop, eConsoleAppContainer, eTimer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS

import six


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

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block

ColorSelfList = [
	("F0A30A", _("amber")),
	("B27708", _("amber dark")),
	("1B1775", _("blue")),
	("0E0C3F", _("blue dark")),
	("7D5929", _("brown")),
	("3F2D15", _("brown dark")),
	("0050EF", _("cobalt")),
	("001F59", _("cobalt dark")),
	("1BA1E2", _("cyan")),
	("0F5B7F", _("cyan dark")),
	("FFEA04", _("yellow")),
	("999999", _("grey")),
	("3F3F3F", _("grey dark")),
	("70AD11", _("green")),
	("213305", _("green dark")),
	("A19181", _("Kraven")),
	("28150B", _("Kraven dark")),
	("6D8764", _("olive")),
	("313D2D", _("olive dark")),
	("C3461B", _("orange")),
	("892E13", _("orange dark")),
	("F472D0", _("pink")),
	("723562", _("pink dark")),
	("E51400", _("red")),
	("330400", _("red dark")),
	("000000", _("black")),
	("008A00", _("emerald")),
	("647687", _("steel")),
	("262C33", _("steel dark")),
	("6C0AAB", _("violet")),
	("1F0333", _("violet dark")),
	("ffffff", _("white")),
	("self", _("self"))
	]

BackgroundList = [
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
	("008A00", _("emerald")),
	("647687", _("steel")),
	("262C33", _("steel dark")),
	("131619", _("steel very dark")),
	("6C0AAB", _("violet")),
	("1F0333", _("violet dark")),
	("11001E", _("violet very dark")),
	("ffffff", _("white"))
	]

TextureList = []

for i in range(1, 50):
	n=str(i)
	if fileExists("/usr/share/enigma2/Kraven-user-icons/usertexture"+n+".png") or fileExists("/usr/share/enigma2/Kraven-user-icons/usertexture"+n+".jpg"):
		TextureList.append(("usertexture"+n, _("user texture")+" "+n))
for i in range(1, 50):
	n=str(i)
	if fileExists("/usr/share/enigma2/KravenHD/textures/texture"+n+".png") or fileExists("/usr/share/enigma2/KravenHD/textures/texture"+n+".jpg"):
		TextureList.append(("texture"+n, _("texture")+" "+n))

BorderSelfList = deepcopy(ColorSelfList)
BorderSelfList.append(("none", _("off")))

BackgroundSelfList = deepcopy(BackgroundList)
BackgroundSelfList.append(("self", _("self")))

BackgroundSelfGradientList = deepcopy(BackgroundSelfList)
BackgroundSelfGradientList.append(("gradient", _("gradient")))

BackgroundSelfTextureList = deepcopy(BackgroundSelfList)
BackgroundSelfTextureList.append(("texture", _("texture")))

BackgroundSelfGradientTextureList = deepcopy(BackgroundSelfGradientList)
BackgroundSelfGradientTextureList.append(("texture", _("texture")))

LanguageList = [
	("de", _("Deutsch")),
	("en", _("English")),
	("ru", _("Russian")),
	("it", _("Italian")),
	("es", _("Spanish (es)")),
	("sp", _("Spanish (sp)")),
	("uk", _("Ukrainian (uk)")),
	("ua", _("Ukrainian (ua)")),
	("pt", _("Portuguese")),
	("ro", _("Romanian")),
	("pl", _("Polish")),
	("fi", _("Finnish")),
	("nl", _("Dutch")),
	("fr", _("French")),
	("bg", _("Bulgarian")),
	("sv", _("Swedish (sv)")),
	("se", _("Swedish (se)")),
	("zh_tw", _("Chinese Traditional")),
	("zh", _("Chinese Simplified (zh)")),
	("zh_cn", _("Chinese Simplified (zh_cn)")),
	("tr", _("Turkish")),
	("hr", _("Croatian")),
	("ca", _("Catalan"))
	]

TransList = [
	("00", "0%"),
	("0C", "5%"),
	("18", "10%"),
	("32", "20%"),
	("58", "35%"),
	("7E", "50%")
	]

ProgressList = [
	("F0A30A", _("amber")),
	("B27708", _("amber dark")),
	("1B1775", _("blue")),
	("0E0C3F", _("blue dark")),
	("7D5929", _("brown")),
	("3F2D15", _("brown dark")),
	("progress", _("colorfull")),
	("0050EF", _("cobalt")),
	("001F59", _("cobalt dark")),
	("1BA1E2", _("cyan")),
	("0F5B7F", _("cyan dark")),
	("FFEA04", _("yellow")),
	("999999", _("grey")),
	("3F3F3F", _("grey dark")),
	("70AD11", _("green")),
	("213305", _("green dark")),
	("A19181", _("Kraven")),
	("28150B", _("Kraven dark")),
	("6D8764", _("olive")),
	("313D2D", _("olive dark")),
	("C3461B", _("orange")),
	("892E13", _("orange dark")),
	("F472D0", _("pink")),
	("723562", _("pink dark")),
	("E51400", _("red")),
	("330400", _("red dark")),
	("000000", _("black")),
	("008A00", _("emerald")),
	("647687", _("steel")),
	("262C33", _("steel dark")),
	("6C0AAB", _("violet")),
	("1F0333", _("violet dark")),
	("ffffff", _("white")),
	("self", _("self"))
	]

config.plugins.KravenHD = ConfigSubsection()
currenttime = time.localtime()
primetime = (currenttime[0],currenttime[1],currenttime[2], 20, 15, 0, 0, 0, 0)
config.plugins.KravenHD.Primetime = ConfigClock(default=time.mktime(primetime))
config.plugins.KravenHD.InfobarAntialias = ConfigSlider(default=10, increment=1, limits=(0, 20))
config.plugins.KravenHD.ECMLineAntialias = ConfigSlider(default=10, increment=1, limits=(0, 20))
config.plugins.KravenHD.ScreensAntialias = ConfigSlider(default=10, increment=1, limits=(0, 20))
config.plugins.KravenHD.SelfColorR = ConfigSlider(default=0, increment=5, limits=(0, 255))
config.plugins.KravenHD.SelfColorG = ConfigSlider(default=0, increment=5, limits=(0, 255))
config.plugins.KravenHD.SelfColorB = ConfigSlider(default=75, increment=5, limits=(0, 255))

config.plugins.KravenHD.customProfile = ConfigSelection(default="1", choices = [
				("1", _("1")),
				("2", _("2")),
				("3", _("3")),
				("4", _("4")),
				("5", _("5"))
				])

profList = [("default", _("0 (hardcoded)"))]
for i in range(1, 21):
	n = name = str(i)
	if fileExists("/etc/enigma2/kravenhd_default_" + n):
		if i == 1:
			name = '1 ' + _("MiniTV")
		elif i == 2:
			name = '2 ' + _("dark")
		elif i == 3:
			name = '3 ' + _("light")
		elif i == 4:
			name = '4 ' + _("colored")
		profList.append((n, _(name)))
config.plugins.KravenHD.defaultProfile = ConfigSelection(default="default", choices = profList)
				
config.plugins.KravenHD.refreshInterval = ConfigSelection(default="60", choices = [
				("15", _("15")),
				("30", _("30")),
				("60", _("60")),
				("120", _("120")),
				("240", _("240")),
				("480", _("480"))
				])

config.plugins.KravenHD.Volume = ConfigSelection(default="volume-border", choices = [
				("volume-original", _("original")),
				("volume-border", _("with Border")),
				("volume-left", _("left")),
				("volume-right", _("right")),
				("volume-top", _("top")),
				("volume-center", _("center"))
				])

config.plugins.KravenHD.BackgroundColorTrans = ConfigSelection(default="32", choices = TransList)

config.plugins.KravenHD.InfobarColorTrans = ConfigSelection(default="00", choices = TransList)

config.plugins.KravenHD.BackgroundListColor = ConfigSelection(default="self", choices = BackgroundSelfGradientTextureList)
config.plugins.KravenHD.BackgroundSelfColor = ConfigText(default="000000")
config.plugins.KravenHD.BackgroundColor = ConfigText(default="000000")

config.plugins.KravenHD.BackgroundAlternateListColor = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenHD.BackgroundAlternateSelfColor = ConfigText(default="000000")
config.plugins.KravenHD.BackgroundAlternateColor = ConfigText(default="000000")

config.plugins.KravenHD.InfobarGradientListColor = ConfigSelection(default="self", choices = BackgroundSelfTextureList)
config.plugins.KravenHD.InfobarGradientSelfColor = ConfigText(default="000000")
config.plugins.KravenHD.InfobarGradientColor = ConfigText(default="000000")

config.plugins.KravenHD.InfobarBoxListColor = ConfigSelection(default="self", choices = BackgroundSelfGradientTextureList)
config.plugins.KravenHD.InfobarBoxSelfColor = ConfigText(default="000000")
config.plugins.KravenHD.InfobarBoxColor = ConfigText(default="000000")

config.plugins.KravenHD.InfobarAlternateListColor = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenHD.InfobarAlternateSelfColor = ConfigText(default="000000")
config.plugins.KravenHD.InfobarAlternateColor = ConfigText(default="000000")

config.plugins.KravenHD.BackgroundGradientListColorPrimary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenHD.BackgroundGradientSelfColorPrimary = ConfigText(default="000000")
config.plugins.KravenHD.BackgroundGradientColorPrimary = ConfigText(default="000000")

config.plugins.KravenHD.BackgroundGradientListColorSecondary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenHD.BackgroundGradientSelfColorSecondary = ConfigText(default="000000")
config.plugins.KravenHD.BackgroundGradientColorSecondary = ConfigText(default="000000")

config.plugins.KravenHD.InfobarGradientListColorPrimary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenHD.InfobarGradientSelfColorPrimary = ConfigText(default="000000")
config.plugins.KravenHD.InfobarGradientColorPrimary = ConfigText(default="000000")

config.plugins.KravenHD.InfobarGradientListColorSecondary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenHD.InfobarGradientSelfColorSecondary = ConfigText(default="000000")
config.plugins.KravenHD.InfobarGradientColorSecondary = ConfigText(default="000000")

config.plugins.KravenHD.Font1List = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.Font1Self = ConfigText(default="ffffff")
config.plugins.KravenHD.Font1 = ConfigText(default="ffffff")

config.plugins.KravenHD.Font2List = ConfigSelection(default="F0A30A", choices = ColorSelfList)
config.plugins.KravenHD.Font2Self = ConfigText(default="F0A30A")
config.plugins.KravenHD.Font2 = ConfigText(default="F0A30A")

config.plugins.KravenHD.IBFont1List = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.IBFont1Self = ConfigText(default="ffffff")
config.plugins.KravenHD.IBFont1 = ConfigText(default="ffffff")

config.plugins.KravenHD.IBFont2List = ConfigSelection(default="F0A30A", choices = ColorSelfList)
config.plugins.KravenHD.IBFont2Self = ConfigText(default="F0A30A")
config.plugins.KravenHD.IBFont2 = ConfigText(default="F0A30A")

config.plugins.KravenHD.PermanentClockFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.PermanentClockFontSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.PermanentClockFont = ConfigText(default="ffffff")

config.plugins.KravenHD.SelectionFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.SelectionFontSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.SelectionFont = ConfigText(default="ffffff")

config.plugins.KravenHD.MarkedFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.MarkedFontSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.MarkedFont = ConfigText(default="ffffff")

config.plugins.KravenHD.ECMFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.ECMFontSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.ECMFont = ConfigText(default="ffffff")

config.plugins.KravenHD.ChannelnameFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.ChannelnameFontSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.ChannelnameFont = ConfigText(default="ffffff")

config.plugins.KravenHD.PrimetimeFontList = ConfigSelection(default="70AD11", choices = ColorSelfList)
config.plugins.KravenHD.PrimetimeFontSelf = ConfigText(default="70AD11")
config.plugins.KravenHD.PrimetimeFont = ConfigText(default="70AD11")

config.plugins.KravenHD.ButtonTextList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.ButtonTextSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.ButtonText = ConfigText(default="ffffff")

config.plugins.KravenHD.AndroidList = ConfigSelection(default="000000", choices = ColorSelfList)
config.plugins.KravenHD.AndroidSelf = ConfigText(default="000000")
config.plugins.KravenHD.Android = ConfigText(default="000000")

config.plugins.KravenHD.BorderList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.BorderSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.Border = ConfigText(default="ffffff")

config.plugins.KravenHD.ProgressList = ConfigSelection(default="C3461B", choices = ProgressList)
config.plugins.KravenHD.ProgressSelf = ConfigText(default="C3461B")
config.plugins.KravenHD.Progress = ConfigText(default="C3461B")

config.plugins.KravenHD.LineList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.LineSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.Line = ConfigText(default="ffffff")

config.plugins.KravenHD.IBLineList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.IBLineSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.IBLine = ConfigText(default="ffffff")

config.plugins.KravenHD.IBStyle = ConfigSelection(default="grad", choices = [
				("grad", _("gradient")),
				("box", _("box"))
				])

config.plugins.KravenHD.InfoStyle = ConfigSelection(default="gradient", choices = [
				("gradient", _("gradient")),
				("primary", _("          Primary Color")),
				("secondary", _("          Secondary Color"))
				])

config.plugins.KravenHD.InfobarTexture = ConfigSelection(default="texture1", choices = TextureList)
				
config.plugins.KravenHD.BackgroundTexture = ConfigSelection(default="texture1", choices = TextureList)

config.plugins.KravenHD.SelectionStyle = ConfigSelection(default="color", choices = [
				("color", _("solid color")),
				("pixmap", _("two-colored"))
				])

config.plugins.KravenHD.SelectionBackgroundList = ConfigSelection(default="0050EF", choices = ColorSelfList)
config.plugins.KravenHD.SelectionBackgroundSelf = ConfigText(default="0050EF")
config.plugins.KravenHD.SelectionBackground = ConfigText(default="0050EF")

config.plugins.KravenHD.SelectionBackground2List = ConfigSelection(default="001F59", choices = BackgroundSelfList)
config.plugins.KravenHD.SelectionBackground2Self = ConfigText(default="001F59")
config.plugins.KravenHD.SelectionBackground2 = ConfigText(default="001F59")

config.plugins.KravenHD.SelectionBorderList = ConfigSelection(default="ffffff", choices = BorderSelfList)
config.plugins.KravenHD.SelectionBorderSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.SelectionBorder = ConfigText(default="ffffff")

config.plugins.KravenHD.MiniTVBorderList = ConfigSelection(default="3F3F3F", choices = ColorSelfList)
config.plugins.KravenHD.MiniTVBorderSelf = ConfigText(default="3F3F3F")
config.plugins.KravenHD.MiniTVBorder = ConfigText(default="3F3F3F")

config.plugins.KravenHD.AnalogColorList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.AnalogColorSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.AnalogColor = ConfigText(default="ffffff")

config.plugins.KravenHD.InfobarStyle = ConfigSelection(default="infobar-style-x3", choices = [
				("infobar-style-nopicon", _("no Picon")),
				("infobar-style-x1", _("X1")),
				("infobar-style-x2", _("X2")),
				("infobar-style-x3", _("X3")),
				("infobar-style-z1", _("Z1")),
				("infobar-style-z2", _("Z2")),
				("infobar-style-zz1", _("ZZ1")),
				("infobar-style-zz2", _("ZZ2")),
				("infobar-style-zz3", _("ZZ3")),
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

config.plugins.KravenHD.IBFontSize = ConfigSelection(default="big", choices = [
				("small", _("small")),
				("middle", _("middle")),
				("big", _("big"))
				])

config.plugins.KravenHD.TypeWriter = ConfigSelection(default="runningtext", choices = [
				("typewriter", _("typewriter")),
				("runningtext", _("runningtext")),
				("none", _("off"))
				])

config.plugins.KravenHD.ChannelSelectionStyle = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-nopicon2", _("no Picon2")),
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
				("channelselection-style-nobile-minitv3", _("Nobile Preview")),
				("channelselection-style-minitv-picon", _("MiniTV Picon"))
				])

config.plugins.KravenHD.ChannelSelectionStyle2 = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-nopicon2", _("no Picon2")),
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
				("channelselection-style-nobile-minitv33", _("Nobile Extended Preview")),
				("channelselection-style-minitv-picon", _("MiniTV Picon"))
				])

config.plugins.KravenHD.ChannelSelectionStyle3 = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-nopicon2", _("no Picon2")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-minitv-picon", _("MiniTV Picon"))
				])

config.plugins.KravenHD.ChannelSelectionMode = ConfigSelection(default="zap", choices = [
				("zap", _("Zap (1xOK)")),
				("preview", _("Preview (2xOK)"))
				])

config.plugins.KravenHD.ChannelSelectionTrans = ConfigSelection(default="32", choices = TransList)

config.plugins.KravenHD.ChannelSelectionEPGSize1 = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenHD.ChannelSelectionEPGSize2 = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenHD.ChannelSelectionEPGSize3 = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenHD.ChannelSelectionServiceNAList = ConfigSelection(default="FFEA04", choices = ColorSelfList)
config.plugins.KravenHD.ChannelSelectionServiceNASelf = ConfigText(default="FFEA04")
config.plugins.KravenHD.ChannelSelectionServiceNA = ConfigText(default="FFEA04")

config.plugins.KravenHD.NumberZapExt = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("numberzapext-xpicon", _("X-Picons")),
				("numberzapext-zpicon", _("Z-Picons")),
				("numberzapext-zzpicon", _("ZZ-Picons")),
				("numberzapext-zzzpicon", _("ZZZ-Picons"))
				])

config.plugins.KravenHD.NZBorderList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.NZBorderSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.NZBorder = ConfigText(default="ffffff")

config.plugins.KravenHD.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("MiniTV")),
				("cooltv-picon", _("Picon"))
				])

config.plugins.KravenHD.GraphicalEPG = ConfigSelection(default="text-minitv", choices = [
				("text", _("Text")),
				("text-minitv", _("Text with MiniTV")),
				("graphical", _("graphical")),
				("graphical-minitv", _("graphical with MiniTV"))
				])

config.plugins.KravenHD.GMEDescriptionSize = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenHD.GMESelFgList = ConfigSelection(default="ffffff", choices = [
				("ffffff", _("white")),
				("F0A30A", _("amber")),
				("self", _("self"))
				])
config.plugins.KravenHD.GMESelFgSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.GMESelFg = ConfigText(default="ffffff")

config.plugins.KravenHD.GMESelBgList = ConfigSelection(default="389416", choices = [
				("389416", _("green")),
				("0064c7", _("blue")),
				("self", _("self"))
				])
config.plugins.KravenHD.GMESelBgSelf = ConfigText(default="389416")
config.plugins.KravenHD.GMESelBg = ConfigText(default="389416")

config.plugins.KravenHD.GMENowFgList = ConfigSelection(default="F0A30A", choices = [
				("ffffff", _("white")),
				("F0A30A", _("amber")),
				("self", _("self"))
				])
config.plugins.KravenHD.GMENowFgSelf = ConfigText(default="F0A30A")
config.plugins.KravenHD.GMENowFg = ConfigText(default="F0A30A")

config.plugins.KravenHD.GMENowBgList = ConfigSelection(default="0064c7", choices = [
				("389416", _("green")),
				("0064c7", _("blue")),
				("self", _("self"))
				])
config.plugins.KravenHD.GMENowBgSelf = ConfigText(default="0064c7")
config.plugins.KravenHD.GMENowBg = ConfigText(default="0064c7")

config.plugins.KravenHD.GMEBorderList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.GMEBorderSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.GMEBorder = ConfigText(default="ffffff")

config.plugins.KravenHD.MovieSelection = ConfigSelection(default="movieselection-no-cover", choices = [
				("movieselection-no-cover", _("no Cover")),
				("movieselection-no-cover2", _("no Cover2")),
				("movieselection-small-cover", _("small Cover")),
				("movieselection-big-cover", _("big Cover")),
				("movieselection-minitv", _("MiniTV")),
				("movieselection-minitv-cover", _("MiniTV + Cover"))
				])

config.plugins.KravenHD.EPGSelection = ConfigSelection(default="epgselection-standard", choices = [
				("epgselection-standard", _("standard")),
				("epgselection-minitv", _("MiniTV"))
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
				("emc-minitv2", _("MiniTV2")),
				("emc-full", _("full"))
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

config.plugins.KravenHD.RunningTextSpeed2 = ConfigSelection(default="steptime=100", choices = [
				("steptime=200", _("5 px/sec")),
				("steptime=100", _("10 px/sec")),
				("steptime=50", _("20 px/sec")),
				("steptime=33", _("30 px/sec"))
				])

config.plugins.KravenHD.ScrollBar = ConfigSelection(default="on", choices = [
				("on", _("on")),
				("none", _("off"))
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
				("clock-flip", _("flip")),
				("clock-weather", _("weather icon"))
				])

config.plugins.KravenHD.ClockStyleNoInternet = ConfigSelection(default="clock-classic", choices = [
				("clock-classic", _("standard")),
				("clock-classic-big", _("standard big")),
				("clock-analog", _("analog")),
				("clock-color", _("colored")),
				("clock-flip", _("flip"))
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

config.plugins.KravenHD.WeatherStyle3 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-left", _("on")),
				("netatmobar", _("NetatmoBar"))
				])

config.plugins.KravenHD.WeatherStyleNoInternet = ConfigSelection(default="none", choices = [
				("none", _("off"))
				])

config.plugins.KravenHD.ECMVisible = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("ib", _("Infobar")),
				("sib", _("SecondInfobar")),
				("ib+sib", _("Infobar & SecondInfobar"))
				])

config.plugins.KravenHD.ECMLine1 = ConfigSelection(default="ShortReader", choices = [
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact"))
				])

config.plugins.KravenHD.ECMLine2 = ConfigSelection(default="ShortReader", choices = [
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact")),
				("Normal", _("balanced")),
				("Long", _("extensive")),
				("VeryLong", _("complete"))
				])

config.plugins.KravenHD.ECMLine3 = ConfigSelection(default="ShortReader", choices = [
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
				("sib1", _("MiniTV/weather")),
				("sib2", _("left/right")),
				("sib3", _("single")),
				("sib4", _("MiniTV")),
				("sib5", _("MiniTV2")),
				("sib6", _("Weather")),
				("sib7", _("Weather2"))
				])

config.plugins.KravenHD.TunerBusyList = ConfigSelection(default="CCCC00", choices = [
				("CCCC00", _("yellow")),
				("self", _("self"))
				])
config.plugins.KravenHD.TunerBusySelf = ConfigText(default="CCCC00")
config.plugins.KravenHD.TunerBusy = ConfigText(default="CCCC00")

config.plugins.KravenHD.TunerLiveList = ConfigSelection(default="00B400", choices = [
				("00B400", _("green")),
				("self", _("self"))
				])
config.plugins.KravenHD.TunerLiveSelf = ConfigText(default="00B400")
config.plugins.KravenHD.TunerLive = ConfigText(default="00B400")

config.plugins.KravenHD.TunerRecordList = ConfigSelection(default="FF0C00", choices = [
				("FF0C00", _("red")),
				("self", _("self"))
				])
config.plugins.KravenHD.TunerRecordSelf = ConfigText(default="FF0C00")
config.plugins.KravenHD.TunerRecord = ConfigText(default="FF0C00")

config.plugins.KravenHD.TunerXtremeBusyList = ConfigSelection(default="1BA1E2", choices = [
				("1BA1E2", _("cyan")),
				("self", _("self"))
				])
config.plugins.KravenHD.TunerXtremeBusySelf = ConfigText(default="1BA1E2")
config.plugins.KravenHD.TunerXtremeBusy = ConfigText(default="1BA1E2")

config.plugins.KravenHD.ShowUnusedTuner = ConfigSelection(default="on", choices = [
				("on", _("on")),
				("none", _("off"))
				])

config.plugins.KravenHD.ShowAgcSnr = ConfigSelection(default="none", choices = [
				("on", _("on")),
				("none", _("off"))
				])
				
config.plugins.KravenHD.Infobox = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("db", _("Tuner/Satellite + dB")),
				("tunerinfo", _("Tunerinfo")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])
				
config.plugins.KravenHD.Infobox2 = ConfigSelection(default="tunerinfo", choices = [
				("tunerinfo", _("Tunerinfo")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])

config.plugins.KravenHD.IBColor = ConfigSelection(default="all-screens", choices = [
				("all-screens", _("in all Screens")),
				("only-infobar", _("only Infobar, SecondInfobar & Players"))
				])

config.plugins.KravenHD.About = ConfigSelection(default="about", choices = [
				("about", _("KravenHD"))
				])

config.plugins.KravenHD.Logo = ConfigSelection(default="minitv", choices = [
				("logo", _("Logo")),
				("minitv", _("MiniTV")),
				("metrix-icons", _("Icons")),
				("minitv-metrix-icons", _("MiniTV + Icons"))
				])

config.plugins.KravenHD.LogoNoInternet = ConfigSelection(default="minitv", choices = [
				("logo", _("Logo")),
				("minitv", _("MiniTV"))
				])

config.plugins.KravenHD.MainmenuFontsize = ConfigSelection(default="mainmenu-big", choices = [
				("mainmenu-small", _("small")),
				("mainmenu-middle", _("middle")),
				("mainmenu-big", _("big"))
				])

config.plugins.KravenHD.MainmenuHorTitleFontList = ConfigSelection(default="F0A30A", choices = ColorSelfList)
config.plugins.KravenHD.MainmenuHorTitleFontSelf = ConfigText(default="F0A30A")
config.plugins.KravenHD.MainmenuHorTitleFont = ConfigText(default="F0A30A")

config.plugins.KravenHD.MainmenuHorIconColorList = ConfigSelection(default="3F3F3F", choices = ColorSelfList)
config.plugins.KravenHD.MainmenuHorIconColorSelf = ConfigText(default="3F3F3F")
config.plugins.KravenHD.MainmenuHorIconColor = ConfigText(default="3F3F3F")

config.plugins.KravenHD.MenuIcons = ConfigSelection(default="stony272", choices = [
				("stony272", _("stony272")),
				("stony272-metal", _("stony272-metal")),
				("stony272-gold-round", _("stony272-gold-round")),
				("stony272-gold-square", _("stony272-gold-square")),
				("rennmaus-kleinerteufel", _("rennmaus-kleiner.teufel"))
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

config.plugins.KravenHD.Primetimeavailable = ConfigSelection(default="primetime-on", choices = [
				("none", _("off")),
				("primetime-on", _("on"))
				])

config.plugins.KravenHD.EMCSelectionColors = ConfigSelection(default="global", choices = [
				("global", _("global colors")),
				("custom", _("define new colors"))
				])

config.plugins.KravenHD.EMCSelectionBackgroundList = ConfigSelection(default="213305", choices = ColorSelfList)
config.plugins.KravenHD.EMCSelectionBackgroundSelf = ConfigText(default="213305")
config.plugins.KravenHD.EMCSelectionBackground = ConfigText(default="213305")

config.plugins.KravenHD.EMCSelectionFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.EMCSelectionFontSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.EMCSelectionFont = ConfigText(default="ffffff")

config.plugins.KravenHD.SerienRecorder = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("serienrecorder", _("on"))
				])

config.plugins.KravenHD.MediaPortal = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("mediaportal", _("on"))
				])

config.plugins.KravenHD.PVRState = ConfigSelection(default="pvrstate-center-big", choices = [
				("pvrstate-center-big", _("center big")),
				("pvrstate-center-small", _("center small")),
				("pvrstate-left-small", _("left small")),
				("pvrstate-off", _("off"))
				])

config.plugins.KravenHD.PigStyle = ConfigText(default="")
config.plugins.KravenHD.PigMenuActive = ConfigYesNo(default=False)

config.plugins.KravenHD.FileCommander = ConfigSelection(default="filecommander-hor", choices = [
				("filecommander-hor", _("horizontal")),
				("filecommander-ver", _("vertical"))
				])

config.plugins.KravenHD.weather_cityname = ConfigText(default = "")
config.plugins.KravenHD.weather_language = ConfigSelection(default="de", choices = LanguageList)

config.plugins.KravenHD.weather_search_over = ConfigSelection(default="ip", choices = [
				("ip", _("Auto (IP)")),
				("name", _("Search String"))
				])

config.plugins.KravenHD.weather_accu_latlon = ConfigText(default = "")
config.plugins.KravenHD.weather_accu_apikey = ConfigText(default = "")
config.plugins.KravenHD.weather_accu_id = ConfigText(default = "")
config.plugins.KravenHD.weather_foundcity = ConfigText(default = "")

config.plugins.KravenHD.PlayerClock = ConfigSelection(default="player-classic", choices = [
				("player-classic", _("standard")),
				("player-android", _("android")),
				("player-flip", _("flip")),
				("player-weather", _("weather icon"))
				])

config.plugins.KravenHD.Android2List = ConfigSelection(default="000000", choices = ColorSelfList)
config.plugins.KravenHD.Android2Self = ConfigText(default="000000")
config.plugins.KravenHD.Android2 = ConfigText(default="000000")

config.plugins.KravenHD.CategoryProfiles = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategorySystem = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryGlobalColors = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryInfobarLook = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryInfobarContents = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryWeather = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryClock = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryECMInfos = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryViews = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryChannellist = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryNumberZap = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryGraphicalEPG = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryEMC = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryPlayers = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryAntialiasing = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.CategoryVarious = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenHD.UnwatchedColorList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.UnwatchedColorSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.UnwatchedColor = ConfigText(default="ffffff")

config.plugins.KravenHD.WatchingColorList = ConfigSelection(default="0050EF", choices = ColorSelfList)
config.plugins.KravenHD.WatchingColorSelf = ConfigText(default="0050EF")
config.plugins.KravenHD.WatchingColor = ConfigText(default="0050EF")

config.plugins.KravenHD.FinishedColorList = ConfigSelection(default="70AD11", choices = ColorSelfList)
config.plugins.KravenHD.FinishedColorSelf = ConfigText(default="70AD11")
config.plugins.KravenHD.FinishedColor = ConfigText(default="70AD11")

config.plugins.KravenHD.PermanentClock = ConfigSelection(default="permanentclock-infobar-big", choices = [
				("permanentclock-infobar-big", _("infobar colors big")),
				("permanentclock-infobar-small", _("infobar colors small")),
				("permanentclock-global-big", _("global colors big")),
				("permanentclock-global-small", _("global colors small")),
				("permanentclock-transparent-big", _("transparent big")),
				("permanentclock-transparent-small", _("transparent small"))
				])

config.plugins.KravenHD.KravenIconVPosition = ConfigSelection(default="vposition-2", choices = [
				("vposition-3", _("-3")),
				("vposition-2", _("-2")),
				("vposition-1", _("-1")),
				("vposition0", _("0")),
				("vposition+1", _("+1")),
				("vposition+2", _("+2")),
				("vposition+3", _("+3"))
				])

config.plugins.KravenHD.SkinResolution = ConfigSelection(default="hd", choices = [
				("hd", _("HD")),
				("fhd", _("FHD"))
				])

config.plugins.KravenHD.PopupStyle = ConfigSelection(default="popup-grad-trans", choices = [
				("popup-grad-trans", _("gradient transparent")),
				("popup-grad", _("gradient")),
				("popup-box-trans", _("box transparent")),
				("popup-box", _("box"))
				])

config.plugins.KravenHD.IBProgressList = ConfigSelection(default="ffffff", choices = ProgressList)
config.plugins.KravenHD.IBProgressSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.IBProgress = ConfigText(default="ffffff")

config.plugins.KravenHD.IBProgressBackgroundList = ConfigSelection(default="1BA1E2", choices = BorderSelfList)
config.plugins.KravenHD.IBProgressBackgroundSelf = ConfigText(default="1BA1E2")
config.plugins.KravenHD.IBProgressBackground = ConfigText(default="1BA1E2")

config.plugins.KravenHD.IBProgressBorderLine = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("ib-progress-border", _("border")),
				("ib-progress-line", _("line"))
				])

config.plugins.KravenHD.IBProgressBorderLineColorList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenHD.IBProgressBorderLineColorSelf = ConfigText(default="ffffff")
config.plugins.KravenHD.IBProgressBorderLineColor = ConfigText(default="ffffff")

config.plugins.KravenHD.InfobarSelfColorR = ConfigSlider(default=0, increment=5, limits=(0, 255))
config.plugins.KravenHD.InfobarSelfColorG = ConfigSlider(default=0, increment=5, limits=(0, 255))
config.plugins.KravenHD.InfobarSelfColorB = ConfigSlider(default=0, increment=5, limits=(0, 255))
config.plugins.KravenHD.BackgroundSelfColorR = ConfigSlider(default=0, increment=5, limits=(0, 255))
config.plugins.KravenHD.BackgroundSelfColorG = ConfigSlider(default=0, increment=5, limits=(0, 255))
config.plugins.KravenHD.BackgroundSelfColorB = ConfigSlider(default=75, increment=5, limits=(0, 255))

class KravenHD(ConfigListScreen, Screen):

	if DESKTOP_WIDTH <= 1280:
	  skin = """
<screen name="KravenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#00000000">
  <widget backgroundColor="#00000000" source="Title" render="Label" font="Regular;34" foregroundColor="#00f0a30a" position="42,7" size="736,46" valign="center" transparent="1" />
  <widget source="global.CurrentTime" render="Label" position="1138,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <widget backgroundColor="#00000000" name="config" font="Regular;22" foregroundColor="#00ffffff" itemHeight="30" position="42,85" size="736,540" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />
  <eLabel backgroundColor="#00000000" text="KravenHD" font="Regular;36" foregroundColor="#00f0a30a" position="830,80" size="402,46" halign="center" valign="center" transparent="1" />
  <widget backgroundColor="#00000000" source="version" render="Label" font="Regular;30" foregroundColor="#00ffffff" position="845,139" size="372,40" halign="center" valign="center" transparent="1" />
  <eLabel backgroundColor="#00f0a30a" position="847,208" size="368,2" />
  <eLabel backgroundColor="#00f0a30a" position="847,417" size="368,2" />
  <eLabel backgroundColor="#00f0a30a" position="845,208" size="2,211" />
  <eLabel backgroundColor="#00f0a30a" position="1215,208" size="2,211" />
  <widget backgroundColor="#00000000" name="helperimage" position="847,210" size="368,207" zPosition="1" />
  <widget backgroundColor="#00000000" source="Canvas" render="Canvas" position="847,210" size="368,207" zPosition="-1" />
  <widget backgroundColor="#00000000" source="help" render="Label" font="Regular;20" foregroundColor="#00f0a30a" position="830,435" size="402,190" halign="center" valign="top" transparent="1" />
  <widget backgroundColor="#00000000" source="key_red" render="Label" font="Regular;20" foregroundColor="#00ffffff" position="47,670" size="220,26" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_green" render="Label" font="Regular;20" foregroundColor="#00ffffff" position="297,670" size="220,26" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_yellow" render="Label" font="Regular;20" foregroundColor="#00ffffff" position="547,670" size="220,26" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_blue" render="Label" font="Regular;20" foregroundColor="#00ffffff" position="797,670" size="220,26" valign="center" transparent="1" zPosition="1" />
  <eLabel backgroundColor="#00E61805" position="42,697" size="150,5" />
  <eLabel backgroundColor="#005FE500" position="292,697" size="150,5" />
  <eLabel backgroundColor="#00E5DD00" position="542,697" size="150,5" />
  <eLabel backgroundColor="#000082E5" position="792,697" size="150,5" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
</screen>
"""
	else:
	  skin = """
<screen name="KravenHD" position="0,0" size="1920,1080" flags="wfNoBorder" backgroundColor="#00000000">
  <widget backgroundColor="#00000000" source="Title" render="Label" font="Regular;50" foregroundColor="#00f0a30a" position="63,10" size="1500,69" valign="center" transparent="1" />
  <widget source="global.CurrentTime" render="Label" position="1707,24" size="150,42" font="Regular;39" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <widget backgroundColor="#00000000" name="config" font="Regular;32" foregroundColor="#00ffffff" itemHeight="45" position="63,127" size="1104,810" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />
  <eLabel backgroundColor="#00000000" text="KravenHD" font="Regular;54" foregroundColor="#00f0a30a" position="1245,120" size="603,69" halign="center" valign="center" transparent="1" />
  <widget backgroundColor="#00000000" source="version" render="Label" font="Regular;45" foregroundColor="#00ffffff" position="1267,208" size="558,60" halign="center" valign="center" transparent="1" />
  <eLabel backgroundColor="#00f0a30a" position="1359,303" size="374,3" />
  <eLabel backgroundColor="#00f0a30a" position="1359,513" size="374,3" />
  <eLabel backgroundColor="#00f0a30a" position="1359,306" size="3,207" />
  <eLabel backgroundColor="#00f0a30a" position="1730,306" size="3,207" />
  <widget backgroundColor="#00000000" name="helperimage" position="1362,306" size="368,207" zPosition="1" />
  <widget backgroundColor="#00000000" source="Canvas" render="Canvas" position="1362,306" size="368,207" zPosition="-1" />
  <widget backgroundColor="#00000000" source="help" render="Label" font="Regular;32" foregroundColor="#00f0a30a" position="1240,560" size="612,369" halign="center" valign="top" transparent="1" />
  <widget backgroundColor="#00000000" source="key_red" render="Label" font="Regular;30" foregroundColor="#00ffffff" position="71,1004" size="330,39" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_green" render="Label" font="Regular;30" foregroundColor="#00ffffff" position="446,1004" size="330,39" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_yellow" render="Label" font="Regular;30" foregroundColor="#00ffffff" position="821,1004" size="330,39" valign="center" transparent="1" zPosition="1" />
  <widget backgroundColor="#00000000" source="key_blue" render="Label" font="Regular;30" foregroundColor="#00ffffff" position="1196,1004" size="330,39" valign="center" transparent="1" zPosition="1" />
  <eLabel backgroundColor="#00E61805" position="63,1045" size="225,7" />
  <eLabel backgroundColor="#005FE500" position="438,1045" size="225,7" />
  <eLabel backgroundColor="#00E5DD00" position="813,1045" size="225,7" />
  <eLabel backgroundColor="#000082E5" position="1188,1045" size="225,7" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1920,1080" transparent="0" zPosition="-9" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.datei = "/usr/share/enigma2/KravenHD/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		self.picPath = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/"
		self.profiles = "/etc/enigma2/"
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		self["Canvas"] = CanvasSource()
		self["help"] = StaticText()
		self["version"] = StaticText()

		list = []
		ConfigListScreen.__init__(self, list)

		self["actions"] = ActionMap(["KravenHDConfigActions", "OkCancelActions", "DirectionActions", "ColorActions", "InputActions"],
		{
			"upUp": self.keyUpLong,
			"downUp": self.keyDownLong,
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"red": self.faq,
			"green": self.save,
			"yellow": self.categoryDown,
			"blue": self.categoryUp,
			"cancel": self.exit,
			"pageup": self.pageUp,
			"papedown": self.pageDown,
			"ok": self.OK
		}, -1)

		self["key_red"] = StaticText(_("FAQs"))
		self["key_green"] = StaticText(_("Save skin"))
		self["key_yellow"] = StaticText()
		self["key_blue"] = StaticText()
		self["Title"] = StaticText(_("Configuration tool for KravenHD"))

		self.UpdatePicture()

		self.timer = eTimer()
		self.timer.callback.append(self.updateMylist)
		self.onLayoutFinish.append(self.updateMylist)

		self.lastProfile="0"

		self.actClockstyle=""
		self.actWeatherstyle=""
		self.actChannelselectionstyle=""
		self.actMenustyle=""
		self.actCity=""

		self.skincolorinfobarcolor=""
		self.skincolorbackgroundcolor=""

		self.actListColorSelection=None
		self.actSelfColorSelection=None

		self.BoxName=self.getBoxName()
		self.Tuners=self.getTuners()
		self.InternetAvailable=self.getInternetAvailable()
		self.UserMenuIconsAvailable=self.getUserMenuIconsAvailable()

	def mylist(self):
		self.timer.start(100, True)

	def updateMylist(self):

		if config.plugins.KravenHD.customProfile.value!=self.lastProfile:
			self.loadProfile()
			self.lastProfile=config.plugins.KravenHD.customProfile.value

		list = []

		# page 1
		emptyLines=0
		list.append(getConfigListEntry(_("About"), config.plugins.KravenHD.About, _("The KravenHD skin will be generated by this plugin according to your preferences. Make your settings and watch the changes in the preview window above. When finished, save your skin by pressing the green button and restart the GUI.")))
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))

		# page 1 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("PROFILES ________________________________________________________________________________"), config.plugins.KravenHD.CategoryProfiles, _("This sections offers all profile settings. Different settings can be saved, modified, shared and cloned. Read the FAQs.")))
		list.append(getConfigListEntry(_("Active Profile / Save"), config.plugins.KravenHD.customProfile, _("Select the profile you want to work with. Profiles are saved automatically on switching them or by pressing the OK button. New profiles will be generated based on the actual one. Profiles are interchangeable between boxes.")))
		list.append(getConfigListEntry(_("Default Profile / Reset"), config.plugins.KravenHD.defaultProfile, _("Select the default profile you want to use when resetting the active profile (OK button). You can add your own default profiles under /etc/enigma2/kravenhd_default_n (n<=20).")))
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))

		# page 1 (category 3)
		emptyLines=0
		list.append(getConfigListEntry(_("SYSTEM ________________________________________________________________________________"), config.plugins.KravenHD.CategorySystem, _("This sections offers all basic settings.")))
		list.append(getConfigListEntry(_("Skin Resolution"), config.plugins.KravenHD.SkinResolution, _("Choose the resolution of the skin.")))
		list.append(getConfigListEntry(_("Icons (except Infobar)"), config.plugins.KravenHD.IconStyle2, _("Choose between light and dark icons in system screens. The icons in the infobars are not affected.")))
		list.append(getConfigListEntry(_("Running Text (Delay)"), config.plugins.KravenHD.RunningText, _("Choose the start delay for running text.")))
		if not config.plugins.KravenHD.RunningText.value == "none":
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				list.append(getConfigListEntry(_("Running Text (Speed)"), config.plugins.KravenHD.RunningTextSpeed, _("Choose the speed for running text.")))
			else:
				list.append(getConfigListEntry(_("Running Text (Speed)"), config.plugins.KravenHD.RunningTextSpeed2, _("Choose the speed for running text.")))
		else:
			emptyLines+=1
		list.append(getConfigListEntry(_("Scrollbars"), config.plugins.KravenHD.ScrollBar, _("Choose whether scrollbars should be shown.")))
		list.append(getConfigListEntry(_("Show Infobar-Background"), config.plugins.KravenHD.IBColor, _("Choose whether you want to see the infobar background in all screens (bicolored background).")))
		if self.InternetAvailable or self.UserMenuIconsAvailable:
			list.append(getConfigListEntry(_("Menus"), config.plugins.KravenHD.Logo, _("Choose from different options to display the system menus. Press red button for the FAQs with details on installing menu icons.")))
			self.actMenustyle=config.plugins.KravenHD.Logo.value
			if config.plugins.KravenHD.Logo.value in ("metrix-icons", "minitv-metrix-icons"):
				list.append(getConfigListEntry(_("Menu-Icons"), config.plugins.KravenHD.MenuIcons, _("Choose from different icon sets for the menu screens. Many thanks to rennmaus and kleiner.teufel for their icon set.")))
			else:
				emptyLines+=1
		else:
			list.append(getConfigListEntry(_("Menus"), config.plugins.KravenHD.LogoNoInternet, _("Choose from different options to display the system menus. Press red button for the FAQs with details on installing menu icons.")))
			self.actMenustyle=config.plugins.KravenHD.LogoNoInternet.value
			emptyLines+=1
		list.append(getConfigListEntry(_("Mainmenu Fontsize ('Standard' Style)"), config.plugins.KravenHD.MainmenuFontsize, _("Choose the font size for 'Standard' mainmenus.")))
		list.append(getConfigListEntry(_("Mainmenu Title Color ('Horizontal' Styles)"), config.plugins.KravenHD.MainmenuHorTitleFontList, _("Choose the title font color for 'Horizontal' and 'Horizontal-Icons' mainmenus.")))
		list.append(getConfigListEntry(_("Mainmenu Icons Gradient Color ('Horizontal-Icons' Style)"), config.plugins.KravenHD.MainmenuHorIconColorList, _("Choose the gradient color of the icons for 'Horizontal-Icons' mainmenus.")))
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))

		# page 2
		emptyLines=0
		list.append(getConfigListEntry(_("GLOBAL COLORS ________________________________________________________________________________"), config.plugins.KravenHD.CategoryGlobalColors, _("This sections offers offers all basic color settings.")))
		list.append(getConfigListEntry(_("Background"), config.plugins.KravenHD.BackgroundListColor, _("Choose the background for all screens. You can choose from a list of predefined colors or textures, create your own color using RGB sliders or define a color gradient. Also read the FAQs regarding your own textures.")))
		if config.plugins.KravenHD.BackgroundListColor.value == "gradient":
			list.append(getConfigListEntry(_("          Primary Color"), config.plugins.KravenHD.BackgroundGradientListColorPrimary, _("Choose the primary color for the background gradient. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("          Secondary Color"), config.plugins.KravenHD.BackgroundGradientListColorSecondary, _("Choose the secondary color for the background gradient. Press OK to define your own RGB color.")))
			emptyLines+=1
		elif config.plugins.KravenHD.BackgroundListColor.value == "texture":
			list.append(getConfigListEntry(_("          Texture"), config.plugins.KravenHD.BackgroundTexture, _("Choose the texture for the background.")))
			list.append(getConfigListEntry(_("          Alternate Color"), config.plugins.KravenHD.BackgroundAlternateListColor, _("Choose the alternate color for the background. It should match the texture at the best. Press OK to define your own RGB color.")))
			emptyLines+=1
		else:
			emptyLines+=3
		list.append(getConfigListEntry(_("Background-Transparency"), config.plugins.KravenHD.BackgroundColorTrans, _("Choose the degree of background transparency for all screens except channellists.")))
		list.append(getConfigListEntry(_("Listselection-Style"), config.plugins.KravenHD.SelectionStyle, _("Choose from different options to display selection bars.")))
		if config.plugins.KravenHD.SelectionStyle.value == "color":
			list.append(getConfigListEntry(_("          Color"), config.plugins.KravenHD.SelectionBackgroundList, _("Choose the background color of selection bars. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("          Border"), config.plugins.KravenHD.SelectionBorderList, _("Choose the border color of selection bars or deactivate borders completely. Press OK to define your own RGB color.")))
		else:
			list.append(getConfigListEntry(_("          Primary Color"), config.plugins.KravenHD.SelectionBackgroundList, _("Choose the primary background color of selection bars. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("          Secondary Color"), config.plugins.KravenHD.SelectionBackground2List, _("Choose the secondary background color of selection bars. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Listselection-Font"), config.plugins.KravenHD.SelectionFontList, _("Choose the color of the font in selection bars. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.KravenHD.ProgressList, _("Choose the color of progress bars. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Border"), config.plugins.KravenHD.BorderList, _("Choose the global border color. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("MiniTV-Border"), config.plugins.KravenHD.MiniTVBorderList, _("Choose the border color of MiniTV's. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Lines"), config.plugins.KravenHD.LineList, _("Choose the color of all lines. This affects dividers as well as the line in the center of some progress bars. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Primary-Font"), config.plugins.KravenHD.Font1List, _("Choose the color of the primary font. The primary font is used for list items, textboxes and other important information. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Secondary-Font"), config.plugins.KravenHD.Font2List, _("Choose the color of the secondary font. The secondary font is used for headers, labels and other additional information. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Marking-Font"), config.plugins.KravenHD.MarkedFontList, _("Choose the font color of marked list items. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Colorbutton-Font"), config.plugins.KravenHD.ButtonTextList, _("Choose the font color of the color button labels. Press OK to define your own RGB color.")))
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))

		# page 3
		emptyLines=0
		list.append(getConfigListEntry(_("INFOBAR-LOOK ________________________________________________________________________________"), config.plugins.KravenHD.CategoryInfobarLook, _("This sections offers all settings for the infobar-look.")))
		list.append(getConfigListEntry(_("Infobar-Style"), config.plugins.KravenHD.InfobarStyle, _("Choose from different infobar styles. Please note that not every style provides every feature. Therefore some features might be unavailable for the chosen style.")))
		list.append(getConfigListEntry(_("Infobar-Background-Style"), config.plugins.KravenHD.IBStyle, _("Choose from different infobar background styles.")))
		if config.plugins.KravenHD.IBStyle.value == "box":
			list.append(getConfigListEntry(_("Infobar-Box-Line"), config.plugins.KravenHD.IBLineList, _("Choose the color of the infobar box lines. Press OK to define your own RGB color.")))
		else:
			emptyLines+=1
		if config.plugins.KravenHD.IBStyle.value == "grad":
			list.append(getConfigListEntry(_("Infobar-Background"), config.plugins.KravenHD.InfobarGradientListColor, _("Choose the background for the infobars. You can choose from a list of predefined colors or textures or create your own color using RGB sliders.")))
		else:
			list.append(getConfigListEntry(_("Infobar-Background"), config.plugins.KravenHD.InfobarBoxListColor, _("Choose the background for the infobars. You can choose from a list of predefined colors or textures, create your own color using RGB sliders or define a color gradient.")))
		if config.plugins.KravenHD.IBStyle.value == "box" and config.plugins.KravenHD.InfobarBoxListColor.value == "gradient":
			list.append(getConfigListEntry(_("          Primary Color"), config.plugins.KravenHD.InfobarGradientListColorPrimary, _("Choose the primary color for the infobar gradient. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("          Secondary Color"), config.plugins.KravenHD.InfobarGradientListColorSecondary, _("Choose the secondary color for the infobar gradient. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("          Info Panels"), config.plugins.KravenHD.InfoStyle, _("Choose gradient or color for the info panels (Sysinfos, Timeshiftbar etc.).")))
		elif config.plugins.KravenHD.IBStyle.value == "box" and config.plugins.KravenHD.InfobarBoxListColor.value == "texture":
			list.append(getConfigListEntry(_("          Texture"), config.plugins.KravenHD.InfobarTexture, _("Choose the texture for the infobars.")))
			list.append(getConfigListEntry(_("          Alternate Color"), config.plugins.KravenHD.InfobarAlternateListColor, _("Choose the alternate color for the infobars. It should match the texture at the best. Press OK to define your own RGB color.")))
			emptyLines+=1
		elif config.plugins.KravenHD.IBStyle.value == "grad" and config.plugins.KravenHD.InfobarGradientListColor.value == "texture":
			list.append(getConfigListEntry(_("          Texture"), config.plugins.KravenHD.InfobarTexture, _("Choose the texture for the infobars.")))
			list.append(getConfigListEntry(_("          Alternate Color"), config.plugins.KravenHD.InfobarAlternateListColor, _("Choose the alternate color for the infobars. It should match the texture at the best. Press OK to define your own RGB color.")))
			emptyLines+=1
		else:
			emptyLines+=3
		list.append(getConfigListEntry(_("Infobar-Transparency"), config.plugins.KravenHD.InfobarColorTrans, _("Choose the degree of background transparency for the infobars.")))
		list.append(getConfigListEntry(_("Primary-Infobar-Font"), config.plugins.KravenHD.IBFont1List, _("Choose the color of the primary infobar font. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Secondary-Infobar-Font"), config.plugins.KravenHD.IBFont2List, _("Choose the color of the secondary infobar font. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Infobar-Icons"), config.plugins.KravenHD.IconStyle, _("Choose between light and dark infobar icons.")))
		list.append(getConfigListEntry(_("Eventname Fontsize"), config.plugins.KravenHD.IBFontSize, _("Choose the font size of eventname.")))
		list.append(getConfigListEntry(_("Eventname effect"), config.plugins.KravenHD.TypeWriter, _("Choose from different effects to display eventname.")))
		list.append(getConfigListEntry(_("Progress-Bar"), config.plugins.KravenHD.IBProgressList, _("Choose the color of progress bar. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Progress-Background"), config.plugins.KravenHD.IBProgressBackgroundList, _("Choose the color of progress bar background or deactivate it completely. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Progress-Border/Line"), config.plugins.KravenHD.IBProgressBorderLine, _("Choose whether progress bar displayed with border or line or without them.")))
		if config.plugins.KravenHD.IBProgressBorderLine.value == "ib-progress-border":
			list.append(getConfigListEntry(_("Progress-Border Color"), config.plugins.KravenHD.IBProgressBorderLineColorList, _("Choose the border color of progress bar. Press OK to define your own RGB color.")))
		elif config.plugins.KravenHD.IBProgressBorderLine.value == "ib-progress-line":
			list.append(getConfigListEntry(_("Progress-Line Color"), config.plugins.KravenHD.IBProgressBorderLineColorList, _("Choose the line color of progress bar. Press OK to define your own RGB color.")))
		else:
			emptyLines+=1
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))

		# page 4
		emptyLines=0
		list.append(getConfigListEntry(_("INFOBAR-CONTENTS ________________________________________________________________________________"), config.plugins.KravenHD.CategoryInfobarContents, _("This sections offers all settings for infobar-contents.")))
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-x2", "infobar-style-z1", "infobar-style-zz1", "infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Busy color"), config.plugins.KravenHD.TunerBusyList, _("Choose the color for engaged tuners. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Active color"), config.plugins.KravenHD.TunerLiveList, _("Choose the color for the current live tuner. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Record color"), config.plugins.KravenHD.TunerRecordList, _("Choose the color for recording tuners. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Active record color"), config.plugins.KravenHD.TunerXtremeBusyList, _("Choose the color for the current live tuner when also recording. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Show unused Tuners"), config.plugins.KravenHD.ShowUnusedTuner, _("Choose whether unused tuners are displayed or not.")))
		else:
			emptyLines+=5
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-nopicon":
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenHD.Infobox2, _("Choose which informations will be shown in the info box.")))
			emptyLines+=1
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x1", "infobar-style-x2", "infobar-style-z1"):
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenHD.Infobox, _("Choose which informations will be shown in the info box.")))
			emptyLines+=1
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Show AGC/SNR"), config.plugins.KravenHD.ShowAgcSnr, _("Choose whether AGC/SNR are displayed or not.")))
			if config.plugins.KravenHD.ShowAgcSnr.value == "on":
				list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenHD.Infobox2, _("Choose which informations will be shown in the info box.")))
			else:
				list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenHD.Infobox, _("Choose which informations will be shown in the info box.")))
		else:
			emptyLines+=2
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2", "infobar-style-zz1"):
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenHD.InfobarChannelName, _("Choose from different options to show the channel name and number in the infobar.")))
			if not config.plugins.KravenHD.InfobarChannelName.value == "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenHD.ChannelnameFontList, _("Choose the font color of channel name and number. Press OK to define your own RGB color.")))
			else:
				emptyLines+=1
		else:
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenHD.InfobarChannelName2, _("Choose from different options to show the channel name and number in the infobar.")))
			if not config.plugins.KravenHD.InfobarChannelName2.value == "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenHD.ChannelnameFontList, _("Choose the font color of channel name and number. Press OK to define your own RGB color.")))
			else:
				emptyLines+=1
		list.append(getConfigListEntry(_("System-Infos"), config.plugins.KravenHD.SystemInfo, _("Choose from different additional windows with system informations or deactivate them completely.")))
		for i in range(emptyLines+7):
			list.append(getConfigListEntry(_(" "), ))

		# page 5
		emptyLines=0
		list.append(getConfigListEntry(_("WEATHER ________________________________________________________________________________"), config.plugins.KravenHD.CategoryWeather, _("This sections offers all weather settings.")))
		if self.InternetAvailable:
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-x3", "infobar-style-z2", "infobar-style-zz1", "infobar-style-zz2", "infobar-style-zz3", "infobar-style-zzz1"):
				list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyle, _("Choose from different options to show the weather in the infobar.")))
				self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle.value
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
					list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyle3, _("Activate or deactivate displaying the weather in the infobar.")))
					self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle3.value
				else:
					list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyle2, _("Activate or deactivate displaying the weather in the infobar.")))
					self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle2.value
			list.append(getConfigListEntry(_("Accuweather API Key"), config.plugins.KravenHD.weather_accu_apikey, _("Press OK to enter your API Key.\nYou will receive the key at\n\"https://developer.accuweather.com/\".")))
			list.append(getConfigListEntry(_("Search by"), config.plugins.KravenHD.weather_search_over, _("Choose from different options to specify your location.")))
			if config.plugins.KravenHD.weather_search_over.value == 'name':
				list.append(getConfigListEntry(_("Search String"), config.plugins.KravenHD.weather_cityname, _("Specify any search string for your location (zip/city/district/state single or combined). Press OK to use the virtual keyboard. Step up or down in the menu to start the search.")))
			else:
				emptyLines+=1
			list.append(getConfigListEntry(_("Language"), config.plugins.KravenHD.weather_language, _("Specify the language for the weather output.")))
			list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.KravenHD.refreshInterval, _("Choose the frequency of loading weather data from the internet.")))
			list.append(getConfigListEntry(_("Weather-Style"), config.plugins.KravenHD.WeatherView, _("Choose between graphical weather symbols and Meteo symbols.")))
			if config.plugins.KravenHD.WeatherView.value == "meteo":
				list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenHD.MeteoColor, _("Choose between light and dark Meteo symbols.")))
			else:
				emptyLines+=1
		else:
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenHD.WeatherStyleNoInternet, _("You have no internet connection. This function is disabled.")))
			self.actWeatherstyle="none"
			emptyLines+=7
		for i in range(emptyLines+2):
			list.append(getConfigListEntry(_(" "), ))

		# page 5 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("CLOCK ________________________________________________________________________________"), config.plugins.KravenHD.CategoryClock, _("This sections offers all settings for the different clocks.")))
		if self.InternetAvailable:
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenHD.ClockStyle, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenHD.ClockStyle.value
			if self.actClockstyle == "clock-analog":
				list.append(getConfigListEntry(_("Analog-Clock-Color"), config.plugins.KravenHD.AnalogColorList, _("Choose from different colors for the analog type clock in the infobar.")))
			elif self.actClockstyle == "clock-android":
				list.append(getConfigListEntry(_("Android-Temp-Color"), config.plugins.KravenHD.AndroidList, _("Choose the font color of android-clock temperature. Press OK to define your own RGB color.")))
			else:
				emptyLines+=1
		else:
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenHD.ClockStyleNoInternet, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenHD.ClockStyleNoInternet.value
			emptyLines+=1
		for i in range(emptyLines+4):
			list.append(getConfigListEntry(_(" "), ))

		# page 6
		emptyLines=0
		list.append(getConfigListEntry(_("ECM INFOS ________________________________________________________________________________"), config.plugins.KravenHD.CategoryECMInfos, _("This sections offers all settings for showing the decryption infos.")))
		list.append(getConfigListEntry(_("Show ECM Infos"), config.plugins.KravenHD.ECMVisible, _("Choose from different options where to display the ECM informations.")))
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1" and not config.plugins.KravenHD.ECMVisible.value == "none":
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenHD.ECMLine1, _("Choose from different options to display the ECM informations.")))
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFontList, _("Choose the font color of the ECM information. Press OK to define your own RGB color.")))
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2") and not config.plugins.KravenHD.ECMVisible.value == "none":
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenHD.ECMLine2, _("Choose from different options to display the ECM informations.")))
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFontList, _("Choose the font color of the ECM information. Press OK to define your own RGB color.")))
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zz2", "infobar-style-zz3", "infobar-style-zzz1") and not config.plugins.KravenHD.ECMVisible.value == "none":
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenHD.ECMLine3, _("Choose from different options to display the ECM informations.")))
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenHD.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenHD.ECMFontList, _("Choose the font color of the ECM information. Press OK to define your own RGB color.")))
		else:
			emptyLines+=3
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))

		# page 6 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("VIEWS ________________________________________________________________________________"), config.plugins.KravenHD.CategoryViews, _("This sections offers all settings for skinned plugins.")))
		list.append(getConfigListEntry(_("Volume"), config.plugins.KravenHD.Volume, _("Choose from different styles for the volume display.")))
		list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenHD.SIB, _("Choose from different styles for SecondInfobar. \nActivate the SecondInfobar in the \nOSD settings. \n2nd infobar -> 2nd Infobar INFO")))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.KravenHD.CoolTVGuide, _("Choose from different styles for CoolTVGuide.")))
		list.append(getConfigListEntry(_("MovieSelection"), config.plugins.KravenHD.MovieSelection, _("Choose from different styles for MovieSelection.")))
		list.append(getConfigListEntry(_("EPGSelection"), config.plugins.KravenHD.EPGSelection, _("Choose from different styles to display EPGSelection.")))
		list.append(getConfigListEntry(_("SerienRecorder"), config.plugins.KravenHD.SerienRecorder, _("Choose whether you want the Kraven skin to be applied to 'Serienrecorder' or not. Activation of this option prohibits the skin selection in the SR-plugin.")))
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py"):
			list.append(getConfigListEntry(_("MediaPortal"), config.plugins.KravenHD.MediaPortal, _("Choose whether you want the Kraven skin to be applied to 'MediaPortal' or not. To remove it again, you must deactivate it here and activate another skin in 'MediaPortal'.")))
		else:
			emptyLines+=1
		list.append(getConfigListEntry(_("FileCommander"), config.plugins.KravenHD.FileCommander, _("Choose from different styles to display FileCommander.")))
		list.append(getConfigListEntry(_("Popups"), config.plugins.KravenHD.PopupStyle, _("Choose from different styles to display popups like 'MessageBox', 'ChoiceBox', 'ExtensionsList', 'VirtualKeyboard' and more.")))
		list.append(getConfigListEntry(_("PermanentClock-Color"), config.plugins.KravenHD.PermanentClock, _("Choose the colors of PermanentClock.")))
		if config.plugins.KravenHD.PermanentClock.value in ("permanentclock-transparent-big", "permanentclock-transparent-small"):
			list.append(getConfigListEntry(_("PermanentClock-Font"), config.plugins.KravenHD.PermanentClockFontList, _("Choose the font color of PermanentClock. Press OK to define your own RGB color.")))
		else:
			emptyLines+=1
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))

		# page 7
		emptyLines=0
		list.append(getConfigListEntry(_("CHANNELLIST ________________________________________________________________________________"), config.plugins.KravenHD.CategoryChannellist, _("This sections offers all channellist settings.")))
		if SystemInfo.get("NumVideoDecoders", 1) > 1:
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenHD.ChannelSelectionStyle2, _("Choose from different styles for the channel selection screen.")))
			self.actChannelselectionstyle=config.plugins.KravenHD.ChannelSelectionStyle2.value
		else:
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenHD.ChannelSelectionStyle, _("Choose from different styles for the channel selection screen.")))
			self.actChannelselectionstyle=config.plugins.KravenHD.ChannelSelectionStyle.value
		if self.actChannelselectionstyle in ("channelselection-style-minitv", "channelselection-style-minitv2", "channelselection-style-minitv22", "channelselection-style-minitv33", "channelselection-style-minitv4", "channelselection-style-nobile-minitv", "channelselection-style-nobile-minitv33", "channelselection-style-minitv-picon"):
			list.append(getConfigListEntry(_("Channellist-Mode"), config.plugins.KravenHD.ChannelSelectionMode, _("Choose between direct zapping (1xOK) and zapping after preview (2xOK).")))
		else:
			emptyLines+=1
		if not self.actChannelselectionstyle in ("channelselection-style-minitv", "channelselection-style-minitv2", "channelselection-style-minitv3", "channelselection-style-minitv4", "channelselection-style-minitv22", "channelselection-style-nobile-minitv", "channelselection-style-nobile-minitv3", "channelselection-style-minitv-picon"):
			list.append(getConfigListEntry(_("Channellist-Transparenz"), config.plugins.KravenHD.ChannelSelectionTrans, _("Choose the degree of background transparency for the channellists.")))
		else:
			emptyLines+=1
		if self.actChannelselectionstyle in ("channelselection-style-nobile", "channelselection-style-nobile2", "channelselection-style-nobile-minitv", "channelselection-style-nobile-minitv3", "channelselection-style-nobile-minitv33"):
			list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenHD.ChannelSelectionEPGSize1, _("Choose the font size of event description, EPG list and primetime.")))
		elif self.actChannelselectionstyle == "channelselection-style-minitv22":
			list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenHD.ChannelSelectionEPGSize2, _("Choose the font size of EPG list and primetime.")))
		else:
			list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenHD.ChannelSelectionEPGSize3, _("Choose the font size of event description, EPG list and primetime.")))
		list.append(getConfigListEntry(_("'Not available'-Font"), config.plugins.KravenHD.ChannelSelectionServiceNAList, _("Choose the font color of channels that are unavailable at the moment. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Primetime"), config.plugins.KravenHD.Primetimeavailable, _("Choose whether primetime program information is displayed or not.")))
		if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on":
			list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenHD.Primetime, _("Specify the time for your primetime.")))
			list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenHD.PrimetimeFontList, _("Choose the font color of the primetime information. Press OK to define your own RGB color.")))
		else:
			emptyLines+=2
		for i in range(emptyLines+5):
			list.append(getConfigListEntry(_(" "), ))

		# page 7 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("NUMBERZAP ________________________________________________________________________________"), config.plugins.KravenHD.CategoryNumberZap, _("This sections offers all settings for NumberZap.")))
		list.append(getConfigListEntry(_("NumberZap-Style"), config.plugins.KravenHD.NumberZapExt, _("Choose from different styles for NumberZap.")))
		if not config.plugins.KravenHD.NumberZapExt.value == "none":
			list.append(getConfigListEntry(_("Border Color"), config.plugins.KravenHD.NZBorderList, _("Choose the border color for NumberZap. Press OK to define your own RGB color.")))
		else:
			emptyLines+=1
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))

		# page 8
		emptyLines=0
		list.append(getConfigListEntry(_("GRAPHICALEPG ________________________________________________________________________________"), config.plugins.KravenHD.CategoryGraphicalEPG, _("This sections offers all settings for GraphicalEPG.")))
		list.append(getConfigListEntry(_("GraphicalEPG-Style"), config.plugins.KravenHD.GraphicalEPG, _("Choose from different styles for GraphicalEPG.")))
		list.append(getConfigListEntry(_("Event Description Fontsize"), config.plugins.KravenHD.GMEDescriptionSize, _("Choose the font size of event description.")))
		if config.plugins.KravenHD.GraphicalEPG.value in ("text", "text-minitv"):
			list.append(getConfigListEntry(_("Selected Event Fontcolor"), config.plugins.KravenHD.GMESelFgList, _("Choose the font color of selected events for GraphicalEPG. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Selected Event Background"), config.plugins.KravenHD.GMESelBgList, _("Choose the background color of selected events for GraphicalEPG. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Running Event Fontcolor"), config.plugins.KravenHD.GMENowFgList, _("Choose the font color of running events for GraphicalEPG. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Running Event Background"), config.plugins.KravenHD.GMENowBgList, _("Choose the background color of running events for GraphicalEPG. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("Border Color"), config.plugins.KravenHD.GMEBorderList, _("Choose the border color for GraphicalEPG. Press OK to define your own RGB color.")))
		else:
			emptyLines+=5
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))

		# page 8 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("ENHANCED MOVIE CENTER ________________________________________________________________________________"), config.plugins.KravenHD.CategoryEMC, _("This sections offers all settings for EMC ('EnhancedMovieCenter').")))
		list.append(getConfigListEntry(_("EMC-Style"), config.plugins.KravenHD.EMCStyle, _("Choose from different styles for EnhancedMovieCenter.")))
		list.append(getConfigListEntry(_("Unwatched Color"), config.plugins.KravenHD.UnwatchedColorList, _("Choose the font color of unwatched movies. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Watching Color"), config.plugins.KravenHD.WatchingColorList, _("Choose the font color of watching movies. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("Finished Color"), config.plugins.KravenHD.FinishedColorList, _("Choose the font color of watched movies. Press OK to define your own RGB color.")))
		list.append(getConfigListEntry(_("EMC-Selection-Colors"), config.plugins.KravenHD.EMCSelectionColors, _("Choose whether you want to customize the selection-colors for EnhancedMovieCenter.")))
		if config.plugins.KravenHD.EMCSelectionColors.value == "custom":
			list.append(getConfigListEntry(_("EMC-Listselection"), config.plugins.KravenHD.EMCSelectionBackgroundList, _("Choose the background color of selection bars for EnhancedMovieCenter. Press OK to define your own RGB color.")))
			list.append(getConfigListEntry(_("EMC-Selection-Font"), config.plugins.KravenHD.EMCSelectionFontList, _("Choose the color of the font in selection bars for EnhancedMovieCenter. Press OK to define your own RGB color.")))
		else:
			emptyLines+=2
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))

		# page 9
		emptyLines=0
		list.append(getConfigListEntry(_("PLAYER ________________________________________________________________________________"), config.plugins.KravenHD.CategoryPlayers, _("This sections offers all settings for the movie players.")))
		list.append(getConfigListEntry(_("Clock"), config.plugins.KravenHD.PlayerClock, _("Choose from different options to show the clock in the players.")))
		if config.plugins.KravenHD.PlayerClock.value == "player-android":
			list.append(getConfigListEntry(_("Android-Temp-Color"), config.plugins.KravenHD.Android2List, _("Choose the font color of android-clock temperature. Press OK to define your own RGB color.")))
		else:
			emptyLines+=1
		list.append(getConfigListEntry(_("PVRState"), config.plugins.KravenHD.PVRState, _("Choose from different options to display the PVR state.")))
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 9 (category 2)
		emptyLines=0
		if config.plugins.KravenHD.IBStyle.value == "grad":
			list.append(getConfigListEntry(_("ANTIALIASING BRIGHTNESS ________________________________________________________________________________"), config.plugins.KravenHD.CategoryAntialiasing, _("This sections offers all antialiasing settings. Distortions or color frames around fonts can be reduced by this settings.")))
			list.append(getConfigListEntry(_("Infobar"), config.plugins.KravenHD.InfobarAntialias, _("Reduce distortions (faint/blurry) or color frames around fonts in the infobar and widgets by adjusting the antialiasing brightness.")))
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenHD.ECMLineAntialias, _("Reduce distortions (faint/blurry) or color frames around the ECM information in the infobar by adjusting the antialiasing brightness.")))
			list.append(getConfigListEntry(_("Screens"), config.plugins.KravenHD.ScreensAntialias, _("Reduce distortions (faint/blurry) or color frames around fonts at top and bottom of screens by adjusting the antialiasing brightness.")))
			emptyLines=1
		else:
			emptyLines+=0
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))

		# page 9 (category 3)
		emptyLines=0
		list.append(getConfigListEntry(_("VARIOUS SETTINGS ________________________________________________________________________________"), config.plugins.KravenHD.CategoryVarious, _("This sections offers various settings.")))
		list.append(getConfigListEntry(_("Screennames"), config.plugins.KravenHD.DebugNames, _("Activate or deactivate small screen names for debugging purposes.")))
		list.append(getConfigListEntry(_("Icon-Font vertical position"), config.plugins.KravenHD.KravenIconVPosition, _("Correct the vertical font position within some icons for the infobars and players.")))
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))

		### Assign list or self color
		if config.plugins.KravenHD.BackgroundListColor.value == "self":
			config.plugins.KravenHD.BackgroundColor.value = config.plugins.KravenHD.BackgroundSelfColor.value
		else:
			config.plugins.KravenHD.BackgroundColor.value = config.plugins.KravenHD.BackgroundListColor.value
		if config.plugins.KravenHD.InfobarBoxListColor.value == "self":
			config.plugins.KravenHD.InfobarBoxColor.value = config.plugins.KravenHD.InfobarBoxSelfColor.value
		else:
			config.plugins.KravenHD.InfobarBoxColor.value = config.plugins.KravenHD.InfobarBoxListColor.value
		if config.plugins.KravenHD.InfobarGradientListColor.value == "self":
			config.plugins.KravenHD.InfobarGradientColor.value = config.plugins.KravenHD.InfobarGradientSelfColor.value
		else:
			config.plugins.KravenHD.InfobarGradientColor.value = config.plugins.KravenHD.InfobarGradientListColor.value
		if config.plugins.KravenHD.SelectionBackgroundList.value == "self":
			config.plugins.KravenHD.SelectionBackground.value = config.plugins.KravenHD.SelectionBackgroundSelf.value
		else:
			config.plugins.KravenHD.SelectionBackground.value = config.plugins.KravenHD.SelectionBackgroundList.value
		if config.plugins.KravenHD.SelectionBackground2List.value == "self":
			config.plugins.KravenHD.SelectionBackground2.value = config.plugins.KravenHD.SelectionBackground2Self.value
		else:
			config.plugins.KravenHD.SelectionBackground2.value = config.plugins.KravenHD.SelectionBackground2List.value
		if config.plugins.KravenHD.SelectionBorderList.value == "self":
			config.plugins.KravenHD.SelectionBorder.value = config.plugins.KravenHD.SelectionBorderSelf.value
		else:
			config.plugins.KravenHD.SelectionBorder.value = config.plugins.KravenHD.SelectionBorderList.value
		if config.plugins.KravenHD.Font1List.value == "self":
			config.plugins.KravenHD.Font1.value = config.plugins.KravenHD.Font1Self.value
		else:
			config.plugins.KravenHD.Font1.value = config.plugins.KravenHD.Font1List.value
		if config.plugins.KravenHD.Font2List.value == "self":
			config.plugins.KravenHD.Font2.value = config.plugins.KravenHD.Font2Self.value
		else:
			config.plugins.KravenHD.Font2.value = config.plugins.KravenHD.Font2List.value
		if config.plugins.KravenHD.IBFont1List.value == "self":
			config.plugins.KravenHD.IBFont1.value = config.plugins.KravenHD.IBFont1Self.value
		else:
			config.plugins.KravenHD.IBFont1.value = config.plugins.KravenHD.IBFont1List.value
		if config.plugins.KravenHD.IBFont2List.value == "self":
			config.plugins.KravenHD.IBFont2.value = config.plugins.KravenHD.IBFont2Self.value
		else:
			config.plugins.KravenHD.IBFont2.value = config.plugins.KravenHD.IBFont2List.value
		if config.plugins.KravenHD.BackgroundGradientListColorPrimary.value == "self":
			config.plugins.KravenHD.BackgroundGradientColorPrimary.value = config.plugins.KravenHD.BackgroundGradientSelfColorPrimary.value
		else:
			config.plugins.KravenHD.BackgroundGradientColorPrimary.value = config.plugins.KravenHD.BackgroundGradientListColorPrimary.value
		if config.plugins.KravenHD.BackgroundGradientListColorSecondary.value == "self":
			config.plugins.KravenHD.BackgroundGradientColorSecondary.value = config.plugins.KravenHD.BackgroundGradientSelfColorSecondary.value
		else:
			config.plugins.KravenHD.BackgroundGradientColorSecondary.value = config.plugins.KravenHD.BackgroundGradientListColorSecondary.value
		if config.plugins.KravenHD.InfobarGradientListColorPrimary.value == "self":
			config.plugins.KravenHD.InfobarGradientColorPrimary.value = config.plugins.KravenHD.InfobarGradientSelfColorPrimary.value
		else:
			config.plugins.KravenHD.InfobarGradientColorPrimary.value = config.plugins.KravenHD.InfobarGradientListColorPrimary.value
		if config.plugins.KravenHD.InfobarGradientListColorSecondary.value == "self":
			config.plugins.KravenHD.InfobarGradientColorSecondary.value = config.plugins.KravenHD.InfobarGradientSelfColorSecondary.value
		else:
			config.plugins.KravenHD.InfobarGradientColorSecondary.value = config.plugins.KravenHD.InfobarGradientListColorSecondary.value
		if config.plugins.KravenHD.BackgroundAlternateListColor.value == "self":
			config.plugins.KravenHD.BackgroundAlternateColor.value = config.plugins.KravenHD.BackgroundAlternateSelfColor.value
		else:
			config.plugins.KravenHD.BackgroundAlternateColor.value = config.plugins.KravenHD.BackgroundAlternateListColor.value
		if config.plugins.KravenHD.InfobarAlternateListColor.value == "self":
			config.plugins.KravenHD.InfobarAlternateColor.value = config.plugins.KravenHD.InfobarAlternateSelfColor.value
		else:
			config.plugins.KravenHD.InfobarAlternateColor.value = config.plugins.KravenHD.InfobarAlternateListColor.value
		if config.plugins.KravenHD.MarkedFontList.value == "self":
			config.plugins.KravenHD.MarkedFont.value = config.plugins.KravenHD.MarkedFontSelf.value
		else:
			config.plugins.KravenHD.MarkedFont.value = config.plugins.KravenHD.MarkedFontList.value
		if config.plugins.KravenHD.SelectionFontList.value == "self":
			config.plugins.KravenHD.SelectionFont.value = config.plugins.KravenHD.SelectionFontSelf.value
		else:
			config.plugins.KravenHD.SelectionFont.value = config.plugins.KravenHD.SelectionFontList.value
		if config.plugins.KravenHD.PermanentClockFontList.value == "self":
			config.plugins.KravenHD.PermanentClockFont.value = config.plugins.KravenHD.PermanentClockFontSelf.value
		else:
			config.plugins.KravenHD.PermanentClockFont.value = config.plugins.KravenHD.PermanentClockFontList.value
		if config.plugins.KravenHD.ECMFontList.value == "self":
			config.plugins.KravenHD.ECMFont.value = config.plugins.KravenHD.ECMFontSelf.value
		else:
			config.plugins.KravenHD.ECMFont.value = config.plugins.KravenHD.ECMFontList.value
		if config.plugins.KravenHD.ChannelnameFontList.value == "self":
			config.plugins.KravenHD.ChannelnameFont.value = config.plugins.KravenHD.ChannelnameFontSelf.value
		else:
			config.plugins.KravenHD.ChannelnameFont.value = config.plugins.KravenHD.ChannelnameFontList.value
		if config.plugins.KravenHD.PrimetimeFontList.value == "self":
			config.plugins.KravenHD.PrimetimeFont.value = config.plugins.KravenHD.PrimetimeFontSelf.value
		else:
			config.plugins.KravenHD.PrimetimeFont.value = config.plugins.KravenHD.PrimetimeFontList.value
		if config.plugins.KravenHD.ButtonTextList.value == "self":
			config.plugins.KravenHD.ButtonText.value = config.plugins.KravenHD.ButtonTextSelf.value
		else:
			config.plugins.KravenHD.ButtonText.value = config.plugins.KravenHD.ButtonTextList.value
		if config.plugins.KravenHD.AndroidList.value == "self":
			config.plugins.KravenHD.Android.value = config.plugins.KravenHD.AndroidSelf.value
		else:
			config.plugins.KravenHD.Android.value = config.plugins.KravenHD.AndroidList.value
		if config.plugins.KravenHD.BorderList.value == "self":
			config.plugins.KravenHD.Border.value = config.plugins.KravenHD.BorderSelf.value
		else:
			config.plugins.KravenHD.Border.value = config.plugins.KravenHD.BorderList.value
		if config.plugins.KravenHD.ProgressList.value == "self":
			config.plugins.KravenHD.Progress.value = config.plugins.KravenHD.ProgressSelf.value
		else:
			config.plugins.KravenHD.Progress.value = config.plugins.KravenHD.ProgressList.value
		if config.plugins.KravenHD.LineList.value == "self":
			config.plugins.KravenHD.Line.value = config.plugins.KravenHD.LineSelf.value
		else:
			config.plugins.KravenHD.Line.value = config.plugins.KravenHD.LineList.value
		if config.plugins.KravenHD.IBLineList.value == "self":
			config.plugins.KravenHD.IBLine.value = config.plugins.KravenHD.IBLineSelf.value
		else:
			config.plugins.KravenHD.IBLine.value = config.plugins.KravenHD.IBLineList.value
		if config.plugins.KravenHD.MiniTVBorderList.value == "self":
			config.plugins.KravenHD.MiniTVBorder.value = config.plugins.KravenHD.MiniTVBorderSelf.value
		else:
			config.plugins.KravenHD.MiniTVBorder.value = config.plugins.KravenHD.MiniTVBorderList.value
		if config.plugins.KravenHD.AnalogColorList.value == "self":
			config.plugins.KravenHD.AnalogColor.value = config.plugins.KravenHD.AnalogColorSelf.value
		else:
			config.plugins.KravenHD.AnalogColor.value = config.plugins.KravenHD.AnalogColorList.value
		if config.plugins.KravenHD.ChannelSelectionServiceNAList.value == "self":
			config.plugins.KravenHD.ChannelSelectionServiceNA.value = config.plugins.KravenHD.ChannelSelectionServiceNASelf.value
		else:
			config.plugins.KravenHD.ChannelSelectionServiceNA.value = config.plugins.KravenHD.ChannelSelectionServiceNAList.value
		if config.plugins.KravenHD.NZBorderList.value == "self":
			config.plugins.KravenHD.NZBorder.value = config.plugins.KravenHD.NZBorderSelf.value
		else:
			config.plugins.KravenHD.NZBorder.value = config.plugins.KravenHD.NZBorderList.value
		if config.plugins.KravenHD.GMESelFgList.value == "self":
			config.plugins.KravenHD.GMESelFg.value = config.plugins.KravenHD.GMESelFgSelf.value
		else:
			config.plugins.KravenHD.GMESelFg.value = config.plugins.KravenHD.GMESelFgList.value
		if config.plugins.KravenHD.GMESelBgList.value == "self":
			config.plugins.KravenHD.GMESelBg.value = config.plugins.KravenHD.GMESelBgSelf.value
		else:
			config.plugins.KravenHD.GMESelBg.value = config.plugins.KravenHD.GMESelBgList.value
		if config.plugins.KravenHD.GMENowFgList.value == "self":
			config.plugins.KravenHD.GMENowFg.value = config.plugins.KravenHD.GMENowFgSelf.value
		else:
			config.plugins.KravenHD.GMENowFg.value = config.plugins.KravenHD.GMENowFgList.value
		if config.plugins.KravenHD.GMENowBgList.value == "self":
			config.plugins.KravenHD.GMENowBg.value = config.plugins.KravenHD.GMENowBgSelf.value
		else:
			config.plugins.KravenHD.GMENowBg.value = config.plugins.KravenHD.GMENowBgList.value
		if config.plugins.KravenHD.GMEBorderList.value == "self":
			config.plugins.KravenHD.GMEBorder.value = config.plugins.KravenHD.GMEBorderSelf.value
		else:
			config.plugins.KravenHD.GMEBorder.value = config.plugins.KravenHD.GMEBorderList.value
		if config.plugins.KravenHD.EMCSelectionBackgroundList.value == "self":
			config.plugins.KravenHD.EMCSelectionBackground.value = config.plugins.KravenHD.EMCSelectionBackgroundSelf.value
		else:
			config.plugins.KravenHD.EMCSelectionBackground.value = config.plugins.KravenHD.EMCSelectionBackgroundList.value
		if config.plugins.KravenHD.EMCSelectionFontList.value == "self":
			config.plugins.KravenHD.EMCSelectionFont.value = config.plugins.KravenHD.EMCSelectionFontSelf.value
		else:
			config.plugins.KravenHD.EMCSelectionFont.value = config.plugins.KravenHD.EMCSelectionFontList.value
		if config.plugins.KravenHD.Android2List.value == "self":
			config.plugins.KravenHD.Android2.value = config.plugins.KravenHD.Android2Self.value
		else:
			config.plugins.KravenHD.Android2.value = config.plugins.KravenHD.Android2List.value
		if config.plugins.KravenHD.UnwatchedColorList.value == "self":
			config.plugins.KravenHD.UnwatchedColor.value = config.plugins.KravenHD.UnwatchedColorSelf.value
		else:
			config.plugins.KravenHD.UnwatchedColor.value = config.plugins.KravenHD.UnwatchedColorList.value
		if config.plugins.KravenHD.WatchingColorList.value == "self":
			config.plugins.KravenHD.WatchingColor.value = config.plugins.KravenHD.WatchingColorSelf.value
		else:
			config.plugins.KravenHD.WatchingColor.value = config.plugins.KravenHD.WatchingColorList.value
		if config.plugins.KravenHD.FinishedColorList.value == "self":
			config.plugins.KravenHD.FinishedColor.value = config.plugins.KravenHD.FinishedColorSelf.value
		else:
			config.plugins.KravenHD.FinishedColor.value = config.plugins.KravenHD.FinishedColorList.value
		if config.plugins.KravenHD.TunerBusyList.value == "self":
			config.plugins.KravenHD.TunerBusy.value = config.plugins.KravenHD.TunerBusySelf.value
		else:
			config.plugins.KravenHD.TunerBusy.value = config.plugins.KravenHD.TunerBusyList.value
		if config.plugins.KravenHD.TunerLiveList.value == "self":
			config.plugins.KravenHD.TunerLive.value = config.plugins.KravenHD.TunerLiveSelf.value
		else:
			config.plugins.KravenHD.TunerLive.value = config.plugins.KravenHD.TunerLiveList.value
		if config.plugins.KravenHD.TunerRecordList.value == "self":
			config.plugins.KravenHD.TunerRecord.value = config.plugins.KravenHD.TunerRecordSelf.value
		else:
			config.plugins.KravenHD.TunerRecord.value = config.plugins.KravenHD.TunerRecordList.value
		if config.plugins.KravenHD.TunerXtremeBusyList.value == "self":
			config.plugins.KravenHD.TunerXtremeBusy.value = config.plugins.KravenHD.TunerXtremeBusySelf.value
		else:
			config.plugins.KravenHD.TunerXtremeBusy.value = config.plugins.KravenHD.TunerXtremeBusyList.value
		if config.plugins.KravenHD.IBProgressList.value == "self":
			config.plugins.KravenHD.IBProgress.value = config.plugins.KravenHD.IBProgressSelf.value
		else:
			config.plugins.KravenHD.IBProgress.value = config.plugins.KravenHD.IBProgressList.value
		if config.plugins.KravenHD.IBProgressBackgroundList.value == "self":
			config.plugins.KravenHD.IBProgressBackground.value = config.plugins.KravenHD.IBProgressBackgroundSelf.value
		else:
			config.plugins.KravenHD.IBProgressBackground.value = config.plugins.KravenHD.IBProgressBackgroundList.value
		if config.plugins.KravenHD.IBProgressBorderLineColorList.value == "self":
			config.plugins.KravenHD.IBProgressBorderLineColor.value = config.plugins.KravenHD.IBProgressBorderLineColorSelf.value
		else:
			config.plugins.KravenHD.IBProgressBorderLineColor.value = config.plugins.KravenHD.IBProgressBorderLineColorList.value
		if config.plugins.KravenHD.MainmenuHorTitleFontList.value == "self":
			config.plugins.KravenHD.MainmenuHorTitleFont.value = config.plugins.KravenHD.MainmenuHorTitleFontSelf.value
		else:
			config.plugins.KravenHD.MainmenuHorTitleFont.value = config.plugins.KravenHD.MainmenuHorTitleFontList.value
		if config.plugins.KravenHD.MainmenuHorIconColorList.value == "self":
			config.plugins.KravenHD.MainmenuHorIconColor.value = config.plugins.KravenHD.MainmenuHorIconColorSelf.value
		else:
			config.plugins.KravenHD.MainmenuHorIconColor.value = config.plugins.KravenHD.MainmenuHorIconColorList.value

		### global background
		if config.plugins.KravenHD.BackgroundColor.value == "gradient":
			self.skincolorbackgroundcolor = config.plugins.KravenHD.BackgroundGradientColorPrimary.value
		elif config.plugins.KravenHD.BackgroundColor.value == "texture":
			self.skincolorbackgroundcolor = config.plugins.KravenHD.BackgroundAlternateColor.value
		else:
			self.skincolorbackgroundcolor = config.plugins.KravenHD.BackgroundColor.value

		### infobar background
		if config.plugins.KravenHD.IBStyle.value == "grad":
			if config.plugins.KravenHD.InfobarGradientColor.value == "texture":
				self.skincolorinfobarcolor = config.plugins.KravenHD.InfobarAlternateColor.value
			else:
				self.skincolorinfobarcolor = config.plugins.KravenHD.InfobarGradientColor.value
		else:
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skincolorinfobarcolor = config.plugins.KravenHD.InfobarGradientColorPrimary.value
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skincolorinfobarcolor = config.plugins.KravenHD.InfobarAlternateColor.value
			else:
				self.skincolorinfobarcolor = config.plugins.KravenHD.InfobarBoxColor.value

		### folders and factor
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			self.data = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/"
			self.templates = "/usr/share/enigma2/KravenHD/templates/hd/"
			self.factor = 1
		else:
			self.data = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/"
			self.templates = "/usr/share/enigma2/KravenHD/templates/fhd/"
			self.factor = 1.5
		self.graphics = "/usr/share/enigma2/KravenHD/graphics/"

		### Build list and define situation
		self["config"].list = list
		self["config"].l.setList(list)
		self.updateHelp()
		self["helperimage"].hide()
		self.ShowPicture()
		option = self["config"].getCurrent()[1]
		position = self["config"].instance.getCurrentIndex()

		if position == 0: # about
			self["key_yellow"].setText("<< " + _("various"))
			self["key_blue"].setText(_("profiles") + " >>")
		if (2 <= position <= 4): # profiles
			self["key_yellow"].setText("<< " + _("about"))
			self["key_blue"].setText(_("system") + " >>")
		if (6 <= position <= 17): # system
			self["key_yellow"].setText("<< " + _("profiles"))
			self["key_blue"].setText(_("global colors") + " >>")
		if (18 <= position <= 35): # global colors
			self["key_yellow"].setText("<< " + _("system"))
			self["key_blue"].setText(_("infobar-look") + " >>")
		if (36 <= position <= 53): # infobar-look
			self["key_yellow"].setText("<< " + _("global colors"))
			self["key_blue"].setText(_("infobar-contents") + " >>")
		if (54 <= position <= 64): # infobar-contents
			self["key_yellow"].setText("<< " + _("infobar-look"))
			self["key_blue"].setText(_("weather") + " >>")
		if (72 <= position <= 81): # weather
			self["key_yellow"].setText("<< " + _("infobar-contents"))
			self["key_blue"].setText(_("clock") + " >>")
		if (83 <= position <= 85): # clock
			self["key_yellow"].setText("<< " + _("weather"))
			self["key_blue"].setText(_("ECM infos") + " >>")
		if (90 <= position <= 94): # ecm infos
			self["key_yellow"].setText("<< " + _("clock"))
			self["key_blue"].setText(_("views") + " >>")
		if (96 <= position <= 107): # views
			self["key_yellow"].setText("<< " + _("ECM infos"))
			self["key_blue"].setText(_("channellist") + " >>")
		if (108 <= position <= 116): # channellist
			self["key_yellow"].setText("<< " + _("views"))
			self["key_blue"].setText(_("NumberZap") + " >>")
		if (122 <= position <= 124): # numberzap
			self["key_yellow"].setText("<< " + _("channellist"))
			self["key_blue"].setText(_("GraphicalEPG") + " >>")
		if (126 <= position <= 133): # graphicalepg
			self["key_yellow"].setText("<< " + _("NumberZap"))
			self["key_blue"].setText(_("EMC") + " >>")
		if (135 <= position <= 143): # emc
			self["key_yellow"].setText("<< " + _("GraphicalEPG"))
			self["key_blue"].setText(_("player") + " >>")
		if config.plugins.KravenHD.IBStyle.value == "box":
			if (144 <= position <= 147): # player
				self["key_yellow"].setText("<< " + _("EMC"))
				self["key_blue"].setText(_("various") + " >>")
		else:
			if (144 <= position <= 147): # player
				self["key_yellow"].setText("<< " + _("EMC"))
				self["key_blue"].setText(_("antialiasing") + " >>")
		if config.plugins.KravenHD.IBStyle.value == "box":
			if (149 <= position <= 151): # various
				self["key_yellow"].setText("<< " + _("player"))
				self["key_blue"].setText(_("about") + " >>")
		else:
			if (149 <= position <= 152): # antialiasing
				self["key_yellow"].setText("<< " + _("player"))
				self["key_blue"].setText(_("various") + " >>")
			if (154 <= position <= 156): # various
				self["key_yellow"].setText("<< " + _("antialiasing"))
				self["key_blue"].setText(_("about") + " >>")

		### version
		versionpath = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/version"
		versionfile = open(versionpath, "r")
		for line in versionfile:
			version = line.rstrip()
			self["version"].setText(version)
		versionfile.close()

		### preview
		option = self["config"].getCurrent()[1]

		if option == config.plugins.KravenHD.customProfile:
			if config.plugins.KravenHD.customProfile.value==self.lastProfile:
				self.saveProfile(msg=False)

		if option.value == "none":
			self.showText(62, _("Off"))
		elif option.value == "on":
			self.showText(62, _("On"))
		elif option == config.plugins.KravenHD.customProfile:
			self.showText(23, "/etc/enigma2/kravenhd_profile_"+str(config.plugins.KravenHD.customProfile.value))
		elif option == config.plugins.KravenHD.defaultProfile:
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/"+str(config.plugins.KravenHD.defaultProfile.value)+".jpg"):
				self["helperimage"].show()
			else:
				self.showText(23, "/etc/enigma2/kravenhd_default_"+str(config.plugins.KravenHD.defaultProfile.value))
		elif option == config.plugins.KravenHD.TypeWriter:
			if option.value == "runningtext":
				self.showText(48, _("runningtext"))
			elif option.value == "typewriter":
				self.showText(48, _("typewriter"))
		elif option == config.plugins.KravenHD.RunningText:
			if option.value == "startdelay=2000":
				self.showText(50, _("2 sec"))
			elif option.value == "startdelay=4000":
				self.showText(50, _("4 sec"))
			elif option.value == "startdelay=6000":
				self.showText(50, _("6 sec"))
			elif option.value == "startdelay=8000":
				self.showText(50, _("8 sec"))
			elif option.value == "startdelay=10000":
				self.showText(50, _("10 sec"))
			elif option.value == "startdelay=15000":
				self.showText(50, _("15 sec"))
			elif option.value == "startdelay=20000":
				self.showText(50, _("20 sec"))
		elif option == config.plugins.KravenHD.RunningTextSpeed:
			if option.value == "steptime=200":
				self.showText(50, _("5 px/sec"))
			elif option.value == "steptime=100":
				self.showText(50, _("10 px/sec"))
			elif option.value == "steptime=66":
				self.showText(50, _("15 px/sec"))
			elif option.value == "steptime=50":
				self.showText(50, _("20 px/sec"))
		elif option == config.plugins.KravenHD.RunningTextSpeed2:
			if option.value == "steptime=200":
				self.showText(62, _("5 px/sec"))
			elif option.value == "steptime=100":
				self.showText(62, _("10 px/sec"))
			elif option.value == "steptime=50":
				self.showText(62, _("20 px/sec"))
			elif option.value == "steptime=33":
				self.showText(62, _("30 px/sec"))
		elif option == config.plugins.KravenHD.Primetimeavailable:
			if option.value == "primetime-on":
				self.showText(62, _("On"))
		elif option == config.plugins.KravenHD.SkinResolution:
			if option.value == "hd":
				self.showText(54, _("HD \n1280 x 720"))
			elif option.value == "fhd":
				self.showText(54, _("FHD \n1920 x 1080"))
		elif option == config.plugins.KravenHD.PopupStyle:
			if option.value == "popup-grad":
				self.showText(30, _("gradient-style \nwithout transparency \nglobal background"))
			elif option.value == "popup-grad-trans":
				self.showText(30, _("gradient-style \nwith transparency \nglobal background"))
			elif option.value == "popup-box":
				self.showText(30, _("box-style \nwithout transparency \nglobal background \nglobal border"))
			elif option.value == "popup-box-trans":
				self.showText(30, _("box-style \nwith transparency \nglobal background \nglobal border"))
		elif option in (config.plugins.KravenHD.InfobarChannelName, config.plugins.KravenHD.InfobarChannelName2):
			if option.value == "infobar-channelname-small":
				self.showText(40, _("RTL"))
			elif option.value == "infobar-channelname-number-small":
				self.showText(40, _("5 - RTL"))
			elif option.value == "infobar-channelname":
				self.showText(76, _("RTL"))
			elif option.value == "infobar-channelname-number":
				self.showText(76, _("5 - RTL"))
		elif option in (config.plugins.KravenHD.ECMLine1, config.plugins.KravenHD.ECMLine2, config.plugins.KravenHD.ECMLine3):
			if option.value == "VeryShortCaid":
				self.showText(17, "CAID - Time")
			elif option.value == "VeryShortReader":
				self.showText(17, "Reader - Time")
			elif option.value == "ShortReader":
				self.showText(17, "CAID - Reader - Time")
			elif option.value == "Normal":
				self.showText(17, "CAID - Reader - Hops - Time")
			elif option.value == "Long":
				self.showText(17, "CAID - System - Reader - Hops - Time")
			elif option.value == "VeryLong":
				self.showText(17, "CAM - CAID - System - Reader - Hops - Time")
		elif option == config.plugins.KravenHD.FTA and option.value == "FTAVisible":
			self.showText(17, _("free to air"))
		elif option in (config.plugins.KravenHD.weather_cityname, config.plugins.KravenHD.weather_search_over):
			self.get_weather_data()
			self.showText(20, self.actCity)
		elif option == config.plugins.KravenHD.weather_language:
			self.showText(60, option.value)
		elif option == config.plugins.KravenHD.refreshInterval:
			if option.value == "15":
				self.showText(50, "00:15")
			elif option.value == "30":
				self.showText(50, "00:30")
			elif option.value == "60":
				self.showText(50, "01:00")
			elif option.value == "120":
				self.showText(50, "02:00")
			elif option.value == "240":
				self.showText(50, "04:00")
			elif option.value == "480":
				self.showText(50, "08:00")
		elif option in (config.plugins.KravenHD.Infobox, config.plugins.KravenHD.Infobox2):
			if option.value == "sat":
				self.showText(50, "19.2E S:99%")
			elif option.value == "db":
				self.showText(50, "19.2E 12.9dB")
			elif option.value == "tunerinfo":
				self.showText(50, "19.2E DVB-S")
			elif option.value == "cpu":
				self.showText(50, "19% L:0.47")
			elif option.value == "temp":
				self.showText(50, "37°C U:1540")
		elif option == config.plugins.KravenHD.ChannelSelectionMode:
			if option.value == "zap":
				self.showText(50, "1 x OK")
			elif option.value == "preview":
				self.showText(50, "2 x OK")
		elif option == config.plugins.KravenHD.PVRState:
			if option.value == "pvrstate-center-big":
				self.showText(52, ">> 8x")
			elif option.value == "pvrstate-center-small":
				self.showText(32, ">> 8x")
			else:
				self["helperimage"].show()
		elif option == config.plugins.KravenHD.ChannelSelectionEPGSize1:
			if config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "small":
				self.showText(30, _("small"))
			elif config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "big":
				self.showText(40, _("big"))
		elif option == config.plugins.KravenHD.ChannelSelectionEPGSize2:
			if config.plugins.KravenHD.ChannelSelectionEPGSize2.value == "small":
				self.showText(30, _("small"))
			elif config.plugins.KravenHD.ChannelSelectionEPGSize2.value == "big":
				self.showText(40, _("big"))
		elif option == config.plugins.KravenHD.ChannelSelectionEPGSize3:
			if config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "small":
				self.showText(30, _("small"))
			elif config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "big":
				self.showText(40, _("big"))
		elif option == config.plugins.KravenHD.GMEDescriptionSize:
			if config.plugins.KravenHD.GMEDescriptionSize.value == "small":
				self.showText(30, _("small"))
			elif config.plugins.KravenHD.GMEDescriptionSize.value == "big":
				self.showText(40, _("big"))
		elif option == config.plugins.KravenHD.IBFontSize:
			if config.plugins.KravenHD.IBFontSize.value == "small":
				self.showText(30, _("small"))
			elif config.plugins.KravenHD.IBFontSize.value == "middle":
				self.showText(35, _("middle"))
			elif config.plugins.KravenHD.IBFontSize.value == "big":
				self.showText(40, _("big"))
		elif option in (config.plugins.KravenHD.InfobarAntialias, config.plugins.KravenHD.ECMLineAntialias, config.plugins.KravenHD.ScreensAntialias):
			if option.value == 10:
				self.showText(50, "+/- 0%")
			elif option.value in range(0, 10):
				self.showText(50, "- "+str(100-option.value*10)+"%")
			elif option.value in range(11, 21):
				self.showText(50, "+ "+str(option.value*10-100)+"%")
		elif option == config.plugins.KravenHD.DebugNames and option.value == "screennames-on":
			self.showText(50, "Debug")
		elif option in (config.plugins.KravenHD.BackgroundColorTrans, config.plugins.KravenHD.InfobarColorTrans, config.plugins.KravenHD.ChannelSelectionTrans) and option.value == "00":
			self.showText(50, _("Off"))
		elif option == config.plugins.KravenHD.BackgroundListColor:
			if config.plugins.KravenHD.BackgroundListColor.value == "gradient":
				self.showGradient(config.plugins.KravenHD.BackgroundGradientColorPrimary.value, config.plugins.KravenHD.BackgroundGradientColorSecondary.value)
			elif config.plugins.KravenHD.BackgroundListColor.value == "texture":
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.BackgroundColor.value))
		elif option == config.plugins.KravenHD.BackgroundGradientListColorPrimary:
			self.showGradient(config.plugins.KravenHD.BackgroundGradientColorPrimary.value, config.plugins.KravenHD.BackgroundGradientColorSecondary.value)
		elif option == config.plugins.KravenHD.BackgroundGradientListColorSecondary:
			self.showGradient(config.plugins.KravenHD.BackgroundGradientColorPrimary.value, config.plugins.KravenHD.BackgroundGradientColorSecondary.value)
		elif option == config.plugins.KravenHD.BackgroundAlternateListColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenHD.SelectionStyle:
			if config.plugins.KravenHD.SelectionStyle.value == "pixmap":
				self.showGradient(config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value)
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionBackground.value))
		elif option == config.plugins.KravenHD.SelectionBackgroundList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionBackground.value))
		elif option == config.plugins.KravenHD.SelectionBackground2List:
			self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionBackground2.value))
		elif option == config.plugins.KravenHD.SelectionBorderList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionBorder.value))
		elif option == config.plugins.KravenHD.IBProgressList:
			if config.plugins.KravenHD.IBProgressList.value == "progress":
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.IBProgress.value))
		elif option == config.plugins.KravenHD.IBProgressBackgroundList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.IBProgressBackground.value))
		elif option == config.plugins.KravenHD.IBProgressBorderLine:
			if option.value == "ib-progress-border":
				self.showText(30, _("border \nchoose the color below"))
			elif option.value == "ib-progress-line":
				self.showText(30, _("line \nchoose the color below"))
		elif option == config.plugins.KravenHD.IBProgressBorderLineColorList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.IBProgressBorderLineColor.value))
		elif option == config.plugins.KravenHD.EMCSelectionColors:
			if config.plugins.KravenHD.EMCSelectionColors.value == "global":
				if config.plugins.KravenHD.SelectionStyle.value == "pixmap":
					self.showGradient(config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value)
				else:
					self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionBackground.value))
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.EMCSelectionBackground.value))
		elif option == config.plugins.KravenHD.EMCSelectionBackgroundList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.EMCSelectionBackground.value))
		elif option == config.plugins.KravenHD.ProgressList:
			if config.plugins.KravenHD.ProgressList.value == "progress":
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenHD.Progress.value))
		elif option == config.plugins.KravenHD.BorderList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Border.value))
		elif option == config.plugins.KravenHD.MiniTVBorderList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.MiniTVBorder.value))
		elif option == config.plugins.KravenHD.AnalogColorList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.AnalogColor.value))
		elif option == config.plugins.KravenHD.NZBorderList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.NZBorder.value))
		elif option == config.plugins.KravenHD.GMEBorderList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.GMEBorder.value))
		elif option == config.plugins.KravenHD.GMESelFgList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.GMESelFg.value))
		elif option == config.plugins.KravenHD.GMESelBgList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.GMESelBg.value))
		elif option == config.plugins.KravenHD.GMENowFgList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.GMENowFg.value))
		elif option == config.plugins.KravenHD.GMENowBgList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.GMENowBg.value))
		elif option == config.plugins.KravenHD.LineList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Line.value))
		elif option == config.plugins.KravenHD.Font1List:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Font1.value))
		elif option == config.plugins.KravenHD.Font2List:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Font2.value))
		elif option == config.plugins.KravenHD.IBFont1List:
			self.showColor(self.hexRGB(config.plugins.KravenHD.IBFont1.value))
		elif option == config.plugins.KravenHD.IBFont2List:
			self.showColor(self.hexRGB(config.plugins.KravenHD.IBFont2.value))
		elif option == config.plugins.KravenHD.PermanentClockFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.PermanentClockFont.value))
		elif option == config.plugins.KravenHD.SelectionFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.SelectionFont.value))
		elif option == config.plugins.KravenHD.EMCSelectionFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.EMCSelectionFont.value))
		elif option == config.plugins.KravenHD.UnwatchedColorList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.UnwatchedColor.value))
		elif option == config.plugins.KravenHD.WatchingColorList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.WatchingColor.value))
		elif option == config.plugins.KravenHD.FinishedColorList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.FinishedColor.value))
		elif option == config.plugins.KravenHD.MarkedFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.MarkedFont.value))
		elif option == config.plugins.KravenHD.ButtonTextList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ButtonText.value))
		elif option == config.plugins.KravenHD.AndroidList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Android.value))
		elif option == config.plugins.KravenHD.Android2List:
			self.showColor(self.hexRGB(config.plugins.KravenHD.Android2.value))
		elif option == config.plugins.KravenHD.ChannelSelectionServiceNAList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ChannelSelectionServiceNA.value))
		elif option == config.plugins.KravenHD.IBLine:
			self["helperimage"].show()
		elif option == config.plugins.KravenHD.InfobarGradientListColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenHD.InfobarBoxListColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenHD.InfobarGradientListColorPrimary:
			self["helperimage"].show()
		elif option == config.plugins.KravenHD.InfobarGradientListColorSecondary:
			self["helperimage"].show()
		elif option == config.plugins.KravenHD.InfoStyle:
			if config.plugins.KravenHD.InfoStyle.value == "primary":
				self.showColor(self.hexRGB(config.plugins.KravenHD.InfobarGradientColorPrimary.value))
			elif config.plugins.KravenHD.InfoStyle.value == "secondary":
				self.showColor(self.hexRGB(config.plugins.KravenHD.InfobarGradientColorSecondary.value))
			else:
				self.showGradient(config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value)
		elif option == config.plugins.KravenHD.InfobarAlternateListColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenHD.ChannelnameFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ChannelnameFont.value))
		elif option == config.plugins.KravenHD.ECMFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.ECMFont.value))
		elif option == config.plugins.KravenHD.PrimetimeFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.PrimetimeFont.value))
		elif option == config.plugins.KravenHD.TunerBusyList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.TunerBusy.value))
		elif option == config.plugins.KravenHD.TunerLiveList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.TunerLive.value))
		elif option == config.plugins.KravenHD.TunerRecordList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.TunerRecord.value))
		elif option == config.plugins.KravenHD.TunerXtremeBusyList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.TunerXtremeBusy.value))
		elif option == config.plugins.KravenHD.MainmenuHorTitleFontList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.MainmenuHorTitleFont.value))
		elif option == config.plugins.KravenHD.MainmenuHorIconColorList:
			self.showColor(self.hexRGB(config.plugins.KravenHD.MainmenuHorIconColor.value))
		elif option == config.plugins.KravenHD.ECMVisible:
			if option.value == "0":
				self.showText(36, _("Off"))
			elif option.value == "ib":
				self.showText(36, _("Infobar"))
			elif option.value == "sib":
				self.showText(36, "SecondInfobar")
			elif option.value == "ib+sib":
				self.showText(36, _("Infobar & \nSecondInfobar"))
		else:
			self["helperimage"].show()

	def updateHelp(self):
		cur = self["config"].getCurrent()
		if cur:
			self["help"].text = cur[2]

	def GetPicturePath(self):
		try:
			optionValue = self["config"].getCurrent()[1]
			returnValue = self["config"].getCurrent()[1].value
			if optionValue == config.plugins.KravenHD.BackgroundListColor and config.plugins.KravenHD.BackgroundListColor.value == "texture":
				self.makeTexturePreview(config.plugins.KravenHD.BackgroundTexture.value)
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.BackgroundTexture:
				self.makeTexturePreview(returnValue)
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.InfobarTexture:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.BackgroundAlternateListColor:
				self.makeAlternatePreview(config.plugins.KravenHD.BackgroundTexture.value, config.plugins.KravenHD.BackgroundAlternateColor.value)
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.InfobarAlternateListColor:
				self.makeAlternatePreview(config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarAlternateColor.value)
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.IBStyle:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.IBLineList:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.InfobarGradientListColor:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue == config.plugins.KravenHD.InfobarBoxListColor:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif optionValue in (config.plugins.KravenHD.InfobarGradientListColorPrimary, config.plugins.KravenHD.InfobarGradientListColorSecondary):
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg"
			elif returnValue in ("about", "about2"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/about.png"
			elif returnValue == ("meteo-light"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/meteo.jpg"
			elif returnValue == "progress":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/colorfull.jpg"
			elif returnValue in ("self", config.plugins.KravenHD.PermanentClock.value):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/colors.jpg"
			elif returnValue == ("channelselection-style-minitv3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/channelselection-style-minitv.jpg"
			elif returnValue == "channelselection-style-nobile-minitv3":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/channelselection-style-nobile-minitv.jpg"
			elif returnValue == "all-screens":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/emc-smallcover.jpg"
			elif returnValue == "player-classic":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-classic.jpg"
			elif returnValue == "player-android":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-android.jpg"
			elif returnValue == "player-flip":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-flip.jpg"
			elif returnValue == "player-weather":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/clock-weather.jpg"
			elif returnValue == "box":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/2.jpg"
			elif returnValue == "grad":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/infobar-style-x2.jpg"
			elif returnValue == "only-infobar":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/infobar-style-x3.jpg"
			elif returnValue in ("0C", "18", "32", "58", "7E"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/transparent.jpg"
			elif optionValue == config.plugins.KravenHD.KravenIconVPosition:
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/vposition.jpg"
			elif fileExists("/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/" + returnValue + ".jpg"):
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
		self.PicLoad.setPara([self["helperimage"].instance.size().width(), self["helperimage"].instance.size().height(), self.Scale[0], self.Scale[1], 0, 1, "#00000000"])
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

	def keyUpLong(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.mylist()

	def keyDownLong(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.mylist()

	def pageUp(self):
		self["config"].instance.moveSelection(self["config"].instance.pageUp)
		self.mylist()

	def pageDown(self):
		self["config"].instance.moveSelection(self["config"].instance.pageDown)
		self.mylist()

	def categoryDown(self):
		position = self["config"].instance.getCurrentIndex()
		if config.plugins.KravenHD.IBStyle.value == "box":
			if position == 0: # about
				self["config"].instance.moveSelectionTo(163)
		else:
			if position == 0: # about
				self["config"].instance.moveSelectionTo(168)
		if (2 <= position <= 4): # profiles
			self["config"].instance.moveSelectionTo(0)
		if (6 <= position <= 17): # system
			self["config"].instance.moveSelectionTo(3)
		if (18 <= position <= 35): # global colors
			self["config"].instance.moveSelectionTo(7)
		if (36 <= position <= 53): # infobar-look
			self["config"].instance.moveSelectionTo(19)
		if (54 <= position <= 64): # infobar-contents
			self["config"].instance.moveSelectionTo(37)
		if (72 <= position <= 81): # weather
			self["config"].instance.moveSelectionTo(55)
		if (83 <= position <= 85): # clock
			self["config"].instance.moveSelectionTo(73)
		if (90 <= position <= 94): # ecm infos
			self["config"].instance.moveSelectionTo(84)
		if (96 <= position <= 107): # views
			self["config"].instance.moveSelectionTo(91)
		if (108 <= position <= 116): # channellist
			self["config"].instance.moveSelectionTo(97)
		if (122 <= position <= 124): # numberzap
			self["config"].instance.moveSelectionTo(109)
		if (126 <= position <= 133): # graphicalepg
			self["config"].instance.moveSelectionTo(123)
		if (135 <= position <= 143): # emc
			self["config"].instance.moveSelectionTo(127)
		if (144 <= position <= 147): # player
			self["config"].instance.moveSelectionTo(136)
		if config.plugins.KravenHD.IBStyle.value == "box":
			if (149 <= position <= 151): # various
				self["config"].instance.moveSelectionTo(145)
		else:
			if (149 <= position <= 152): # antialiasing
				self["config"].instance.moveSelectionTo(145)
			if (154 <= position <= 156): # various
				self["config"].instance.moveSelectionTo(150)
		self.mylist()

	def categoryUp(self):
		position = self["config"].instance.getCurrentIndex()
		if position == 0: # about
			self["config"].instance.moveSelectionTo(3)
		if (2 <= position <= 4): # profiles
			self["config"].instance.moveSelectionTo(7)
		if (6 <= position <= 17): # system
			self["config"].instance.moveSelectionTo(19)
		if (18 <= position <= 35): # global colors
			self["config"].instance.moveSelectionTo(37)
		if (36 <= position <= 53): # infobar-look
			self["config"].instance.moveSelectionTo(55)
		if (54 <= position <= 64): # infobar-contents
			self["config"].instance.moveSelectionTo(73)
		if (72 <= position <= 81): # weather
			self["config"].instance.moveSelectionTo(84)
		if (83 <= position <= 85): # clock
			self["config"].instance.moveSelectionTo(91)
		if (90 <= position <= 94): # ecm infos
			self["config"].instance.moveSelectionTo(97)
		if (96 <= position <= 107): # views
			self["config"].instance.moveSelectionTo(109)
		if (108 <= position <= 116): # channellist
			self["config"].instance.moveSelectionTo(123)
		if (122 <= position <= 124): # numberzap
			self["config"].instance.moveSelectionTo(127)
		if (126 <= position <= 133): # graphicalepg
			self["config"].instance.moveSelectionTo(136)
		if (135 <= position <= 143): # emc
			self["config"].instance.moveSelectionTo(145)
		if (144 <= position <= 147): # player
			self["config"].instance.moveSelectionTo(150)
		if config.plugins.KravenHD.IBStyle.value == "box":
			if (149 <= position <= 151): # various
				self["config"].instance.moveSelectionTo(0)
		else:
			if (149 <= position <= 152): # antialiasing
				self["config"].instance.moveSelectionTo(155)
			if (154 <= position <= 156): # various
				self["config"].instance.moveSelectionTo(0)
		self.mylist()

	def VirtualKeyBoardCallBack(self, callback):
		try:
			if callback:  
				self["config"].getCurrent()[1].value = callback
			else:
				pass
		except:
			pass

	def ColorSelectionCallBack(self, callback):
		try:
			if callback:
				self.actSelfColorSelection.value = callback
				self.actListColorSelection.value = "self"
				self.mylist()
			else:
				pass
		except:
			pass

	def OK(self):
		option = self["config"].getCurrent()[1]
		optionislistcolor=False

		if option == config.plugins.KravenHD.BackgroundListColor:
			if not config.plugins.KravenHD.BackgroundListColor.value in ("gradient", "texture"):
				optionislistcolor=True
				self.actSelfColorSelection = config.plugins.KravenHD.BackgroundSelfColor
		elif option == config.plugins.KravenHD.InfobarBoxListColor:
			if not config.plugins.KravenHD.InfobarBoxListColor.value in ("gradient", "texture"):
				optionislistcolor=True
				self.actSelfColorSelection = config.plugins.KravenHD.InfobarBoxSelfColor
		elif option == config.plugins.KravenHD.InfobarGradientListColor:
			if not config.plugins.KravenHD.InfobarGradientListColor.value == "texture":
				optionislistcolor=True
				self.actSelfColorSelection = config.plugins.KravenHD.InfobarGradientSelfColor
		elif option == config.plugins.KravenHD.SelectionBackgroundList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.SelectionBackgroundSelf
		elif option == config.plugins.KravenHD.SelectionBackground2List:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.SelectionBackground2Self
		elif option == config.plugins.KravenHD.SelectionBorderList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.SelectionBorderSelf
		elif option == config.plugins.KravenHD.IBProgressList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.IBProgressSelf
		elif option == config.plugins.KravenHD.IBProgressBackgroundList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.IBProgressBackgroundSelf
		elif option == config.plugins.KravenHD.IBProgressBorderLineColorList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.IBProgressBorderLineColorSelf
		elif option == config.plugins.KravenHD.Font1List:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.Font1Self
		elif option == config.plugins.KravenHD.Font2List:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.Font2Self
		elif option == config.plugins.KravenHD.IBFont1List:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.IBFont1Self
		elif option == config.plugins.KravenHD.IBFont2List:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.IBFont2Self
		elif option == config.plugins.KravenHD.BackgroundGradientListColorPrimary:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.BackgroundGradientSelfColorPrimary
		elif option == config.plugins.KravenHD.BackgroundGradientListColorSecondary:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.BackgroundGradientSelfColorSecondary
		elif option == config.plugins.KravenHD.InfobarGradientListColorPrimary:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.InfobarGradientSelfColorPrimary
		elif option == config.plugins.KravenHD.InfobarGradientListColorSecondary:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.InfobarGradientSelfColorSecondary
		elif option == config.plugins.KravenHD.BackgroundAlternateListColor:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.BackgroundAlternateSelfColor
		elif option == config.plugins.KravenHD.InfobarAlternateListColor:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.InfobarAlternateSelfColor
		elif option == config.plugins.KravenHD.MarkedFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.MarkedFontSelf
		elif option == config.plugins.KravenHD.PermanentClockFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.PermanentClockFontSelf
		elif option == config.plugins.KravenHD.SelectionFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.SelectionFontSelf
		elif option == config.plugins.KravenHD.ECMFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.ECMFontSelf
		elif option == config.plugins.KravenHD.ChannelnameFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.ChannelnameFontSelf
		elif option == config.plugins.KravenHD.PrimetimeFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.PrimetimeFontSelf
		elif option == config.plugins.KravenHD.ButtonTextList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.ButtonTextSelf
		elif option == config.plugins.KravenHD.AndroidList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.AndroidSelf
		elif option == config.plugins.KravenHD.BorderList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.BorderSelf
		elif option == config.plugins.KravenHD.ProgressList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.ProgressSelf
		elif option == config.plugins.KravenHD.LineList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.LineSelf
		elif option == config.plugins.KravenHD.IBLineList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.IBLineSelf
		elif option == config.plugins.KravenHD.MiniTVBorderList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.MiniTVBorderSelf
		elif option == config.plugins.KravenHD.AnalogColorList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.AnalogColorSelf
		elif option == config.plugins.KravenHD.ChannelSelectionServiceNAList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.ChannelSelectionServiceNASelf
		elif option == config.plugins.KravenHD.NZBorderList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.NZBorderSelf
		elif option == config.plugins.KravenHD.GMESelFgList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.GMESelFgSelf
		elif option == config.plugins.KravenHD.GMESelBgList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.GMESelBgSelf
		elif option == config.plugins.KravenHD.GMENowFgList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.GMENowFgSelf
		elif option == config.plugins.KravenHD.GMENowBgList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.GMENowBgSelf
		elif option == config.plugins.KravenHD.GMEBorderList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.GMEBorderSelf
		elif option == config.plugins.KravenHD.EMCSelectionBackgroundList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.EMCSelectionBackgroundSelf
		elif option == config.plugins.KravenHD.EMCSelectionFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.EMCSelectionFontSelf
		elif option == config.plugins.KravenHD.Android2List:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.Android2Self
		elif option == config.plugins.KravenHD.UnwatchedColorList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.UnwatchedColorSelf
		elif option == config.plugins.KravenHD.WatchingColorList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.WatchingColorSelf
		elif option == config.plugins.KravenHD.FinishedColorList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.FinishedColorSelf
		elif option == config.plugins.KravenHD.TunerBusyList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.TunerBusySelf
		elif option == config.plugins.KravenHD.TunerLiveList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.TunerLiveSelf
		elif option == config.plugins.KravenHD.TunerRecordList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.TunerRecordSelf
		elif option == config.plugins.KravenHD.TunerXtremeBusyList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.TunerXtremeBusySelf
		elif option == config.plugins.KravenHD.MainmenuHorTitleFontList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.MainmenuHorTitleFontSelf
		elif option == config.plugins.KravenHD.MainmenuHorIconColorList:
			optionislistcolor=True
			self.actSelfColorSelection = config.plugins.KravenHD.MainmenuHorIconColorSelf

		if optionislistcolor:
			self.actListColorSelection=option
			title = _("Use the sliders to define your color:")
			if self.actListColorSelection.value=="self":
				color = self.actSelfColorSelection.value
			elif self.actListColorSelection.value=="none":
				color = "000000"
			elif self.actListColorSelection.value == "progress":
				color = "C3461B"
			else:
				color = self.actListColorSelection.value
			self.session.openWithCallback(self.ColorSelectionCallBack, KravenHDColorSelection, title = title, color = color)
		elif option == config.plugins.KravenHD.weather_cityname:
			text = self["config"].getCurrent()[1].value
			if config.plugins.KravenHD.weather_search_over.value == 'name':
				title = _("Enter the city name of your location:")
			self.session.openWithCallback(self.VirtualKeyBoardCallBack, VirtualKeyBoard, title = title, text = text)
		elif option == config.plugins.KravenHD.weather_accu_apikey:
			text = self["config"].getCurrent()[1].value
			title = _("Enter your API Key:")
			self.session.openWithCallback(self.VirtualKeyBoardCallBack, VirtualKeyBoard, title = title, text = text)
		elif option == config.plugins.KravenHD.customProfile:
			self.saveProfile(msg=True)
		elif option == config.plugins.KravenHD.defaultProfile:
			self.reset()

	def faq(self):
		from Plugins.SystemPlugins.MPHelp import PluginHelp, XMLHelpReader
		reader = XMLHelpReader(resolveFilename(SCOPE_PLUGINS, "Extensions/KravenHD/faq.xml"))
		KravenHDFaq = PluginHelp(*reader)
		KravenHDFaq.open(self.session)

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
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

	def save(self, answer=True):
		self.saveProfile(msg=False)
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
			else:
				pass

		self.skinSearchAndReplace = []

		### Background (global)
		self.skinSearchAndReplace.append(['name="Kravenbg" value="#00000000', 'name="Kravenbg" value="#' + config.plugins.KravenHD.BackgroundColorTrans.value + self.skincolorbackgroundcolor])

		### Background2 (non-transparent)
		self.skinSearchAndReplace.append(['name="Kravenbg2" value="#00000000', 'name="Kravenbg2" value="#00' + self.skincolorbackgroundcolor])
		self.skinSearchAndReplace.append(['name="background" value="#00000000', 'name="background" value="#00' + self.skincolorbackgroundcolor])

		### Background3 (Menus Transparency)
		if self.actMenustyle in ("logo", "metrix-icons"):
			self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#' + config.plugins.KravenHD.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#00' + self.skincolorbackgroundcolor])

		### Background4 (Channellist)
		self.skinSearchAndReplace.append(['name="Kravenbg4" value="#00000000', 'name="Kravenbg4" value="#' + config.plugins.KravenHD.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])

		### Background5 (Radio Channellist, MSNWeather)
		self.skinSearchAndReplace.append(['name="Kravenbg5" value="#00000000', 'name="Kravenbg5" value="#' + "80" + self.skincolorbackgroundcolor])

		### Background6 (Popups, bsWindow)
		if config.plugins.KravenHD.PopupStyle.value in ("popup-grad-trans", "popup-box-trans"):
			self.skinSearchAndReplace.append(['name="Kravenbg6" value="#00000000', 'name="Kravenbg6" value="#' + "3F" + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg6" value="#00000000', 'name="Kravenbg6" value="#' + "00" + self.skincolorbackgroundcolor])

		### Background graphics
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			if config.plugins.KravenHD.BackgroundColor.value in ("gradient", "texture"):
				self.skinSearchAndReplace.append(['<!-- globalbg */-->', '<ePixmap pixmap="KravenHD/graphics/globalbg.png" position="0,0" size="1280,720" zPosition="-10" alphatest="blend" />'])
				self.skinSearchAndReplace.append(['<!-- nontransbg */-->', '<ePixmap pixmap="KravenHD/graphics/nontransbg.png" position="0,0" size="1280,720" zPosition="-10" />'])
				self.skinSearchAndReplace.append(['<!-- channelbg */-->', '<ePixmap pixmap="KravenHD/graphics/channelbg.png" position="0,0" size="1280,720" zPosition="-10" alphatest="blend" />'])
			else:
				self.skinSearchAndReplace.append(['<!-- globalbg */-->', '<eLabel backgroundColor="Kravenbg" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])
				self.skinSearchAndReplace.append(['<!-- nontransbg */-->', '<eLabel backgroundColor="Kravenbg2" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])
				self.skinSearchAndReplace.append(['<!-- channelbg */-->', '<eLabel backgroundColor="Kravenbg4" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])
		else:
			if config.plugins.KravenHD.BackgroundColor.value in ("gradient", "texture"):
				self.skinSearchAndReplace.append(['<!-- globalbg */-->', '<ePixmap pixmap="KravenHD/graphics/globalbg.png" position="0,0" size="1920,1080" zPosition="-10" alphatest="blend" />'])
				self.skinSearchAndReplace.append(['<!-- nontransbg */-->', '<ePixmap pixmap="KravenHD/graphics/nontransbg.png" position="0,0" size="1920,1080" zPosition="-10" />'])
				self.skinSearchAndReplace.append(['<!-- channelbg */-->', '<ePixmap pixmap="KravenHD/graphics/channelbg.png" position="0,0" size="1920,1080" zPosition="-10" alphatest="blend" />'])
			else:
				self.skinSearchAndReplace.append(['<!-- globalbg */-->', '<eLabel backgroundColor="Kravenbg" position="0,0" size="1920,1080" transparent="0" zPosition="-10" />'])
				self.skinSearchAndReplace.append(['<!-- nontransbg */-->', '<eLabel backgroundColor="Kravenbg2" position="0,0" size="1920,1080" transparent="0" zPosition="-10" />'])
				self.skinSearchAndReplace.append(['<!-- channelbg */-->', '<eLabel backgroundColor="Kravenbg4" position="0,0" size="1920,1080" transparent="0" zPosition="-10" />'])

		### ECM. Transparency of infobar, color of text
		if config.plugins.KravenHD.IBStyle.value == "grad":
			self.skinSearchAndReplace.append(['name="KravenECMbg" value="#F1325698', 'name="KravenECMbg" value="#' + config.plugins.KravenHD.InfobarColorTrans.value + self.calcBrightness(self.skincolorinfobarcolor, config.plugins.KravenHD.ECMLineAntialias.value)])
		else:
			self.skinSearchAndReplace.append(['name="KravenECMbg" value="#F1325698', 'name="KravenECMbg" value="#' + config.plugins.KravenHD.InfobarColorTrans.value + self.skincolorinfobarcolor])

		### Infobar. Transparency of infobar, color of infobar
		self.skinSearchAndReplace.append(['name="KravenIBbg" value="#001B1775', 'name="KravenIBbg" value="#' + config.plugins.KravenHD.InfobarColorTrans.value + self.skincolorinfobarcolor])

		### Screens. Lower Transparency of infobar and background, color of infobar or color of background, if ibar invisible
		if config.plugins.KravenHD.IBColor.value == "all-screens":
			if config.plugins.KravenHD.IBStyle.value == "grad":
				self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#' + self.calcTransparency(config.plugins.KravenHD.InfobarColorTrans.value, config.plugins.KravenHD.BackgroundColorTrans.value) + self.calcBrightness(self.skincolorinfobarcolor, config.plugins.KravenHD.ScreensAntialias.value)])
				self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#' + self.calcTransparency(config.plugins.KravenHD.InfobarColorTrans.value, config.plugins.KravenHD.BackgroundColorTrans.value) + self.calcBrightness(self.skincolorinfobarcolor, config.plugins.KravenHD.ScreensAntialias.value)])
				self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#' + self.calcTransparency(config.plugins.KravenHD.InfobarColorTrans.value, config.plugins.KravenHD.ChannelSelectionTrans.value) + self.calcBrightness(self.skincolorinfobarcolor, config.plugins.KravenHD.ScreensAntialias.value)])
			else:
				self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#' + config.plugins.KravenHD.BackgroundColorTrans.value + self.skincolorinfobarcolor])
				self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#' + config.plugins.KravenHD.ChannelSelectionTrans.value + self.skincolorinfobarcolor])
				if self.actMenustyle in ("logo", "metrix-icons"):
					self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#' + config.plugins.KravenHD.BackgroundColorTrans.value + self.skincolorinfobarcolor])
				else:
					self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#00' + self.skincolorinfobarcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg5" value="#00000000', 'name="KravenIBbg5" value="#00' + self.skincolorinfobarcolor])
		else:
			self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#' + config.plugins.KravenHD.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#' + config.plugins.KravenHD.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])
			if self.actMenustyle in ("logo", "metrix-icons"):
				self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#' + config.plugins.KravenHD.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#00' + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg5" value="#00000000', 'name="KravenIBbg5" value="#00' + self.skincolorbackgroundcolor])

		### Menu
		if not self.actChannelselectionstyle in ("channelselection-style-minitv2", "channelselection-style-minitv22", "channelselection-style-minitv33", "channelselection-style-nobile-minitv33", "channelselection-style-minitv3", "channelselection-style-nobile-minitv3"):
			self.skinSearchAndReplace.append(['render="KravenHDMenuPig"', 'render="Pig"'])

		if self.actMenustyle == "minitv":
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<panel name="Logo1"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<panel name="Icons1"/>'])
		elif self.actMenustyle == "logo":
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<panel name="Logo2"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<panel name="Icons2"/>'])
		elif self.actMenustyle == "metrix-icons":
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<panel name="Logo3"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<panel name="Icons3"/>'])
		else:
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<panel name="Logo4"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<panel name="Icons4"/>'])

		### check/install graphics (HD / FHD)
		graphpackfile = "/usr/share/enigma2/KravenHD/graphpackfile"
		graphpackname = " "
		if fileExists(graphpackfile):
			pFile = open(graphpackfile, "r")
			for line in pFile:
				graphpackname = line.strip('\n')
			pFile.close()
			if graphpackname != config.plugins.KravenHD.SkinResolution.value:
				console1 = eConsoleAppContainer()
				if config.plugins.KravenHD.SkinResolution.value == "hd":
					console1.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/share.tar.gz -C /usr/share/enigma2/KravenHD/")
					print ("KravenPlugin: HD graphics now installed")
				else:
					console1.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/share.tar.gz -C /usr/share/enigma2/KravenHD/")
					print ("KravenPlugin: FHD graphics now installed")
			else:
				print ("KravenPlugin: No need to install other graphics")

		### Mainmenu Fontsize
		if config.plugins.KravenHD.MainmenuFontsize.value == "mainmenu-small":
			self.skinSearchAndReplace.append(['<panel name="mainmenu-big"/>', '<panel name="mainmenu-small"/>'])
		elif config.plugins.KravenHD.MainmenuFontsize.value == "mainmenu-middle":
			self.skinSearchAndReplace.append(['<panel name="mainmenu-big"/>', '<panel name="mainmenu-middle"/>'])

		### Infobar. Background-Style
		if config.plugins.KravenHD.IBStyle.value == "box":

			### Infobar - Background
			self.skinSearchAndReplace.append(['<!--<eLabel position', '<eLabel position'])
			self.skinSearchAndReplace.append(['zPosition="-8" />-->', 'zPosition="-8" />'])

			### Infobar - Line
			self.skinSearchAndReplace.append(['name="KravenIBLine" value="#00ffffff', 'name="KravenIBLine" value="#00' + config.plugins.KravenHD.IBLine.value])

			### Infobar
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
					self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', '<panel name="infobar-style-x2-z1-topbar-box2"/>'])

				if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-x2-x3-box2"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-z1", "infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-z1-z2-box2"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-zz1", "infobar-style-zzz1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-box2"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-zz2-zz3-box2"/>'])

			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
					self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', '<panel name="infobar-style-x2-z1-topbar-texture"/>'])

				if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-x2-x3-texture"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-z1", "infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-z1-z2-texture"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-zz1", "infobar-style-zzz1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-texture"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-zz2-zz3-texture"/>'])

			else:
				if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
					self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', '<panel name="infobar-style-x2-z1-topbar-box"/>'])

				if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-x2-x3-box"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-z1", "infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-z1-z2-box"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-zz1", "infobar-style-zzz1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-box"/>'])
				elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-zz2-zz3-box"/>'])

			### NetatmoBar - Background
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="infobar-style-x2-z1-netatmobar-gradient"/>', '<panel name="infobar-style-x2-z1-netatmobar-box2"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="infobar-style-x2-z1-netatmobar-gradient"/>', '<panel name="infobar-style-x2-z1-netatmobar-texture"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="infobar-style-x2-z1-netatmobar-gradient"/>', '<panel name="infobar-style-x2-z1-netatmobar-box"/>'])

			### SIB - Background
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="gradient-sib"/>', '<panel name="box2-sib"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="gradient-sib"/>', '<panel name="texture-sib"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="gradient-sib"/>', '<panel name="box-sib"/>'])

			### clock-android - ibar-Position
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2") and self.actClockstyle == "clock-android":
				if config.plugins.KravenHD.SkinResolution.value == "hd":
					self.skinSearchAndReplace.append(['position="0,576" size="1280,144"', 'position="0,566" size="1280,154"'])
					self.skinSearchAndReplace.append(['position="0,576" size="1280,2"', 'position="0,566" size="1280,2"'])
					self.skinSearchAndReplace.append(['position="0,580" size="1280,140"', 'position="0,566" size="1280,154"'])
					self.skinSearchAndReplace.append(['position="0,580" size="1280,2"', 'position="0,566" size="1280,2"'])
				else:
					self.skinSearchAndReplace.append(['position="0,864" size="1920,216"', 'position="0,849" size="1920,231"'])
					self.skinSearchAndReplace.append(['position="0,864" size="1920,3"', 'position="0,849" size="1920,3"'])
					self.skinSearchAndReplace.append(['position="0,870" size="1920,210"', 'position="0,849" size="1920,231"'])
					self.skinSearchAndReplace.append(['position="0,870" size="1920,3"', 'position="0,849" size="1920,3"'])

			### EMCMediaCenter, MoviePlayer, DVDPlayer - Background
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="gradient-player"/>', '<panel name="box2-player"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="gradient-player"/>', '<panel name="texture-player"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="gradient-player"/>', '<panel name="box-player"/>'])

			### EPGSelectionEPGBar - Background
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="gradient-EPGBar"/>', '<panel name="box2-EPGBar"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="gradient-EPGBar"/>', '<panel name="texture-EPGBar"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="gradient-EPGBar"/>', '<panel name="box-EPGBar"/>'])

			### ChannelSelectionRadio
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="gradient-csr"/>', '<panel name="box2-csr"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="gradient-csr"/>', '<panel name="texture-csr"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="gradient-csr"/>', '<panel name="box-csr"/>'])

			### RadioInfoBar
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="gradient-rib"/>', '<panel name="box2-rib"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="gradient-rib"/>', '<panel name="texture-rib"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="gradient-rib"/>', '<panel name="box-rib"/>'])

			### GraphicalInfoBarEPG, QuickEPG
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="gradient-ibepg"/>', '<panel name="box2-ibepg"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="gradient-ibepg"/>', '<panel name="texture-ibepg"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="gradient-ibepg"/>', '<panel name="box-ibepg"/>'])

			### InfoBarEventView
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="gradient-ibev"/>', '<panel name="box2-ibev"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="gradient-ibev"/>', '<panel name="texture-ibev"/>'])
			else:
				self.skinSearchAndReplace.append(['<panel name="gradient-ibev"/>', '<panel name="box-ibev"/>'])

			### MediaPortal-Player
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py") and config.plugins.KravenHD.MediaPortal.value == "mediaportal":
				if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<screen name="box2-mpplayer">', '<screen name="ib-mpplayer">'])
				elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<screen name="texture-mpplayer">', '<screen name="ib-mpplayer">'])
				else:
					self.skinSearchAndReplace.append(['<screen name="box-mpplayer">', '<screen name="ib-mpplayer">'])

		else:
			### Infobar
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
				self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', '<panel name="infobar-style-x2-z1-topbar-gradient"/>'])

			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-x2-x3-gradient"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-z1", "infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-z1-z2-gradient"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-zz1", "infobar-style-zzz1"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-gradient"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<panel name="infobar-style-zz2-zz3-gradient"/>'])

			### MediaPortal-Player
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py") and config.plugins.KravenHD.MediaPortal.value == "mediaportal":
				self.skinSearchAndReplace.append(['<screen name="gradient-mpplayer">', '<screen name="ib-mpplayer">'])

		### Font Colors
		self.skinSearchAndReplace.append(['name="KravenFont1" value="#00ffffff', 'name="KravenFont1" value="#00' + config.plugins.KravenHD.Font1.value])
		self.skinSearchAndReplace.append(['name="KravenFont2" value="#00F0A30A', 'name="KravenFont2" value="#00' + config.plugins.KravenHD.Font2.value])
		self.skinSearchAndReplace.append(['name="foreground" value="#00dddddd', 'name="foreground" value="#00' + config.plugins.KravenHD.Font1.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont1" value="#00ffffff', 'name="KravenIBFont1" value="#00' + config.plugins.KravenHD.IBFont1.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont2" value="#00F0A30A', 'name="KravenIBFont2" value="#00' + config.plugins.KravenHD.IBFont2.value])
		self.skinSearchAndReplace.append(['name="KravenIBGFont1" value="#00ffffff', 'name="KravenIBGFont1" value="#00' + config.plugins.KravenHD.IBFont1.value])
		self.skinSearchAndReplace.append(['name="KravenIBGFont2" value="#00F0A30A', 'name="KravenIBGFont2" value="#00' + config.plugins.KravenHD.IBFont2.value])
		self.skinSearchAndReplace.append(['name="KravenPermanentClock" value="#00ffffff', 'name="KravenPermanentClock" value="#00' + config.plugins.KravenHD.PermanentClockFont.value])
		self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#00' + config.plugins.KravenHD.SelectionFont.value])
		self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#00' + config.plugins.KravenHD.SelectionBackground.value])
		if config.plugins.KravenHD.EMCSelectionColors.value == "global":
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#00' + config.plugins.KravenHD.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#00' + config.plugins.KravenHD.SelectionBackground.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#00' + config.plugins.KravenHD.EMCSelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#00' + config.plugins.KravenHD.EMCSelectionBackground.value])
		self.skinSearchAndReplace.append(['name="selectedFG" value="#00ffffff', 'name="selectedFG" value="#00' + config.plugins.KravenHD.SelectionFont.value])
		self.skinSearchAndReplace.append(['name="KravenMarked" value="#00ffffff', 'name="KravenMarked" value="#00' + config.plugins.KravenHD.MarkedFont.value])
		self.skinSearchAndReplace.append(['name="KravenECM" value="#00ffffff', 'name="KravenECM" value="#00' + config.plugins.KravenHD.ECMFont.value])
		self.skinSearchAndReplace.append(['name="KravenName" value="#00ffffff', 'name="KravenName" value="#00' + config.plugins.KravenHD.ChannelnameFont.value])
		self.skinSearchAndReplace.append(['name="KravenButton" value="#00ffffff', 'name="KravenButton" value="#00' + config.plugins.KravenHD.ButtonText.value])
		self.skinSearchAndReplace.append(['name="KravenAndroid" value="#00ffffff', 'name="KravenAndroid" value="#00' + config.plugins.KravenHD.Android.value])
		self.skinSearchAndReplace.append(['name="KravenAndroid2" value="#00ffffff', 'name="KravenAndroid2" value="#00' + config.plugins.KravenHD.Android2.value])
		self.skinSearchAndReplace.append(['name="KravenPrime" value="#0070AD11', 'name="KravenPrime" value="#00' + config.plugins.KravenHD.PrimetimeFont.value])
		self.skinSearchAndReplace.append(['name="KravenMainmenuHorTitleFont" value="#00999999', 'name="KravenMainmenuHorTitleFont" value="#00' + config.plugins.KravenHD.MainmenuHorTitleFont.value])

		### Infobar (Serviceevent) Font-Size
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			if config.plugins.KravenHD.IBFontSize.value == "small":
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,553" size="500,38"', 'font="Regular;22" position="545,560" size="500,27"']) # ZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,643" size="393,38"', 'font="Regular;22" position="545,650" size="393,27"']) # ZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,526" size="500,38"', 'font="Regular;22" position="545,533" size="500,27"']) # ZZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,616" size="393,38"', 'font="Regular;22" position="545,623" size="393,27"']) # ZZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="438,614" size="472,38"', 'font="Regular;22" position="438,621" size="472,27"']) # ZZ2, ZZ3 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="510,666" size="437,38"', 'font="Regular;22" position="510,673" size="437,27"']) # ZZ3 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,614" size="481,38"', 'font="Regular;22" position="430,621" size="481,27"']) # X2, X3, Z1, Z2 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,666" size="481,38"', 'font="Regular;22" position="430,673" size="481,27"']) # X2, X3, Z1, Z2 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,558" size="481,38"', 'font="Regular;22" position="430,565" size="481,27"']) # X1 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,649" size="481,38"', 'font="Regular;22" position="430,656" size="481,27"']) # X1 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="199,584" size="708,38"', 'font="Regular;22" position="199,591" size="708,27"']) # no picon now
				self.skinSearchAndReplace.append(['font="Regular;30" position="199,636" size="708,38"', 'font="Regular;22" position="199,643" size="708,27"']) # no picon next
			elif config.plugins.KravenHD.IBFontSize.value == "middle":
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,553" size="500,38"', 'font="Regular;26" position="545,556" size="500,33"']) # ZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,643" size="393,38"', 'font="Regular;26" position="545,646" size="393,33"']) # ZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,526" size="500,38"', 'font="Regular;26" position="545,529" size="500,33"']) # ZZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="545,616" size="393,38"', 'font="Regular;26" position="545,619" size="393,33"']) # ZZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="438,614" size="472,38"', 'font="Regular;26" position="438,617" size="472,33"']) # ZZ2, ZZ3 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="510,666" size="437,38"', 'font="Regular;26" position="510,669" size="437,33"']) # ZZ3 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,614" size="481,38"', 'font="Regular;26" position="430,617" size="481,33"']) # X2, X3, Z1, Z2 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,666" size="481,38"', 'font="Regular;26" position="430,669" size="481,33"']) # X2, X3, Z1, Z2 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,558" size="481,38"', 'font="Regular;26" position="430,561" size="481,33"']) # X1 now
				self.skinSearchAndReplace.append(['font="Regular;30" position="430,649" size="481,38"', 'font="Regular;26" position="430,652" size="481,33"']) # X1 next
				self.skinSearchAndReplace.append(['font="Regular;30" position="199,584" size="708,38"', 'font="Regular;26" position="199,587" size="708,33"']) # no picon now
				self.skinSearchAndReplace.append(['font="Regular;30" position="199,636" size="708,38"', 'font="Regular;26" position="199,639" size="708,33"']) # no picon next
		else:
			if config.plugins.KravenHD.IBFontSize.value == "size-33":
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,830" size="750,55"', 'font="Regular;33" position="817,839" size="750,42"']) # ZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,965" size="589,55"', 'font="Regular;33" position="817,974" size="589,42"']) # ZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,790" size="750,55"', 'font="Regular;33" position="817,799" size="750,42"']) # ZZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,925" size="589,55"', 'font="Regular;33" position="817,931" size="589,42"']) # ZZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="657,921" size="708,55"', 'font="Regular;33" position="657,930" size="708,42"']) # ZZ2, ZZ3 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="765,999" size="655,55"', 'font="Regular;33" position="765,1008" size="655,42"']) # ZZ3 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,921" size="722,55"', 'font="Regular;33" position="644,930" size="722,42"']) # X2, X3, Z1, Z2 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,999" size="722,55"', 'font="Regular;33" position="644,1008" size="722,42"']) # X2, X3, Z1, Z2 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,837" size="722,55"', 'font="Regular;33" position="644,846" size="722,42"']) # X1 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,972" size="722,55"', 'font="Regular;33" position="644,981" size="722,42"']) # X1 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="298,876" size="1061,55"', 'font="Regular;33" position="298,885" size="1061,42"']) # no picon now
				self.skinSearchAndReplace.append(['font="Regular;45" position="298,954" size="1061,55"', 'font="Regular;33" position="298,963" size="1061,42"']) # no picon next
			elif config.plugins.KravenHD.IBFontSize.value == "size-39":
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,830" size="750,55"', 'font="Regular;39" position="817,833" size="750,49"']) # ZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,965" size="589,55"', 'font="Regular;39" position="817,968" size="589,49"']) # ZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,790" size="750,55"', 'font="Regular;39" position="817,793" size="750,49"']) # ZZZ1 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="817,925" size="589,55"', 'font="Regular;39" position="817,928" size="589,49"']) # ZZZ1 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="657,921" size="708,55"', 'font="Regular;39" position="657,924" size="708,49"']) # ZZ2, ZZ3 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="765,999" size="655,55"', 'font="Regular;39" position="765,1002" size="655,49"']) # ZZ3 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,921" size="722,55"', 'font="Regular;39" position="644,924" size="722,49"']) # X2, X3, Z1, Z2 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,999" size="722,55"', 'font="Regular;39" position="644,1002" size="722,49"']) # X2, X3, Z1, Z2 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,837" size="722,55"', 'font="Regular;39" position="644,840" size="722,49"']) # X1 now
				self.skinSearchAndReplace.append(['font="Regular;45" position="644,972" size="722,55"', 'font="Regular;39" position="644,975" size="722,49"']) # X1 next
				self.skinSearchAndReplace.append(['font="Regular;45" position="298,876" size="1061,55"', 'font="Regular;39" position="298,879" size="1061,49"']) # no picon now
				self.skinSearchAndReplace.append(['font="Regular;45" position="298,954" size="1061,55"', 'font="Regular;39" position="298,957" size="1061,49"']) # no picon next

		### ChannelSelection (Event-Description) Font-Size and Primetime
		if self.actChannelselectionstyle == "channelselection-style-minitv3":
			if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-minitv-small"/>', '<panel name="channelselection-style-minitv-big-prime"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "none" and config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-minitv-small"/>', '<panel name="channelselection-style-minitv-big"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-minitv-small"/>', '<panel name="channelselection-style-minitv-small-prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nobile-minitv3":
			if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-nobile-minitv-small"/>', '<panel name="channelselection-style-nobile-minitv-big-prime"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "none" and config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-nobile-minitv-small"/>', '<panel name="channelselection-style-nobile-minitv-big"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-nobile-minitv-small"/>', '<panel name="channelselection-style-nobile-minitv-small-prime"/>'])
		elif self.actChannelselectionstyle in ("channelselection-style-nobile", "channelselection-style-nobile2", "channelselection-style-nobile-minitv", "channelselection-style-nobile-minitv3", "channelselection-style-nobile-minitv33"):
			if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<panel name="' + self.actChannelselectionstyle + '-small"/>', '<panel name="' + self.actChannelselectionstyle + '-big-prime"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "none" and config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<panel name="' + self.actChannelselectionstyle + '-small"/>', '<panel name="' + self.actChannelselectionstyle + '-big"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append(['<panel name="' + self.actChannelselectionstyle + '-small"/>', '<panel name="' + self.actChannelselectionstyle + '-small-prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv22":
			if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize2.value == "big":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-minitv22-small"/>', '<panel name="channelselection-style-minitv22-big-prime"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "none" and config.plugins.KravenHD.ChannelSelectionEPGSize2.value == "big":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-minitv22-small"/>', '<panel name="channelselection-style-minitv22-big"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize2.value == "small":
				self.skinSearchAndReplace.append(['<panel name="channelselection-style-minitv22-small"/>', '<panel name="channelselection-style-minitv22-small-prime"/>'])
		else:
			if config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<panel name="' + self.actChannelselectionstyle + '-small"/>', '<panel name="' + self.actChannelselectionstyle + '-big-prime"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "none" and config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<panel name="' + self.actChannelselectionstyle + '-small"/>', '<panel name="' + self.actChannelselectionstyle + '-big"/>'])
			elif config.plugins.KravenHD.Primetimeavailable.value == "primetime-on" and config.plugins.KravenHD.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<panel name="' + self.actChannelselectionstyle + '-small"/>', '<panel name="' + self.actChannelselectionstyle + '-small-prime"/>'])

		### ChannelSelection 'not available' Font
		self.skinSearchAndReplace.append(['name="KravenNotAvailable" value="#00FFEA04', 'name="KravenNotAvailable" value="#00' + config.plugins.KravenHD.ChannelSelectionServiceNA.value])

		### GraphicalEPG colors
		self.skinSearchAndReplace.append(['name="KravenGMESelFg" value="#00ffffff', 'name="KravenGMESelFg" value="#00' + config.plugins.KravenHD.GMESelFg.value])
		self.skinSearchAndReplace.append(['name="KravenGMESelBg" value="#00389416', 'name="KravenGMESelBg" value="#00' + config.plugins.KravenHD.GMESelBg.value])
		self.skinSearchAndReplace.append(['name="KravenGMENowFg" value="#00F0A30A', 'name="KravenGMENowFg" value="#00' + config.plugins.KravenHD.GMENowFg.value])
		self.skinSearchAndReplace.append(['name="KravenGMENowBg" value="#00389416', 'name="KravenGMENowBg" value="#00' + config.plugins.KravenHD.GMENowBg.value])
		self.skinSearchAndReplace.append(['name="KravenGMEBorder" value="#00ffffff', 'name="KravenGMEBorder" value="#00' + config.plugins.KravenHD.GMEBorder.value])

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
				self.skinSearchAndReplace.append(["infobar-icons", "icons-dark"])
			elif config.plugins.KravenHD.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["infobar-icons", "icons-light"])
		elif config.plugins.KravenHD.IBColor.value == "all-screens":
			if config.plugins.KravenHD.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-dark/"])
			elif config.plugins.KravenHD.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-light/"])
			if config.plugins.KravenHD.IconStyle.value == "icons-dark":
				self.skinSearchAndReplace.append(['name="KravenIcon" value="#00fff0e0"', 'name="KravenIcon" value="#00000000"'])
				self.skinSearchAndReplace.append(["infobar-icons", "icons-dark"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-dark/"])
			elif config.plugins.KravenHD.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["infobar-icons", "icons-light"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-light/"])

		console2 = eConsoleAppContainer()
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			if config.plugins.KravenHD.IconStyle2.value == "icons-light2":
				console2.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/icons-white.tar.gz -C /usr/share/enigma2/KravenHD/")
			else:
				console2.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/icons-black.tar.gz -C /usr/share/enigma2/KravenHD/")
		else:
			if config.plugins.KravenHD.IconStyle2.value == "icons-light2":
				console2.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/icons-white.tar.gz -C /usr/share/enigma2/KravenHD/")
			else:
				console2.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/icons-black.tar.gz -C /usr/share/enigma2/KravenHD/")

		### Weather-Server
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			if config.plugins.KravenHD.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo; 40" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenHDWetterPicon" alphatest="blend"', 'size="50,50" render="Label" font="Meteo; 45" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo; 60" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="100,100" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="100,100" render="Label" font="Meteo; 1000" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])
		else:
			if config.plugins.KravenHD.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="75,75" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="75,75" render="Label" font="Meteo;60" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="75,75" path="WetterIcons" render="KravenHDWetterPicon" alphatest="blend"', 'size="75,75" render="Label" font="Meteo;67" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="105,105" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="105,105" render="Label" font="Meteo;90" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="150,150" render="KravenHDWetterPicon" alphatest="blend" path="WetterIcons"', 'size="150,150" render="Label" font="Meteo;1500" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])

		### Meteo-Font
		if config.plugins.KravenHD.MeteoColor.value == "meteo-dark":
			self.skinSearchAndReplace.append(['name="KravenMeteo" value="#00fff0e0"', 'name="KravenMeteo" value="#00000000"'])

		### Selection Style
		if config.plugins.KravenHD.EMCSelectionColors.value == "custom":
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_28.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_32.png"', " "])
		if config.plugins.KravenHD.SelectionStyle.value == "color":
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_CS.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_MS.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_ES.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_ESM.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_30.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_36.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_40.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_45.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_50.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_53.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_60.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_70.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_75.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_90.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_110.png"', " "])
			self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_135.png"', " "])
			if config.plugins.KravenHD.EMCSelectionColors.value == "global":
				self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_28.png"', " "])
				self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_32.png"', " "])
		else:
			# ChannelSelection
			CSitems = config.usage.serviceitems_per_page.value
			if self.actChannelselectionstyle in ("channelselection-style-nobile-minitv", "channelselection-style-nobile-minitv3", "channelselection-style-nobile-minitv33"):
				if (CSitems <= 9):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_45.png'])
				if (10 <= CSitems <= 11):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_36.png'])
				if (12 <= CSitems):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_30.png'])
			elif self.actChannelselectionstyle in ("channelselection-style-nobile", "channelselection-style-nobile2"):
				if (CSitems <= 11):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_70.png'])
				if (12 <= CSitems <= 14):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_50.png'])
				if (15 <= CSitems <= 16):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_40.png'])
				if (17 <= CSitems <= 19):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_36.png'])
				if (20 <= CSitems):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_30.png'])
			elif self.actChannelselectionstyle in ("channelselection-style-minitv2", "channelselection-style-minitv-picon"):
				if (CSitems <= 11):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_50.png'])
				if (12 <= CSitems <= 13):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_36.png'])
				if (14 <= CSitems):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_30.png'])
			else:
				if (CSitems <= 11):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_70.png'])
				if (12 <= CSitems <= 13):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_50.png'])
				if (14 <= CSitems <= 15):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_40.png'])
				if (16 <= CSitems <= 18):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_36.png'])
				if (19 <= CSitems):
					self.skinSearchAndReplace.append(['sel_CS.png', 'sel_30.png'])

			# MovieSelection
			MSitems = config.movielist.itemsperpage.value
			if (MSitems <= 8):
				self.skinSearchAndReplace.append(['sel_MS.png', 'sel_90.png'])
			if (9 <= MSitems <= 11):
				self.skinSearchAndReplace.append(['sel_MS.png', 'sel_60.png'])
			if (12 <= MSitems <= 14):
				self.skinSearchAndReplace.append(['sel_MS.png', 'sel_45.png'])
			if (15 <= MSitems <= 17):
				self.skinSearchAndReplace.append(['sel_MS.png', 'sel_36.png'])
			if (18 <= MSitems):
				self.skinSearchAndReplace.append(['sel_MS.png', 'sel_30.png'])

			# EPGSelection
			ESitems = config.epgselection.enhanced_itemsperpage.value
			if (ESitems <= 10):
				self.skinSearchAndReplace.append(['sel_ES.png', 'sel_70.png'])
			if (11 <= ESitems <= 13):
				self.skinSearchAndReplace.append(['sel_ES.png', 'sel_45.png'])
			if (14 <= ESitems <= 16):
				self.skinSearchAndReplace.append(['sel_ES.png', 'sel_36.png'])
			if (17 <= ESitems):
				self.skinSearchAndReplace.append(['sel_ES.png', 'sel_30.png'])

			# EPGSelectionMulti
			ESMitems = config.epgselection.multi_itemsperpage.value
			if (ESMitems <= 10):
				self.skinSearchAndReplace.append(['sel_ESM.png', 'sel_70.png'])
			if (11 <= ESMitems <= 13):
				self.skinSearchAndReplace.append(['sel_ESM.png', 'sel_45.png'])
			if (14 <= ESMitems <= 16):
				self.skinSearchAndReplace.append(['sel_ESM.png', 'sel_36.png'])
			if (17 <= ESMitems):
				self.skinSearchAndReplace.append(['sel_ESM.png', 'sel_30.png'])

		### Progress
		if not config.plugins.KravenHD.Progress.value == "progress":
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress18.png"', " "])
			self.skinSearchAndReplace.append([' picServiceEventProgressbar="KravenHD/progress/progress52.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress170.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress248.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress270.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress300.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress328.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress380.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress410.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress480.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress657.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress736.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress990.png"', " "])
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress1265.png"', " "])
			self.skinSearchAndReplace.append(['name="KravenProgress" value="#00C3461B', 'name="KravenProgress" value="#00' + config.plugins.KravenHD.Progress.value])

		### Infobar Progress
		if not config.plugins.KravenHD.IBProgress.value == "progress":
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress581.png"', " "]) # zz2, zz3
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress657_2.png"', " "]) # zz1, zzz1
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress749.png"', " "]) # x1, x2, x3, z1, z2, timeshift
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress858.png"', " "]) # player
			self.skinSearchAndReplace.append([' pixmap="KravenHD/progress/progress977.png"', " "]) # nopicon
			self.skinSearchAndReplace.append(['name="KravenIBProgress" value="#00000000', 'name="KravenIBProgress" value="#00' + config.plugins.KravenHD.IBProgress.value])

		### Infobar Progress Background
		if config.plugins.KravenHD.IBProgressBackgroundList.value == "none":
			self.skinSearchAndReplace.append(['<IBProgressBackground', '<!-- <ePixmap'])
			self.skinSearchAndReplace.append(['"IBProgressBackground" />', '"blend" /> -->'])
		else:
			self.skinSearchAndReplace.append(['<IBProgressBackground', '<ePixmap'])
			self.skinSearchAndReplace.append(['"IBProgressBackground" />', '"blend" />'])
			self.makeProgressBackground(878, config.plugins.KravenHD.IBProgressBackground.value, "progress_bg_pl") # player
			self.makeProgressBackground(769, config.plugins.KravenHD.IBProgressBackground.value, "progress_bg_ts") # x1, x2, x3, z1, z2, timeshift
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-nopicon":
				self.makeProgressBackground(997, config.plugins.KravenHD.IBProgressBackground.value, "progress_bg_np") # nopicon
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zzz1"):
				self.makeProgressBackground(677, config.plugins.KravenHD.IBProgressBackground.value, "progress_bg_zz1") # zz1, zzz1
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
				self.makeProgressBackground(601, config.plugins.KravenHD.IBProgressBackground.value, "progress_bg_zz2") # zz2, zz3

		### Infobar Progress Border/line
		if config.plugins.KravenHD.IBProgressBorderLine.value == "ib-progress-border":
			self.skinSearchAndReplace.append(['name="KravenIBProgressBorderLine" value="#00000000', 'name="KravenIBProgressBorderLine" value="#00' + config.plugins.KravenHD.IBProgressBorderLineColor.value])
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBProgressBorderLine" zPosition="2"', 'backgroundColor="KravenIBProgressBorderLine" zPosition="-99"'])
		elif config.plugins.KravenHD.IBProgressBorderLine.value == "ib-progress-line":
			self.skinSearchAndReplace.append(['name="KravenIBProgressBorderLine" value="#00000000', 'name="KravenIBProgressBorderLine" value="#00' + config.plugins.KravenHD.IBProgressBorderLineColor.value])
			self.skinSearchAndReplace.append(['borderColor="KravenIBProgressBorderLine" borderWidth="1"', ' '])
		else:
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBProgressBorderLine" zPosition="2"', 'backgroundColor="KravenIBProgressBorderLine" zPosition="-99"'])
			self.skinSearchAndReplace.append(['borderColor="KravenIBProgressBorderLine" borderWidth="1"', ' '])

		### Border
		self.skinSearchAndReplace.append(['name="KravenBorder" value="#00ffffff', 'name="KravenBorder" value="#00' + config.plugins.KravenHD.Border.value])

		### MiniTV Border
		self.skinSearchAndReplace.append(['name="KravenBorder2" value="#003F3F3F', 'name="KravenBorder2" value="#00' + config.plugins.KravenHD.MiniTVBorder.value])

		### NumberZap Border
		if not config.plugins.KravenHD.NumberZapExt.value == "none":
			self.skinSearchAndReplace.append(['name="KravenNZBorder" value="#00ffffff', 'name="KravenNZBorder" value="#00' + config.plugins.KravenHD.NZBorder.value])

		### Line
		self.skinSearchAndReplace.append(['name="KravenLine" value="#00ffffff', 'name="KravenLine" value="#00' + config.plugins.KravenHD.Line.value])

		### Runningtext
		if config.plugins.KravenHD.RunningText.value == "none":
			self.skinSearchAndReplace.append(["movetype=running", "movetype=none"])
		else:
			self.skinSearchAndReplace.append(["startdelay=5000", config.plugins.KravenHD.RunningText.value])

			# vertical RunningText
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				self.skinSearchAndReplace.append(["steptime=90", config.plugins.KravenHD.RunningTextSpeed.value])
			else:
				self.skinSearchAndReplace.append(["steptime=90", config.plugins.KravenHD.RunningTextSpeed2.value])

			# horizontal RunningText
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				if config.plugins.KravenHD.RunningTextSpeed.value == "steptime=200":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=66"])
				elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=100":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=33"])
				elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=66":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=22"])
				elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=50":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=17"])
			else:
				if config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=200":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=66"])
				elif config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=100":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=33"])
				elif config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=50":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=17"])
				elif config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=33":
					self.skinSearchAndReplace.append(["steptime=80", "steptime=11"])

		### Scrollbar
		if config.plugins.KravenHD.ScrollBar.value == "on":
			self.skinSearchAndReplace.append(['scrollbarMode="showNever"', 'scrollbarMode="showOnDemand"'])
		else:
			self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])
					
		### Scrollbar - showNever
		self.skinSearchAndReplace.append(['scrollbarMode="never"', 'scrollbarMode="showNever"'])

		### ibar invisible
		if config.plugins.KravenHD.IBColor.value == "only-infobar":
			self.skinSearchAndReplace.append(['foregroundColor="KravenIBGFont1"', 'foregroundColor="KravenFont1"']) # IB font 1 -> global font 1
			self.skinSearchAndReplace.append(['foregroundColor="KravenIBGFont2"', 'foregroundColor="KravenFont2"']) # IB font 2 -> global font 2
			self.skinSearchAndReplace.append(['<panel name="gradient-cs"/>', " "])
			self.skinSearchAndReplace.append(['<panel name="gradient-cooltv"/>', " "])
			self.skinSearchAndReplace.append(['<panel name="gradient-emc"/>', " "])

		### Menu
		if config.plugins.KravenHD.IBColor.value == "all-screens":
			if config.plugins.KravenHD.IBStyle.value == "box":
				if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<panel name="gradient-menu"/>', '<panel name="box2-menu"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-cs"/>', '<panel name="box2-cs"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-cooltv"/>', '<panel name="box2-cooltv"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-emc"/>', '<panel name="box2-emc"/>'])
				elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<panel name="gradient-menu"/>', '<panel name="texture-menu"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-cs"/>', '<panel name="texture-cs"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-cooltv"/>', '<panel name="texture-cooltv"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-emc"/>', '<panel name="texture-emc"/>'])
				else:
					self.skinSearchAndReplace.append(['<panel name="gradient-menu"/>', '<panel name="box-menu"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-cs"/>', '<panel name="box-cs"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-cooltv"/>', '<panel name="box-cooltv"/>'])
					self.skinSearchAndReplace.append(['<panel name="gradient-emc"/>', '<panel name="box-emc"/>'])

		### MediaPortal IB style
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py") and config.plugins.KravenHD.MediaPortal.value == "mediaportal":
			if config.plugins.KravenHD.IBColor.value == "all-screens":
				if config.plugins.KravenHD.IBStyle.value == "box":
					if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
						self.skinSearchAndReplace.append(['<screen name="box2-mp">', '<screen name="ib-mp">'])
					elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
						self.skinSearchAndReplace.append(['<screen name="texture-mp">', '<screen name="ib-mp">'])
					else:
						self.skinSearchAndReplace.append(['<screen name="box-mp">', '<screen name="ib-mp">'])
				else:
					self.skinSearchAndReplace.append(['<screen name="gradient-mp">', '<screen name="ib-mp">'])
			else:
				self.skinSearchAndReplace.append(['<screen name="nonib-mp">', '<screen name="ib-mp">'])

		### Tuner
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-x2", "infobar-style-z1", "infobar-style-zz1", "infobar-style-zzz1"):

			### Tuner Colors
			self.skinSearchAndReplace.append(['name="KravenTunerBusy" value="#00CCCC00', 'name="KravenTunerBusy" value="#00' + config.plugins.KravenHD.TunerBusy.value])
			self.skinSearchAndReplace.append(['name="KravenTunerLive" value="#0000B400', 'name="KravenTunerLive" value="#00' + config.plugins.KravenHD.TunerLive.value])
			self.skinSearchAndReplace.append(['name="KravenTunerRecord" value="#00FF0C00', 'name="KravenTunerRecord" value="#00' + config.plugins.KravenHD.TunerRecord.value])
			self.skinSearchAndReplace.append(['name="KravenTunerXtremeBusy" value="#001BA1E2', 'name="KravenTunerXtremeBusy" value="#00' + config.plugins.KravenHD.TunerXtremeBusy.value])

			### Show unused Tuners
			if config.plugins.KravenHD.ShowUnusedTuner.value == "none":
				self.skinSearchAndReplace.append([',ShowUnused', ''])

			### Set align for Tuners
			if not config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append([',RightAlign2', ''])
				self.skinSearchAndReplace.append([',RightAlign4', ''])
				self.skinSearchAndReplace.append([',RightAlign8', ''])

		### SecondInfobar Textsize
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			HSize_list = [270, 300, 330, 390, 450]
			EventNowLineHeight = 30
		else:
			HSize_list = [405, 450, 495, 585, 675]
			EventNowLineHeight = 45

		for i in HSize_list:
			HSize_old = str(i)
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1"):
				HSize_new = str(i - EventNowLineHeight)
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zz2", "infobar-style-zz3"):
				HSize_new = str(i - (EventNowLineHeight * 2))
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
				HSize_new = str(i - (EventNowLineHeight * 4))
			else:
				HSize_new = str(i)

			self.skinSearchAndReplace.append([',' + HSize_old + '" name="KravenEventNowHeight"', ',' + HSize_new + '"'])

		### Clock Analog Color
		if self.actClockstyle == "clock-analog":
			self.changeColor("analogclock", "analogclock", config.plugins.KravenHD.AnalogColor.value, None)

		### Horizontal Menu Icon
		self.makeHorMenupng(config.plugins.KravenHD.MainmenuHorIconColor.value, self.skincolorbackgroundcolor)

		### Screennames
		if config.plugins.KravenHD.DebugNames.value == "screennames-on":
			begin = '<!--*'
			end = '*-->'

			if config.plugins.KravenHD.SkinResolution.value == "hd":
				begin_new = '<eLabel backgroundColor="#00000000" font="Regular;15" foregroundColor="white" text="'
				end_new = ' " position="42,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9" /><eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />'
			else:
				begin_new = '<eLabel backgroundColor="#00000000" font="Regular;22" foregroundColor="white" text="'
				end_new = ' " position="63,0" size="750,27" halign="left" valign="center" transparent="1" zPosition="9" /><eLabel position="0,0" size="1920,27" backgroundColor="#00000000" zPosition="8" />'

			self.skinSearchAndReplace.append([begin, begin_new])
			self.skinSearchAndReplace.append([end, end_new])

		### KravenIconVPosition
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			VPos_list = [23, 680, 687, 690, 692]
		else:
			VPos_list = [34, 1020, 1030, 1035, 1038]

		for i in VPos_list:
			VPos_old = str(i)
			if config.plugins.KravenHD.KravenIconVPosition.value == "vposition-3":
				VPos_new = str(i -3)
			elif config.plugins.KravenHD.KravenIconVPosition.value == "vposition-2":
				VPos_new = str(i -2)
			elif config.plugins.KravenHD.KravenIconVPosition.value == "vposition-1":
				VPos_new = str(i -1)
			elif config.plugins.KravenHD.KravenIconVPosition.value == "vposition0":
				VPos_new = str(i)
			elif config.plugins.KravenHD.KravenIconVPosition.value == "vposition+1":
				VPos_new = str(i +1)
			elif config.plugins.KravenHD.KravenIconVPosition.value == "vposition+2":
				VPos_new = str(i +2)
			elif config.plugins.KravenHD.KravenIconVPosition.value == "vposition+3":
				VPos_new = str(i +3)

			self.skinSearchAndReplace.append([',' + VPos_old + '" name="KravenIconVPosition"', ',' + VPos_new + '"'])

		### delete Font-Shadow if Channelname is inside the box
		if config.plugins.KravenHD.IBStyle.value == "box" and config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3", "infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['backgroundColor="KravenNamebg"', 'backgroundColor="KravenIBbg"'])

		### Infobar - ecm-info
		if config.plugins.KravenHD.FTA.value == "none":
			self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine1.value])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
			self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine2.value])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zz2", "infobar-style-zz3", "infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['<convert type="KravenHDECMLine">ShortReader', '<convert type="KravenHDECMLine">' + config.plugins.KravenHD.ECMLine3.value])

		### Infobar typewriter effect
		if config.plugins.KravenHD.TypeWriter.value == "runningtext":
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				self.skinSearchAndReplace.append(['render="KravenHDEmptyEpg"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',' + config.plugins.KravenHD.RunningTextSpeed.value + ',wrap=0,always=0,repeat=2,oneshot=1"'])
			else:
				self.skinSearchAndReplace.append(['render="KravenHDEmptyEpg"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',' + config.plugins.KravenHD.RunningTextSpeed2.value + ',wrap=0,always=0,repeat=2,oneshot=1"'])
		elif config.plugins.KravenHD.TypeWriter.value == "none":
			self.skinSearchAndReplace.append(['render="KravenHDEmptyEpg"', 'render="KravenHDEmptyEpg2"'])

		### Header begin
		self.appendSkinFile(self.data + "header-begin.xml")

		### Selection Border
		if config.plugins.KravenHD.SelectionStyle.value == "color" and not config.plugins.KravenHD.SelectionBorderList.value == "none":
			self.appendSkinFile(self.data + "selectionborder.xml")
			self.makeborsetpng(config.plugins.KravenHD.SelectionBorder.value)

		### Header end
		self.appendSkinFile(self.data + "header-end.xml")

		### Templates xml
		self.appendSkinFile(self.data + 'templates-main.xml')
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py") and config.plugins.KravenHD.MediaPortal.value == "mediaportal":
			self.appendSkinFile(self.data + 'templates-mediaportal.xml')
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1"):
			self.appendSkinFile(self.data + 'templates-' + config.plugins.KravenHD.InfobarStyle.value + '.xml')
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
			self.appendSkinFile(self.data + 'templates-infobar-style-x2-x3-z1-z2.xml')
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zzz1"):
			self.appendSkinFile(self.data + 'templates-infobar-style-zz1-zzz1.xml')
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
			self.appendSkinFile(self.data + 'templates-infobar-style-zz2-zz3.xml')

		### ChannelSelection - horizontal RunningText
		if not self.BoxName == "solo2":
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				if config.plugins.KravenHD.RunningTextSpeed.value == "steptime=200":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=66,wrap=0,always=0,repeat=2,oneshot=1"'])
				elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=100":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=33,wrap=0,always=0,repeat=2,oneshot=1"'])
				elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=66":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=22,wrap=0,always=0,repeat=2,oneshot=1"'])
				elif config.plugins.KravenHD.RunningTextSpeed.value == "steptime=50":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=17,wrap=0,always=0,repeat=2,oneshot=1"'])
			else:
				if config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=200":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=66,wrap=0,always=0,repeat=2,oneshot=1"'])
				elif config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=100":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=33,wrap=0,always=0,repeat=2,oneshot=1"'])
				elif config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=50":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=17,wrap=0,always=0,repeat=2,oneshot=1"'])
				elif config.plugins.KravenHD.RunningTextSpeed2.value == "steptime=33":
					self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenHD.RunningText.value + ',steptime=11,wrap=0,always=0,repeat=2,oneshot=1"'])
		else:
			self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenHDEmptyEpg2"'])

		### ChannelSelection
		config.usage.servicelist_mode.value = "standard"
		config.usage.servicelist_mode.save()
		if self.actChannelselectionstyle in ("channelselection-style-nopicon", "channelselection-style-nopicon2", "channelselection-style-xpicon", "channelselection-style-zpicon", "channelselection-style-zzpicon", "channelselection-style-zzzpicon", "channelselection-style-minitv3", "channelselection-style-nobile-minitv3") or config.plugins.KravenHD.ChannelSelectionMode.value == "zap":
			config.usage.servicelistpreview_mode.value = False
		else:
			config.usage.servicelistpreview_mode.value = True
		config.usage.servicelistpreview_mode.save()
		if self.actChannelselectionstyle in ("channelselection-style-minitv2", "channelselection-style-minitv22"): #DualTV
			config.plugins.KravenHD.PigStyle.value = "DualTV"
			config.plugins.KravenHD.PigStyle.save()
		elif self.actChannelselectionstyle in ("channelselection-style-minitv33", "channelselection-style-nobile-minitv33"): #ExtPreview
			config.plugins.KravenHD.PigStyle.value = "ExtPreview"
			config.plugins.KravenHD.PigStyle.save()
		elif self.actChannelselectionstyle in ("channelselection-style-minitv3", "channelselection-style-nobile-minitv3"): #Preview
			config.plugins.KravenHD.PigStyle.value = "Preview"
			config.plugins.KravenHD.PigStyle.save()
		else:
			self.skinSearchAndReplace.append(['render="KravenHDPig3"', 'render="Pig"'])
		self.appendSkinFile(self.data + self.actChannelselectionstyle + ".xml")

		### Infobar Clock
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-x2-x3-z1-z2-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-zz2-zz3-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-zz1-zzz1-' + self.actClockstyle + '"/>'])

		### Infobar Channelname
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-nopicon" and not config.plugins.KravenHD.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->', '<panel name="infobar-style-nopicon-' + config.plugins.KravenHD.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1" and not config.plugins.KravenHD.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->', '<panel name="infobar-style-x1-' + config.plugins.KravenHD.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2") and not config.plugins.KravenHD.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->', '<panel name="infobar-style-x2-x3-z1-z2-' + config.plugins.KravenHD.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1" and not config.plugins.KravenHD.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-' + config.plugins.KravenHD.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3") and not config.plugins.KravenHD.InfobarChannelName2.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->', '<panel name="infobar-style-zz2-zz3-' + config.plugins.KravenHD.InfobarChannelName2.value + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1" and not config.plugins.KravenHD.InfobarChannelName2.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-' + config.plugins.KravenHD.InfobarChannelName2.value + '"/>'])

		### Infobar/SIB - ecm-info
		if config.plugins.KravenHD.ECMVisible.value in ("ib", "ib+sib"):
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-ecminfo"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->', '<panel name="infobar-style-x2-x3-z1-z2-ecminfo"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->', '<panel name="infobar-style-zz2-zz3-ecminfo"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-ecminfo"/>'])

		if config.plugins.KravenHD.ECMVisible.value in ("sib", "ib+sib"):
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-ecminfo"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->', '<panel name="infobar-style-x2-x3-z1-z2-ecminfo"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->', '<panel name="infobar-style-zz2-zz3-ecminfo"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-ecminfo"/>'])

		### Infobar weather-style
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-x3", "infobar-style-z2", "infobar-style-zz1", "infobar-style-zz2", "infobar-style-zz3", "infobar-style-zzz1"):
			self.actWeatherstyle = config.plugins.KravenHD.WeatherStyle.value
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
				self.actWeatherstyle = config.plugins.KravenHD.WeatherStyle3.value
			else:
				self.actWeatherstyle = config.plugins.KravenHD.WeatherStyle2.value

		if self.actWeatherstyle == "weather-small":
			if config.plugins.KravenHD.IBStyle.value == "box":
				if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="box2-weather-small"/>'])
				elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="texture-weather-small"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="box-weather-small"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-small2"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="gradient-weather-small"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-small"/>'])

		elif self.actWeatherstyle == "weather-left":
			self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-left"/>'])

		elif self.actWeatherstyle == "weather-big":
			if config.plugins.KravenHD.IBStyle.value == "box":
				if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="box2-weather-big"/>'])
				elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="texture-weather-big"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="box-weather-big"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="gradient-weather-big"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-big"/>'])

		if config.plugins.KravenHD.refreshInterval.value == "0":
			config.plugins.KravenHD.refreshInterval.value = config.plugins.KravenHD.refreshInterval.default
			config.plugins.KravenHD.refreshInterval.save()

		### Infobar system-info
		if not config.plugins.KravenHD.SystemInfo.value == "none":
			if config.plugins.KravenHD.IBStyle.value == "box":
				if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->', '<panel name="box2-' + config.plugins.KravenHD.SystemInfo.value + '"/>'])
				elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->', '<panel name="texture-' + config.plugins.KravenHD.SystemInfo.value + '"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->', '<panel name="box-' + config.plugins.KravenHD.SystemInfo.value + '"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar systeminfo -->', '<panel name="' + config.plugins.KravenHD.SystemInfo.value + '2"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->', '<panel name="gradient-' + config.plugins.KravenHD.SystemInfo.value + '"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar systeminfo -->', '<panel name="' + config.plugins.KravenHD.SystemInfo.value + '"/>'])

		### Infobar
		# mainstyles
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
			self.skinSearchAndReplace.append(['<!-- Infobar mainstyles -->', '<panel name="infobar-style-x2-x3-z1-z2"/>'])
		else:
			self.skinSearchAndReplace.append(['<!-- Infobar mainstyles -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '"/>'])

		# picon
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3"):
			self.skinSearchAndReplace.append(['<!-- Infobar picon -->', '<panel name="infobar-style-x2-x3-picon"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-z1", "infobar-style-z2"):
			self.skinSearchAndReplace.append(['<!-- Infobar picon -->', '<panel name="infobar-style-z1-z2-picon"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zzz1"):
			if config.plugins.KravenHD.ShowAgcSnr.value == "on":
				self.skinSearchAndReplace.append(['<!-- Infobar picon -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-agc-snr"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar picon -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-picon"/>'])

		# tuners / some icons / Infobox
		if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-nopicon":
			self.skinSearchAndReplace.append(['<!-- Infobar tuners -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-' + self.Tuners + '"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar icons -->', '<panel name="infobar-style-nopicon-icons"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar infobox -->', '<panel name="infobar-style-nopicon-infobox-' + config.plugins.KravenHD.Infobox2.value + '"/>'])

		elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
			self.skinSearchAndReplace.append(['<!-- Infobar tuners -->', '<panel name="infobar-style-x1-' + self.Tuners + '"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar infobox -->', '<panel name="infobar-style-x1-infobox-' + config.plugins.KravenHD.Infobox.value + '"/>'])

		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
			self.skinSearchAndReplace.append(['<!-- Infobar topbaricons -->', '<panel name="infobar-style-x2-z1-icons"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar topbartuners -->', '<panel name="infobar-style-x2-z1-' + self.Tuners + '"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar topbarinfobox -->', '<panel name="infobar-style-x2-z1-infobox-' + config.plugins.KravenHD.Infobox.value + '"/>'])

		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['<!-- Infobar icons -->', '<panel name="infobar-style-zz1-zzz1-icons"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar tuners -->', '<panel name="infobar-style-zz1-zzz1-' + self.Tuners + '"/>'])
			self.actInfobox = ''
			if config.plugins.KravenHD.ShowAgcSnr.value == "on":
				self.actInfobox = config.plugins.KravenHD.Infobox2.value
			else:
				self.actInfobox = config.plugins.KravenHD.Infobox.value
			self.skinSearchAndReplace.append(['<!-- Infobar infobox -->', '<panel name="infobar-style-zz1-zzz1-infobox-' + self.actInfobox + '"/>'])

		### SecondInfobar
		self.skinSearchAndReplace.append(['<!-- SIB style -->', '<panel name="' + config.plugins.KravenHD.SIB.value + '"/>'])

		### Players clockstyle
		self.skinSearchAndReplace.append(['<!-- Player clockstyle -->', '<panel name="' + config.plugins.KravenHD.PlayerClock.value + '"/>'])

		### Volume
		self.skinSearchAndReplace.append(['<!-- Volume style -->', '<panel name="' + config.plugins.KravenHD.Volume.value + '"/>'])
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			if config.plugins.KravenHD.Volume.value == "volume-left":
				self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"', 'screen name="Volume" position="10,130" size="28,360"'])
			elif config.plugins.KravenHD.Volume.value == "volume-right":
				self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"', 'screen name="Volume" position="1240,130" size="28,360"'])
			elif config.plugins.KravenHD.Volume.value == "volume-top":
				self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"', 'screen name="Volume" position="center,25" size="400,28"'])
			elif config.plugins.KravenHD.Volume.value == "volume-center":
				self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"', 'screen name="Volume" position="548,286" size="184,184"'])
		else:
			if config.plugins.KravenHD.Volume.value == "volume-left":
				self.skinSearchAndReplace.append(['screen name="Volume" position="70,57" size="495,120"', 'screen name="Volume" position="15,195" size="42,540"'])
			elif config.plugins.KravenHD.Volume.value == "volume-right":
				self.skinSearchAndReplace.append(['screen name="Volume" position="70,57" size="495,120"', 'screen name="Volume" position="1860,195" size="42,540"'])
			elif config.plugins.KravenHD.Volume.value == "volume-top":
				self.skinSearchAndReplace.append(['screen name="Volume" position="70,57" size="495,120"', 'screen name="Volume" position="center,37" size="600,42"'])
			elif config.plugins.KravenHD.Volume.value == "volume-center":
				self.skinSearchAndReplace.append(['screen name="Volume" position="70,57" size="495,120"', 'screen name="Volume" position="868,448" size="184,184"'])

		### PVRState
		if config.plugins.KravenHD.IBStyle.value == "box":
			if config.plugins.KravenHD.InfobarBoxColor.value in ("gradient", "texture") and not config.plugins.KravenHD.PVRState.value == "pvrstate-off":
				if config.plugins.KravenHD.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', '<panel name="pvrstate-box-' + config.plugins.KravenHD.InfobarBoxColor.value + '"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', '<panel name="pvrstate2-box-' + config.plugins.KravenHD.InfobarBoxColor.value + '"/>'])
			if not config.plugins.KravenHD.InfobarBoxColor.value in ("gradient", "texture") and not config.plugins.KravenHD.PVRState.value == "pvrstate-off":
				if config.plugins.KravenHD.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', '<panel name="pvrstate-bg"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', '<panel name="pvrstate2-bg"/>'])
		else:
			if not config.plugins.KravenHD.PVRState.value == "pvrstate-off":
				if config.plugins.KravenHD.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', '<panel name="pvrstate-bg"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', '<panel name="pvrstate2-bg"/>'])

		if not config.plugins.KravenHD.PVRState.value == "pvrstate-off":
			self.skinSearchAndReplace.append(['<!-- PVRState style -->', '<panel name="' + config.plugins.KravenHD.PVRState.value + '"/>'])
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				if config.plugins.KravenHD.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="center,center" size="220,90"'])
				elif config.plugins.KravenHD.PVRState.value == "pvrstate-center-small":
					self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="center,center" size="110,45"'])
				elif config.plugins.KravenHD.PVRState.value == "pvrstate-left-small":
					self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="30,20" size="110,45"'])
			else:
				if config.plugins.KravenHD.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="center,center" size="330,135"'])
				elif config.plugins.KravenHD.PVRState.value == "pvrstate-center-small":
					self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="center,center" size="165,67"'])
				elif config.plugins.KravenHD.PVRState.value == "pvrstate-left-small":
					self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="45,30" size="165,67"'])

		### Main XML
		self.appendSkinFile(self.data + "main.xml")

		if config.plugins.KravenHD.IBStyle.value == "grad":
			### Timeshift_begin
			self.appendSkinFile(self.data + "timeshift-begin.xml")

			if self.actWeatherstyle in ("weather-big", "weather-left"):
				if config.plugins.KravenHD.SystemInfo.value == "systeminfo-bigsat":
					self.appendSkinFile(self.data + "timeshift-begin-leftlow.xml")
				else:
					self.appendSkinFile(self.data + "timeshift-begin-low.xml")
			elif self.actWeatherstyle == "weather-small":
				self.appendSkinFile(self.data + "timeshift-begin-left.xml")
			else:
				self.appendSkinFile(self.data + "timeshift-begin-high.xml")

			### Timeshift_end
			self.appendSkinFile(self.data + "timeshift-end.xml")

			### InfobarTunerState
			if self.actWeatherstyle in ("weather-big", "weather-left", "netatmobar"):
				if config.plugins.KravenHD.SystemInfo.value == "systeminfo-bigsat":
					self.appendSkinFile(self.data + "infobartunerstate-low.xml")
				else:
					self.appendSkinFile(self.data + "infobartunerstate-mid.xml")
			else:
				self.appendSkinFile(self.data + "infobartunerstate-high.xml")

		elif config.plugins.KravenHD.IBStyle.value == "box":
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<panel name="timeshift-bg"/>', '<panel name="timeshift-bg-box2"/>'])
				self.skinSearchAndReplace.append(['<panel name="ibts-bg"/>', '<panel name="ibts-bg-box2"/>'])
				self.skinSearchAndReplace.append(['<panel name="autoresolution-bg"/>', '<panel name="autoresolution-bg-box2"/>'])
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<panel name="timeshift-bg"/>', '<panel name="timeshift-bg-texture"/>'])
				self.skinSearchAndReplace.append(['<panel name="ibts-bg"/>', '<panel name="ibts-bg-texture"/>'])
				self.skinSearchAndReplace.append(['<panel name="autoresolution-bg"/>', '<panel name="autoresolution-bg-texture"/>'])
			self.appendSkinFile(self.data + "timeshift-ibts-ar.xml")

		### PermanentClock
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			if config.plugins.KravenHD.PermanentClock.value == "permanentclock-infobar-small":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="KravenIBbg" name="PermanentClockScreen" size="80,20"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-infobar-small"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-global-big":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="120,30"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-global-big"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-global-small":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="80,20"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-global-small"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-transparent-big":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="transparent" name="PermanentClockScreen" size="120,30"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-transparent-big"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-transparent-small":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="transparent" name="PermanentClockScreen" size="80,20"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-transparent-small"/>'])
		else:
			if config.plugins.KravenHD.PermanentClock.value == "permanentclock-infobar-small":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="180,45"', 'backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-infobar-small"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-global-big":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="180,45"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="180,45"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-global-big"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-global-small":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="180,45"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="120,30"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-global-small"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-transparent-big":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="180,45"', 'backgroundColor="transparent" name="PermanentClockScreen" size="180,45"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-transparent-big"/>'])
			elif config.plugins.KravenHD.PermanentClock.value == "permanentclock-transparent-small":
				self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="180,45"', 'backgroundColor="transparent" name="PermanentClockScreen" size="120,30"'])
				self.skinSearchAndReplace.append(['<panel name="permanentclock-infobar-big"/>', '<panel name="permanentclock-transparent-small"/>'])

		### Plugins
		self.appendSkinFile(self.data + "plugins.xml")

		### MSNWeather
		if fileExists("/usr/lib/enigma2/python/Components/Converter/MSNWeather.pyo"):
			if config.plugins.KravenHD.IBStyle.value == "grad" or config.plugins.KravenHD.PopupStyle.value in ("popup-grad", "popup-grad-trans"):
				self.changeColor("msnbg_gr", "msnbg", self.skincolorbackgroundcolor, None)
			else:
				self.changeColor("msnbg", "msnbg", self.skincolorbackgroundcolor, None)
			self.appendSkinFile(self.data + "weatherplugin.xml")
			if self.InternetAvailable and not fileExists("/usr/share/enigma2/KravenHD/msn_weather_icons/1.png"):
				console3 = eConsoleAppContainer()
				console3.execute("wget -q http://picons.mynonpublic.com/msn-icon.tar.gz -O /tmp/msn-icon.tar.gz; tar xf /tmp/msn-icon.tar.gz -C /usr/share/enigma2/KravenHD/")
		else:
			self.appendSkinFile(self.data + "weatherplugin2.xml")

		### NetatmoBar
		if self.InternetAvailable:
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
					if self.actWeatherstyle == "netatmobar":
						self.appendSkinFile(self.data + "netatmobar.xml")

		### EMC (MovieList) Font-Colors
		self.skinSearchAndReplace.append(['UnwatchedColor="unwatched"', 'UnwatchedColor="#00' + config.plugins.KravenHD.UnwatchedColor.value + '"'])
		self.skinSearchAndReplace.append(['WatchingColor="watching"', 'WatchingColor="#00' + config.plugins.KravenHD.WatchingColor.value + '"'])
		self.skinSearchAndReplace.append(['FinishedColor="finished"', 'FinishedColor="#00' + config.plugins.KravenHD.FinishedColor.value + '"'])

		### EMC
		self.appendSkinFile(self.data + config.plugins.KravenHD.EMCStyle.value + ".xml")

		### NumberZapExt
		self.appendSkinFile(self.data + config.plugins.KravenHD.NumberZapExt.value + ".xml")
		if not config.plugins.KravenHD.NumberZapExt.value == "none":
			config.usage.numberzap_show_picon.value = True
			config.usage.numberzap_show_picon.save()
			config.usage.numberzap_show_servicename.value = True
			config.usage.numberzap_show_servicename.save()

		### FileCommander
		self.appendSkinFile(self.data + config.plugins.KravenHD.FileCommander.value + ".xml")

		### EPGSelection
		self.appendSkinFile(self.data + config.plugins.KravenHD.EPGSelection.value + ".xml")

		### CoolTVGuide
		self.appendSkinFile(self.data + config.plugins.KravenHD.CoolTVGuide.value + ".xml")

		### GraphicalEPG (Event-Description) Font-Size
		if config.plugins.KravenHD.GMEDescriptionSize.value == "big":
			self.skinSearchAndReplace.append(['<panel name="GE-small"/>', '<panel name="GE-big"/>'])
			self.skinSearchAndReplace.append(['<panel name="GEMT-small"/>', '<panel name="GEMT-big"/>'])

		### GraphicalEPG
		if config.plugins.KravenHD.GraphicalEPG.value == "text":
			config.epgselection.graph_type_mode.value = False
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = False
			config.epgselection.graph_pig.save()
		elif config.plugins.KravenHD.GraphicalEPG.value == "text-minitv":
			config.epgselection.graph_type_mode.value = False
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = True
			config.epgselection.graph_pig.save()
		elif config.plugins.KravenHD.GraphicalEPG.value == "graphical":
			config.epgselection.graph_type_mode.value = "graphics"
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = False
			config.epgselection.graph_pig.save()
		elif config.plugins.KravenHD.GraphicalEPG.value == "graphical-minitv":
			config.epgselection.graph_type_mode.value = "graphics"
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = True
			config.epgselection.graph_pig.save()

		### MovieSelection
		self.appendSkinFile(self.data + config.plugins.KravenHD.MovieSelection.value + ".xml")

		### bsWindow
		self.makebsWindowpng()

		### SerienRecorder
		if config.plugins.KravenHD.SerienRecorder.value == "serienrecorder":
			self.appendSkinFile(self.data + config.plugins.KravenHD.SerienRecorder.value + ".xml")
			self.changeColor("popup_bg", "popup_bg", self.skincolorbackgroundcolor, config.plugins.KravenHD.Border.value)

		### MediaPortal
		console4 = eConsoleAppContainer()
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py"):
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				if config.plugins.KravenHD.MediaPortal.value == "mediaportal":
					console4.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/")
				else:
					if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/MP_skin.xml"):
						console4.execute("rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD")
			else:
				if config.plugins.KravenHD.MediaPortal.value == "mediaportal":
					console4.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/")
				else:
					if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD/MP_skin.xml"):
						console4.execute("rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD")

		### skin-user
		try:
			self.appendSkinFile(self.data + "skin-user.xml")
		except:
			pass

		### skin-end
		self.appendSkinFile(self.data + "skin-end.xml")

		xFile = open(self.dateiTMP, "w")
		for xx in self.skin_lines:
			xFile.writelines(xx)
		xFile.close()

		move(self.dateiTMP, self.datei)

		### Menu icons download - we do it here to give it some time
		if self.InternetAvailable:
			if config.plugins.KravenHD.Logo.value in ("metrix-icons", "minitv-metrix-icons"):
				self.installIcons(config.plugins.KravenHD.MenuIcons.value)

		### Get weather data to make sure the helper config values are not empty
		self.get_weather_data()

		# make global background graphics
		if config.plugins.KravenHD.BackgroundColor.value == "gradient":
			self.makeBGGradientpng()
		elif config.plugins.KravenHD.BackgroundColor.value == "texture":
			self.makeBGTexturepng()

		# make infobar background graphics
		if config.plugins.KravenHD.IBStyle.value == "grad":
			if config.plugins.KravenHD.InfobarGradientColor.value == "texture":
				self.makeIBGradTexturepng()
			else: # single color
				self.makeIBGradColorpng()
		elif config.plugins.KravenHD.IBStyle.value == "box":
			if config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				self.makeIBGradientpng()
			elif config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				self.makeIBTexturepng()

		# make selection pixmaps
		if config.plugins.KravenHD.SelectionStyle.value == "pixmap":
			self.makeSELGradientpng()

		# copy bsWindow to MediaPortal-folder
		console5 = eConsoleAppContainer()
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/MP_skin.xml") and config.plugins.KravenHD.MediaPortal.value == "mediaportal" and config.plugins.KravenHD.SkinResolution.value == "hd":
			console5.execute("cp /usr/share/enigma2/KravenHD/graphics/bs_* /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/images/")
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD/MP_skin.xml") and config.plugins.KravenHD.MediaPortal.value == "mediaportal" and config.plugins.KravenHD.SkinResolution.value == "fhd":
			console5.execute("cp /usr/share/enigma2/KravenHD/graphics/bs_* /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD/images/")

		# Thats it
		self.restart()

	def restart(self):
		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
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
		askExit = self.session.openWithCallback(self.doExit, MessageBox, _("Do you really want to exit without saving?"), MessageBox.TYPE_YESNO)
		askExit.setTitle(_("Exit"))

	def doExit(self, answer):
		if answer is True:
			for x in self["config"].list:
				if len(x) > 1:
						x[1].cancel()
				else:
						pass
			self.close()
		else:
			self.mylist()

	def getBoxName(self):
		if fileExists("/proc/stb/info/vumodel"):
			file = open('/proc/stb/info/vumodel', 'r')
			boxname = file.readline().strip()
			file.close()
			return boxname
		else:
			try:
				from boxbranding import getMachineName
				return getMachineName()
			except ImportError:
				return "unknown"

	def getTuners(self):
		from Components.Sources.TunerInfo import TunerInfo
		tinfo = TunerInfo()
		tuners = tinfo.getTunerAmount()
		if tuners == 1:
			return "1-tuner"
		elif tuners == 2:
			return "2-tuner"
		elif (3 <= tuners <= 4):
			return "4-tuner"
		elif (5 <= tuners):
			return "8-tuner"
		else:
			return "1-tuner"

	def getInternetAvailable(self):
		from . import ping
		r = ping.doOne("8.8.8.8", 1.5)
		if r != None and r <= 1.5:
			return True
		else:
			return False

	def getUserMenuIconsAvailable(self):
		userpath="/usr/share/enigma2/Kraven-user-icons"
		if path.exists(userpath) and any(File.endswith(".png") for File in listdir(userpath)):
			return True
		else:
			return False

	def reset(self):
		askReset = self.session.openWithCallback(self.doReset, MessageBox, _("Do you really want to reset all values to the selected default profile?"), MessageBox.TYPE_YESNO)
		askReset.setTitle(_("Reset profile"))

	def doReset(self, answer):
		if answer is True:
			if config.plugins.KravenHD.defaultProfile.value == "default":
				for name in config.plugins.KravenHD.dict():
					if not name in ("customProfile", "DebugNames"):
						item=(getattr(config.plugins.KravenHD, name))
						item.value=item.default
			else:
				self.loadProfile(loadDefault=True)
		self.mylist()

	def showColor(self, actcolor):
		c = self["Canvas"]
		c.fill(0, 0, 368, 207, actcolor)
		c.flush()

	def showGradient(self, color1, color2):
		width=368
		height=207
		color1=color1[-6:]
		r1=int(color1[0:2], 16)
		g1=int(color1[2:4], 16)
		b1=int(color1[4:6], 16)
		color2=color2[-6:]
		r2=int(color2[0:2], 16)
		g2=int(color2[2:4], 16)
		b2=int(color2[4:6], 16)
		c = self["Canvas"]
		if color1!=color2:
			for pos in range(0, height):
				p=pos/float(height)
				r=r2*p+r1*(1-p)
				g=g2*p+g1*(1-p)
				b=b2*p+b1*(1-p)
				c.fill(0, pos, width, 1, self.RGB(int(r), int(g), int(b)))
		else:
			c.fill(0, 0, width, height, self.RGB(int(r1), int(g1), int(b1)))
		c.flush()

	def showText(self, fontsize, text):
		from enigma import gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER
		c = self["Canvas"]
		c.fill(0, 0, 368, 207, self.RGB(0, 0, 0))
		c.writeText(0, 0, 368, 207, self.RGB(255, 255, 255), self.RGB(0, 0, 0), gFont("Regular", fontsize), text, RT_HALIGN_CENTER+RT_VALIGN_CENTER)
		c.flush()

	def loadProfile(self,loadDefault=False):
		if loadDefault:
			profile=config.plugins.KravenHD.defaultProfile.value
			fname=self.profiles+"kravenhd_default_"+profile
		else:
			profile=config.plugins.KravenHD.customProfile.value
			fname=self.profiles+"kravenhd_profile_"+profile
		if profile and fileExists(fname):
			print ("KravenPlugin: Load profile "+fname)
			
			pFile=open(fname, "r")
			for line in pFile:
				try:
					line=line.split("|")
					name=line[0]
					value=line[1]
					type=line[2].strip('\n')
					if not (name in ("customProfile", "DebugNames", "weather_search_over", "weather_accu_latlon", "weather_accu_id", "weather_accu_apikey", "weather_foundcity", "weather_cityname", "weather_language") or (loadDefault and name == "defaultProfile")):
						# fix for changed value "gradient"/"grad"
						if name=="IBStyle" and value=="gradient":
							value="grad"
						# fix for changed name "InfobarColor"/"InfobarGradientColor"
						if name=="InfobarColor":
							config.plugins.KravenHD.InfobarGradientColor.value=value
						if type == "<type 'int'>":
							getattr(config.plugins.KravenHD, name).value=int(value)
						elif type == "<type 'hex'>":
							getattr(config.plugins.KravenHD, name).value=hex(value)
						elif type == "<type 'list'>":
							getattr(config.plugins.KravenHD, name).value=eval(value)
						else:
							getattr(config.plugins.KravenHD, name).value=str(value)
				except:
					pass
			pFile.close()

		elif not loadDefault:
			print ("KravenPlugin: Create profile "+fname)
			self.saveProfile(msg=False)

	def saveProfile(self,msg=True):
		profile=config.plugins.KravenHD.customProfile.value
		if profile:
			try:
				fname=self.profiles+"kravenhd_profile_"+profile
				print ("KravenPlugin: Save profile "+fname)
				pFile=open(fname, "w")
				for name in config.plugins.KravenHD.dict():
					if not name in ("customProfile", "DebugNames", "weather_accu_latlon", "weather_accu_id", "weather_accu_apikey", "weather_foundcity", "weather_cityname", "weather_language"):
						value=getattr(config.plugins.KravenHD, name).value
						pFile.writelines(name+"|"+str(value)+"|"+str(type(value))+"\n")
				pFile.close()
				if msg:
					self.session.open(MessageBox, _("Profile ")+str(profile)+_(" saved successfully."), MessageBox.TYPE_INFO, timeout=5)
			except:
				self.session.open(MessageBox, _("Profile ")+str(profile)+_(" could not be saved!"), MessageBox.TYPE_INFO, timeout=15)

	def installIcons(self, author):

		if self.InternetAvailable == False: 
			return

		pathname="http://picons.mynonpublic.com/"
		instname="/usr/share/enigma2/Kraven-menu-icons/iconpackname"
		versname="Kraven-Menu-Icons-by-"+author+".packname"
		
		# Read iconpack version on box
		packinstalled = "not installed"
		if fileExists(instname):
			pFile=open(instname, "r")
			for line in pFile:
				packinstalled=line.strip('\n')
			pFile.close()
		print ("KravenPlugin: Iconpack on box is "+packinstalled)
		
		# Read iconpack version on server
		packonserver = "unknown"
		fullversname=pathname+versname
		sub=subprocess.Popen("wget -q "+fullversname+" -O /tmp/"+versname, shell=True)
		sub.wait()
		if fileExists("/tmp/"+versname):
			pFile=open("/tmp/"+versname, "r")
			for line in pFile:
				packonserver=line.strip('\n')
			pFile.close()
			popen("rm /tmp/"+versname)
			print ("KravenPlugin: Iconpack on server is "+packonserver)

			# Download an install icon pack, if needed
			if packinstalled != packonserver:
				packname=packonserver
				fullpackname=pathname+packname
				sub=subprocess.Popen("rm -rf /usr/share/enigma2/Kraven-menu-icons/*.*; rm -rf /usr/share/enigma2/Kraven-menu-icons; wget -q "+fullpackname+" -O /tmp/"+packname+"; tar xf /tmp/"+packname+" -C /usr/share/enigma2/", shell=True)
				sub.wait()
				popen("rm /tmp/"+packname)
				print ("KravenPlugin: Installed iconpack "+fullpackname)
			else:
				print ("KravenPlugin: No need to install other iconpack")

	def makeTexturePreview(self, style):
		width = 368
		height = 207
		inpath = "/usr/share/enigma2/KravenHD/textures/"
		usrpath = "/usr/share/enigma2/Kraven-user-icons/"
		outpath = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/"

		if fileExists(usrpath + style + ".png"):
			bg = Image.open(usrpath + style + ".png")
		elif fileExists(usrpath + style + ".jpg"):
			bg = Image.open(usrpath + style + ".jpg")
		elif fileExists(inpath + style + ".png"):
			bg = Image.open(inpath + style + ".png")
		elif fileExists(inpath + style + ".jpg"):
			bg = Image.open(inpath + style + ".jpg")
		bg_w, bg_h = bg.size
		image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, height, bg_h):
				image.paste(bg, (i, j))
		image.save(outpath + "preview.jpg")
		
	def makeAlternatePreview(self, style, color):
		width = 368
		height = 207
		inpath = "/usr/share/enigma2/KravenHD/textures/"
		usrpath = "/usr/share/enigma2/Kraven-user-icons/"
		outpath = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/"

		if fileExists(usrpath + style + ".png"):
			bg = Image.open(usrpath + style + ".png")
		elif fileExists(usrpath + style + ".jpg"):
			bg = Image.open(usrpath + style + ".jpg")
		elif fileExists(inpath + style + ".png"):
			bg = Image.open(inpath + style + ".png")
		elif fileExists(inpath + style + ".jpg"):
			bg = Image.open(inpath + style + ".jpg")
		bg_w, bg_h = bg.size
		image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, height, bg_h):
				image.paste(bg, (i, j))
		color=color[-6:]
		r=int(color[0:2], 16)
		g=int(color[2:4], 16)
		b=int(color[4:6], 16)
		image.paste((int(r), int(g), int(b), 255), (0, int(height/2), width, height))
		image.save(outpath + "preview.jpg")
		
	def makePreview(self):
		width = 368
		height = 208
		lineheight = 3
		boxbarheight = 40
		gradbarheight = 80
		inpath = "/usr/share/enigma2/KravenHD/textures/"
		usrpath = "/usr/share/enigma2/Kraven-user-icons/"
			
		# background
		if config.plugins.KravenHD.BackgroundColor.value == "texture":
			style = config.plugins.KravenHD.BackgroundTexture.value
			if fileExists(usrpath + style + ".png"):
				bg = Image.open(usrpath + style + ".png")
			elif fileExists(usrpath + style + ".jpg"):
				bg = Image.open(usrpath + style + ".jpg")
			elif fileExists(inpath + style + ".png"):
				bg = Image.open(inpath + style + ".png")
			elif fileExists(inpath + style + ".jpg"):
				bg = Image.open(inpath + style + ".jpg")
			bg_w, bg_h = bg.size
			img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
			for i in range(0, width, bg_w):
				for j in range(0, height, bg_h):
					img.paste(bg, (i, j))
		elif config.plugins.KravenHD.BackgroundColor.value == "gradient":
			c1=config.plugins.KravenHD.BackgroundGradientColorPrimary.value
			c2=config.plugins.KravenHD.BackgroundGradientColorSecondary.value
			c1=c1[-6:]
			r1=int(c1[0:2], 16)
			g1=int(c1[2:4], 16)
			b1=int(c1[4:6], 16)
			c2=c2[-6:]
			r2=int(c2[0:2], 16)
			g2=int(c2[2:4], 16)
			b2=int(c2[4:6], 16)
			if c1!=c2:
				img = Image.new("RGBA", (1, height))
				for pos in range(0, height):
					p=pos/float(height)
					r=r2*p+r1*(1-p)
					g=g2*p+g1*(1-p)
					b=b2*p+b1*(1-p)
					img.putpixel((0, pos), (int(r), int(g), int(b), 255))
				img = img.resize((width, height))
			else:
				img = Image.new("RGBA", (width, height), (int(r1), int(g1), int(b1), 255))
		else:
			c=self.skincolorbackgroundcolor
			c=c[-6:]
			r=int(c[0:2], 16)
			g=int(c[2:4], 16)
			b=int(c[4:6], 16)
			img = Image.new("RGBA", (width, height), (int(r), int(g), int(b), 255))
		
		# infobars
		if config.plugins.KravenHD.IBStyle.value=="grad":
			if config.plugins.KravenHD.InfobarGradientColor.value == "texture":
				style = config.plugins.KravenHD.InfobarTexture.value
				if fileExists(usrpath + style + ".png"):
					bg = Image.open(usrpath + style + ".png")
				elif fileExists(usrpath + style + ".jpg"):
					bg = Image.open(usrpath + style + ".jpg")
				elif fileExists(inpath + style + ".png"):
					bg = Image.open(inpath + style + ".png")
				elif fileExists(inpath + style + ".jpg"):
					bg = Image.open(inpath + style + ".jpg")
				bg_w, bg_h = bg.size
				ib = Image.new("RGBA", (width, gradbarheight), (0, 0, 0, 0))
				for i in range(0, width, bg_w):
					for j in range(0, gradbarheight, bg_h):
						ib.paste(bg, (i, j))
			else:
				c=self.skincolorinfobarcolor
				c=c[-6:]
				r=int(c[0:2], 16)
				g=int(c[2:4], 16)
				b=int(c[4:6], 16)
				ib = Image.new("RGBA", (width, gradbarheight), (int(r), int(g), int(b), 255))
			trans=(255-int(config.plugins.KravenHD.InfobarColorTrans.value, 16))/255.0
			gr = Image.new("L", (1, gradbarheight), int(255*trans))
			for pos in range(0, gradbarheight):
				gr.putpixel((0, pos), int(self.dexpGradient(gradbarheight, 2.0, pos)*trans))
			gr=gr.resize(ib.size)
			img.paste(ib, (0, height-gradbarheight), gr)
			ib=ib.transpose(Image.ROTATE_180)
			gr=gr.transpose(Image.ROTATE_180)
			img.paste(ib, (0, 0), gr)
		else: # config.plugins.KravenHD.IBStyle.value=="box":
			if config.plugins.KravenHD.InfobarBoxColor.value == "texture":
				style = config.plugins.KravenHD.InfobarTexture.value
				if fileExists(usrpath + style + ".png"):
					bg = Image.open(usrpath + style + ".png")
				elif fileExists(usrpath + style + ".jpg"):
					bg = Image.open(usrpath + style + ".jpg")
				elif fileExists(inpath + style + ".png"):
					bg = Image.open(inpath + style + ".png")
				elif fileExists(inpath + style + ".jpg"):
					bg = Image.open(inpath + style + ".jpg")
				bg_w, bg_h = bg.size
				ib = Image.new("RGBA", (width, boxbarheight), (0, 0, 0, 0))
				for i in range(0, width, bg_w):
					for j in range(0, boxbarheight, bg_h):
						ib.paste(bg, (i, j))
				img.paste(ib, (0, 0))
				img.paste(ib, (0, height-boxbarheight))
			elif config.plugins.KravenHD.InfobarBoxColor.value == "gradient":
				c1=config.plugins.KravenHD.InfobarGradientColorPrimary.value
				c2=config.plugins.KravenHD.InfobarGradientColorSecondary.value
				c1=c1[-6:]
				r1=int(c1[0:2], 16)
				g1=int(c1[2:4], 16)
				b1=int(c1[4:6], 16)
				c2=c2[-6:]
				r2=int(c2[0:2], 16)
				g2=int(c2[2:4], 16)
				b2=int(c2[4:6], 16)
				if c1!=c2:
					ib = Image.new("RGBA", (1, boxbarheight))
					for pos in range(0, boxbarheight):
						p=pos/float(boxbarheight)
						r=r2*p+r1*(1-p)
						g=g2*p+g1*(1-p)
						b=b2*p+b1*(1-p)
						ib.putpixel((0, pos), (int(r), int(g), int(b), 255))
					ib=ib.resize((width, boxbarheight))
					img.paste(ib, (0, height-boxbarheight))
					ib=ib.transpose(Image.ROTATE_180)
					img.paste(ib, (0, 0))
				else:
					ib = Image.new("RGBA", (width, boxbarheight), (int(r1), int(g1), int(b1), 255))
					img.paste(ib, (0, 0))
					img.paste(ib, (0, height-boxbarheight))
			else:
				c=self.skincolorinfobarcolor
				c=c[-6:]
				r=int(c[0:2], 16)
				g=int(c[2:4], 16)
				b=int(c[4:6], 16)
				ib = Image.new("RGBA", (width, boxbarheight), (int(r), int(g), int(b), 255))
				img.paste(ib, (0, 0))
				img.paste(ib, (0, height-boxbarheight))
			c=config.plugins.KravenHD.IBLine.value
			c=c[-6:]
			r=int(c[0:2], 16)
			g=int(c[2:4], 16)
			b=int(c[4:6], 16)
			img.paste((int(r), int(g), int(b), 255), (0, boxbarheight, width, boxbarheight+lineheight))
			img.paste((int(r), int(g), int(b), 255), (0, height-boxbarheight-lineheight, width, height-boxbarheight))
				
		img.save("/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/images/preview.jpg")

	def makeIBGradTexturepng(self):
		self.makeIbarTextureGradientpng(config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarColorTrans.value) # ibars
		self.makeRectTexturepng(config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarColorTrans.value, 906, 170, "shift") # timeshift bar
		self.makeRectTexturepng(config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarColorTrans.value, 400, 200, "wsmall") # weather small
		if config.plugins.KravenHD.SystemInfo.value == "systeminfo-small":
			self.makeRectTexturepng(config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarColorTrans.value, 400, 185, "info") # sysinfo small
		elif config.plugins.KravenHD.SystemInfo.value == "systeminfo-big":
			self.makeRectTexturepng(config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarColorTrans.value, 400, 275, "info") # sysinfo big
		else:
			self.makeRectTexturepng(config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarColorTrans.value, 400, 375, "info") # sysinfo bigsat

	def makeIBGradColorpng(self):
		self.makeIbarColorGradientpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value) # ibars
		self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 906, 170, "shift") # timeshift bar
		self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 200, "wsmall") # weather small
		if config.plugins.KravenHD.SystemInfo.value == "systeminfo-small":
			self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 185, "info") # sysinfo small
		elif config.plugins.KravenHD.SystemInfo.value == "systeminfo-big":
			self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 275, "info") # sysinfo big
		else:
			self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenHD.InfobarColorTrans.value, 400, 375, "info") # sysinfo bigsat

	def makeIbarColorGradientpng(self, newcolor, newtrans):
		width = int(1280 * self.factor) # width of the png file
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder
		ibarheight = int(310 * self.factor) # height of ibar
		ibargradientstart = int(50 * self.factor) # start of ibar gradient (from top)
		ibargradientsize = int(100 * self.factor) # size of ibar gradient
		ibaroheight = int(165 * self.factor) # height of ibaro
		ibarogradientstart = int(65 * self.factor) # start of ibaro gradient (from top)
		ibarogradientsize = int(100 * self.factor) # size of ibaro gradient
		ibaro2height = int(110 * self.factor) # height of ibaro2
		ibaro2gradientstart = int(20 * self.factor) # start of ibaro2 gradient (from top)
		ibaro2gradientsize = int(90 * self.factor) # size of ibaro2 gradient
		ibaro3height = int(145 * self.factor) # height of ibaro3
		ibaro3gradientstart = int(45 * self.factor) # start of ibaro3 gradient (from top)
		ibaro3gradientsize = int(100 * self.factor) # size of ibaro3 gradient
		trans = (255-int(newtrans, 16))/255.0

		newcolor = newcolor[-6:]
		r = int(newcolor[0:2], 16)
		g = int(newcolor[2:4], 16)
		b = int(newcolor[4:6], 16)

		img = Image.new("RGBA", (width, ibarheight), (r, g, b, 0))
		gradient = Image.new("L", (1, ibarheight), int(255*trans))
		for pos in range(0, ibargradientstart):
			gradient.putpixel((0, pos), 0)
		for pos in range(0, ibargradientsize):
			gradient.putpixel((0, ibargradientstart+pos), int(self.dexpGradient(ibargradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibar.png")

		img = Image.new("RGBA", (width, ibaroheight), (r, g, b, 0))
		gradient = Image.new("L", (1, ibaroheight), 0)
		for pos in range(0, ibarogradientstart):
			gradient.putpixel((0, pos), int(255*trans))
		for pos in range(0, ibarogradientsize):
			gradient.putpixel((0, ibarogradientstart+ibarogradientsize-pos-1), int(self.dexpGradient(ibarogradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibaro.png")

		img = Image.new("RGBA", (width, ibaro2height), (r, g, b, 0))
		gradient = Image.new("L", (1, ibaro2height), 0)
		for pos in range(0, ibaro2gradientstart):
			gradient.putpixel((0, pos), int(255*trans))
		for pos in range(0, ibaro2gradientsize):
			gradient.putpixel((0, ibaro2gradientstart+ibaro2gradientsize-pos-1), int(self.dexpGradient(ibaro2gradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibaro2.png")

		img = Image.new("RGBA", (width, ibaro3height), (r, g, b, 0))
		gradient = Image.new("L", (1, ibaro3height), 0)
		for pos in range(0, ibaro3gradientstart):
			gradient.putpixel((0, pos), int(255*trans))
		for pos in range(0, ibaro3gradientsize):
			gradient.putpixel((0, ibaro3gradientstart+ibaro3gradientsize-pos-1), int(self.dexpGradient(ibaro3gradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibaro3.png")

	def makeIbarTextureGradientpng(self, style, trans):
		width = int(1280 * self.factor) # width of the png file
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder
		ibarheight = int(310 * self.factor) # height of ibar
		ibargradientstart = int(50 * self.factor) # start of ibar gradient (from top)
		ibargradientsize = int(100 * self.factor) # size of ibar gradient
		ibaroheight = int(165 * self.factor) # height of ibaro
		ibarogradientstart = int(65 * self.factor) # start of ibaro gradient (from top)
		ibarogradientsize = int(100 * self.factor) # size of ibaro gradient
		ibaro2height = int(110 * self.factor) # height of ibaro2
		ibaro2gradientstart = int(20 * self.factor) # start of ibaro2 gradient (from top)
		ibaro2gradientsize = int(90 * self.factor) # size of ibaro2 gradient
		ibaro3height = int(145 * self.factor) # height of ibaro3
		ibaro3gradientstart = int(45 * self.factor) # start of ibaro3 gradient (from top)
		ibaro3gradientsize = int(100 * self.factor) # size of ibaro3 gradient
		trans = (255-int(trans, 16))/255.0

		inpath = "/usr/share/enigma2/KravenHD/textures/"
		usrpath = "/usr/share/enigma2/Kraven-user-icons/"

		if fileExists(usrpath + style + ".png"):
			bg = Image.open(usrpath + style + ".png")
		elif fileExists(usrpath + style + ".jpg"):
			bg = Image.open(usrpath + style + ".jpg")
		elif fileExists(inpath + style + ".png"):
			bg = Image.open(inpath + style + ".png")
		elif fileExists(inpath + style + ".jpg"):
			bg = Image.open(inpath + style + ".jpg")
		bg_w, bg_h = bg.size

		img = Image.new("RGBA", (width, ibarheight), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, ibarheight, bg_h):
				img.paste(bg, (i, j))
		gradient = Image.new("L", (1, ibarheight), int(255*trans))
		for pos in range(0, ibargradientstart):
			gradient.putpixel((0, pos), 0)
		for pos in range(0, ibargradientsize):
			gradient.putpixel((0, ibargradientstart+pos), int(self.dexpGradient(ibargradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibar.png")

		img = Image.new("RGBA", (width, ibaroheight), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, ibaroheight, bg_h):
				img.paste(bg, (i, j))
		gradient = Image.new("L", (1, ibaroheight), 0)
		for pos in range(0, ibarogradientstart):
			gradient.putpixel((0, pos), int(255*trans))
		for pos in range(0, ibarogradientsize):
			gradient.putpixel((0, ibarogradientstart+ibarogradientsize-pos-1), int(self.dexpGradient(ibarogradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibaro.png")

		img = Image.new("RGBA", (width, ibaro2height), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, ibaroheight, bg_h):
				img.paste(bg, (i, j))
		gradient = Image.new("L", (1, ibaro2height), 0)
		for pos in range(0, ibaro2gradientstart):
			gradient.putpixel((0, pos), int(255*trans))
		for pos in range(0, ibaro2gradientsize):
			gradient.putpixel((0, ibaro2gradientstart+ibaro2gradientsize-pos-1), int(self.dexpGradient(ibaro2gradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibaro2.png")

		img = Image.new("RGBA", (width, ibaro3height), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, ibaroheight, bg_h):
				img.paste(bg, (i, j))
		gradient = Image.new("L", (1, ibaro3height), 0)
		for pos in range(0, ibaro3gradientstart):
			gradient.putpixel((0, pos), int(255*trans))
		for pos in range(0, ibaro3gradientsize):
			gradient.putpixel((0, ibaro3gradientstart+ibaro3gradientsize-pos-1), int(self.dexpGradient(ibaro3gradientsize, gradientspeed, pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save(self.graphics + "ibaro3.png")

	def makeRectColorpng(self, newcolor, newtrans, width, height, pngname):
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder
		gradientsize = int(80 * self.factor) # size of gradient
		width = int(width * self.factor)
		height = int(height * self.factor)
		trans = (255-int(newtrans, 16))/255.0

		newcolor = newcolor[-6:]
		r = int(newcolor[0:2], 16)
		g = int(newcolor[2:4], 16)
		b = int(newcolor[4:6], 16)

		img = Image.new("RGBA", (width, height), (r, g, b, int(255*trans)))
		gradient = Image.new("RGBA", (1, gradientsize), (r, g, b, 0))
		for pos in range(0, gradientsize):
			gradient.putpixel((0, pos), (r, g, b, int((self.dexpGradient(gradientsize, gradientspeed, pos))*trans)))

		hgradient = gradient.resize((width-2*gradientsize, gradientsize))
		img.paste(hgradient, (gradientsize, 0, width-gradientsize, gradientsize))
		hgradient = hgradient.transpose(Image.ROTATE_180)
		img.paste(hgradient, (gradientsize, height-gradientsize, width-gradientsize, height))

		vgradient = gradient.transpose(Image.ROTATE_90)
		vgradient = vgradient.resize((gradientsize, height-2*gradientsize))
		img.paste(vgradient, (0, gradientsize, gradientsize, height-gradientsize))
		vgradient = vgradient.transpose(Image.ROTATE_180)
		img.paste(vgradient, (width-gradientsize, gradientsize, width, height-gradientsize))

		corner = Image.new("RGBA", (gradientsize, gradientsize), (r, g, b, 0))
		for xpos in range(0, gradientsize):
			for ypos in range(0, gradientsize):
				dist = int(round((xpos**2+ypos**2)**0.503))
				corner.putpixel((xpos, ypos), (r, g, b, int((self.dexpGradient(gradientsize, gradientspeed, gradientsize-dist-1))*trans)))
		corner = corner.filter(ImageFilter.BLUR)
		img.paste(corner, (width-gradientsize, height-gradientsize, width, height))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (width-gradientsize, 0, width, gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (0, 0, gradientsize, gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (0, height-gradientsize, gradientsize, height))
		img.save(self.graphics + pngname + ".png")

	def makeRectTexturepng(self, style, trans, width, height, pngname):
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder
		gradientsize = int(80 * self.factor) # size of gradient
		width = int(width * self.factor)
		height = int(height * self.factor)
		trans = (255 - int(trans, 16)) / 255.0

		inpath = "/usr/share/enigma2/KravenHD/textures/"
		usrpath = "/usr/share/enigma2/Kraven-user-icons/"

		if fileExists(usrpath + style + ".png"):
			bg = Image.open(usrpath + style + ".png")
		elif fileExists(usrpath + style + ".jpg"):
			bg = Image.open(usrpath + style + ".jpg")
		elif fileExists(inpath + style + ".png"):
			bg = Image.open(inpath + style + ".png")
		elif fileExists(inpath + style + ".jpg"):
			bg = Image.open(inpath + style + ".jpg")
		bg_w, bg_h = bg.size
		img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, height, bg_h):
				img.paste(bg, (i, j))

		mask = Image.new("L", (width, height), 255 * trans)
		gradient = Image.new("L", (1, gradientsize), 0)
		for pos in range(0, gradientsize):
			gradient.putpixel((0, pos), int((self.dexpGradient(gradientsize, gradientspeed, pos)) * trans))

		hgradient = gradient.resize((width - 2 * gradientsize, gradientsize))
		mask.paste(hgradient, (gradientsize, 0, width - gradientsize, gradientsize))
		hgradient = hgradient.transpose(Image.ROTATE_180)
		mask.paste(hgradient, (gradientsize, height - gradientsize, width - gradientsize, height))

		vgradient = gradient.transpose(Image.ROTATE_90)
		vgradient = vgradient.resize((gradientsize, height - 2 * gradientsize))
		mask.paste(vgradient, (0, gradientsize, gradientsize, height - gradientsize))
		vgradient = vgradient.transpose(Image.ROTATE_180)
		mask.paste(vgradient, (width - gradientsize, gradientsize, width, height - gradientsize))

		corner = Image.new("L", (gradientsize, gradientsize), 0)
		for xpos in range(0, gradientsize):
			for ypos in range(0, gradientsize):
				dist = int(round((xpos **2 + ypos **2) **0.503))
				corner.putpixel((xpos, ypos), int((self.dexpGradient(gradientsize, gradientspeed, gradientsize - dist - 1)) * trans))
		corner = corner.filter(ImageFilter.BLUR)
		mask.paste(corner, (width - gradientsize, height - gradientsize, width, height))
		corner = corner.transpose(Image.ROTATE_90)
		mask.paste(corner, (width - gradientsize, 0, width, gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		mask.paste(corner, (0, 0, gradientsize, gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		mask.paste(corner, (0, height - gradientsize, gradientsize, height))
		img.putalpha(mask)
		img.save(self.graphics + pngname + ".png")

	def makeBGGradientpng(self):
		self.makeGradientpng("globalbg", 1280, 720, config.plugins.KravenHD.BackgroundGradientColorPrimary.value, config.plugins.KravenHD.BackgroundGradientColorSecondary.value, config.plugins.KravenHD.BackgroundColorTrans.value)
		self.makeGradientpng("nontransbg", 1280, 720, config.plugins.KravenHD.BackgroundGradientColorPrimary.value, config.plugins.KravenHD.BackgroundGradientColorSecondary.value, "00")
		self.makeGradientpng("channelbg", 1280, 720, config.plugins.KravenHD.BackgroundGradientColorPrimary.value, config.plugins.KravenHD.BackgroundGradientColorSecondary.value, config.plugins.KravenHD.ChannelSelectionTrans.value)

	def makeIBGradientpng(self):
		width = 1280
		#Ibar
		ibarheights=[
			("infobar-style-nopicon", 166),
			("infobar-style-x1", 166),
			("infobar-style-zz1", 198),
			("infobar-style-zz2", 186),
			("infobar-style-zz3", 186),
			("infobar-style-zzz1", 248)
			]
		for pair in ibarheights:
			if config.plugins.KravenHD.InfobarStyle.value == pair[0]:
				self.makeGradientpng("ibar", width, pair[1], config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3"):
			if self.actClockstyle == "clock-android":
				self.makeGradientpng("ibar", width, 154, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
			else:
				self.makeGradientpng("ibar", width, 144, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-z1", "infobar-style-z2"):
			if self.actClockstyle == "clock-android":
				self.makeGradientpng("ibar", width, 154, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
			else:
				self.makeGradientpng("ibar", width, 140, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		self.makeGradientpng("ibar2", width, 64, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		self.makeGradientpng("ibar3", width, 70, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		self.makeGradientpng("ibar4", width, 80, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		self.makeGradientpng("ibar5", width, 110, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		self.makeGradientpng("ibar6", width, 206, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		self.makeGradientpng("ibar7", width, 285, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarColorTrans.value)
		#Ibaro
		ibaroheights=[
			("ibaro", 59),
			("ibaro2", 70),
			("ibaro3", 116),
			("ibaro4", 150)
			]
		for pair in ibaroheights:
			self.makeGradientpng(pair[0], width, pair[1], config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarColorTrans.value)

		#Sysinfo
		if config.plugins.KravenHD.InfoStyle.value == "primary":
			FirstColor=config.plugins.KravenHD.InfobarGradientColorPrimary.value
			SecondColor=config.plugins.KravenHD.InfobarGradientColorPrimary.value
		elif config.plugins.KravenHD.InfoStyle.value == "secondary":
			FirstColor=config.plugins.KravenHD.InfobarGradientColorSecondary.value
			SecondColor=config.plugins.KravenHD.InfobarGradientColorSecondary.value
		else:
			FirstColor=config.plugins.KravenHD.InfobarGradientColorPrimary.value
			SecondColor=config.plugins.KravenHD.InfobarGradientColorSecondary.value
		if config.plugins.KravenHD.SystemInfo.value == "systeminfo-small":
			self.makeGradientpng("info", 300, 80, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)
		elif config.plugins.KravenHD.SystemInfo.value == "systeminfo-big":
			self.makeGradientpng("info", 300, 170, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)
		elif config.plugins.KravenHD.SystemInfo.value == "systeminfo-bigsat":
			self.makeGradientpng("info", 300, 260, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)

		#Timeshift
		self.makeGradientpng("shift", 785, 62, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)

		#InfobarTunerState
		self.makeGradientpng("ibts", 1280, 32, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)

		#AutoResolution
		self.makeGradientpng("autoresolution", 252, 62, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)

		#PVRState
		if config.plugins.KravenHD.PVRState.value == "pvrstate-center-big":
			self.makeGradientpng("pvrstate", 220, 90, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)
		elif config.plugins.KravenHD.PVRState.value in ("pvrstate-center-small", "pvrstate-left-small"):
			self.makeGradientpng("pvrstate", 110, 45, FirstColor, SecondColor, config.plugins.KravenHD.InfobarColorTrans.value)

		#Weather-small
		if self.actWeatherstyle == "weather-small":
			self.makeGradientpng("wsmall", 300, 120, config.plugins.KravenHD.InfobarGradientColorSecondary.value, config.plugins.KravenHD.InfobarGradientColorPrimary.value, config.plugins.KravenHD.InfobarColorTrans.value)

	def makeSELGradientpng(self):
		self.makeGradientpng("sel_30", 1220, 30, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_36", 1196, 36, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_40", 870, 40, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_45", 747, 45, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_50", 765, 50, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_53", 736, 54, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_60", 747, 60, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_70", 765, 70, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_75", 736, 75, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_90", 870, 90, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_110", 736, 110, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		self.makeGradientpng("sel_135", 736, 136, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
		if config.plugins.KravenHD.EMCSelectionColors.value == "global":
			if config.plugins.KravenHD.EMCStyle.value in ("emc-verybigcover", "emc-verybigcover2"):
				self.makeGradientpng("sel_28", 777, 28, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
			else:
				self.makeGradientpng("sel_32", 1196, 32, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")

	def makeGradientpng(self, name, width, height, color1, color2, trans):
		width = int(width * self.factor)
		height = int(height * self.factor)
		trans = 255 - int(trans, 16)

		color1 = color1[-6:]
		r1 = int(color1[0:2], 16)
		g1 = int(color1[2:4], 16)
		b1 = int(color1[4:6], 16)
		color2 = color2[-6:]
		r2 = int(color2[0:2], 16)
		g2 = int(color2[2:4], 16)
		b2 = int(color2[4:6], 16)

		gradient = Image.new("RGBA", (1, height), (r2, g2, b2, trans))
		for pos in range(0, height):
			p = pos / float(height)
			r = r2 * p + r1 * (1 - p)
			g = g2 * p + g1 * (1 - p)
			b = b2 * p + b1 * (1 - p)
			gradient.putpixel((0, pos), (int(r), int(g), int(b), int(trans)))
		gradient = gradient.resize((width, height))
		gradient.save(self.graphics + name + ".png")

	def makeBGTexturepng(self):
		self.makeTexturepng("globalbg", 1280, 720, config.plugins.KravenHD.BackgroundTexture.value, config.plugins.KravenHD.BackgroundColorTrans.value)
		self.makeTexturepng("nontransbg", 1280, 720, config.plugins.KravenHD.BackgroundTexture.value, "00")
		self.makeTexturepng("channelbg", 1280, 720, config.plugins.KravenHD.BackgroundTexture.value, config.plugins.KravenHD.ChannelSelectionTrans.value)

	def makeIBTexturepng(self):
		self.makeTexturepng("ibtexture", 1280, 720, config.plugins.KravenHD.InfobarTexture.value, config.plugins.KravenHD.InfobarColorTrans.value)

	def makeTexturepng(self, name, width, height, style, trans):
		width = int(width * self.factor)
		height = int(height * self.factor)
		trans = 255 - int(trans, 16)

		path = "/usr/share/enigma2/KravenHD/textures/"
		usrpath = "/usr/share/enigma2/Kraven-user-icons/"

		if fileExists(usrpath + style + ".png"):
			bg = Image.open(usrpath + style + ".png")
		elif fileExists(usrpath + style + ".jpg"):
			bg = Image.open(usrpath + style + ".jpg")
		elif fileExists(path + style + ".png"):
			bg = Image.open(path + style + ".png")
		elif fileExists(path + style + ".jpg"):
			bg = Image.open(path + style + ".jpg")
		bg_w, bg_h = bg.size
		image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
		for i in range(0, width, bg_w):
			for j in range(0, height, bg_h):
				image.paste(bg, (i, j))
		alpha = Image.new("L", (width, height), trans)
		image.putalpha(alpha)
		image.save(self.graphics + name + ".png")

	def makebsWindowpng(self):
		addition = ""
		border = None
		if config.plugins.KravenHD.PopupStyle.value == "popup-grad-trans":
			addition = "_gr_tr"
			border = None
		elif config.plugins.KravenHD.PopupStyle.value == "popup-grad":
			addition = "_gr"
			border = None
		elif config.plugins.KravenHD.PopupStyle.value == "popup-box-trans":
			addition = "_bx_tr"
			border = config.plugins.KravenHD.Border.value
		elif config.plugins.KravenHD.PopupStyle.value == "popup-box":
			addition = "_bx"
			border = config.plugins.KravenHD.Border.value

		self.changeColor("bs_b" + addition, "bs_b", self.skincolorbackgroundcolor, border)
		self.changeColor("bs_bl" + addition, "bs_bl", self.skincolorbackgroundcolor, border)
		self.changeColor("bs_br" + addition, "bs_br", self.skincolorbackgroundcolor, border)
		self.changeColor("bs_l" + addition, "bs_l", self.skincolorbackgroundcolor, border)
		self.changeColor("bs_r" + addition, "bs_r", self.skincolorbackgroundcolor, border)
		self.changeColor("bs_t" + addition, "bs_t", self.skincolorbackgroundcolor, border)
		self.changeColor("bs_tl" + addition, "bs_tl", self.skincolorbackgroundcolor, border)
		self.changeColor("bs_tr" + addition, "bs_tr", self.skincolorbackgroundcolor, border)

	def makeHorMenupng(self, color1, color2):
		width = int(192 * self.factor)
		height = int(92 * self.factor)
		radius = int(10 * self.factor)
		gradientsize = int(24 * self.factor)
		trans = 230

		color1 = color1[-6:]
		r1 = int(color1[0:2], 16)
		g1 = int(color1[2:4], 16)
		b1 = int(color1[4:6], 16)
		color2 = color2[-6:]
		r2 = int(color2[0:2], 16)
		g2 = int(color2[2:4], 16)
		b2 = int(color2[4:6], 16)

		mask = Image.new("L", (width, height), trans)
		corner = Image.new('L', (radius, radius), 0)
		draw = ImageDraw.Draw(corner)
		draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, trans)
		mask.paste(corner, (0, 0))
		mask.paste(corner.transpose(Image.FLIP_LEFT_RIGHT), (width - radius, 0))
		mask.paste(corner.transpose(Image.ROTATE_180), (width - radius, height - radius))
		mask.paste(corner.transpose(Image.FLIP_TOP_BOTTOM), (0, height - radius))

		if six.PY2:
			gradient = Image.new("RGBA", (1, height / 2), (r2, g2, b2, trans))
		else:
			gradient = Image.new("RGBA", (1, int(height / 2)), (r2, g2, b2, trans))
		for pos in range(0, gradientsize):
			p = pos / float(gradientsize)
			r = r2 * p + r1 * (1 - p)
			g = g2 * p + g1 * (1 - p)
			b = b2 * p + b1 * (1 - p)
			gradient.putpixel((0, pos), (int(r), int(g), int(b), trans))
		if six.PY2:
			gradient = gradient.resize((width, height / 2))
		else:
			gradient = gradient.resize((width, int(height / 2)))

		img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
		img.paste(gradient, (0, 0))
		if six.PY2:
			img.paste(gradient.transpose(Image.FLIP_TOP_BOTTOM), (0, height / 2))
		else:
			img.paste(gradient.transpose(Image.FLIP_TOP_BOTTOM), (0, int(height / 2)))
		img.putalpha(mask)
		img.save("/usr/share/enigma2/KravenHD/buttons/icon1.png")

	def makeProgressBackground(self, width, color, output):
		height = int(21 * self.factor)
		width = int(width * self.factor)

		color = color[-6:]
		r1 = int(color[0:2], 16)
		g1 = int(color[2:4], 16)
		b1 = int(color[4:6], 16)

		img = Image.open(self.templates + "progress_bg_m.png")
		img = img.resize((width, height))
		side = Image.open(self.templates + "progress_bg_s.png")
		img.paste(side, (0, 0))
		img.paste(side.transpose(Image.FLIP_LEFT_RIGHT), (width - int(10 * self.factor), 0))

		pixels = img.load()
		for x in range(width):
			for y in range(height):
				r, g, b, a = pixels[x, y]
				if (r, g, b) == (0, 0, 0):
					pixels[x, y] = (r1, g1, b1, a)
		img.save(self.graphics + output + ".png")

	def changeColor(self, input, output, color1, color2):
		img = Image.open(self.templates + input + ".png")

		color1 = color1[-6:]
		r1 = int(color1[0:2], 16)
		g1 = int(color1[2:4], 16)
		b1 = int(color1[4:6], 16)

		pixels = img.load()
		for x in range(img.size[0]):
			for y in range(img.size[1]):
				r, g, b, a = pixels[x, y]
				if (r, g, b) == (0, 0, 0):
					pixels[x, y] = (r1, g1, b1, a)
				if color2 is not None:
					color2 = color2[-6:]
					r2 = int(color2[0:2], 16)
					g2 = int(color2[2:4], 16)
					b2 = int(color2[4:6], 16)
					if (r, g, b) == (254, 254, 254):
						pixels[x, y] = (r2, g2, b2, a)
		img.save(self.graphics + output + ".png")

	def makeborsetpng(self, color):
		color = color[-6:]
		r = int(color[0:2], 16)
		g = int(color[2:4], 16)
		b = int(color[4:6], 16)

		img = Image.new("RGBA", (2, 2), (r, g, b, 255))
		img.save(self.graphics + "borset.png")

	def dexpGradient(self, len, spd, pos):
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

	def calcBrightness(self, color, factor):
		f = int(int(factor)*25.5-255)
		color = color[-6:]
		r = int(color[0:2], 16)+f
		g = int(color[2:4], 16)+f
		b = int(color[4:6], 16)+f
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

	def calcTransparency(self, trans1, trans2):
		t1 = int(trans1, 16)
		t2 = int(trans2, 16)
		return str(hex(min(t1, t2))[2:4]).zfill(2)

	def hexRGB(self, color):
		color = color[-6:]
		r = int(color[0:2], 16)
		g = int(color[2:4], 16)
		b = int(color[4:6], 16)
		return (r<<16)|(g<<8)|b

	def RGB(self, r, g, b):
		return (r<<16)|(g<<8)|b

	def get_weather_data(self):
			self.city = ''
			self.lat = ''
			self.lon = ''
			self.accu_id = ''
			self.gm_code = ''
			self.preview_text = ''
			self.preview_warning = ''

			if config.plugins.KravenHD.weather_search_over.value == 'ip':
				self.get_accu_by_ip()
			elif config.plugins.KravenHD.weather_search_over.value == 'name':
				self.get_accu_by_name()

			self.actCity=self.preview_text+self.preview_warning

	def get_accu_by_ip(self):

		if self.InternetAvailable==False: 
			return

		try:
			res = requests.get('http://ip-api.com/json/?lang=de&fields=status,city', timeout=1)
			data = res.json()

			if data['status'] == 'success':
				city = data['city']
				apikey = config.plugins.KravenHD.weather_accu_apikey.value
				language = config.plugins.KravenHD.weather_language.value
				res1 = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search?q=%s&apikey=%s&language=%s' % (str(city), str(apikey), str(language)), timeout=1)
				data1 = res1.json()

				if 'Code' in data1:
					if data1['Code'] == 'ServiceUnavailable':
						self.preview_warning = _('API requests exceeded')
					elif data1['Code'] == 'Unauthorized':
						self.preview_warning = _('API authorization failed')
				else:
					self.accu_id = data1[0]['Key']
					self.city = data1[0]['LocalizedName']
					self.lat = data1[0]['GeoPosition']['Latitude']
					self.lon = data1[0]['GeoPosition']['Longitude']
					self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
					config.plugins.KravenHD.weather_accu_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenHD.weather_language.value))
					config.plugins.KravenHD.weather_accu_latlon.save()
					config.plugins.KravenHD.weather_accu_id.value = str(self.accu_id)
					config.plugins.KravenHD.weather_accu_id.save()
					config.plugins.KravenHD.weather_foundcity.value = str(self.city)
					config.plugins.KravenHD.weather_foundcity.save()
			else:
				self.preview_text = _('No data for IP')
		except:
			self.preview_warning = _('No Accu ID found')

	def get_accu_by_name(self):

		if self.InternetAvailable==False: 
			return

		try:
			city = config.plugins.KravenHD.weather_cityname.getValue()
			apikey = config.plugins.KravenHD.weather_accu_apikey.value
			language = config.plugins.KravenHD.weather_language.value

			res = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search?q=%s&apikey=%s&language=%s' % (str(city), str(apikey), str(language)), timeout=1)
			data = res.json()

			if 'Code' in data:
				if data['Code'] == 'ServiceUnavailable':
					self.preview_warning = _('API requests exceeded')
				elif data['Code'] == 'Unauthorized':
					self.preview_warning = _('API authorization failed')
			else:
				self.accu_id = data[0]['Key']
				self.city = data[0]['LocalizedName']
				self.lat = data[0]['GeoPosition']['Latitude']
				self.lon = data[0]['GeoPosition']['Longitude']
				self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
				config.plugins.KravenHD.weather_accu_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenHD.weather_language.value))
				config.plugins.KravenHD.weather_accu_latlon.save()
				config.plugins.KravenHD.weather_accu_id.value = str(self.accu_id)
				config.plugins.KravenHD.weather_accu_id.save()
				config.plugins.KravenHD.weather_foundcity.value = str(self.city)
				config.plugins.KravenHD.weather_foundcity.save()
		except:
			self.preview_warning = _('No Accu ID found')
