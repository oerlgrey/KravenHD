# -*- coding: utf-8 -*-

#  Activate Skin Settings Code
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
from __future__ import print_function
from copy import deepcopy
from Components.config import config, configfile, getConfigListEntry, ConfigYesNo, ConfigSubsection, ConfigSelection, ConfigText, ConfigClock, ConfigSlider
from Components.SystemInfo import SystemInfo
from PIL import Image, ImageFilter, ImageDraw
from Components.PluginComponent import plugins
from shutil import move
from os import remove, system, popen, path
import time, subprocess
from Tools.Directories import fileExists
from six.moves import range

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

config.plugins.KravenHD.CustomWeatherIcons = ConfigSelection(default="none", choices = [
				("on", _("on")),
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

config.plugins.KravenHD.msn_language = ConfigSelection(default="de-DE", choices = [
				("de-DE", _("Deutsch")),
				("en-US", _("English")),
				("ru-RU", _("Russian")),
				("it-IT", _("Italian")),
				("es-ES", _("Spanish")),
				("uk-UA", _("Ukrainian")),
				("pt-PT", _("Portuguese")),
				("ro-RO", _("Romanian")),
				("pl-PL", _("Polish")),
				("fi-FI", _("Finnish")),
				("nl-NL", _("Dutch")),
				("fr-FR", _("French")),
				("bg-BG", _("Bulgarian")),
				("sv-SE", _("Swedish")),
				("tr-TR", _("Turkish")),
				("hr-HR", _("Croatian")),
				("ca-AD", _("Catalan")),
				("sk-SK", _("Slovak"))
				])

config.plugins.KravenHD.msn_searchby = ConfigSelection(default="auto-ip", choices = [
				("auto-ip", _("IP")),
				("location", _("Enter location manually"))
				])

SearchResultList = []
config.plugins.KravenHD.msn_list = ConfigSelection(default = "", choices = SearchResultList)

config.plugins.KravenHD.msn_cityfound = ConfigText(default = "")
config.plugins.KravenHD.msn_cityname = ConfigText(default = "")
config.plugins.KravenHD.msn_code = ConfigText(default = "")

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

config.plugins.KravenHD.PosterView = ConfigSelection(default="none", choices = [
				("on", _("on")),
				("none", _("off"))
				])

config.plugins.KravenHD.OnlineInfo = ConfigSelection(default="none", choices = [
				("on", _("on")),
				("none", _("off"))
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

class ActivateSkinSettings:

	def __init__(self):
		self.datei = "/usr/share/enigma2/KravenHD/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		if config.plugins.KravenHD.SkinResolution.value == "hd":
			self.data = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/"
			self.templates = "/usr/share/enigma2/KravenHD/templates/hd/"
			self.factor = 1
		else:
			self.data = "/usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/"
			self.templates = "/usr/share/enigma2/KravenHD/templates/fhd/"
			self.factor = 1.5
		self.graphics = "/usr/share/enigma2/KravenHD/graphics/"
		self.profiles = "/etc/enigma2/"
		self.BoxName=self.getBoxName()
		self.Tuners=self.getTuners()
		self.InternetAvailable=self.getInternetAvailable()

	def WriteSkin(self, silent=False):
		#silent = True  -> returned 0 or 1 (no gui mode)
		#silent = False -> returned some optional code for messages or another things in gui mode

		#error codes for silent mode 
		#0:"No Error"
		#1:"Error occurred"

		self.silent = silent

		if self.silent:
			if config.skin.primary_skin.value != "KravenHD/skin.xml":
				print('KravenHD is not the primary skin. No restore action needed!')
				return 0
			self.E2settings = open("/etc/enigma2/settings", "r").read()
		return self.save()

	def calcBackgrounds(self, bg = None):

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

		if bg == 'background':
			return self.skincolorbackgroundcolor
		elif bg == 'infobar':
			return self.skincolorinfobarcolor

	def save(self):
		#refresh internet
		if not self.silent:
			self.InternetAvailable=self.getInternetAvailable()

		#clock
		self.actClockstyle="none"
		if self.InternetAvailable:
			self.actClockstyle=config.plugins.KravenHD.ClockStyle.value
		else:
			self.actClockstyle=config.plugins.KravenHD.ClockStyleNoInternet.value

		#weather
		self.actWeatherstyle="none"
		if self.InternetAvailable:
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-nopicon", "infobar-style-x1", "infobar-style-x3", "infobar-style-z2", "infobar-style-zz1", "infobar-style-zz2", "infobar-style-zz3", "infobar-style-zzz1"):
				self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle.value
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-z1"):
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
					self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle3.value
				else:
					self.actWeatherstyle=config.plugins.KravenHD.WeatherStyle2.value

		#channelselection
		self.actChannelselectionstyle="none"
		if SystemInfo.get("NumVideoDecoders", 1) > 1:
			self.actChannelselectionstyle=config.plugins.KravenHD.ChannelSelectionStyle2.value
		else:
			self.actChannelselectionstyle=config.plugins.KravenHD.ChannelSelectionStyle.value

		#menu
		self.actMenustyle="none"
		if self.InternetAvailable:
			self.actMenustyle=config.plugins.KravenHD.Logo.value
		else:
			self.actMenustyle=config.plugins.KravenHD.LogoNoInternet.value

		### Calculate Backgrounds
		self.calcBackgrounds()

		self.skin_lines = []
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
				if config.plugins.KravenHD.SkinResolution.value == "hd":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/share.tar.gz -C /usr/share/enigma2/KravenHD/")
					print("KravenPlugin: HD graphics now installed")
				else:
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/share.tar.gz -C /usr/share/enigma2/KravenHD/")
					print("KravenPlugin: FHD graphics now installed")
			else:
				print("KravenPlugin: No need to install other graphics")

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
			if config.plugins.KravenHD.IBFontSize.value == "small":
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
			elif config.plugins.KravenHD.IBFontSize.value == "middle":
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

		if config.plugins.KravenHD.SkinResolution.value == "hd":
			if config.plugins.KravenHD.IconStyle2.value == "icons-light2":
				system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/icons-white.tar.gz -C /usr/share/enigma2/KravenHD/")
			else:
				system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/icons-black.tar.gz -C /usr/share/enigma2/KravenHD/")
		else:
			if config.plugins.KravenHD.IconStyle2.value == "icons-light2":
				system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/icons-white.tar.gz -C /usr/share/enigma2/KravenHD/")
			else:
				system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/icons-black.tar.gz -C /usr/share/enigma2/KravenHD/")

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
			if not self.silent:
				# ChannelSelection
				CSitems = config.usage.serviceitems_per_page.value
				CSheight = ""
				CSlines = ""
				self.actCSItemHeight = ""
				if config.usage.servicelist_twolines.value == True:
					CSlines = 2
				else:
					CSlines = 1
				if self.actChannelselectionstyle in ("channelselection-style-nobile-minitv", "channelselection-style-nobile-minitv3", "channelselection-style-nobile-minitv33"):
					CSheight = 348
				elif self.actChannelselectionstyle in ("channelselection-style-nobile", "channelselection-style-nobile2"):
					CSheight = 580
				elif self.actChannelselectionstyle == "channelselection-style-minitv2":
					CSheight = 420
				elif self.actChannelselectionstyle == "channelselection-style-minitv-picon":
					CSheight = 396
				else:
					CSheight = 560
				self.actCSItemHeight = int(((CSheight / CSitems) * CSlines) +1)

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

			else: # if self.silent:
				self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_CS.png"', " "])
				self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_MS.png"', " "])
				self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_ES.png"', " "])
				self.skinSearchAndReplace.append(['selectionPixmap="KravenHD/graphics/sel_ESM.png"', " "])

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

		### Custom Weather Icons
		if config.plugins.KravenHD.CustomWeatherIcons.value == "on" and fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
			self.skinSearchAndReplace.append(["/usr/share/enigma2/KravenHD/WetterIcons/", "/usr/share/enigma2/Kraven-user-icons/"])
		else:
			config.plugins.KravenHD.CustomWeatherIcons.value = "none"
			config.plugins.KravenHD.CustomWeatherIcons.save()

		### Clock Analog Color
		if self.actClockstyle == "clock-analog":
			self.changeColor("analogclock", "analogclock", config.plugins.KravenHD.AnalogColor.value, None)

		### HDF-Radio Icon Color
		self.changeColor("play", "play", config.plugins.KravenHD.Font1.value, None)
		self.changeColor("pause", "pause", config.plugins.KravenHD.Font1.value, None)
		self.changeColor("stop", "stop", config.plugins.KravenHD.Font1.value, None)
		self.changeColor("sorted", "sorted", config.plugins.KravenHD.Font1.value, None)
		self.changeColor("shuffle", "shuffle", config.plugins.KravenHD.Font1.value, None)

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
		if not self.silent:
			config.usage.servicelist_mode.value = "standard"
			config.usage.servicelist_mode.save()
		if not self.silent and (self.actChannelselectionstyle in ("channelselection-style-nopicon", "channelselection-style-nopicon2", "channelselection-style-xpicon", "channelselection-style-zpicon", "channelselection-style-zzpicon", "channelselection-style-zzzpicon", "channelselection-style-minitv3", "channelselection-style-nobile-minitv3") or config.plugins.KravenHD.ChannelSelectionMode.value == "zap"):
			config.usage.servicelistpreview_mode.value = False
		elif not self.silent:
			config.usage.servicelistpreview_mode.value = True
		if not self.silent:
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
			if self.actClockstyle in ("clock-android", "clock-weather") and fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
				self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-' + self.actClockstyle + '_OAWeather"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
			if self.actClockstyle in ("clock-android", "clock-weather") and fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
				self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-x2-x3-z1-z2-' + self.actClockstyle + '_OAWeather"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-x2-x3-z1-z2-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
			if self.actClockstyle in ("clock-android", "clock-weather") and fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
				self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-zz2-zz3-' + self.actClockstyle + '_OAWeather"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-zz2-zz3-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zzz1"):
			if self.actClockstyle in ("clock-android", "clock-weather") and fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
				self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->', '<panel name="infobar-style-zz1-zzz1-' + self.actClockstyle + '_OAWeather"/>'])
			else:
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
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
					self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-small2_OAWeather"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-small2"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', '<panel name="gradient-weather-small"/>'])
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
					self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-small_OAWeather"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-small"/>'])

		elif self.actWeatherstyle == "weather-left":
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
				self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-left_OAWeather"/>'])
			else:
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
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
				self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', '<panel name="weather-big_OAWeather"/>'])
			else:
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

		# show poster
		if config.plugins.KravenHD.PosterView.value == "on":
			if config.plugins.KravenHD.InfobarStyle.value == "infobar-style-nopicon":
				if config.plugins.KravenHD.InfobarChannelName.value == "none":
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-nopicon-poster"/>'])
				elif config.plugins.KravenHD.InfobarChannelName.value in ("infobar-channelname-small", "infobar-channelname-number-small"):
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-nopicon-poster-smallname"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-nopicon-poster-bigname"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-x1":
				if config.plugins.KravenHD.InfobarChannelName.value == "none":
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-x1-poster"/>'])
				elif config.plugins.KravenHD.InfobarChannelName.value in ("infobar-channelname-small", "infobar-channelname-number-small"):
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-x1-poster-smallname"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-x1-poster-bigname"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
				if config.plugins.KravenHD.InfobarChannelName.value == "none":
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-x2-x3-z1-z2-poster"/>'])
				elif config.plugins.KravenHD.InfobarChannelName.value in ("infobar-channelname-small", "infobar-channelname-number-small"):
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-x2-x3-z1-z2-poster-smallname"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-x2-x3-z1-z2-poster-bigname"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zz1":
				if config.plugins.KravenHD.InfobarChannelName.value == "none":
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-zz1-poster"/>'])
				elif config.plugins.KravenHD.InfobarChannelName.value in ("infobar-channelname-small", "infobar-channelname-number-small"):
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-zz1-poster-smallname"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-zz1-poster-bigname"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-zz2-zz3-poster"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value == "infobar-style-zzz1":
				self.skinSearchAndReplace.append(['<!-- Poster view -->', '<panel name="infobar-style-zzz1-poster"/>'])

		# show online info
		if config.plugins.KravenHD.OnlineInfo.value == "on":
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- Online info -->', '<panel name="infobar-style-x2-x3-z1-z2-online"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- Online info -->', '<panel name="infobar-style-zz2-zz3-online"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Online info -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-online"/>'])

		# show online info in SecondInfoBar
		if config.plugins.KravenHD.OnlineInfo.value == "on":
			if config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-x2", "infobar-style-x3", "infobar-style-z1", "infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- SIB Online info -->', '<panel name="infobar-style-x2-x3-z1-z2-sib-online"/>'])
			elif config.plugins.KravenHD.InfobarStyle.value in ("infobar-style-zz2", "infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- SIB Online info -->', '<panel name="infobar-style-zz2-zz3-sib-online"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- SIB Online info -->', '<panel name="' + config.plugins.KravenHD.InfobarStyle.value + '-sib-online"/>'])

		### SecondInfoBar
		if config.plugins.KravenHD.SIB.value in ("sib1", "sib6", "sib7") and fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
			self.skinSearchAndReplace.append(['<!-- SIB style -->', '<panel name="' + config.plugins.KravenHD.SIB.value + '_OAWeather"/>'])
		else:
			self.skinSearchAndReplace.append(['<!-- SIB style -->', '<panel name="' + config.plugins.KravenHD.SIB.value + '"/>'])

		### Players clockstyle
		if config.plugins.KravenHD.PlayerClock.value in ("player-android", "player-weather") and fileExists("/usr/lib/enigma2/python/Plugins/Extensions/OAWeather/plugin.pyc"):
			self.skinSearchAndReplace.append(['<!-- Player clockstyle -->', '<panel name="' + config.plugins.KravenHD.PlayerClock.value + '_OAWeather"/>'])
		else:
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
		if fileExists("/usr/lib/enigma2/python/Components/Converter/MSNWeather.pyc"):
			if config.plugins.KravenHD.IBStyle.value == "grad" or config.plugins.KravenHD.PopupStyle.value in ("popup-grad", "popup-grad-trans"):
				self.changeColor("msnbg_gr", "msnbg", self.skincolorbackgroundcolor, None)
			else:
				self.changeColor("msnbg", "msnbg", self.skincolorbackgroundcolor, None)
			self.appendSkinFile(self.data + "weatherplugin.xml")
			if self.InternetAvailable and not fileExists("/usr/share/enigma2/KravenHD/msn_weather_icons/1.png"):
				system("wget -q http://picons.mynonpublic.com/msn-icon.tar.gz -O /tmp/msn-icon.tar.gz; tar xf /tmp/msn-icon.tar.gz -C /usr/share/enigma2/KravenHD/")
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
		if not self.silent and not config.plugins.KravenHD.NumberZapExt.value == "none":
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
		if not self.silent and config.plugins.KravenHD.GraphicalEPG.value == "text":
			config.epgselection.graph_type_mode.value = False
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = False
			config.epgselection.graph_pig.save()
		elif not self.silent and config.plugins.KravenHD.GraphicalEPG.value == "text-minitv":
			config.epgselection.graph_type_mode.value = False
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = True
			config.epgselection.graph_pig.save()
		elif not self.silent and config.plugins.KravenHD.GraphicalEPG.value == "graphical":
			config.epgselection.graph_type_mode.value = "graphics"
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = False
			config.epgselection.graph_pig.save()
		elif not self.silent and config.plugins.KravenHD.GraphicalEPG.value == "graphical-minitv":
			config.epgselection.graph_type_mode.value = "graphics"
			config.epgselection.graph_type_mode.save()
			config.epgselection.graph_pig.value = True
			config.epgselection.graph_pig.save()

		### MovieSelection
		self.appendSkinFile(self.data + config.plugins.KravenHD.MovieSelection.value + ".xml")

		### bsWindow
		self.makebsWindowpng()

		### VirtualKeyBoard
		if config.plugins.KravenHD.PopupStyle.value == "popup-grad-trans":
			self.changeColor("virtualkeyboard_gr_tr","virtualkeyboard",self.skincolorbackgroundcolor,None)
		elif config.plugins.KravenHD.PopupStyle.value == "popup-grad":
			self.changeColor("virtualkeyboard_gr","virtualkeyboard",self.skincolorbackgroundcolor,None)
		elif config.plugins.KravenHD.PopupStyle.value == "popup-box-trans":
			self.changeColor("virtualkeyboard_bx_tr","virtualkeyboard",self.skincolorbackgroundcolor,config.plugins.KravenHD.Border.value)
		elif config.plugins.KravenHD.PopupStyle.value == "popup-box":
			self.changeColor("virtualkeyboard_bx","virtualkeyboard",self.skincolorbackgroundcolor,config.plugins.KravenHD.Border.value)

		### SerienRecorder
		if config.plugins.KravenHD.SerienRecorder.value == "serienrecorder":
			self.appendSkinFile(self.data + config.plugins.KravenHD.SerienRecorder.value + ".xml")
			self.changeColor("popup_bg", "popup_bg", self.skincolorbackgroundcolor, config.plugins.KravenHD.Border.value)

		### MediaPortal
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py"):
			if config.plugins.KravenHD.SkinResolution.value == "hd":
				if config.plugins.KravenHD.MediaPortal.value == "mediaportal":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/HD/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/")
				else:
					if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/MP_skin.xml"):
						system("rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD")
			else:
				if config.plugins.KravenHD.MediaPortal.value == "mediaportal":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenHD/data/FHD/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/")
				else:
					if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD/MP_skin.xml"):
						system("rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD")

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
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/MP_skin.xml") and config.plugins.KravenHD.MediaPortal.value == "mediaportal" and config.plugins.KravenHD.SkinResolution.value == "hd":
			system("cp /usr/share/enigma2/KravenHD/graphics/bs_* /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenHD/images/")
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD/MP_skin.xml") and config.plugins.KravenHD.MediaPortal.value == "mediaportal" and config.plugins.KravenHD.SkinResolution.value == "fhd":
			system("cp /usr/share/enigma2/KravenHD/graphics/bs_* /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_1080/KravenHD/images/")

		# Thats it
		return 0

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
		print("KravenPlugin: Iconpack on box is "+packinstalled)

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
			print("KravenPlugin: Iconpack on server is "+packonserver)

			# Download an install icon pack, if needed
			if packinstalled != packonserver:
				packname=packonserver
				fullpackname=pathname+packname
				sub=subprocess.Popen("rm -rf /usr/share/enigma2/Kraven-menu-icons/*.*; rm -rf /usr/share/enigma2/Kraven-menu-icons; wget -q "+fullpackname+" -O /tmp/"+packname+"; tar xf /tmp/"+packname+" -C /usr/share/enigma2/", shell=True)
				sub.wait()
				popen("rm /tmp/"+packname)
				print("KravenPlugin: Installed iconpack "+fullpackname)
			else:
				print("KravenPlugin: No need to install other iconpack")

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
		self.makeGradientpng("sel_CS", 765, self.actCSItemHeight, config.plugins.KravenHD.SelectionBackground.value, config.plugins.KravenHD.SelectionBackground2.value, "00")
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

		gradient = Image.new("RGBA", (1, int(height / 2)), (r2, g2, b2, trans))
		for pos in range(0, gradientsize):
			p = pos / float(gradientsize)
			r = r2 * p + r1 * (1 - p)
			g = g2 * p + g1 * (1 - p)
			b = b2 * p + b1 * (1 - p)
			gradient.putpixel((0, pos), (int(r), int(g), int(b), trans))
		gradient = gradient.resize((width, int(height / 2)))

		img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
		img.paste(gradient, (0, 0))
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
