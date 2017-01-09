from toontown.toonbase import ToontownGlobals, TTLocalizer
import TTHLauncherGUI
import urllib, urllib2, hashlib, os, errno, sys, subprocess
from panda3d.core import *
from toontown.toontowngui import TTDialog

TTH_ROOT = "C:\\ToontownHouseBeta"

def md5_for_file(f, block_size=2**20):
    f = open(f, 'rb')   
    md5 = hashlib.md5(f.read())
    f.close()
    return md5.hexdigest()
    
def test_md5(file, expected):
    if not os.path.isfile(file):
        return 0
        
    local = md5_for_file(file)
    return local == expected
    
BAT_FILE = '''@echo off
echo Updating TTH files...
ping 1.1.1.1 -n 1 -w 4500 > nul\n'''

# fuck localizer
ErrorMsg = "An error occurred while downloading the game. Please restart it manually!"
OKMsg = "The game has been updated. Click 'OK' to restart it."
ChangeLangConfirm = "To change the language, you'll need to manually restart the game. Continue?"
FuckedBat = "Somehow the game tried to start in a strange way (invalid commands). Please redownload and run the installer. If the problem continues, contact us for help. Thank you!"

class TTHLauncher:
    loginDoneEvent = 'TTHLauncherLoginDone'
    server = 'https://api.toontownhouse.net'
    loginEndPoint = '/genToken.php'
    newsEndPoint = '/newslauncher.php'
    expectedTokenSize = 128
    
    def __init__(self):
        self.files = []
        
    def load(self):
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        self.gui = TTHLauncherGUI.TTHLauncherGUI(self)
        
    def enter(self):
        # hack: test for fucked game
        for x in base.cr.serverList:
            if '/-t:' in repr(x):
                base.accept('fucked-bat-ack', sys.exit)
                TTDialog.TTGlobalDialog(text=FuckedBat, doneEvent='fucked-bat-ack', style=TTDialog.Acknowledge)
                base.transitions.fadeScreen(1)
                return
            
        if base.cr.playToken != "_launcher":
            self.mountPhases()
            messenger.send(self.loginDoneEvent)
        
        else:
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
            self.gui.show()
            self.gui.start()
            
    def post(self, url, data = {}):
        headers = {'User-Agent' : 'TTHLauncherAgent'}
        data["anticacheagent"] = str(id(data) + id(url))
        data = urllib.urlencode(data)
        
        req = urllib2.Request(url, data, headers)
        try: response = urllib2.urlopen(req)
        except: return "__err__"
        return response.read()
        
    def doLogin(self, user, password):        
        data = {"u": user, "p": hashlib.sha512(password).hexdigest()}
        token = self.post(self.server + self.loginEndPoint, data).strip()
            
        #print [token, data]
            
        if not token or token == "__err__":
            return self.gui.serverError()
            
        if len(token) != self.expectedTokenSize:
            self.gui.authError()

        else:
            ret = self.isDownloaded()
            if ret < 0:
                self.mountPhases() 
                self.success(token)
                
            elif ret != 2**30:
                self.__token = token
                self.gui.cleanupPopup()
                self.gui.loadDownloadGui()
                self.download()
        
    def success(self, token):
        base.cr.playToken = token
        messenger.send(self.loginDoneEvent)
        
    def exit(self):
        self.gui.hide()
        
    def unload(self):
        self.gui.unload()
        del self.gui
            
    def getOnlineNews(self):
        return self.post(self.server + self.newsEndPoint) or 'Last news: President Mickey goes to hospital after kids music show!'
        
    # downloading methods
        
    def isDownloaded(self):
        # list files
        r = self.post('https://toontownhouse.net/data/filelist')
        if not r or r == "__err__":
            self.downloadError()
            return 2**30
            
        files = dict(x.split(':', 1) for x in r.split('\n') if x)
        self.files = []
        self.sizes = {}
        for file, data in files.items():
            hash, size = data.split(':')
            if not test_md5(os.path.join(TTH_ROOT, file), hash):
                self.files.append(file)
                self.sizes[file] = float(size) / 100.0
            
        return len(self.files) - 1
        
    def download(self):
        # start
        self.nextFile()
        
    def __handle_down(self):
        self.file = self.files.pop()
        print self.file

        self.http = HTTPClient()
        self.channel = self.http.makeChannel(True)
        self.channel.beginGetDocument(DocumentSpec('https://toontownhouse.net/data/' + self.file))
        self.rf = Ramfile()
        self.channel.downloadToRam(self.rf)
        
        print self.sizes[self.file]
        
        taskMgr.add(self.downloadTask, 'download')
 
    def downloadTask(self, task):
        if self.channel.run():
            pc = round(self.channel.getBytesDownloaded() / self.sizes[self.file], 1)
            self.gui.downloadBar['value'] = pc
            self.gui.downloadBar['text'] = '%s (%s%%)' % (self.file, pc)
            return task.cont
            
        if not self.channel.isDownloadComplete():
            print "Error downloading file."
            self.downloadError()
            return task.done
            
        # assuming it downloaded everything correctly
        print 'Finished downloading %s' % self.file
        self.save()
        
        taskMgr.doMethodLater(0, self.nextFile, "nextFile")
        return task.done
        
    def save(self):
        target_f = self.ensure_dir(self.file)
        print 'Saving', target_f
        
        with open(target_f + '.upd', "wb") as f:
            f.write(self.rf.getData())
            
        global BAT_FILE
        BAT_FILE += 'move /y %s %s\n' % (self.file + '.upd', self.file)
            
    @classmethod
    def ensure_dir(cls, filename):
        d = os.path.dirname(os.path.join(TTH_ROOT, filename))
        try:
            os.makedirs(d)
            
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
        
        return os.path.join(TTH_ROOT, filename)
   
    def nextFile(self, task=None):            
        if self.files:
            self.__handle_down()
        
        else:
            print 'Downloader is done'
            self.downloadDone()
            
    def downloadError(self):
        if hasattr(self.gui, 'downloadGui'):
            self.gui.unloadDownloadGui()
            
        base.accept('download-error-ack', sys.exit)
        TTDialog.TTGlobalDialog(text=ErrorMsg, doneEvent='download-error-ack', style=TTDialog.Acknowledge)
        base.transitions.fadeScreen(1)
        
    def downloadDone(self):
        if hasattr(self.gui, 'downloadGui'):
            self.gui.unloadDownloadGui()
            
        base.accept('download-done-ack', self.__run)
        TTDialog.TTGlobalDialog(text=OKMsg, doneEvent='download-done-ack', style=TTDialog.Acknowledge)
        base.transitions.fadeScreen(1)
        
    def __run(self):
        THIS = "start %s -t %s" % (sys.executable, self.__token)
        # write the bat
        kickoff = open(os.path.join(TTH_ROOT, 'kickoff.bat'), 'wb')
        kickoff.write(BAT_FILE + '\n' + THIS + '\nrem del kickoff.bat\nexit')
        kickoff.close()
        
        # exec it and leave
        DETACHED_PROCESS = 0x00000008
        print subprocess.Popen('start ' + os.path.join(TTH_ROOT, 'kickoff.bat'), creationflags=DETACHED_PROCESS, cwd=TTH_ROOT, shell=True).pid
        sys.exit()
        
    def mountPhases(self):
        if __debug__:
            return
            
        print 'Mounting phases...'
        def mountSingle(filename):
            result = vfs.mount(filename, "resources", 0)
            if not result:
                base.notify.error("Cannot mount mf %s" % filename)
                
            base.notify.info("Mounted %s" % filename)
            
        for i in (3.5, 4, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13):
            mountSingle(Filename.fromOsSpecific("%s/phase_%s.mf" % (TTH_ROOT, i)))
        
    def _handleChangeLang(self, choice):
        base.accept('change-lang-diag', self._handleNewLangRes)
        self.__langDiag = TTDialog.TTGlobalDialog(text=ChangeLangConfirm, doneEvent='change-lang-diag', style=TTDialog.TwoChoice)
        base.transitions.fadeScreen(.6)
        self.__langChoice = choice
        
    def _handleNewLangRes(self):
        if self.__langDiag.doneStatus == 'ok':
            with open('launcher.lang', 'wb') as f:
                f.write(self.__langChoice)
                
            sys.exit()
        
        self.__langDiag.cleanup()
 