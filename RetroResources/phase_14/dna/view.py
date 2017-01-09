import sys
from panda3d.core import *

loadPrcFileData('', 'want-directtools #t')

import direct.directbase.DirectStart

sys.path.append('../../..')
getModelPath().appendDirectory('../..')

mode = "7100"
if len(sys.argv) > 1:
    mode = sys.argv[1]

from libpandadna import DNAStorage, DNALoader
s = DNAStorage.DNAStorage()
ld = DNALoader.DNALoader()

def load(x):
    return ld.loadDNAFile(s, x)
    
load('../../phase_4/dna/storage.pdna')
load('../../phase_5/dna/storage_town.pdna')
load('storage_FF.pdna')
load('storage_FF_%s.pdna' % ("sz" if mode == "sz" else "town"))
m = load('funny_farm_%s.pdna' % mode)
dnaEnviron = render.attachNewNode('dna_render')
m.reparentTo(dnaEnviron)
base.disableMouse()

if mode == "7100":
    base.cam.setPos(0, -150, 10)
    base.cam.setH(0)

base.oobe()

class DistributedSuitPlanner:
    def __init__(self):
        self.suitWalkSpeed = 5
        self.dnaStore = s
        self.pointIndexes = {}
        self.pathViz = None

    def hidePaths(self):
        if self.pathViz:
            self.pathViz.detachNode()
            self.pathViz = None
        return

    def showPaths(self):
        self.hidePaths()
        vizNode = GeomNode(self.uniqueName('PathViz'))
        lines = LineSegs()
        self.pathViz = render.attachNewNode(vizNode)
        points = self.frontdoorPointList + self.sidedoorPointList + self.cogHQDoorPointList + self.streetPointList
        while len(points) > 0:
            self.__doShowPoints(vizNode, lines, None, points)

        cnode = CollisionNode('battleCells')
        cnode.setCollideMask(BitMask32.allOff())
        for zoneId, cellPos in self.battlePosDict.items():
            cnode.addSolid(CollisionSphere(cellPos, 9))
            text = '%s' % zoneId
            self.__makePathVizText(text, cellPos[0], cellPos[1], cellPos[2] + 9, (1, 1, 1, 1))

        self.pathViz.attachNewNode(cnode).show()
        return

    def __doShowPoints(self, vizNode, lines, p, points):
        if p == None:
            pi = len(points) - 1
            if pi < 0:
                return
            p = points[pi]
            del points[pi]
        else:
            if p not in points:
                return
            pi = points.index(p)
            del points[pi]
        text = '%s' % p.getIndex()
        pos = p.getPos()
        if p.getPointType() == 1:#DNASuitPoint.FRONTDOORPOINT:
            color = (1, 0, 0, 1)
        elif p.getPointType() == 2:#DNASuitPoint.SIDEDOORPOINT:
            color = (0, 0, 1, 1)
        else:
            color = (0, 1, 0, 1)
        self.__makePathVizText(text, pos[0], pos[1], pos[2], color)
        adjacent = self.dnaStore.getAdjacentPoints(p)
        numPoints = adjacent.getNumPoints()
        for i in range(numPoints):
            qi = adjacent.getPointIndex(i)
            q = self.dnaStore.getSuitPointWithIndex(qi)
            pp = p.getPos()
            qp = q.getPos()
            v = Vec3(qp - pp)
            v.normalize()
            c = v.cross(Vec3.up())
            p1a = pp + v * 2 + c * 0.5
            p1b = pp + v * 3
            p1c = pp + v * 2 - c * 0.5
            lines.reset()
            lines.moveTo(pp)
            lines.drawTo(qp)
            lines.moveTo(p1a)
            lines.drawTo(p1b)
            lines.drawTo(p1c)
            lines.create(vizNode, 0)
            self.__doShowPoints(vizNode, lines, q, points)

        return

    def __makePathVizText(self, text, x, y, z, color):
        if not hasattr(self, 'debugTextNode'):
            self.debugTextNode = TextNode('debugTextNode')
            self.debugTextNode.setAlign(TextNode.ACenter)
        self.debugTextNode.setTextColor(*color)
        self.debugTextNode.setText(text)
        np = self.pathViz.attachNewNode(self.debugTextNode.generate())
        np.setPos(x, y, z + 4)
        np.setScale(1.0)
        np.setBillboardPointEye(2)
        np.node().setAttrib(TransparencyAttrib.make(TransparencyAttrib.MDual), 2)
        
    def setupDNA(self):
        self.initDNAInfo()
        return None

    def extractGroupName(self, groupFullName):
        return str(groupFullName).split(':', 1)[0]

    def initDNAInfo(self):
        numGraphs = self.dnaStore.discoverContinuity()
        if numGraphs != 1:
            print('zone %s has %s disconnected suit paths.' % (self.zoneId, numGraphs))
        self.battlePosDict = {}
        self.cellToGagBonusDict = {}
        for i in range(self.dnaStore.getNumDNAVisGroupsAI()):
            vg = self.dnaStore.getDNAVisGroupAI(i)
            zoneId = int(self.extractGroupName(vg.getName()))
            if vg.getNumBattleCells() == 1:
                battleCell = vg.getBattleCell(0)
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()
            elif vg.getNumBattleCells() > 1:
                self.notify.warning('multiple battle cells for zone: %d' % zoneId)
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()

        self.dnaStore.resetDNAGroups()
        self.dnaStore.resetDNAVisGroups()
        self.dnaStore.resetDNAVisGroupsAI()
        self.streetPointList = []
        self.frontdoorPointList = []
        self.sidedoorPointList = []
        self.cogHQDoorPointList = []
        numPoints = self.dnaStore.getNumSuitPoints()
        for i in range(numPoints):
            point = self.dnaStore.getSuitPointAtIndex(i)
            
            if point.getPointType() == 1:#DNASuitPoint.FRONTDOORPOINT:
                self.frontdoorPointList.append(point)
                
            elif point.getPointType() == 2:#DNASuitPoint.SIDEDOORPOINT:
                self.sidedoorPointList.append(point)
                
            elif point.getPointType() >= 3:#== DNASuitPoint.COGHQINPOINT or point.getPointType() == DNASuitPoint.COGHQOUTPOINT:
                self.cogHQDoorPointList.append(point)
                
            else:
                self.streetPointList.append(point)
                
            self.pointIndexes[point.getIndex()] = point

        return None

    def performPathTest(self):
        startAndEnd = self.pickPath()
        if not startAndEnd:
            return None
        startPoint = startAndEnd[0]
        endPoint = startAndEnd[1]
        path = self.dnaStore.getSuitPath(startPoint, endPoint)
        numPathPoints = path.getNumPoints()
        for i in range(numPathPoints - 1):
            zone = self.dnaStore.getSuitEdgeZone(path.getPointIndex(i), path.getPointIndex(i + 1))
            travelTime = self.dnaStore.getSuitEdgeTravelTime(path.getPointIndex(i), path.getPointIndex(i + 1), self.suitWalkSpeed)
            print('edge from point ' + `i` + ' to point ' + `(i + 1)` + ' is in zone: ' + `zone` + ' and will take ' + `travelTime` + ' seconds to walk.')

        return None

    def genPath(self, startPoint, endPoint, minPathLen, maxPathLen, overrideStreetOnly = None):
        if overrideStreetOnly is None:
            overrideStreetOnly = self.gspStreetOnly
            
        return self.dnaStore.getSuitPath(startPoint, endPoint, minPathLen, maxPathLen, overrideStreetOnly)

    def getDnaStore(self):
        return self.dnaStore
        
    def uniqueName(self, x):
        return x

