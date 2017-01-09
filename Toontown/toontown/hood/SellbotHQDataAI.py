from toontown.toonbase import ToontownGlobals
from HoodDataAI import HoodDataAI
from toontown.suit import DistributedSellbotBossAI
from toontown.building import FADoorCodes
from toontown.building import DistributedVPElevatorAI
from toontown.coghq import LobbyManagerAI
from toontown.building import DoorTypes
from toontown.coghq import DistributedCogHQDoorAI
from toontown.building import DistributedBoardingPartyAI
from toontown.coghq.DistributedFactoryElevatorExtAI import DistributedFactoryElevatorExtAI

from direct.directnotify import DirectNotifyGlobal

from toontown.suit import DistributedSuitPlannerAI
import ZoneUtil

class SellbotHQDataAI(HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotHQDataAI')
    HOOD = ToontownGlobals.SellbotHQ
    
    def __init__(self, air):
        HoodDataAI.__init__(self, air, ToontownGlobals.SellbotHQ, ToontownGlobals.SellbotHQ)
    
    def startup(self):
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(self.air, DistributedSellbotBossAI.DistributedSellbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.SellbotLobby)

        self.lobbyElevator = DistributedVPElevatorAI.DistributedVPElevatorAI(self.air, self.lobbyMgr, ToontownGlobals.SellbotLobby, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.SellbotLobby)

        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.SellbotLobby)

        destinationZone = ToontownGlobals.SellbotLobby
        extDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=0, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoor1 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=1, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoor2 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=2, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoor3 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=3, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoorList = [extDoor0, extDoor1, extDoor2, extDoor3]
        intDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.SellbotHQ, doorIndex=0)
        intDoor0.setOtherDoor(extDoor0)
        intDoor0.zoneId = ToontownGlobals.SellbotLobby
        for extDoor in extDoorList:
            extDoor.setOtherDoor(intDoor0)
            extDoor.zoneId = ToontownGlobals.SellbotHQ
            extDoor.generateWithRequired(ToontownGlobals.SellbotHQ)
            extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

        intDoor0.generateWithRequired(ToontownGlobals.SellbotLobby)
        intDoor0.sendUpdate('setDoorIndex', [intDoor0.getDoorIndex()])
        
        mins = ToontownGlobals.FactoryLaffMinimums[0]
        
        self.factoryFrontElevator = DistributedFactoryElevatorExtAI(self.air, self.air.factoryMgr, ToontownGlobals.SellbotFactoryInt, 0, antiShuffle = 0, minLaff = mins[0])
        self.factoryFrontElevator.generateWithRequired(ToontownGlobals.SellbotFactoryExt)
        self.factorySideElevator = DistributedFactoryElevatorExtAI(self.air, self.air.factoryMgr, ToontownGlobals.SellbotFactoryInt, 1, antiShuffle = 0, minLaff = mins[1])
        self.factorySideElevator.generateWithRequired(ToontownGlobals.SellbotFactoryExt)
        factoryIdList = [
            self.factoryFrontElevator.doId,
            self.factorySideElevator.doId]
        if simbase.config.GetBool('want-boarding-groups', 1):
            self.factoryBoardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, factoryIdList, 4)
            self.factoryBoardingParty.generateWithRequired(ToontownGlobals.SellbotFactoryExt)
        
        self.createPlanner(ToontownGlobals.SellbotHQ, extDoorList)
        self.createPlanner(ToontownGlobals.SellbotFactoryExt, extDoorList)

    def createPlanner(self, zoneId, cogHQDoors = []):
        zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
        sp = DistributedSuitPlannerAI.DistributedSuitPlannerAI(self.air, zoneId)
        sp.cogHQDoors = cogHQDoors
        sp.generateWithRequired(zoneId)
        sp.d_setZoneId(zoneId)
        sp.initTasks()
        self.suitPlanners.append(sp)
        self.air.suitPlanners[zoneId] = sp
        self.notify.info('Created new SuitPlanner at %s' % zoneId)

        
