from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import ToontownGlobals, TTLocalizer as TTL
from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toontowngui import TTDialog

MaxCustomToonsPerAccount = 3

# xxx to do: localizer
T_TITLE = "Where do you wanna start?"
T_HELP = "Help"
T_HELP_CONTENT = "Use this tool to start your Toon in another playground other than Toontown Central. \
                 This way you can grow faster and have more fun, exploring more advanced things!"
T_TTC = TTL.lToontownCentral + "\n15 laff\nCarry 20 gags\nCarry 1 toontask\nCarry 40 jellybeans\n2 gag tracks"
T_DD = TTL.lDonaldsDock + "\n25 laff\nCarry 25 gags\nCarry 2 toontask\nCarry 50 jellybeans\n3 gag tracks"
T_DG = TTL.lDaisyGardens + "\n34 laff\nCarry 30 gags\nCarry 2 toontask\nCarry 60 jellybeans\n4 gag tracks"
T_MM = TTL.lMinniesMelodyland + "\n43 laff\nCarry 35 gags\nCarry 3 toontask\nCarry 80 jellybeans\n4 gag tracks\n1 sellbot suit part"
T_GAG_START = "You selected %s. Press OK to choose the gag tracks or cancel to select another hood."
T_GAG_TITLE = "Select your gag tracks"
T_STATUS = "You selected %s.", "You selected %s and %s."
T_NEXT = TTL.MakeAToonDone

