from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.directnotify import DirectNotifyGlobal

from toontown.suit import SuitDNA

import random

class DistributedSuitInvasionManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuitInvasionManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        
        self.skel = False
        self.curInvading = None
        
        self.startTime = 0
        self.duration = 0
        
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        
    def getCurrentInvasion(self):
        name = self.curInvading or ""
        return (name, self.skel, False, self.startTime, self.duration)
        
    def getInvadingCog(self):
        return (self.curInvading, self.skel)
        
    def hasInvading(self):
        return self.skel or (self.curInvading != None)
        
    def startInvasion(self, suitName = None, skel = False):
        self.withdrawAllCogs()
        
        self.skel = skel
        self.curInvading = suitName if suitName != "" else None
        
        self.duration = int(random.random() * 600 + 300) # 5 - 15 mins
        self.startTime = globalClockDelta.localToNetworkTime(globalClock.getRealTime(), bits = 32)
        
        taskMgr.doMethodLater(self.duration, self.__stop, self.taskName('end-invasion'))
        
        self.sendUpdate("startInvasion", [suitName or "", skel, 0, self.startTime, self.duration])
        
        self.notify.info("Invasion started: %s (%s); duration = %s secs" % (suitName, skel, self.duration))
        messenger.send("startInvasion")
        
    def __stop(self, task = None):
        self.withdrawAllCogs()
        
        self.skel = False
        self.curInvading = None
        self.startTime = self.duration = 0
        
        self.sendUpdate("invasionOver", [])
        messenger.send("endInvasion")
        
        if task:
            self.notify.info("Invasion is over")
            return task.done
            
    def withdrawAllCogs(self):
        for planner in self.air.suitPlanners.values():
            planner.flySuits()
            
    def abort(self):
        self.notify.info("Invasion aborted")
        taskMgr.remove(self.taskName('end-invasion'))
        self.__stop(None)
            
from otp.ai.MagicWordGlobal import *
@magicWord(types = [int], access = 400)
def invasion(index = -1):
    dsi = simbase.air.suitInvasionManager
    
    if not -1 <= index <= 31:
        return "Invalid value! Must be between -1 (stop inv) and 31!"
        
    if index == -1:
        if not dsi.hasInvading():
            return "No invasion in progress!"
            
        else:
            dsi.abort()
    
    else:
        if dsi.hasInvading():
            return "An invasion is already progress! Use ~invasion -1 to stop it!"
            
        else:
            dsi.startInvasion(SuitDNA.suitHeadTypes[index])

@magicWord(access = 500)
def invasionext():
    dsi = simbase.air.suitInvasionManager
        
    if dsi.hasInvading():
        return "An invasion is already progress! Use ~invasion -1 to stop it!"
            
    dsi.startInvasion(suitName = None, skel = True)
    