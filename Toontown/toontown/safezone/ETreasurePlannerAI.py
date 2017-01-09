from toontown.toonbase.ToontownGlobals import *
from direct.distributed import DistributedObjectAI
import RegenTreasurePlannerAI
import DistributedETreasureAI
import TreasureGlobals

class ETreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):
    
    def __init__(self, zoneId):
        self.healAmount = 5
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(self, zoneId, DistributedETreasureAI.DistributedETreasureAI, 'ETreasurePlanner', 15, 3)

    def initSpawnPoints(self):
        self.spawnPoints = [
            (19, -171, 0.0),
            (-3, -100, 3.66),
            (-4, -25, 7.0),
            (1.15, 64.89, 4.858),
            (-89, 43.4, 0.0),
            (-114, -5, 1.8),
            (-106, -98, 0.0),
            (-1, -61, 1.0),
            (130, 30, 0.0),
            (-21, -7, 7.0),
            (-27, 91, 0.0),
            (-57, 0, 2.7),
            (12, -128, -9.97),
            (-1.8, 103.4, -8.0),
            (-27.5, 6, -9.2),
            (-29.6, -34.4, -5.4),
            (-163.7, 13.8, 0.9),
            (1.3, -107, 7.9),
            (-87, -49, 0.05),
            (45, 2.6, 8.0)]
        return self.spawnPoints
        
    def validAvatar(self, treasure, av):
        heal = TreasureGlobals.SafeZoneTreasureSpawns[MyEstate][1]
        if not av.isToonedUp():
            av.toonUp(heal)
            return 1
        
        return 0
        