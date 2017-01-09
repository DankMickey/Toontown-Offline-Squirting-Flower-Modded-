import Street

class FFStreet(Street.Street):
    """ FF streets are setup a la HQs and need visgroup interest stuff """
    
    Zone2InterestMap = {7101: (7101, 7150, 7151),
                        7102: (7101, 7150, 7152)}
                        
    def __init__(self, *args):
        Street.Street.__init__(self, *args)
        self.interests = []
    
    def __removeAllInterests(self):
        map(base.cr.removeInterest, self.interests)
        self.interests = []
    
    def doEnterZone(self, newZoneId):
        if newZoneId != self.zoneId:
            self.__removeAllInterests()
            for z in FFStreet.Zone2InterestMap.get(newZoneId, []):
                self.interests.append(base.cr.addInterest(localAvatar.defaultShard, z, 'ff-street-%d' % z))
            
        Street.Street.doEnterZone(self, newZoneId)
        
    def enterZoneStreetBattle(self, newZoneId):
        # ignore this
        return
        
    def exit(self):
        self.__removeAllInterests()
        Street.Street.exit(self)
