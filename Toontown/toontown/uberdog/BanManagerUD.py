from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify import DirectNotifyGlobal
import urllib2

class BanManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerAI')
    BanUrl = simbase.config.GetString('ban-base-url', 'https://toontownhouse.net/api_ban')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.subscribed = {}
        
    def subscribe(self, avId, access):
        self.subscribed[avId] = access
        self.notify.info('Subscribed avatar %s with access %s' % (avId, access))
        
        dgcleanup = self.dclass.aiFormatUpdate("unsubscribe", self.doId, self.air.ourChannel, self.air.ourChannel, [avId])
        
        dg = PyDatagram()
        dg.addServerHeader(self.GetAccountConnectionChannel(self.avId), self.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.air.send(dg)
        
    def unsubscribe(self, avId):
        if avId in self.subscribed:
            self.notify.info('Unsubscribed avatar %s' % avId)
            del self.subscribed[avId]
            
        else:
            self.notify.warning('Tried to unsubscribe unknown avatar %s' % avId)
        
    def banUD(self, banner, accountId, time):
        # fetch username using CSM
        username = self.air.csm.getUsername(accountId)
        
        if username is None:
            self.notify.warning("Unknown accountId %s, cannot ban!" % accountId)
            return
            
        elif not username:
            self.notify.warning("accountId %s has no username, cannot ban (did you try to ban on local account?)" % accountId)
            return
            
        headers = {'User-Agent' : 'TTHBanManager'}
        data = "target=%s" % username
        data += "&time=%s" % time
        data += "&anticacheagent=%s" % id(username)
        req = urllib2.Request(self.BanUrl, data, headers)
        
        try:
            response = urllib2.urlopen(req)
            
        except:
            self.notify.warning('Failed to ban %s!' % username)
            return
            
        self.notify.info("%s banned %s for %s hours" % (banner, username, time))
        
        # to do: warning subscribed players about the ban
        