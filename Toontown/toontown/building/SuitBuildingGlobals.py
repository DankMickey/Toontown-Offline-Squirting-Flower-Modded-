from ElevatorConstants import *
from toontown.toonbase import ToontownGlobals


try:
    config = base.config
except:
    config = simbase.config

# the planner gets a level pool (eg 50)
# multiplies by current floor multiplier (eg x2, 100)
# generates cogs until the sum of their levels reach the pool (eg 10 cogs level 10)
# last floor has a boss

SuitBuildingInfo = (
                    # format:
                    # (floorMin, floorMax), not revelant for bosses
                    # (lvlMin, lvlMax), obvious
                    # (boss, boss), should be equal
                    # (mult1, mult2, mult3, mult4, mult5), multiplier per floor (increasing level pool)
                    # (1,) at the end means vs 2.0 cogs
                    
                    # normal buildings
                    ((1, 1),  (1, 3),  (4, 4),  (8, 10),  (1,)),
                    ((1, 2),  (2, 4),  (5, 5),  (8, 10),  (1, 1.2)),
                    ((1, 3),  (3, 5),  (6, 6),  (8, 10),  (1, 1.3, 1.6)),
                    ((2, 3),  (4, 6),  (7, 7),  (8, 10),  (1, 1.4, 1.8)),
                    ((2, 4),  (5, 7),  (8, 8),  (8, 10),  (1, 1.6, 1.8, 2)),
                    ((3, 4),  (6, 8),  (9, 9),  (10, 12),  (1, 1.6, 2, 2.4)),
                    ((3, 5),  (7, 9),  (10, 10),  (10, 14),  (1, 1.6, 1.8, 2.2, 2.4)),
                    ((4, 5),  (8, 10),  (11, 11),  (12, 16),  (1, 1.8, 2.4, 3, 3.2)),
                    ((5, 5),  (9, 11),  (12, 12),  (14, 20),  (1.4, 1.8, 2.6, 3.4, 4)),
                    
                    # bosses
                    ((1, 1),  (1, 12),  (12, 12),  (100, 100),  (1, 1, 1, 1, 1)), # vp
                    ((1, 1),  (8, 12),  (12, 12),  (150, 150),  (1, 1, 1, 1, 1)), # vp skel
                    ((1, 1),  (1, 12),  (12, 12),  (125, 125),  (1, 1, 1, 1, 1)), # cfo
                    ((1, 1),  (8, 12),  (12, 12),  (175, 175),  (1, 1, 1, 1, 1)), # cfo skel
                    ((1, 1),  (8, 12),  (12, 12),  (200, 200),  (1, 1, 1, 1, 1)), # cj
                    ((1, 1),  (8, 12),  (12, 12),  (300, 400),  (1, 1, 1, 1, 1), (1,)), # ceo
                    ((1, 1),  (1, 12),  (12, 12),  (67, 67),  (1, 1, 1, 1, 1)), # nerfed vp
                    ((1, 1),  (8, 12),  (12, 12),  (100, 100),  (1, 1, 1, 1, 1)), # nerfed vp skel
                    
                    # special vp
                    ((1, 1), (1, 8), (8, 8), (10, 25), (1, 1, 1, 1, 1)), # easy cogs (1 - 7)
                    ((1, 1), (8, 12), (12, 12), (70, 90), (1, 1, 1, 1, 1)), # hard cogs (8 - 12)
                    
                    ((1, 5), (5, 12), (12, 12), (80, 130), (1, 1, 1, 1, 1), (-1,)) # reserved
                    )

SUIT_BLDG_INFO_FLOORS = 0
SUIT_BLDG_INFO_SUIT_LVLS = 1
SUIT_BLDG_INFO_BOSS_LVLS = 2
SUIT_BLDG_INFO_LVL_POOL = 3
SUIT_BLDG_INFO_LVL_POOL_MULTS = 4
SUIT_BLDG_INFO_REVIVES = 5
VICTORY_RUN_TIME = ElevatorData[ELEVATOR_NORMAL]['openTime'] + TOON_VICTORY_EXIT_TIME
TO_TOON_BLDG_TIME = 8
VICTORY_SEQUENCE_TIME = VICTORY_RUN_TIME + TO_TOON_BLDG_TIME
CLEAR_OUT_TOON_BLDG_TIME = 4
TO_SUIT_BLDG_TIME = 8

