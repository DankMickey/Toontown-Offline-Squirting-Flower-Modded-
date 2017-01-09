from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
import ZoneUtil
from toontown.classicchars import DistributedChipAI
from toontown.classicchars import DistributedPoliceChipAI
from toontown.classicchars import DistributedDaleAI
from toontown.classicchars import DistributedJailbirdDaleAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import OZTreasurePlannerAI
from pandac.PandaModules import *
from toontown.safezone import DistributedPicnicBasketAI
from toontown.distributed import DistributedTimerAI
import string
from toontown.safezone import DistributedPicnicTableAI
from toontown.safezone import DistributedChineseCheckersAI
from toontown.safezone import DistributedCheckersAI
from toontown.dna.DNASpawnerAI import *
import random


class OZHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('OZHoodDataAI')
    numStreets = 0 # 6100 is special, don't use this
     
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.OutdoorZone
        if zoneId == None:
            zoneId = hoodId
 
        self.timer = None
        self.classicCharChip = None
        self.classicCharDale = None
        self.picnicTables = []
        self.gameTables = []
        
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)

    def startup(self):
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-chip-and-dale', True):
                self.createClassicChars()
        self.treasurePlanner = OZTreasurePlannerAI.OZTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
        self.timer = DistributedTimerAI.DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.zoneId)
        HoodDataAI.HoodDataAI.startup(self)
        #DNASpawnerAI().spawnObjects('phase_14/dna/outdoor_zone_6100.pdna', 6100)
                
    def cleanup(self):
        self.timer.delete()

    def createClassicChars(self):
        if ToontownGlobals.HALLOWEEN_COSTUMES in self.air.holidayManager.currentHolidays:
            self.classicCharChip = DistributedPoliceChipAI.DistributedPoliceChipAI(self.air)
            self.classicCharChip.generateWithRequired(self.zoneId)
            self.classicCharChip.start()
            self.classicCharDale = DistributedJailbirdDaleAI.DistributedJailbirdDaleAI(self.air, self.classicCharChip.doId)
            self.classicCharDale.generateWithRequired(self.zoneId)
            self.classicCharDale.start()
            self.classicCharChip.setDaleId(self.classicCharDale.doId)
        else:
            self.classicCharChip = DistributedChipAI.DistributedChipAI(self.air)
            self.classicCharChip.generateWithRequired(self.zoneId)
            self.classicCharChip.start()
            self.classicCharDale = DistributedDaleAI.DistributedDaleAI(self.air, self.classicCharChip.doId)
            self.classicCharDale.generateWithRequired(self.zoneId)
            self.classicCharDale.start()
            self.classicCharChip.setDaleId(self.classicCharDale.doId)