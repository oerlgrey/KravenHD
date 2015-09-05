from Components.config import config
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Poll import Poll

class KravenHDTempFanInfo(Poll, Converter, object):
    TEMPINFO = 0
    FANINFO = 1

    def __init__(self, type):
        Poll.__init__(self)
        Converter.__init__(self, type)
        self.type = type
        self.poll_interval = 2000
        self.poll_enabled = True
        if type == 'TempInfo':
            self.type = self.TEMPINFO
        elif type == 'FanInfo':
            self.type = self.FANINFO

    @cached
    def getText(self):
        textvalue = ''
        service = self.source.service
        if service:
            info = service and service.info()
            if self.type == self.TEMPINFO:
                textvalue = self.tempfile()
            elif self.type == self.FANINFO:
                textvalue = self.fanfile()
        return textvalue

    text = property(getText)

    def tempfile(self):
        temp = ''
        unit = ''
        try:
            f = open('/proc/stb/sensors/temp0/value', 'rb')
            temp = f.readline().strip()
            f.close()
            f = open('/proc/stb/sensors/temp0/unit', 'rb')
            unit = f.readline().strip()
            f.close()
            tempinfo = '' + str(temp) + '\xc2\xb0' + str(unit)
            return tempinfo
        except:
            pass

    def fanfile(self):
        fan = ''
        try:
            f = open('/proc/stb/fp/fan_speed', 'rb')
            fan = f.readline().strip()
            f.close()
            faninfo = '' + str(fan)[:-4]
            return faninfo
        except:
            pass

    def changed(self, what):
        if what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evUpdatedInfo or what[0] == self.CHANGED_POLL:
            Converter.changed(self, what)