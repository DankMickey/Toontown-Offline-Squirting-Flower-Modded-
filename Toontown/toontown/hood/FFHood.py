from pandac.PandaModules import *
import ToonHood
import SkyUtil
from toontown.town import FFTownLoader
from toontown.safezone import FFSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class FFHood(ToonHood.ToonHood):
    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = FunnyFarm
        self.townLoaderClass = FFTownLoader.FFTownLoader
        self.safeZoneLoaderClass = FFSafeZoneLoader.FFSafeZoneLoader
        self.storageDNAFile = 'phase_14/dna/storage_FF.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_14/dna/winter_storage_FF.dna'],
         WACKY_WINTER_DECORATIONS: ['phase_14/dna/winter_storage_FF.dna'],
         HALLOWEEN_PROPS: ['phase_14/dna/halloween_props_storage_FF.dna'],
         SPOOKY_PROPS: ['phase_14/dna/halloween_props_storage_FF.dna']}
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (0.3, 0.6, 1.0, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('FFHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('FFHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        self.notify.debug('The sky is: %s' % self.sky)
        if not self.sky.getTag('sky') == 'Regular':
            self.endSpookySky()
        SkyUtil.startCloudSky(self)

    def startSpookySky(self):
        if hasattr(self, 'sky') and self.sky:
            self.stopSky()
        self.sky = loader.loadModel(self.spookySkyFile)
        self.sky.setTag('sky', 'Halloween')
        self.sky.setScale(1.0)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setColor(0.5, 0.5, 0.5, 1)
        self.sky.setBin('background', 100)
        self.sky.setFogOff()
        self.sky.reparentTo(camera)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.sky.colorScaleInterval(1.5, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0.25), blendType='easeInOut')
        fadeIn.start()
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)