import Playground
from direct.fsm import State
from toontown.safezone import PicnicBasket

class FFPlayground(Playground.Playground):

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.picnicBasketBlockDoneEvent = 'picnicBasketBlockDone'
        self.fsm.addState(State.State('picnicBasketBlock', self.enterPicnicBasketBlock, self.exitPicnicBasketBlock, ['walk']))
        state = self.fsm.getStateNamed('walk')
        state.addTransition('picnicBasketBlock')
        self.picnicBasketDoneEvent = 'picnicBasketDone'

    def enterPicnicBasketBlock(self, picnicBasket):
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('off', 1)
        base.localAvatar.cantLeaveGame = 1
        self.accept(self.picnicBasketDoneEvent, self.handlePicnicBasketDone)
        self.trolley = PicnicBasket.PicnicBasket(self, self.fsm, self.picnicBasketDoneEvent, picnicBasket.getDoId(), picnicBasket.seatNumber)
        self.trolley.load()
        self.trolley.enter()

    def exitPicnicBasketBlock(self):
        base.localAvatar.laffMeter.stop()
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.trolleyDoneEvent)
        self.trolley.unload()
        self.trolley.exit()
        del self.trolley

    def detectedPicnicTableSphereCollision(self, picnicBasket):
        self.fsm.request('picnicBasketBlock', [picnicBasket])

    def handleStartingBlockDone(self, doneStatus):
        self.notify.debug('handling StartingBlock done event')
        where = doneStatus['where']
        if where == 'reject':
            self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'racetrack':
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleStartingBlockDone')

    def handlePicnicBasketDone(self, doneStatus):
        self.notify.debug('handling picnic basket done event')
        mode = doneStatus['mode']
        if mode == 'reject':
            self.fsm.request('walk')
        elif mode == 'exit':
            self.fsm.request('walk')
        else:
            self.notify.error('Unknown mode: ' + mode + ' in handlePicnicBasketDone')