buildingMinMax = {
    ToontownGlobals.SillyStreet: (config.GetInt('silly-street-building-min', 0),
                                  config.GetInt('silly-street-building-max', 3)),
    ToontownGlobals.LoopyLane: (config.GetInt('loopy-lane-building-min', 0),
                                config.GetInt('loopy-lane-building-max', 3)),
    ToontownGlobals.PunchlinePlace: (config.GetInt('punchline-place-building-min', 0),
                                     config.GetInt('punchline-place-building-max', 3)),
    ToontownGlobals.BarnacleBoulevard: (config.GetInt('barnacle-boulevard-building-min', 1),
                                        config.GetInt('barnacle-boulevard-building-max', 5)),
    ToontownGlobals.SeaweedStreet: (config.GetInt('seaweed-street-building-min', 1),
                                    config.GetInt('seaweed-street-building-max', 5)),
    ToontownGlobals.LighthouseLane: (config.GetInt('lighthouse-lane-building-min', 1),
                                     config.GetInt('lighthouse-lane-building-max', 5)),
    ToontownGlobals.ElmStreet: (config.GetInt('elm-street-building-min', 2),
                                config.GetInt('elm-street-building-max', 6)),
    ToontownGlobals.MapleStreet: (config.GetInt('maple-street-building-min', 2),
                                  config.GetInt('maple-street-building-max', 6)),
    ToontownGlobals.OakStreet: (config.GetInt('oak-street-building-min', 2),
                                config.GetInt('oak-street-building-max', 6)),
    ToontownGlobals.AltoAvenue: (config.GetInt('alto-avenue-building-min', 3),
                                 config.GetInt('alto-avenue-building-max', 7)),
    ToontownGlobals.BaritoneBoulevard: (config.GetInt('baritone-boulevard-building-min', 3),
                                        config.GetInt('baritone-boulevard-building-max', 7)),
    ToontownGlobals.TenorTerrace: (config.GetInt('tenor-terrace-building-min', 3),
                                   config.GetInt('tenor-terrace-building-max', 7)),
    ToontownGlobals.WalrusWay: (config.GetInt('walrus-way-building-min', 5),
                                config.GetInt('walrus-way-building-max', 10)),
    ToontownGlobals.SleetStreet: (config.GetInt('sleet-street-building-min', 5),
                                  config.GetInt('sleet-street-building-max', 10)),
    ToontownGlobals.PolarPlace: (config.GetInt('polar-place-building-min', 5),
                                 config.GetInt('polar-place-building-max', 10)),
    ToontownGlobals.LullabyLane: (config.GetInt('lullaby-lane-building-min', 6),
                                  config.GetInt('lullaby-lane-building-max', 12)),
    ToontownGlobals.PajamaPlace: (config.GetInt('pajama-place-building-min', 6),
                                  config.GetInt('pajama-place-building-max', 12)),
    ToontownGlobals.SellbotHQ: (0, 0),
    ToontownGlobals.SellbotFactoryExt: (0, 0),
    ToontownGlobals.CashbotHQ: (0, 0),
    ToontownGlobals.LawbotHQ: (0, 0),
    ToontownGlobals.BossbotHQ: (0, 0)
}

buildingChance = {
    ToontownGlobals.ToontownCentral: 0.0,
    ToontownGlobals.SillyStreet: config.GetFloat('silly-street-building-chance', 2.0),
    ToontownGlobals.LoopyLane: config.GetFloat('loopy-lane-building-chance', 2.0),
    ToontownGlobals.PunchlinePlace: config.GetFloat('punchline-place-building-chance', 2.0),
    ToontownGlobals.BarnacleBoulevard: config.GetFloat('barnacle-boulevard-building-chance', 75.0),
    ToontownGlobals.SeaweedStreet: config.GetFloat('seaweed-street-building-chance', 75.0),
    ToontownGlobals.LighthouseLane: config.GetFloat('lighthouse-lane-building-chance', 75.0),
    ToontownGlobals.ElmStreet: config.GetFloat('elm-street-building-chance', 90.0),
    ToontownGlobals.MapleStreet: config.GetFloat('maple-street-building-chance', 90.0),
    ToontownGlobals.OakStreet: config.GetFloat('oak-street-building-chance', 90.0),
    ToontownGlobals.AltoAvenue: config.GetFloat('alto-avenue-building-chance', 95.0),
    ToontownGlobals.BaritoneBoulevard: config.GetFloat('baritone-boulevard-building-chance', 95.0),
    ToontownGlobals.TenorTerrace: config.GetFloat('tenor-terrace-building-chance', 95.0),
    ToontownGlobals.WalrusWay: config.GetFloat('walrus-way-building-chance', 100.0),
    ToontownGlobals.SleetStreet: config.GetFloat('sleet-street-building-chance', 100.0),
    ToontownGlobals.PolarPlace: config.GetFloat('polar-place-building-chance', 100.0),
    ToontownGlobals.LullabyLane: config.GetFloat('lullaby-lane-building-chance', 100.0),
    ToontownGlobals.PajamaPlace: config.GetFloat('pajama-place-building-chance', 100.0),
    ToontownGlobals.SellbotHQ: 0.0,
    ToontownGlobals.SellbotFactoryExt: 0.0,
    ToontownGlobals.CashbotHQ: 0.0,
    ToontownGlobals.LawbotHQ: 0.0,
    ToontownGlobals.BossbotHQ: 0.0
}


