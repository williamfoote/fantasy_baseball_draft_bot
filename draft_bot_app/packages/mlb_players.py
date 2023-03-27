import pandas as pd
import numpy as np

class DraftState:
    def __init__(self, rosters, turns, freeagents, playerjm=None):
        self.rosters = rosters
        self.freeagents = freeagents
        self.turns = turns
        self.playerJustMoved = playerjm

class MLBPlayer:
    def __init__(self, name, team, position, points):
        self.name = name
        self.team = team
        self.position = str(position)
        self.points = points
    def __repr__(self):
        return self.name
    def pop(self, index=-1) :
        return self.data.pop(index)

def GetResult(self, playerjm):
    """ Get the game result from the viewpoint of playerjm.
    """
    if playerjm is None: return 0
    
    pos_wgts = {
        ("IF"): [1],
        ("OF"): [1],
        ("P"): [1]
        # ("IF", "OF"):[1]
        # ("SS"): [1],
        # ('3B'): [1],
        # # ("1B", "3B"): [.6, .4],
        # # ("2B", "SS"): [.6, .4],
        # # ('LF'):[.3],
        # # ('CF'):[.3],
        # ('OF'):[1],
        # ("C", "1B", "2B", "SS", "3B", 'DH'): [1],
        # ("SP"): [1],
        # ("RP"): [1]
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
    
    pos_max = {"IF": 4, "OF": 4, "P": 4}
    if len(self.turns) == 0: return []
    roster_positions = np.array([p.position for p in self.rosters[self.turns[0]]], dtype=str)
    # moves = [pos for pos, max_ in pos_max.items() if np.sum(roster_positions == pos) < max_]
    moves = list(pos_max.keys())
    return moves
DraftState.GetMoves = GetMoves

def DoMove(self, move):
    """ Update a state by carrying out the given move.
        Must update playerJustMoved.
    """
    player = next(p for p in self.freeagents if p.position == move)
    self.freeagents.remove(player)
    rosterId = self.turns.pop(0)
    self.rosters[rosterId].append(player)
    self.playerJustMoved = rosterId
    
DraftState.DoMove = DoMove

def DoManualMove(self, player_name):
    """ Update a state by carrying out a specific move.
        Must update playerJustMoved.
    """
    player = [p for p in self.freeagents if p.name == player_name][0]
    self.freeagents.remove(player)
    rosterId = self.turns.pop(0)
    self.rosters[rosterId].append(player)
    self.playerJustMoved = rosterId
    
DraftState.DoManualMove = DoManualMove

def Clone(self):
    """ Create a deep clone of this game state.
    """
    rosters = list(map(lambda r: r[:], self.rosters))
    st = DraftState(rosters, self.turns[:], self.freeagents[:],
            self.playerJustMoved)
    return st
DraftState.Clone = Clone

# This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a 
# state.GetRandomMove() or state.DoRandomRollout() function.
# 
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
# 
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
# 
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai
from math import *
import random
class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        self.playerJustMoved = state.playerJustMoved # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        UCTK = 200
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result
def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
    """
    rootnode = Node(state = rootstate)
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)
        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves) 
            state.DoMove(m)
            node = node.AddChild(m,state) # add child and descend tree
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode
    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited