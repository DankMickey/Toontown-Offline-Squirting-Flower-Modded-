# File: D (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.classicchars import DistributedDonaldAI
from toontown.classicchars import DistributedFrankenDonaldAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import DLTreasurePlannerAI
from toontown.safezone import ButterflyGlobals

class DLHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DLHoodDataAI')
    numStreets = 2
    
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.DonaldsDreamland
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
            if simbase.config.GetBool('want-donald-dreamland', True):
                self.createClassicChar()
        self.treasurePlanner = DLTreasurePlannerAI.DLTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
    
    def createClassicChar(self):
        if ToontownGlobals.HALLOWEEN_COSTUMES in self.air.holidayManager.currentHolidays:
            self.classicChar = DistributedFrankenDonaldAI.DistributedFrankenDonaldAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()
        else:
            self.classicChar = DistributedDonaldAI.DistributedDonaldAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()