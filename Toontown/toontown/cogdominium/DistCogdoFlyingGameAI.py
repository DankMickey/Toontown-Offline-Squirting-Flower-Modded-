from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
import CogdoFlyingGameGlobals as Globals

class DistCogdoFlyingGameAI(DistCogdoGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistCogdoFlyingGameAI")
    
    def __init__(self, air):
        DistCogdoGameAI.__init__(self, air)
        self.completed = []
        self.eagles = {}
        
    def requestAction(self, action, data):
        avId = self.air.getAvatarIdFromSender()
                                                
        if action == Globals.AI.GameActions.LandOnWinPlatform:
            self.completed.append(avId)
            for toon in self.toons:
                if toon not in self.completed:
                    return
                    
            self.gameDone()
            
        elif action == Globals.AI.GameActions.BladeLost:
            self.sendUpdate("toonBladeLost", [avId])
            
        elif action == Globals.AI.GameActions.SetBlades:
            self.sendUpdate("toonSetBlades", [avId, data])
            
        elif action == Globals.AI.GameActions.Died:
            self.sendUpdate("toonDied", [avId, globalClockDelta.getRealNetworkTime()])
            
        elif action == Globals.AI.GameActions.Spawn:
            self.sendUpdate("toonSpawn", [avId, globalClockDelta.getRealNetworkTime()])
            
        elif action == Globals.AI.GameActions.RequestEnterEagleInterest:
            if not self.eagles.get(data):
                self.eagles[data] = avId
                self.sendUpdate("toonSetAsEagleTarget", [avId, data, globalClockDelta.getRealNetworkTime()])
                
        elif action == Globals.AI.GameActions.RequestExitEagleInterest:
            if self.eagles.get(data) == avId:
                self.eagles[data] = 0
                self.sendUpdate("toonClearAsEagleTarget", [avId, data, globalClockDelta.getRealNetworkTime()])

    def requestPickUp(self, pickupNum, pickupType):
        avId = self.air.getAvatarIdFromSender()
        if pickupType == 1:
            self.sendUpdate("pickUp", [avId, 1, globalClockDelta.getRealNetworkTime()])
