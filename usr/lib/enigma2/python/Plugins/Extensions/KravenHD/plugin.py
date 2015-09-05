from Plugins.Plugin import PluginDescriptor
from enigma import getDesktop
from Components.Language import language
from os import environ
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
import KravenHD

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
	reload(KravenHD)
	try:
		session.open(KravenHD.KravenHD)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	screenwidth = getDesktop(0).size().width()
	if screenwidth and screenwidth == 1920:
		return [PluginDescriptor(name="KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
	else:
		return [PluginDescriptor(name="KravenHD", description=_("Configuration tool for KravenHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]
