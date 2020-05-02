from dpt.engine.webCommunications import WebCommunication
from dpt.engine.tileManager import TileManager
from dpt.game import Game

import random


class EffectsManagement(WebCommunication):
    listEffects = ["Ice",
                   "Slow",
                   "Fast",
                   "monsterimmortal",
                   "star",
                   "jumpBoost",
                   "inversion",
                   "lowGravity"]

    dicoEffects = {"Ice": "Perm",
                   "Slow": "Temp",
                   "Fast": "Temp",
                   "monsterimmortal": "Temp",
                   "star": "Temp",
                   "jumpBoost": "Temp",
                   "inversion": "Temp",
                   "lowGravity": "Perm"}

    dicoLinks = {"Ice": "PlayerAndEnemy",
                 "Slow": "PlayerAndEnemy",
                 "Fast": "Player",
                 "monsterimmortal": "PlayerAndEnemy",
                 "star": "Player",
                 "jumpBoost": "Player",
                 "inversion": "Player",
                 "lowGravity": "PlayerAndEnemy"}

    def __init__(self):
        super().__init__()
        self.result = None
        self.tempList = []

    def update(self):
        self.vote()
        for effects in self.tempList:
            if EffectsManagement.dicoLinks[effects] == "PlayerAndEnemy":
                for enemies in TileManager.enemy_group:
                    eval("enemies." + effects + " = False")
            for player in Game.player_group:
                eval("player." + effects + " = False")
        if EffectsManagement.dicoEffects[self.result] == "Temp":
            self.tempList.append(self.result)
        if EffectsManagement.dicoLinks[self.result] == "PlayerAndEnemy":
            for enemies in TileManager.enemy_group:
                eval("enemies." + self.result + " = True")
        for player in Game.player_group:
            eval("player." + self.result + " = True")

    def vote(self):
        mod1 = random.choice(EffectsManagement.listEffects)
        mod2 = random.choice(EffectsManagement.listEffects)
        while mod2 == mod1:
            mod2 = random.choice(EffectsManagement.listEffects)
        self.result = self.create_vote_event(mod1, mod2)
