import sys
from panda3d.core import *
import direct.directbase.DirectStart
from direct.gui.DirectGui import *

getModelPath().appendDirectory('../..')

class X:
    i = 0
    k = None
    texts = []
    
def next(a=1):
    X.i += 1
    X.i %= len(x)
    
    if X.k and a:
        X.k.removeNode()
        
    X.k = aspect2d.attachNewNode("blah")
    v = x[X.i].copyTo(X.k)
    v.setScale(.5)
    
    Xv = (-.75, -.25, .25, .75)[X.i % 4]
    X.texts[X.i % 4].setText(v.getName()[5:])
    
    v.setPos(Xv, 0, 0)
    
    if a:
        next(0)
        next(0)
        next(0)

w = loader.loadModel('phase_3.5/models/modules/walls.bam')
x = w.findAllMatches('**/wall_*_*_??')

X.texts.append(OnscreenText(text="", scale=.05, pos=(-.75, -.2)))
X.texts.append(OnscreenText(text="", scale=.05, pos=(-.25, -.2)))
X.texts.append(OnscreenText(text="", scale=.05, pos=(.25, -.2)))
X.texts.append(OnscreenText(text="", scale=.05, pos=(.75, -.2)))

next()

base.accept('space', next)
base.disableMouse()
base.cam.setPos(0, -70, 10)
base.oobe()
render.setTwoSided(1)
run()