pl = DistributedSuitPlanner()
pl.setupDNA()
pl.showPaths()

def gp(a, b):
    print pl.genPath(s.getSuitPointWithIndex(a), s.getSuitPointWithIndex(b), 40, 300, False)
    
class Hood:
    def makeMask(self,wall,parent): 
        toMask = wall.find("**/wall_collide")
        toMask.node().setFromCollideMask(BitMask32(8))
        toMask.reparentTo(parent)
        
    def placewall(self, pos, type, h, width, height, color):
        wallm = loader.loadModel("phase_3.5/models/modules/walls.bam")
        wall = wallm.find("**/"+type)
        wall.reparentTo(render)
        wall.setPos(pos)
        wall.setH(h)
        wall.setSz(height)
        wall.setSx(width)
        wall.setColor(color)
        self.makeMask(wallm,wall)
        return wall

#wall1 = Hood().placewall((48, -75.5, 0),"wall_lg_brick_ur",193,20,10,(0.5, 0.9, 0.33, 1))
#wall2 = Hood().placewall((48, -75.5, 10),"wall_lg_brick_ur",193,20,10,(0.5, 0.9, 0.33, 1))

#wall3 = Hood().placewall((92, -67.5, 0),"wall_md_pillars_ul",-135,20,20,(1, 0.9, 0.73, 1))
 
run()
