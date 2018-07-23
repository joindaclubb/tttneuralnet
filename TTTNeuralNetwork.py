#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from TTTBoard import TTTBoard, X_PLAYER, O_PLAYER
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten

otherPlayer = lambda p: -p

# Build model
def buildModel(in_shape, out_shape):   
    
    model = Sequential()
    model.add(Dense(units = in_shape, kernel_initializer='normal',
                    input_shape = [in_shape, 1],
                    activation = "tanh"))
    model.add(Flatten())
    model.add(Dense(units = out_shape, kernel_initializer='normal',
                    activation = "softmax"))
    model.compile(loss  = "binary_crossentropy",
              optimizer = "adam",
              metrics = ["accuracy"])
    return model

# Training routine
def trainRoutine(model):
    
    def trainRecursively(model, board, player, spaces = 0):
        other = otherPlayer(player)
        
        # Try a move
        for empty in board.allEmpties():
            if spaces < 3:
                print(spaces * "  ", empty)
                
            newBoard = board.stateAt(empty, player)
            reward = newBoard.tryReward(player)
        
            # No immediate win/loss
            if reward == None:
                minResponse = None
                minReward = 1
                maxResponse = None
                maxReward = 0
                
                # Consider moves in response
                for empty2 in newBoard.allEmpties():
                    response = newBoard.stateAt(empty2, other)
                    state = response.posVector()
                    att_reward = model.predict(state)
                    while type(att_reward) == np.ndarray:
                        att_reward = att_reward[0]
                    if att_reward >= maxReward:
                        maxReward = att_reward
                        maxResponse = response
                    if att_reward < minReward:
                        minReward = att_reward
                        minResponse = response
                
                # Logical response
                if player == X_PLAYER:
                    reward = maxReward
                if player == O_PLAYER:
                    reward = minReward
                    
            # Train on chosen move
            posVector = newBoard.posVector()
            reward = np.array([0, reward])
            reward = np.reshape(reward, (1, 2))
            model.fit(posVector, reward, verbose = 0)
            
            # Recursive call
            trainRecursively(model, newBoard, other, spaces + 1)
            
    board = TTTBoard()
    trainRecursively(model, board, X_PLAYER)
    return model