#!/usr/bin/env python3
# -*- coding: utf-8 -*-

X_PLAYER = 1
O_PLAYER = -1

import numpy as np

class TTTBoard:
    """
    represents a tic tac toe board for the board
    """

    def __init__(self, pos = [0 for _ in range(9)]):
        self.pos = pos
        
    def checkPos(self, pos):
        assert self.isValid(pos)
        return self.pos[pos]
    
    def valiateBoard(self):
        assert len(self.pos) == 9
        assert max(self.pos) <  2, self.pos
        assert min(self.pos) > -2, self.pos
    
    def tryReward(self, player = X_PLAYER):
        cols  = [[self.checkPos(loc) for loc in triple] for 
                     triple in ((range(col, 9, 3)) for col in range(3))]
        rows  = [[self.checkPos(loc) for loc in triple] for
                      triple in ((range(row, row + 3)) for row in range(0, 9, 3))]
        diags = [[self.checkPos(loc) for loc in triple] for triple in 
                      ((0, 4, 8), (2, 4, 6))]
        found_fail = False
        for pair in cols + rows + diags:
            if sum(pair) in [3, -3]:
                if pair[0] == player:
                    return 1
                found_fail = True  # OR SHOULD IT BE X_PLAYER
        if found_fail:
            return 0
        return None        
            
    def isValid(self, loc):
        return loc in range(0, 9)
    
    def isEmpty(self, loc):
        self.isValid(loc)
        return self.checkPos(loc) == 0
    
    def adjacents(self, loc):
        assert self.isValid(loc)
        col = loc  % 3
        row = loc // 3
        return [adj for adj in range(9) if (adj // 3) in range(row - 1, row + 2) and
                (adj % 3) in range(col - 1, col + 2) and self.isValid(adj) and adj != loc]
        
    def emptyAdjacents(self, loc):
        assert self.isValid(loc)
        return [adj for adj in self.adjacents(loc) if self.isEmpty(adj) == 0]
    
    def allEmpties(self):
        return [empty for empty in range(9) if self.isEmpty(empty)]
    
    def stateAt(self, location, playerSide):
        self.valiateBoard()
        assert playerSide in [-1, 1]
        assert self.isEmpty(location)
        new = [i for i in self.pos]
        new[location] = playerSide
        return TTTBoard(new)

    def posVector(self):
        self.valiateBoard()
        pos = np.array(self.pos)
        pos = np.reshape(pos, (1, 9, 1))
        assert len(pos.shape) == 3
        return pos
    
    def flipPieces(self):
        self.pos *= -1
