from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
import webbrowser, random, time

class TTHLauncherGUI(DirectObject):
    launcherPhase = 'phase_3'

    def __init__(self, launcher):
        self.launcher = launcher
        self.popup = None
        
        self.background = OnscreenImage(image = self.launcherPhase + '/maps/launcher_bg.jpg', parent = hidden, scale=(1.5,1,1))
        self.gui = aspect2d.attachNewNode('Gui')
        self.gui.hide()
        self.loginGui = self.gui.attachNewNode('LoginGui')
        
        font = loader.loadFont(self.launcherPhase + '/models/fonts/ImpressBT.ttf')
        
        self.logo = OnscreenImage(image = self.launcherPhase + '/maps/toontown-logo-new.png', parent = hidden, scale = (1,1,.5))
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        
        self.userInput = DirectEntry(parent = self.loginGui, color=(255,255,255,1), pos = (-3,0,0),
                                        scale = (.1,1,.130), text_scale = (.5,.4), width = 16,
                                        initialText=OTPLocalizer.CreateAccountScreenUserName,
                                        state = DGG.NORMAL)
        self.passInput = DirectEntry(parent = self.loginGui, color=(255,255,255,1), pos = (3,0,-.150),
                                        scale = (.1,1,.130), text_scale = (.5,.4), width = 16,
                                        initialText=TTLocalizer.AvatarChoicePassword,
                                        state = DGG.NORMAL)
        self.userInput.bind(DGG.B1PRESS, self.__handleInputClick, [0])
        self.passInput.bind(DGG.B1PRESS, self.__handleInputClick, [1])
        
        buttGui = loader.loadModel(self.launcherPhase + '/models/gui/tt_m_gui_mat_mainGui.bam')
        buttUp = buttGui.find('**/tt_t_gui_mat_shuffleUp*')
        buttDown = buttGui.find('**/tt_t_gui_mat_shuffleDown*')
        
        self.loginButton = DirectButton(parent=self.loginGui, scale=.8, geom=(buttUp,buttUp,buttDown), relief=None,
                                        text='Login', text_scale=.1, text_font=font,text_pos=(0,-.030),
                                        text_fg=(255,255,255,1), command=self.__doLogin)
        self.loginButton.setZ(-2)
        
        # Buttons
        self.buttonsNode = self.loginGui.attachNewNode('ButtonsNode')
        self.buttonsNode.setZ(-1)
        self.register = DirectButton(command=self.__url,extraArgs=[0],pos=(0,0,-.8),text=TTLocalizer.LauncherRegister,
                                     parent=self.buttonsNode,scale=.8, geom=(buttUp,buttUp,buttDown), relief=None,
                                     text_scale=.1, text_font=font, text_pos=(0,-.030),text_fg=(255,255,255,1))
        self.website = DirectButton(command=self.__url,extraArgs=[1],pos=(.4,0,-.8),text=TTLocalizer.LauncherWebsite,
                                    parent=self.buttonsNode,scale=.8, geom=(buttUp,buttUp,buttDown), relief=None,
                                    text_scale=.1, text_font=font, text_pos=(0,-.030),text_fg=(255,255,255,1))
        self.textPack = DirectButton(state=DGG.DISABLED,pos=(-.4,0,-.8),text=TTLocalizer.LauncherTextPack,
                                     parent=self.buttonsNode,scale=.8, geom=(buttUp,buttUp,buttDown), relief=None,
                                     text_scale=.1, text_font=font, text_pos=(0,-.030),text_fg=(255,255,255,1))

        self.lastNews = OnscreenText(text=self.launcher.getOnlineNews(),fg=(255,255,255,1),pos=(0,.940),parent=self.gui)
        
        X = 3
        self.newsSequence = self.lastNews.posInterval(15,(-X,0,self.lastNews.getZ()),startPos=(X,0,self.lastNews.getZ()))
        self.newsSequence.loop()
        
        self.__index = 0

        self.accept('enter', self.__doLogin)
        
        self.langButtons = []
        for i, lang in enumerate(('PT', 'EN')):
            geom = hidden.attachNewNode(CardMaker('button%s' % lang).generate())
            geom.setTexture(loader.loadTexture('phase_3/maps/Button%s.png' % lang))
            geom.setTransparency(1)
            bt = DirectButton(parent=self.gui, pos=(.75, 0, -.92 + i * .15), geom=geom, relief=None, scale=(.25, 1, .15),
                              command=launcher._handleChangeLang, extraArgs=[lang.lower()])
            self.langButtons.append(bt)
                
    def unload(self):
        self.background.removeNode()
        self.gui.removeNode()
        self.loginSelector.stop()
        if self.popup:
            self.popup.cleanup()
        
        del self.background
        del self.gui
        del self.loginSelector
        del self.popup
        
    def __url(self, i):
        links = {0:'http://toontownhouse.net/register',1:'http://toontownhouse.net'}
        webbrowser.open(links[i])
        
    def __handleInputClick(self, id, event):
        self.__index = id
        if id == 0:
            self.userInput.set('')
            self.userInput['focus'] = 1
            
        elif id == 1:
            self.passInput.set('')
            self.passInput['obscured'] = 1
            self.passInput['focus'] = 1
            
    def __handleTab(self):
        self.__index = (self.__index + 1) % 2
        self.__handleInputClick(self.__index, None)
            
    def show(self):
        self.gui.show()
        self.gui.unstash()
        self.background.unstash()
        self.accept('CleanupPopup', self.__handleCleanupPopup)
        self.accept('tab', self.__handleTab)
        
    def hide(self):
        self.gui.stash()
        self.background.stash()
        self.__handleCleanupPopup()
        self.ignoreAll()
        
    def start(self):
        self.background.reparentTo(render2d, sort=-5)
        self.logo.reparentTo(self.gui)
        self.logo.setColor(255,255,255,0)
        self.beginTransition()
        
    def beginTransition(self):
        T = 1.25
        logoFade = self.logo.colorInterval(T, (255,255,255,1))
        logoScale = self.logo.scaleInterval(T * .5, (.7,.7,.3))
        logoPos = self.logo.posInterval(T * .5, (0,0,.6))
        logoTrans = Parallel(logoPos, logoScale)
        loginPos = self.userInput.posInterval(T * .3, (-.4,0,0))
        passPos = self.passInput.posInterval(T * .3, (-.4,0,-.150))
        buttPos = self.loginButton.posInterval(T * .3, (0,0,-.3))
        buttsPos = self.buttonsNode.posInterval(T * .3, (0,0,0))
        inputTrans = Parallel(loginPos, passPos, buttPos, buttsPos)
        transSeq = Sequence(logoFade, logoTrans, inputTrans)
        transSeq.start()
        
    def serverError(self):
        if self.popup:
            self.popup.cleanup()
        self.popup = TTDialog.TTGlobalDialog(style=TTDialog.Acknowledge,message=TTLocalizer.LauncherServerError,doneEvent='CleanupPopup')
        self.popup.show()
        
    def authError(self):
        if self.popup:
            self.popup.cleanup()
        self.popup = TTDialog.TTGlobalDialog(style=TTDialog.Acknowledge,message=TTLocalizer.LauncherAuthError,doneEvent='CleanupPopup')
        self.popup.show()
        
    def __doLogin(self):
        self.popup = TTDialog.TTGlobalDialog(message=TTLocalizer.LauncherLoggingIn)
        self.popup.show()
        self.launcher.doLogin(self.userInput.get(), self.passInput.get())
        
    def __handleCleanupPopup(self):
        if self.popup:
            self.popup.cleanup()
            
    def cleanupPopup(self):
        if self.popup:
            self.popup.cleanup()
            
    def loadDownloadGui(self):
        self.loginGui.stash()
        self.downloadGui = self.gui.attachNewNode('DownloadGui')
        self.downloadBar = DirectWaitBar(text='0%', text_scale=.050, text_pos=(0,-.008), parent=self.downloadGui,
                                         frameSize=(-.6,.6,-.030,.030), frameColor=(1,1,1,.4),
                                         barColor=(0,.2,1,.6), borderWidth=(.020,.020))
        self.downloadText = OnscreenText(text=TTLocalizer.LauncherVerifyPhase, scale=.070, pos=(0,.080),
                                         fg=(1,1,1,1), parent=self.downloadGui)
        base.cr.music.stop()
        self.musicPlaylist = ['party_generic_theme', 'party_generic_theme_jazzy',
                              'party_polka_dance', 'party_swing_dance',
                              'party_waltz_dance']
        random.shuffle(self.musicPlaylist)
        self.musicIndex = 0
        self.nextMusic()
        
    def unloadDownloadGui(self):
        self.downloadGui.stash()
        self.musicSequence.finish()
        base.cr.music.play()
        
    def nextMusic(self):
        self.musicSequence = Sequence(self.doPlayMusic(), Func(self.nextMusic))
        self.musicSequence.start()

    def doPlayMusic(self):
        if self.musicIndex != len(self.musicPlaylist):
            nextMusic = self.musicPlaylist[self.musicIndex]
            self.musicIndex += 1

        else:
            nextMusic = random.choice(self.musicPlaylist)
            self.musicIndex = self.musicPlaylist.index(nextMusic)
        
        return SoundInterval(base.loadMusic('phase_3/audio/bgm/tt_theme.ogg')) #'phase_13/audio/bgm/%s.ogg' % nextMusic))
        # WTF UNIOR, FORGOT WE HAVE NO PHASE_13 WHILE DOWNLOADING??
        
        