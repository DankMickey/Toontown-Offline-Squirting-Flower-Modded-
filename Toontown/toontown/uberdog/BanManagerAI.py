from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import urllib2

class BanManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerAI')
        
    # to do: subscribe
        
    def ban(self, banner, target, time):
        dg = PyDatagram()
        dg.addServerHeader(target.GetPuppetConnectionChannel(target.doId), self.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(155)
        dg.addString('You were kicked by a moderator!')
        self.air.send(dg)
        self.sendUpdate("banUD", [banner, target.DISLid, time])
        