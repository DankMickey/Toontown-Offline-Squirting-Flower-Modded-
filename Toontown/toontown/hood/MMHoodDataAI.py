# File: M (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.classicchars import DistributedMinnieAI
from toontown.classicchars import DistributedWitchMinnieAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import MMTreasurePlannerAI
from toontown.safezone import DistributedMMPianoAI

class MMHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('MMHoodDataAI')
    
    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.MinniesMelodyland
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
        self.treasurePlanner = MMTreasurePlannerAI.MMTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-minnie', True):
                self.createClassicChar()
        piano = DistributedMMPianoAI.DistributedMMPianoAI(self.air)
        piano.generateWithRequired(self.zoneId)
        self.addDistObj(piano)

    def createClassicChar(self):
        if ToontownGlobals.HALLOWEEN_COSTUMES in self.air.holidayManager.currentHolidays:
            self.classicChar = DistributedWitchMinnieAI.DistributedWitchMinnieAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()
        else:
            self.classicChar = DistributedMinnieAI.DistributedMinnieAI(self.air)
            self.classicChar.generateWithRequired(self.zoneId)
            self.classicChar.start()