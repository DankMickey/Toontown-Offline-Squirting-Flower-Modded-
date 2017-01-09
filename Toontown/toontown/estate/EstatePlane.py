import math
from panda3d.core import NodePath, TextNode
from toontown.toonbase import TTLocalizer, ToontownGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
 
class EstatePlane:
 
    def __init__(self):
        self.airplane = None
        self.theta = 0
        self.phi = 0
 
    def startAirplane(self):
        self.loadAirplane()
        self.__startAirplaneTask()
 
    def startWitch(self):
        self.loadWitch()
        self.__startAirplaneTask()
 
    def loadAirplane(self):
        self.airplane = loader.loadModel('phase_4/models/props/airplane.bam')
        self.airplane.setScale(4)
        self.airplane.setPos(0, 0, 1)
        self.banner = self.airplane.find('**/*banner')
        bannerText = TextNode('bannerText')
        bannerText.setTextColor(1, 0, 0, 1)
        bannerText.setAlign(bannerText.ACenter)
        bannerText.setFont(ToontownGlobals.getSignFont())
        bannerText.setText(TTLocalizer.EstatePlaneReturn)
        self.bn = self.banner.attachNewNode(bannerText.generate())
        self.bn.setHpr(180, 0, 0)
        self.bn.setPos(-5.8, 0.1, -0.25)
        self.bn.setScale(0.95)
        self.bn.setDepthTest(1)
        self.bn.setDepthWrite(1)
        self.bn.setDepthOffset(500)
        base.airplane = self.airplane
 
    def loadWitch(self):
        self.airplane = loader.loadModel('phase_4/models/props/tt_m_prp_ext_flyingWitch.bam')
        self.airplane.setScale(2)
        self.airplane.setPos(0, 0, 1)
        self.airplane.find('**/').setH(180)
        bannerText = TextNode('bannerText')
        bannerText.setTextColor(1, 0, 0, 1)
        bannerText.setAlign(bannerText.ACenter)
        bannerText.setFont(ToontownGlobals.getSignFont())
        bannerText.setText(TTLocalizer.EstatePlaneHoliday)
        self.bn = self.airplane.attachNewNode(bannerText.generate())
        self.bn.setPos(-20.0, -.1, 0)
        self.bn.setH(180)
        self.bn.setScale(2.35)
        self.bn.setDepthTest(1)
        self.bn.setDepthWrite(1)
        self.bn.setDepthOffset(500)
        base.airplane = self.airplane
 
    def unloadWitch(self):
        self.airplane.reparentTo(hidden)
        del self.airplane
        self.loadAirplane()
 
    def __startAirplaneTask(self):
        self.theta = 0
        self.phi = 0
        taskMgr.remove('estate-airplane')
        taskMgr.add(self.airplaneFlyTask, 'estate-airplane')
 
    def __pauseAirplaneTask(self):
        pause = 45
        self.phi = 0
        self.theta = (self.theta + 10) % 360
        taskMgr.remove('estate-airplane')
        taskMgr.doMethodLater(pause, self.airplaneFlyTask, 'estate-airplane')
 
    def __killAirplaneTask(self):
        taskMgr.remove('estate-airplane')
 
    def airplaneFlyTask(self, Task):
        rad = 300.0
        amp = 80.0
        self.theta += 0.25
        self.phi += 0.005
        sinPhi = math.sin(self.phi)
        if sinPhi <= 0:
            self.__pauseAirplaneTask()
        angle = math.pi * self.theta / 180.0
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        z = amp * sinPhi
        hood = base.cr.playGame.hood
        if hasattr(hood, 'loader'):
            geom = hood.loader.geom
        else:
            return
        self.airplane.reparentTo(geom)
        self.airplane.setH(90 + self.theta)
        self.airplane.setPos(x, y, z)
        return Task.cont
 
    def removeAirplane(self):
        if not self.airplane.isEmpty():
            self.airplane.removeNode()
        del self.airplane
        del base.airplane
        self.__killAirplaneTask()