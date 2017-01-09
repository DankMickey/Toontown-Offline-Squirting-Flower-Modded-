from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import random

class ToontownLoadingScreen():
    __module__ = __name__

    def __init__(self):
        self.__expectedCount = 0
        self.__count = 0
        self.screen = loader.loadModel('phase_3/models/gui/progress-background')
        self.gui = self.screen.find('**/bg')
        self.banner = loader.loadModel('phase_3.5/models/gui/stickerbook_gui').find('**/paper_note')
        self.banner.reparentTo(self.gui)
        self.banner.setScale(1.15, 1.0, 1.0)
        self.banner.setZ(-0.13)
        
        self.tip = DirectLabel(guiId='ToontownLoadingScreenTip', parent = self.banner, relief = None,
                                 text='', text_scale = TTLocalizer.TLStip, textMayChange = 1, pos=(-0.41, 0.0, 0.235),
                                 text_fg = (0.4, 0.3, 0.2, 1), text_wordwrap = 9, text_align = TextNode.ALeft)
                                 
        self.title = DirectLabel(guiId = 'ToontownLoadingScreenTitle', parent = self.gui, relief = None,
                                 pos = (-1.06, 0, -0.77), text = '', textMayChange = 1, text_scale = 0.08,
                                 text_fg = (1, .9, 0, 1), text_align = TextNode.ALeft,
                                 text_font = ToontownGlobals.getToonFont())
                                 
        self.waitBar = DirectWaitBar(guiId = 'ToontownLoadingScreenWaitBar', parent = self.gui,
                                     frameSize = (-1.06, 1.06, -0.03, 0.03), pos = (0, 0, -0.85),
                                     text = '')
                                     
        self.logo = OnscreenImage('phase_3/maps/toontown-logo.png')
        self.logo.reparentTo(self.gui)
        self.logo.setScale(self.gui, (0.53,1,0.35))
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.setZ(0.73)

    def destroy(self):
        self.tip.destroy()
        self.title.destroy()
        self.waitBar.destroy()
        self.gui.removeNode()

    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + '\n' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def begin(self, range, label, gui, tipCategory):
        self.waitBar['range'] = range
        self.title['text'] = label
        self.tip['text'] = self.getTip(tipCategory)
        self.__count = 0
        self.__expectedCount = range
        if gui:
            self.waitBar.reparentTo(self.gui)
            self.title.reparentTo(self.gui)
            self.gui.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        else:
            self.waitBar.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.title.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.gui.reparentTo(hidden)
        self.waitBar.update(self.__count)

    def end(self):
        self.waitBar.finish()
        self.waitBar.reparentTo(self.gui)
        self.title.reparentTo(self.gui)
        self.gui.reparentTo(hidden)
        return (self.__expectedCount, self.__count)

    def abort(self):
        self.gui.reparentTo(hidden)

    def tick(self):
        self.__count = self.__count + 1
        self.waitBar.update(self.__count)
