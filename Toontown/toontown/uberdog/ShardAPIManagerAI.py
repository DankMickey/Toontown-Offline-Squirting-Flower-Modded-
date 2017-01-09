from direct.distributed.DistributedObjectGlobalAI import *
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *
from direct.distributed.ClockDelta import *
import time

from toontown.building import DistributedAnimBuildingAI, DistributedBuildingAI

class ShardAPIManagerAI(DistributedObjectGlobalAI):
    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)
        self.context = 0
        self.accept("startInvasion", lambda *x: self.d_updateInvasion())
        self.accept("endInvasion", lambda *x: self.d_updateInvasion())
        
        self.bldgs = set()
        
    def start(self):
        self.sendUpdate("newShard", [])
            
    def d_setShardData(self):
        dg = PyDatagram()
        
        self.context += 1
        self.context %= 200
        dg.addUint8(self.context)
        
        buildings = self.air.doFindAllInstances(DistributedBuildingAI.DistributedBuildingAI)
        for bldg in buildings:
            if bldg.__class__ in (DistributedBuildingAI.DistributedBuildingAI, DistributedAnimBuildingAI.DistributedAnimBuildingAI):
                if not bldg.zoneId % 1000:
                    # sz bldg, ignore
                    continue
                    
                if bldg.zoneId // 1000 == 7:
                    # ff bldg, ignore now
                    continue
                    
                data = bldg.getPickleData()

                dg.addString("block")
                dg.addUint16(bldg.zoneId - (bldg.zoneId % 1000))
                dg.addUint16(bldg.zoneId)
                dg.addUint8(int(data['block']))
                dg.addString(data['state'].lower())
                dg.addUint8(ord(data['track']))
                dg.addUint8(int(data['difficulty']))
                dg.addInt8(int(data['numFloors']))
                
                self.bldgs.add(bldg)
                    
        self.writeInvasion(dg)                    
        self.sendUpdate("setShardData", [dg.getMessage()])
                            
        self.air.notify.info("Sent shard data to UD")
        taskMgr.doMethodLater(60, self.__timeout, 'UD-sync-timeout')
        
    def __timeout(self, task):
        self.notify.error('Timeout waiting for UD sync, leaving...')
        return task.done
        
    def d_updateBlock(self, bldg):
        if not bldg in self.bldgs:
            return
            
        data = bldg.getPickleData()
        
        dg = PyDatagram()
        dg.addUint16(bldg.zoneId - (bldg.zoneId % 1000))
        dg.addUint16(bldg.zoneId)
        dg.addUint8(int(data['block']))
        
        state = data['state'].lower()
        
        if state.startswith('clear'):
            state = 'cogdo' if state.endswith('cogdo') else 'suit'
            
        dg.addString(state)
        
        dg.addUint8(ord(data['track']))
        dg.addUint8(int(data['difficulty']))
        dg.addInt8(int(data['numFloors']))
        
        self.sendUpdate("doUpdate", ["block", dg.getMessage()])
            
    def setShardDataRes(self, context):
        if self.context == 0:
            self.air.notify.warning("got unexpected setShardDataRes")
            
        elif context != self.context:
            self.air.notify.warning("got bad context for setShardDataRes (%d), expecting (%d)" % (context, self.context))

        self.air.gotUberdogAPISync()
        taskMgr.remove('UD-sync-timeout')
        self.doMethodLater(5, self.d_heartbeat, self.taskName('heartbeat'))
        self.context -= 1
        
    def d_heartbeat(self, task):
        self.sendUpdate("heartbeat", [])
        return task.again
                
    def d_updateInvasion(self):
        dg = PyDatagram()
        self.writeInvasion(dg)
        self.sendUpdate("doUpdate", ["inv", dg.getMessage()])
        
    def writeInvasion(self, dg):
        name, skel, _, startTime, duration = self.air.suitInvasionManager.getCurrentInvasion()

        dg.addString("inv")
        dg.addUint32(int(time.time()))
        dg.addUint16(duration)
        dg.addString(name)
        dg.addUint8(0 if not skel else 1)
        