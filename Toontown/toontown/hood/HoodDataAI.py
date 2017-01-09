# File: H (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
import ZoneUtil
from toontown.building import DistributedBuildingMgrAI
from toontown.suit import DistributedSuitPlannerAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone import DistributedButterflyAI
from pandac.PandaModules import *
from toontown.toon import NPCToons
from toontown.dna.DNASpawnerAI import *

class HoodDataAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('HoodDataAI')
    numStreets = 3
    
    def __init__(self, air, zoneId, canonicalHoodId):
        self.air = air
        self.zoneId = zoneId
        self.canonicalHoodId = canonicalHoodId
        self.treasurePlanner = None
        self.buildingManagers = []
        self.suitPlanners = []
        self.doId2do = { }
        self.replacementHood = None
        self.redirectingToMe = []
        self.hoodPopulation = 0
        self.pgPopulation = 0
        
        self.startup()
 
    def getZoneTable(self):
        zoneTable = [self.zoneId]
        zoneTable.extend(ToontownGlobals.HoodHierarchy.get(self.canonicalHoodId, []))
        return zoneTable
    
    def startup(self):
        self.createBuildingManagers()
        self.createSuitPlanners()
        
        if 'botHQ' in self.__class__.__name__:
            self.numStreets = 0
        
        for i in xrange(self.numStreets + 1):
            zoneId = self.canonicalHoodId + i * 100
            DNASpawnerAI().spawnObjects(self.air.genDNAFileName(zoneId), zoneId)
        
        self.notify.info('Started up')
        
    def shutdown(self):
        self.setRedirect(None)
        if self.treasurePlanner:
            self.treasurePlanner.stop()
            self.treasurePlanner.deleteAllTreasuresNow()
            self.treasurePlanner = None
        
        for suitPlanner in self.suitPlanners:
            suitPlanner.requestDelete()
            del self.air.suitPlanners[suitPlanner.zoneId]
        
        self.suitPlanners = []
        for buildingManager in self.buildingManagers:
            buildingManager.cleanup()
            del self.air.buildingManagers[buildingManager.branchID]
        
        self.buildingManagers = []
        ButterflyGlobals.clearIndexes(self.zoneId)
        del self.fishingPonds
        for distObj in self.doId2do.values():
            distObj.requestDelete()
        
        del self.doId2do
        del self.air

    
    def addDistObj(self, distObj):
        self.doId2do[distObj.doId] = distObj

    
    def removeDistObj(self, distObj):
        del self.doId2do[distObj.doId]

    def createBuildingManagers(self):
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            if zone[1]:
                zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
                dnaStore = self.air.getStorage(zone[0])
                mgr = DistributedBuildingMgrAI.DistributedBuildingMgrAI(self.air, zoneId, dnaStore, None) #self.air.trophyMgr)
                self.buildingManagers.append(mgr)
                self.air.buildingManagers[zoneId] = mgr

    def createSuitPlanners(self):
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            if zone[2]:
                zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
                sp = DistributedSuitPlannerAI.DistributedSuitPlannerAI(self.air, zoneId)
                sp.generateWithRequired(zoneId)
                sp.d_setZoneId(zoneId)
                sp.acceptOnce("startShardActivity", sp.initTasks)
                self.suitPlanners.append(sp)
                self.air.suitPlanners[zoneId] = sp
                self.notify.info('Created new SuitPlanner at %s' % zoneId)
                
            else:
                self.notify.info('Zone[2] @ (%s; %s) is %s' % (zone, self.canonicalHoodId, zone[2]))

    def createButterflies(self, playground):
        ButterflyGlobals.generateIndexes(self.zoneId, playground)
        for i in range(0, ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for j in range(0, ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                bfly = DistributedButterflyAI.DistributedButterflyAI(self.air, playground, i, self.zoneId)
                bfly.generateWithRequired(self.zoneId)
                bfly.start()
                self.addDistObj(bfly)

    def setRedirect(self, replacementHood):
        if self.replacementHood:
            self.replacementHood[0].redirectingToMe.remove(self)
        
        self.replacementHood = replacementHood
        if self.replacementHood:
            self.replacementHood[0].redirectingToMe.append(self)
        

    
    def hasRedirect(self):
        return self.replacementHood != None

    
    def getRedirect(self):
        if self.replacementHood == None:
            return self
        else:
            return self.replacementHood[0].getRedirect()

    
    def incrementPopulation(self, zoneId, increment):
        self.hoodPopulation += increment
        if ZoneUtil.isPlayground(zoneId):
            self.pgPopulation += increment
        

    
    def getHoodPopulation(self):
        population = self.hoodPopulation
        for hood in self.redirectingToMe:
            population += hood.getHoodPopulation()
        
        return population

    
    def getPgPopulation(self):
        population = self.pgPopulation
        for pg in self.redirectingToMe:
            population += pg.getPgPopulation()
        
        return population


