from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

class BanManager(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManager')

    def informBan(self, banner, username, time):
        msg = "%s banned %s for %s hours"
        self.notify.info(msg)
        
        dg = PyDatagram()
        dg.addString(msg)
        dgi = PyDatagramIterator(dg)
        self.cr.handleSystemMessage(dgi)