class CustomStatePanel(DirectFrame):
    doneEvent = 'CustomStatePanel-done'
    
    def __init__(self):
        DirectFrame.__init__(self, frameColor=(.3, .2, .6, 1), frameSize=(.4, -1.2, .8, -.8))
        self.initialiseoptions(CustomStatePanel)
        
        self._font = ToontownGlobals.getToonFont()
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop')
        self.squareUp = gui.find('**/tt_t_gui_mat_namePanelSquareUp')
        self.squareDown = gui.find('**/tt_t_gui_mat_namePanelSquareDown')
        self.squareHover = gui.find('**/tt_t_gui_mat_namePanelSquareHover')
        
        self.title = OnscreenText(parent=self, text=T_TITLE, pos=(-.4, .7), scale=.085, font=self._font)
        self.screen1 = self.attachNewNode('screen1')
        
        self.__hood = -1        
        self.__trackChoice = [-1, -1]
        
        DirectButton(parent=self.screen1, text_scale=.075, text=T_HELP, pos=(-.4, 0, .6), relief=None, text_font=self._font, 
                     image=(self.squareUp, self.squareDown, self.squareHover, self.squareUp), text_pos=(0, -.02), command=self.__help)
        DirectButton(parent=self.screen1, scale=.075, text=T_TTC, pos=(-.8, 0, .45), relief=None, text_font=self._font,
                     command=self.__hoodChosen, extraArgs=[0])
        DirectButton(parent=self.screen1, scale=.075, text=T_DD, pos=(0, 0, .45), relief=None, text_font=self._font,
                     command=self.__hoodChosen, extraArgs=[1])
        DirectButton(parent=self.screen1, scale=.075, text=T_DG, pos=(-.8 if config.GetBool('csp-want-mm', False) else -.4, 0, -.2), relief=None, text_font=self._font,
                     command=self.__hoodChosen, extraArgs=[2])
        if config.GetBool('csp-want-mm', False):
            DirectButton(parent=self.screen1, scale=.075, text=T_MM, pos=(0, 0, -.2), relief=None, text_font=self._font,
                         command=self.__hoodChosen, extraArgs=[3])
        
    def __help(self):
        helpDialog = TTDialog.TTGlobalDialog(message=T_HELP_CONTENT, style=TTDialog.Acknowledge, fadeScreen=.8, doneEvent='helpdone')
        helpDialog.show()
        self.acceptOnce('helpdone', helpDialog.cleanup)
        
    def __hoodChosen(self, index):
        self.__hood = index
        self.screen1.stash()
        if index != 0:
            self.createGagDialog()
            
        else:
            self.done()
        
    def createGagDialog(self):
        hoodName = [TTL.lToontownCentral, TTL.lDonaldsDock, TTL.lDaisyGardens, TTL.lMinniesMelodyland][self.__hood]
        gagDialog = TTDialog.TTGlobalDialog(message=T_GAG_START % hoodName, style=TTDialog.TwoChoice, fadeScreen=1, doneEvent='gagdone')
        gagDialog.show()
        def _c():
            choice = gagDialog.doneStatus
            gagDialog.cleanup()
            
            if choice == 'cancel':
                self.screen1.unstash()
                
            else:
                self.createGagScreen()
            
        self.acceptOnce('gagdone', _c)
        
    def createGagScreen(self):
        self.title.setText(T_GAG_TITLE)
        
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        
        toonupGeom = invModel.find('**/' + AvPropsNew[HEAL_TRACK][5])
        soundGeom = invModel.find('**/' + AvPropsNew[SOUND_TRACK][3])
        
        b1 = DirectButton(text = Tracks[HEAL_TRACK].capitalize(), text_scale=0.075, pos=(-0.2, 0, .5), text_font=self._font,
                          image=toonupGeom, relief=None, text_pos=(.23, 0), scale=1.5, parent=self)
        b2 = DirectButton(text = Tracks[SOUND_TRACK].capitalize(), text_scale=0.075, pos=(-0.6, 0, .5), text_font=self._font,
                          image=soundGeom, relief=None, text_pos=(-.23, 0), scale=1.5, parent=self)
    
        lureGeom = invModel.find('**/' + AvPropsNew[LURE_TRACK][0])
        dropGeom = invModel.find('**/' + AvPropsNew[DROP_TRACK][4])
        
        if self.__hood > 1:
            b3 = DirectButton(text = Tracks[LURE_TRACK].capitalize(), text_scale=0.075, pos=(-0.2, 0, 0), text_font=self._font,
                              image=lureGeom, relief=None, text_pos=(.23, 0), scale=1.5, parent=self)
            b4 = DirectButton(text = Tracks[DROP_TRACK].capitalize(), text_scale=0.075, pos=(-0.6, 0, 0), text_font=self._font,
                              image=dropGeom, relief=None, text_pos=(-.23, 0), scale=1.5, parent=self)
                          
        else:
            b3 = None
            b4 = None
                          
        self.__trackButtons = [b1, b2, b3, b4]
        for i in xrange(len(self.__trackButtons)):
            b = self.__trackButtons[i]
            if b:
                b['command'] = self.__trackChosen
                b['extraArgs'] = [i]
            
        self.__statusText = OnscreenText(parent=self, scale=.075, text='', pos=(-.4, -.45))
        self.__nextButton = DirectButton(parent=self, text_scale=.075, text=T_NEXT, pos=(-.4, 0, -.6), relief=None, text_font=self._font, 
                                         image=(self.squareUp, self.squareDown, self.squareHover, self.squareUp),
                                         text_pos=(0, -.02), command=self.done)
                                         
        self.__nextButton.hide()
            
    def __trackChosen(self, index):
        a = index // 2
        b = [HEAL_TRACK, SOUND_TRACK, LURE_TRACK, DROP_TRACK][index]
        self.__trackChoice[a] = b
        
        if self.__allChosen():
            t = T_STATUS[not self.__hood < 2]
            if self.__hood < 2:
                t %= Tracks[self.__trackChoice[0]].capitalize()
                
            else:
                t %= (Tracks[self.__trackChoice[0]].capitalize(), Tracks[self.__trackChoice[1]].capitalize())
                
            self.__statusText.setText(t)
            self.__nextButton.show()
        
    def __allChosen(self):
        if self.__hood < 2:
            return self.__trackChoice[0] != -1
            
        return -1 not in self.__trackChoice
        
    def done(self):
        messenger.send(self.doneEvent, [self.__hood, self.__trackChoice])
        