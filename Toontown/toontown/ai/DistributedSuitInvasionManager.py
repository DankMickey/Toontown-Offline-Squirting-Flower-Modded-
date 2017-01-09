from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta

from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

from direct.directnotify import DirectNotifyGlobal

from toontown.battle.SuitBattleGlobals import SuitAttributes
from toontown.toonbase import TTLocalizer

InvasionStartMsg = (TTLocalizer.SuitInvasionBegin1, TTLocalizer.SuitInvasionBegin2)
InvasionEndMsg = (TTLocalizer.SuitInvasionEnd1, TTLocalizer.SuitInvasionEnd2)
InvasionProgressMsg = (TTLocalizer.SuitInvasionBulletin1, TTLocalizer.SuitInvasionBulletin2)

class DistributedSuitInvasionManager(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuitInvasionManager")
    deferFor = 7
    neverDisable = 1
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        
        self.startTime = 0
        self._name = ""
        self.waiter = False
        
        self.__msgs = []
        self.cr.DSIMgr = self
        
    def setCurrentInvasion(self, suitName, skel, waiter, startTime, duration):
        if duration == 0:
            self.notify.info('duration 0')
            return
            
        self.startTime = globalClockDelta.networkToLocalTime(startTime, bits = 32)
        elapsed = globalClock.getRealTime() - self.startTime
        remaining = duration - elapsed
        
        self.notify.info("Invasion in progress! Remaining time: %s" % remaining)
        
        self._name, msgs = self.formatInvasionMessage(suitName, skel, False, self.__formatProgress)
        self.displayMsgs(msgs)
        
    def startInvasion(self, suitName, skel, waiter, startTime, duration):            
        self.startTime = globalClockDelta.networkToLocalTime(startTime, bits = 32)
        
        self.notify.info("New invasion! Duration: %s" % duration)
        
        self._name, msgs = self.formatInvasionMessage(suitName, skel, waiter, self.__formatBegin)
        self.displayMsgs(msgs)
        
    def invasionOver(self):
        if not self._name:
            self.notify.warning("Got invasion over without invasion in progress!")
            return
            
        self.startTime = 0
        self.displayMsgs(self.__formatEnd(self._name))
        
        self._name = ""
        self.waiter = False
        
    def formatInvasionMessage(self, suitName, skel, waiter, func):
        if suitName:
            name = SuitAttributes[suitName]["pluralname"]
        
        elif skel:
            name = TTLocalizer.SkeletonP
        
        else:
            self.notify.warning("Cannot format invasion message!")
            return "", []
            
        return name, func(name)
            
    def __formatBegin(self, name):
        return InvasionStartMsg[0], InvasionStartMsg[1] % name
        
    def __formatProgress(self, name):
        return InvasionProgressMsg[0], InvasionProgessMsg[1] % name
        
    def __formatEnd(self, name):
        return InvasionEndMsg[0] % name, InvasionEndMsg[1]
        
    def __displaySingleMsg(self, task):
        msg = self.__msgs.pop(0)
        
        dg = PyDatagram()
        dg.addString(msg)
        dgi = PyDatagramIterator(dg)
        self.cr.handleSystemMessage(dgi)
        
        if self.__msgs:
            task.delayTime = 3
            return task.again
        
        else:
            return task.done
            
    def displayMsgs(self, msgList):
        self.__msgs.extend(msgList)
        
        tn = self.taskName('nextMsg')
        if not taskMgr.hasTaskNamed(tn):
            taskMgr.doMethodLater(0, self.__displaySingleMsg, tn)
        
    def delete(self):
        self.notify.warning('deleted')
        DistributedObject.delete(self)
        