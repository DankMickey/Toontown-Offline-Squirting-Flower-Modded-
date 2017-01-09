# File: T (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.classicchars import DistributedMickeyAI
from toontown.classicchars import DistributedVampireMickeyAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import TTTreasurePlannerAI
from toontown.safezone import ButterflyGlobals
from direct.task import Task

class TTHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTHoodDataAI')
    
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.ToontownCentral
        if zoneId == None:
            zoneId = hoodId
        self.classicChar = None
        
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)

    
    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)
        trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        trolley.generateWithRequired(self.zoneId)
        trolley.start()
        self.addDistObj(trolley)
        self.trolley = trolley
        self.treasurePlanner = TTTreasurePlannerAI.TTTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
        self.createButterflies(ButterflyGlobals.TTC)
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-mickey', True):
                self.createClassicChar()
        if simbase.blinkTrolley:
            taskMgr.doMethodLater(0.5, self._deleteTrolley, 'deleteTrolley')
        
        messenger.send('TTHoodSpawned', [
            self])

    
    def shutdown(self):
        HoodDataAI.HoodDataAI.shutdown(self)
        messenger.send('TTHoodDestroyed', [
            self])

    
    def _deleteTrolley(self, task):
        self.trolley.requestDelete()
        taskMgr.doMethodLater(0.5, self._createTrolley, 'createTrolley')
        return Task.done

    
    def _createTrolley(self, task):
        trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        trolley.generateWithRequired(self.zoneId)
        trolley.start()
        self.trolley = trolley
        taskMgr.doMethodLater(0.5, self._deleteTrolley, 'deleteTrolley')
        return Task.done

    def createClassicChar(self):
        if ToontownGlobals.HALLOWEEN_COSTUMES in self.air.holidayManager.currentHolidays:
            self.classicChar = DistributedVampireMickeyAI.DistributedVampireMickeyAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()
        else:
            self.classicChar = DistributedMickeyAI.DistributedMickeyAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()