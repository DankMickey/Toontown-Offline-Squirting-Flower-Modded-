# File: D (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.classicchars import DistributedDaisyAI
from toontown.classicchars import DistributedSockHopDaisyAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import DGTreasurePlannerAI
from toontown.safezone import DistributedDGFlowerAI
from toontown.safezone import ButterflyGlobals

class DGHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DGHoodDataAI')
    
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.DaisyGardens
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
        
        self.treasurePlanner = DGTreasurePlannerAI.DGTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
        
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-daisy', True):
                self.createClassicChar()
        
        flower = DistributedDGFlowerAI.DistributedDGFlowerAI(self.air)
        flower.generateWithRequired(self.zoneId)
        self.addDistObj(flower)
        
        self.createButterflies(ButterflyGlobals.DG)

    def createClassicChar(self):
        if ToontownGlobals.HALLOWEEN_COSTUMES in self.air.holidayManager.currentHolidays:
            self.classicChar = DistributedSockHopDaisyAI.DistributedSockHopDaisyAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()
        else:
            self.classicChar = DistributedDaisyAI.DistributedDaisyAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()