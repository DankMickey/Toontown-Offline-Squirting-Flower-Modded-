from toontown.toonbase.ToontownGlobals import *
import RegenTreasurePlannerAI
import DistributedFFTreasureAI

class FFTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):
    def __init__(self, zoneId):
        self.healAmount = 8
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(self, zoneId, DistributedFFTreasureAI.DistributedFFTreasureAI, 'FFTreasurePlanner', 20, 5)

    def initSpawnPoints(self):
        self.spawnPoints = [
            (50.6203, -48.7655, 0.0255548),
            (-7.28212, 2.23632, 0.0255548),
            (-58.2855, -7.87096, 0.0255548),
            (-96.4059, -2.39136, 0.0255548),
            (-116.132, 45.8718, 0.0255548),
            (-103.906, 76.6642, 0.0255548),
            (-69.4691, 76.3804, 0.0255548),
            (-15.5558, 97.2077, 0.0255548),
            (40.4045, 89.4397, 0.0255548),
            (83.9763, 68.3644, 0.0255548),
            (79.0471, 31.296, 0.0255548),
            (-5.29712, 23.0919, 0.0255548)]
        return self.spawnPoints
