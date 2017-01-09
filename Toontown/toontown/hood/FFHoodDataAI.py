from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import FFTreasurePlannerAI
from toontown.toon import DistributedNPCFishermanAI

class FFHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('FFHoodDataAI')
    numStreets = 1
    
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.FunnyFarm
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
        self.treasurePlanner = FFTreasurePlannerAI.FFTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()