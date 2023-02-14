import pandas as pd
import numpy as np

class DraftState:
    def __init__(self, rosters, turns, freeagents, playerjm=None):
        self.rosters = rosters
        self.freeagents = freeagents
        self.turns = turns
        self.playerJustMoved = playerjm

class NflPlayer:
    def __init__(self, name, team, position, points):
        self.name = name
        self.team = team
        self.position = position
        self.points = points

def GetResult(self, playerjm):
    """ Get the game result from the viewpoint of playerjm.
    """
    if playerjm is None: return 0
    
    pos_wgts = {
        ("C"): [.6, .4],
        ("1B"): [.7, .7, .4, .2],
        ("2B"): [.7, .7, .4, .2],
        ("SS"): [.6, .4],
        ("1B", "3B"): [.6, .4],
        ("2B", "SS"): [.6, .4],
        ('LF'):[.3],
        ('CF'):[.3],
        ('OF'):[.3],
        ("C", "1B", "2B", "SS", "3B", "DH"): [.2],
        ("SP"): [.6, .3, .1],
        ("RP"): [.6, .3, .1]
    }
    result = 0
    # map the drafted players to the weights
    for p in self.rosters[playerjm]:
        max_wgt, _, max_pos, old_wgts = max(
            ((wgts[0], -len(lineup_pos), lineup_pos, wgts) for lineup_pos, wgts in pos_wgts.items()
                if p.position in lineup_pos),
            default=(0, 0, (), []))
        if max_wgt > 0:
            result += max_wgt * p.points
            old_wgts.pop(0)
            if not old_wgts:
                pos_wgts.pop(max_pos)
                
    # map the remaining weights to the top three free agents
    for pos, wgts in pos_wgts.items():
        result += np.mean([p.points for p in self.freeagents if p.position in pos][:3]) * sum(wgts)
    return result
DraftState.GetResult = GetResult

def GetMoves(self):
    """ Get all possible moves from this state.
    """
    pos_max = {"C": 1, "1B": 1, "2B": 1, "SS": 1, "3B": 1, '1B/3B':1, "2B/SS":1, "CF":2, "LF":2, "RF":2, 'P':10}
    if len(self.turns) == 0: return []
    roster_positions = np.array([p.position for p in  self.rosters[self.turns[0]]], dtype=str)
    moves = [pos for pos, max_ in pos_max.items() if np.sum(roster_positions == pos) < max_]
    return moves
DraftState.GetMoves = GetMoves