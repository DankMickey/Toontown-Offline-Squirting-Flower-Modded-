from toontown.shtiker.CogPageGlobals import *
from toontown.suit import SuitDNA
import random

class CogPageManagerAI:
    maxCogs = 10000
    quotas = COG_QUOTAS
    
    def __init__(self, air):
        self.air = air
        
    def toonKilledCogs(self, toon, suits, zoneId):
        status = list(toon.getCogStatus()[:])
        count = list(toon.getCogCount()[:])
        
        for suit in suits:
            if not suit.get('type'):
                continue
                
            index = SuitDNA.suitHeadTypes.index(suit['type'])
            
            st = COG_DEFEATED
            trackIdx = index % 8
            
            count[index] = min(count[index] + 1, self.quotas[0][trackIdx] if self.maxCogs == -1 else self.maxCogs)
            
            if count[index] >= self.quotas[1][trackIdx]:
                st = COG_COMPLETE2
                
            elif count[index] >= self.quotas[0][trackIdx]:
                st = COG_COMPLETE1
                
            status[index] = st
            
        toon.b_setCogStatus(status)
        toon.b_setCogCount(count)
        
        self.considerUpdateRadar(toon)
        
    def toonEncounteredCogs(self, toon, suits, zoneId):
        status = list(toon.getCogStatus()[:])
        
        for suit in suits:
            if not suit.get('type'):
                continue
                
            index = SuitDNA.suitHeadTypes.index(suit['type'])
            status[index] = max(COG_BATTLED, status[index])
            
        toon.b_setCogStatus(status)
        
    def considerUpdateRadar(self, toon):
        cogRadar = list(toon.getCogRadar()[:])
        bldgRadar = list(toon.getBuildingRadar()[:])
        count = toon.getCogCount()
        
        for dept in xrange(4):
            cogRadar[dept] = all(c >= self.quotas[0][i] for i, c in enumerate(count[dept:dept + 8]))
            bldgRadar[dept] = all(c >= self.quotas[1][i] for i, c in enumerate(count[dept:dept + 8]))
        
        toon.b_setCogRadar(cogRadar)
        toon.b_setBuildingRadar(bldgRadar)
        
    def maxCogGallery(self, toon):
        toon.b_setCogCount([self.maxCogs] * 32 if self.maxCogs != -1 else self.quotas[1])
        toon.b_setCogStatus([COG_COMPLETE2] * 32)
        self.considerUpdateRadar(toon)
        
    def avarageCogGallery(self, toon):
        count = []
        status = []
        
        for i in xrange(32):
            trackIdx = i % 8
            
            _max = self.quotas[1][trackIdx] if self.maxCogs == -1 else min(self.maxCogs, 100)
            
            ct = random.randint(0, _max)
            
            st = COG_BATTLED if ct else COG_UNSEEN
            
            if ct >= self.quotas[1][trackIdx]:
                st = COG_COMPLETE2
                
            elif ct >= self.quotas[0][trackIdx]:
                st = COG_COMPLETE1
                
            count.append(ct)
            status.append(st)
            
        toon.b_setCogCount(count)
        toon.b_setCogStatus(status)
        self.considerUpdateRadar(toon)
        
from otp.ai.MagicWordGlobal import *

@magicWord(category=CATEGORY_CHARACTERSTATS)
def maxGallery():
    simbase.air.cogPageManager.maxCogGallery(spellbook.getInvoker())
    return "Maxed your gallery!"
    
@magicWord(category=CATEGORY_CHARACTERSTATS)
def avGallery():
    simbase.air.cogPageManager.avarageCogGallery(spellbook.getInvoker())
    return "Made your gallery avarage!"
    