# -*- coding: utf-8 -*-

#  Plugin Code
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

from __future__ import absolute_import
from Plugins.Plugin import PluginDescriptor
from enigma import getDesktop
from Components.Language import language
from os import environ
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from . import KravenHD

from six.moves import reload_module


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

def main(session, **kwargs):
	reload_module(KravenHD)
	try:
		session.open(KravenHD.KravenHD)
	except:
		import traceback
		traceback.print_exc()

def main_menu(menuid):
	if menuid == "system":
		return [("KravenHD", main, _("Configuration tool for KravenHD"), 27)]
	else:
		return []

def Plugins(**kwargs):
	screenwidth = getDesktop(0).size().width()
	list = []
	list.append(PluginDescriptor(name="Setup KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_MENU, fnc = main_menu))
	if screenwidth and screenwidth == 1920:
		list.append(PluginDescriptor(name="KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main))
	else:
		list.append(PluginDescriptor(name="KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main))
	return list
