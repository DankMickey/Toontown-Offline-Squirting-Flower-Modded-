# File: D (Python 2.4)

import DistributedTreasureAI
from toontown.toonbase import ToontownGlobals

class DistributedSZTreasureAI(DistributedTreasureAI.DistributedTreasureAI):
    
    def __init__(self, air, treasurePlanner, x, y, z, treasureType = 0):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, treasurePlanner, treasureType, x, y, z)
        self.healAmount = treasurePlanner.healAmount
            
        


