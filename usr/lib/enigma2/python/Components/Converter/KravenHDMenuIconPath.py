#
#  Menu Icon Path Converter
#
#  Coded by tomele for Kraven Skins
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll

class KravenHDMenuIconPath(Poll,Converter,object):
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.poll_interval = 1000
		self.poll_enabled = True
		self.logo = "/usr/share/enigma2/KravenHD/logo.png"
		self.path = "/usr/share/enigma2/Kraven-menu-icons/"
		self.userpath = "/usr/share/enigma2/Kraven-user-icons/"
		self.type = str(type)
		
		self.names=[
		("Inadyn_setup","setup.png"),
		("RecordPaths","hdd.png"),
		("about_screen","info.png"),
		("audio_menu","setup.png"),
		("audio_setup","setup.png"),
		("auto_scan","tuner.png"),
		("autolanguage_setup","setup.png"),
		("autores_setup","service_info.png"),
		("autoshutdown_setup","shutdowntimer.png"),
		("av_setup","movie_list.png"),
		("buttonsetup_setup","setup.png"),
		("cam_setup","camd.png"),
		("channelselection_setup","setup.png"),
		("ci_assign","setup.png"),
		("ci_setup","setup.png"),
		("crontimer_edit","timer.png"),
		("deep_standby","shutdown.png"),
		("default_lists","paket.png"),
		("default_wizard","timezone.png"),
		("device_manager","hdd.png"),
		("device_screen","hdd.png"),
		("device_setup","setup.png"),
		("display_selection","look.png"),
		("display_setup","look.png"),
		("dns_setup","net.png"),
		("dvdplayer","dvd.png"),
		("dvdplayer_setup","dvd.png"),
		("ecm_info","webb.png"),
		("epg_menu","movie_list.png"),
		("epg_setup","movie_list.png"),
		("epgloadsave_menu","movie_list.png"),
		("extended_selection","setup.png"),
		("factory_reset","reset.png"),
		("filecommand","filecom.png"),
		("googlemaps","google.png"),
		("harddisk_check","hdd.png"),
		("harddisk_convert","hdd.png"),
		("harddisk_init","hdd.png"),
		("harddisk_setup","hdd.png"),
		("hardisk_selection","hdd.png"),
		("hdmicec","setup.png"),
		("info_screen","info.png"),
		("infopanel","info.png"),
		("input_device_setup","keyb.png"),
		("keyboard","keyb.png"),
		("keyboard_setup","keyb.png"),
		("language_setup","tuner.png"),
		("lcd4linux","plugin.png"),
		("lcd_setup","setup.png"),
		("lcd_skin_setup","lcd4linux.png"),
		("loadepgcache","setup.png"),
		("logs_setup","setup.png"),
		("manual_scan","tuner.png"),
		("mediaplayer","media.png"),
		("mediaportal","plugin.png"),
		("minidlna_setup","setup.png"),
		("movie_list","movie_list.png"),
		("moviebrowser","plugin.png"),
		("multi_quick","mqb.png"),
		("netafp_setup","net.png"),
		("netftp_setup","net.png"),
		("netmounts_setup","net.png"),
		("netnfs_setup","net.png"),
		("netrts_setup","net.png"),
		("netsabnzbd_setup","net.png"),
		("netsmba_setup","net.png"),
		("nettelnet_setup","net.png"),
		("netushare_setup","net.png"),
		("netvpn_setup","net.png"),
		("network_menu","net.png"),
		("network_setup","net.png"),
		("osd3dsetup","look.png"),
		("osd_setup","look.png"),
		("osdsetup","look.png"),
		("parental_setup","look.png"),
		("picturecenterfs","plugin.png"),
		("plugin_select","plugin.png"),
		("plugin_selection","plugin.png"),
		("powertimer_edit","shutdowntimer.png"),
		("pvmc_mainmenu","plugin.png"),
		("rec_setup","setup.png"),
		("recording_setup","setup.png"),
		("remote_setup","setup.png"),
		("remotecode","setup.png"),
		("restart","restart.png"),
		("restart_enigma","restart_enigma.png"),
		("rfmod_setup","setup.png"),
		("sat_ip_client","net.png"),
		("saveepgcache","movie_list.png"),
		("scart_switch","setup.png"),
		("service_info_screen","service_info.png"),
		("service_searching_selection","tuner.png"),
		("setup_epgenhanced","setup.png"),
		("setup_epggraphical","setup.png"),
		("setup_epginfobar","setup.png"),
		("setup_epginfobargraphical","setup.png"),
		("setup_epgmulti","setup.png"),
		("setup_selection","setup.png"),
		("sibsetup","plugin.png"),
		("skin_setup","setup.png"),
		("sleep","shutdowntimer.png"),
		("software_manager","setup.png"),
		("specialfeatures_menu","setup.png"),
		("sportspub_plugin","plugin.png"),
		("standby","power.png"),
		("standby_restart_list","shutdown.png"),
		("startwizzard","paket.png"),
		("streamconvert","webb.png"),
		("subtitle_selection","sub.png"),
		("subtitle_setup","sub.png"),
		("system_selection","setup.png"),
		("time_setup","timer.png"),
		("timer_edit","timer.png"),
		("timer_menu","timer.png"),
		("timezone_setup","tuner.png"),
		("timshift_setup","movie_list.png"),
		("tuner_setup","setup.png"),
		("usage_setup","setup.png"),
		("user_interface","setup.png"),
		("video_finetune","movie_list.png"),
		("video_menu","movie_list.png"),
		("video_setup","movie_list.png"),
		("videoenhancement_setup","movie_list.png"),
		("vti_epg_panel","paket.png"),
		("vti_menu","vtimenu.png"),
		("vti_movies","movie_list.png"),
		("vti_panel","vtimenu.png"),
		("vti_panel_news","webb.png"),
		("vti_servicelist","service_info.png"),
		("vti_subtitles","sub.png"),
		("vti_system_setup","setup.png"),
		("vti_timer","timer.png"),
		("vti_tv_radio","movie_list.png"),
		("vti_user_interface","camd.png"),
		("webradiofs","plugin.png"),
		("xbmc_starten","plugin.png"),
		("yamp","plugin.png"),
		("yamp_music_player","plugin.png"),
		("youtube_tv","plugin.png")
		]
	
	@cached
	def getText(self):
		try: # is it a menu? then we handle it according to current selection
			cur = self.source.current
			if cur and len(cur) > 2:
				selection = cur[2]
				if selection in ("skin_selector","atilehd_setup"):
					return self.logo
				name = self.userpath+selection.lower()+".png"
				if fileExists(name):
					return name
				name = self.path+selection.lower()+".png"
				if fileExists(name):
					return name
				name=""
				for pair in self.names:
					if pair[0] == selection:
						break
				name=self.userpath+pair[1]
				if name != "" and fileExists(name):
					return name
				name=self.path+pair[1]
				if name != "" and fileExists(name):
					return name
		except:
			try: # is it a screen? then we handle it according to title
				text=self.source.text
				if text in ("zapHistory","Senderhistorie"):
					return self.logo
			except:
				pass
		name=self.userpath+"plugin.png"
		if fileExists(name):
			return name
		name=self.path+"plugin.png"
		if fileExists(name):
			return name
		return self.logo
	
	text = property(getText)
