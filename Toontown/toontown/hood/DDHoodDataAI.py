# File: D (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.classicchars import DistributedDonaldDockAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import DDTreasurePlannerAI
from toontown.safezone import DistributedBoatAI

class DDHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DDHoodDataAI')
    
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.DonaldsDock
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
        self.treasurePlanner = DDTreasurePlannerAI.DDTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-donald-dock', True):
                self.createClassicChar()
        boat = DistributedBoatAI.DistributedBoatAI(self.air)
        boat.generateWithRequired(self.zoneId)
        boat.start()
        self.addDistObj(boat)

    def createClassicChar(self):
        self.classicChar = DistributedDonaldDockAI.DistributedDonaldDockAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()