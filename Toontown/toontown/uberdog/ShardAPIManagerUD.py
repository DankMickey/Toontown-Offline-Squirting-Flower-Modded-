from direct.distributed.DistributedObjectGlobalUD import *
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *

from toontown.toonbase import ToontownGlobals

import time, datetime

blockNames = {}
langAliasMap = {'English': 'en', '_portuguese': 'pt'}

languages = config.GetString('shard-api-block-languages', 'English _portuguese').split()
for lang in languages:
    m = __import__('toontown.toonbase.TTLocalizer%s' % lang, {}, {}, ['toontown.toonbase'])
    zoneDict = m.zone2TitleDict.copy()
    blockNames[langAliasMap[lang]] = zoneDict
    del m

CURRENT_LANG_CONTEXT = 'en'

def setLanguageContext(lang):
    global CURRENT_LANG_CONTEXT
    
    if lang is None:
        CURRENT_LANG_CONTEXT = 'en'
        return True
        
    if not lang in blockNames:
        return False
        
    CURRENT_LANG_CONTEXT = lang
    return True
    
class Block:
    def __init__(self, number, branchZone):
        self.number = number
        self.branchZone = branchZone
     
        self.setToToon(None)
        
    def setToToon(self, args):
        self.type = "toon"
        self.track = ""
        self.height = 0
        self.difficulty = -1
        
    def setToSuit(self, args):
        self.type = "suit"
        self.track = args['track']
        self.height = args['height']
        self.difficulty = args['difficulty']
        
    def setToCogdo(self, args):
        self.setToSuit(args)
        self.type = "cogdo"
        
    def update(self, mode, args):
        if mode == "toon":
            self.setToToon(args)
            
        if mode == "suit":
            self.setToSuit(args)
            
        if mode == "cogdo":
            self.setToCogdo(args)
        
    def writeDict(self):
        return {"title": self.getName(), "type": self.type, "track": self.track,
                "height": self.height, "difficulty": self.difficulty}
                                                                                                     
    def getName(self):
        zoneId = self.number + self.branchZone + 500
        return blockNames[CURRENT_LANG_CONTEXT].get(zoneId, ["???", ""])[0]
        
class StreetHandle:
    def __init__(self, hood, streetId):
        self.hood = hood
        self.streetId = streetId
        self.dnaStore = self.hood.shard.mgr.air.getDnaStore(self.streetId)
        self.blocks = {}

        for i in xrange(self.dnaStore.getNumBlockNumbers()):
            blockNumber = self.dnaStore.getBlockNumberAt(i)
            buildingType = self.dnaStore.getBlockBuildingType(blockNumber)
            
            if buildingType != 'hq':
                self.blocks[blockNumber] = Block(blockNumber, self.streetId)
        
    def writeDict(self):
        d = {}
        for i, block in self.blocks.items():
            d[i] = block.writeDict()
            
        return {"blocks": d}
                        
class HoodHandle:
    def __init__(self, shard, hoodId, numStreets):
        self.shard = shard
        self.hoodId = hoodId
        self.streets = {}
        
        for i in xrange(numStreets):
            z = self.hoodId + (i + 1) * 100
            self.streets[z] = StreetHandle(self, z)
                
    def writeDict(self):
        d = {}
        for i, street in self.streets.items():
            d[i] = street.writeDict()
            
        return {"streets": d}

class ShardHandle:
    def __init__(self, mgr):
        self.mgr = mgr
        self.hoods = {}
        
        self.duration = 0
        self.start = 0
        self.cogName = ""
        self.skel = 0
        
        self.addHood(ToontownGlobals.ToontownCentral)
        self.addHood(ToontownGlobals.DonaldsDock)
        self.addHood(ToontownGlobals.DaisyGardens)
        self.addHood(ToontownGlobals.MinniesMelodyland)
        self.addHood(ToontownGlobals.TheBrrrgh)
        self.addHood(ToontownGlobals.DonaldsDreamland, 2)
        
    def addHood(self, hoodId, numStreets = 3):
        self.hoods[hoodId] = HoodHandle(self, hoodId, numStreets)
        
    def writeDict(self):
        d = {}
        for i, hood in self.hoods.items():
            d[i] = hood.writeDict()
            
        return {"hoods": d}
        
    def updateInvasion(self, name, skel, start, duration):
        self.cogName = name
        self.skel = skel
        self.start = start
        self.duration = duration
        
    def readInvasion(self):
        r = 0
        if self.duration != 0:
            elapsed = int(int(time.time()) - self.start)
            r = self.duration - elapsed
        
        return {"duration": self.duration, "remaining": r, "cogName": self.cogName, "skel": self.skel}

class ShardAPIManagerUD(DistributedObjectGlobalUD):
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.shards = {}
        ShardHandle(self)
        
    def newShard(self):
        self.heartbeat()
        
        shardId = self.air.getMsgSender() + 1
        
        if not shardId in self.shards:
            self.shards[shardId] = ShardHandle(self)
        
    def _doUpdateShard(self, dgi):
        shardId = self.air.getMsgSender() + 1
        if not shardId in self.shards:
            self.newShard()
            
        shard = self.shards[shardId]
            
        updateType = dgi.getString()
            
        if updateType == "block":
            hoodId = dgi.getUint16()
            streetId = dgi.getUint16()
            blockNumber = dgi.getUint8()
            
            args = {}
            type = dgi.getString()
            
            args['track'] = chr(dgi.getUint8())
            args['difficulty'] = dgi.getUint8()
            args['height'] = dgi.getInt8()
            
            hood = shard.hoods[hoodId]
            street = hood.streets[streetId]
            block = street.blocks[blockNumber]
            block.update(type, args)
            
        elif updateType == "inv":
            start = dgi.getUint32()
            duration = dgi.getUint16()
            cogName = dgi.getString()
            skel = dgi.getUint8()
            
            shard.updateInvasion(cogName, skel, start, duration)
            
        else:
            print 'WARNING: Unknown or not implemented updateType %s from %d' % (updateType[:10], shardId)
            
    def setShardData(self, data):
        dg = PyDatagram(data)
        di = PyDatagramIterator(dg)
        context = di.getUint8()
        
        while di.getRemainingSize():
            self._doUpdateShard(di)
            
        if context > 0:
            self.sendUpdateToChannel(self.air.getMsgSender(), "setShardDataRes", [context])
        
    def doUpdate(self, updateType, data):
        self.heartbeat()
        
        if updateType == "inv":
            return # rip crash
            
        dg = PyDatagram()
        dg.addUint8(0)
        dg.addString(updateType)
        dg.appendData(data)
        self.setShardData(dg.getMessage())
        
    def listInvasions(self):
        if not self.shards:
            return {}
            
        invData = {}
        for i, shard in self.shards.items():
            invData[i] = shard.readInvasion()
            
        return invData
        
    def writeDict(self):
        d = {}
        for i, shard in self.shards.items():
            d[i] = shard.writeDict()
            
        return d
        
    def __killShard(self, shardId, task = None):
        if not shardId in self.shards:
            return
            
        print datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), shardId, 'timed out heartbeat, killing...'
        del self.shards[shardId]
        
        if task:
            return task.done
        
    def heartbeat(self):
        shardId = self.air.getMsgSender() + 1
        taskName = self.taskName('kill-shard-%d' % shardId)
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(180, lambda t: self.__killShard(shardId, t), taskName)
        