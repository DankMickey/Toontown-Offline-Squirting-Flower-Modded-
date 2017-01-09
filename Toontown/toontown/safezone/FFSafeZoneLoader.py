from pandac.PandaModules import *
import SafeZoneLoader
import FFPlayground
from direct.fsm import State
from toontown.char import CharDNA
from toontown.char import Char
from toontown.toonbase import ToontownGlobals
from direct.interval.IntervalGlobal import *

class FFSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    ALLOW_GEOM_FLATTEN = False
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = FFPlayground.FFPlayground
        self.musicFile = 'phase_14/audio/bgm/FF_nbrhood.ogg'
        self.activityMusicFile = 'phase_14/audio/bgm/FF_SZ_activity.ogg'
        self.dnaFile = 'phase_14/dna/funny_farm_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_14/dna/storage_FF_sz.dna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.mp3',
         'phase_4/audio/sfx/SZ_TC_bird2.mp3', 'phase_4/audio/sfx/SZ_TC_bird3.mp3'])
        goldenbean = self.createGoldenBean(base.cr.playGame.hood.loader.geom)
        goldenbean.setPosHpr(-127,72,0,46,0,0)

    def unload(self):
        del self.birdSound
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def createGoldenBean(self, parentId):
        facade = loader.loadModel("phase_3.5/models/modules/facade_bN.bam")
        facade.reparentTo(parentId)
        facade.find('**/showcase').setTwoSided(1)
        goldenbean = loader.loadModel("phase_4/models/props/jellybean4.bam")
        goldenbean.reparentTo(facade)
        goldenbean.setPos(0,-1.5,4)
        goldenbean.setHpr(90,0,0)
        goldenbean.setScale(5)
        goldenbean.setBillboardAxis(1.5);goldenbean.setColor(1,0.9,0)
        glow = loader.loadModel("phase_3.5/models/props/glow.bam")
        glow.reparentTo(facade)
        glow.setPos(0,-1.37,4.1);glow.setScale(3)
        glow.setBillboardAxis(1.65)
        glow.setColor(1,0.9,0)
        Sequence(goldenbean.hprInterval(3,Point3(0,0,0),startHpr=Point3(360,0,0)), name="spin").loop()
        return facade
        