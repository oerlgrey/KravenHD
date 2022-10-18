# -*- coding: utf-8 -*-

#  pstrCnvrt Converter
#
#  Coded/Modified/Adapted by örlgrey
#  Based on OpenATV image source code
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

# by digiteng...12-2019

from Components.Converter.Converter import Converter
from Components.Element import cached
import json, re, os, six.moves.urllib.request

if not os.path.isdir('/media/hdd/poster'):
	os.mkdir('/media/hdd/poster')

class KravenHDpstrCnvrt(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""

		if not event is None:
			if self.type == "POSTER":
				self.evnt = event.getEventName()
				try:
					p = '((.*?)) \([T](\d+)\)'
					e1 = re.search(p,self.evnt)
					if e1:
						jr = e1.group(1)
						self.evntNm = re.sub('\s+', '+', jr)
					else:
						self.evntNm = re.sub('\s+', '+', self.evnt)
					self.evntNmPstr = self.evntNm + ".jpg"
					if not os.path.exists("/media/hdd/poster/%s.jpg" % (self.evntNm)):
						ses_ep = self.sessionEpisode(event)
						if ses_ep != "" and len(ses_ep) > 0:
							self.srch = "tv"
							self.searchPoster()
						else:
							self.srch = "multi"
							self.searchPoster()
					else:
						return self.evntNm
				except:
					pass
		else:
			return ""

	text = property(getText)

	def searchPoster(self):
		url_json = "https://api.themoviedb.org/3/search/%s?api_key=3c3efcf47c3577558812bb9d64019d65&query=%s" % (self.srch, self.evntNm)
		jp = json.load(six.moves.urllib.request.urlopen(url_json))

		imgP = (jp['results'][0]['poster_path'])
		url_poster = "https://image.tmdb.org/t/p/w185_and_h278_bestv2%s" % (imgP)
		dwn_poster = "/media/hdd/poster/%s.jpg" % (self.evntNm)
		if not os.path.exists(dwn_poster):
			with open(dwn_poster, 'wb') as f:
				f.write(six.moves.urllib.request.urlopen(url_poster).read())
				f.close()
				return self.evntNm

	def sessionEpisode(self, event):
		fd = event.getShortDescription() + "\n" + event.getExtendedDescription()
		pattern = ["(\d+). Staffel, Folge (\d+)", "T(\d+) Ep.(\d+)", "'Episodio (\d+)' T(\d+)"]
		for i in pattern:
			seg = re.search(i, fd)
			if seg:
				if re.search("Episodio",i):
					return "S" + seg.group(2).zfill(2) + "E" + seg.group(1).zfill(2)
				else :
					return "S" + seg.group(1).zfill(2) + "E" + seg.group(2).zfill(2)
		return ""
