from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
import __builtin__, os

class LocalizerAgentBase(DirectObject):
    language = None
    
    def getGagshopSign(self):
        return None
    
    def handleHookGSSign(self, geom, flatten=True):
        newSign = self.getGagshopSign()
        if newSign:
            gs = geom.find('**/*_gag_shop_DNARoot')
            if not gs.isEmpty():
                sign = gs.find('**/sign')
                if not sign.isEmpty():
                    newSignNP = loader.loadModel(newSign)
                    newSignNP.reparentTo(sign)
                    newSignNP.wrtReparentTo(sign.getParent())
                    sign.removeNode()
            
        if flatten:
            geom.flattenMedium()
        
    def handleHookGSSignInterior(self, geom):
        newSign = self.getGagshopSign()
        if newSign:
            sign = geom.find('**/sign')
            if not sign.isEmpty():
                newSignNP = loader.loadModel(newSign)
                newSignNP.reparentTo(sign.getParent())
                newSignNP.setPos(3, 28, 0)
                newSignNP.setH(180)
                newSignNP.setScale(.4)
                sign.removeNode()

    def findDNA(self, file):
        dir, filename = os.path.split(str(file))
        searchPath = DSearchPath()
        
        searchPath.appendDirectory(Filename(dir))
        
        searchPath.appendDirectory(Filename('resources/' + dir))
            
        dnaFile = Filename(filename)
        return self._doFind(dnaFile, searchPath)
        
    def _doFind(self, filename, searchPath):
        if not vfs.resolveFilename(filename, searchPath):
            raise IOError('Could not find %s' % filename)
            
        return filename

class LocalizerAgentEN(LocalizerAgentBase):
    language = "english"
        
class LocalizerAgentPT(LocalizerAgentBase):
    language = "portuguese"
    
    def getGagshopSign(self):
        return "phase_3.5/pt/GS_pt_sign"
        
    def findDNA(self, file):
        dir, filename = os.path.split(str(file))
        searchPath = DSearchPath()
        
        searchPath.appendDirectory('phase_3.5/pt/dna')
        searchPath.appendDirectory(Filename(dir))
        
        searchPath.appendDirectory(Filename('resources/phase_3.5/pt/dna'))
        searchPath.appendDirectory(Filename('resources/' + dir))
            
        dnaFile = Filename(filename)
        return self._doFind(dnaFile, searchPath)
        
def install(lang):
    if lang == "english":
        __builtin__.localizerAgent = LocalizerAgentEN()
        
    elif lang == "portuguese":
        __builtin__.localizerAgent = LocalizerAgentPT()
        
    else:
        print 'WARNING: Cannot find LocalizerAgent for', lang
        __builtin__.localizerAgent = LocalizerAgentEN()
        