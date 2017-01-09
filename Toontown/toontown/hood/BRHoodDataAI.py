# File: B (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.classicchars import DistributedPlutoAI
from toontown.classicchars import DistributedWesternPlutoAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import BRTreasurePlannerAI
from toontown.toon import DistributedNPCFishermanAI

class BRHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BRHoodDataAI')
    
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.TheBrrrgh
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
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-pluto', True):
                self.createClassicChar()
        self.treasurePlanner = BRTreasurePlannerAI.BRTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
    
    def createClassicChar(self):
        if ToontownGlobals.HALLOWEEN_COSTUMES in self.air.holidayManager.currentHolidays:
            self.classicChar = DistributedWesternPlutoAI.DistributedWesternPlutoAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()
        else:
            self.classicChar = DistributedPlutoAI.DistributedPlutoAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()