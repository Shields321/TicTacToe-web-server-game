""" 
Code Created by Alessio and Dylan
This code requres the use of ngrok executable to be able to function over multiple machines
This is also the main file it uses the DataBaseTicTacToe file to store the data it gets into a database
"""
from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from flask_httpauth import HTTPBasicAuth
from Errors import OutOfBoundsError,InvalidPosition,win
#from Database.DataBaseTicTacToe import Database
from TestSpread import SpreadSheet
import numpy as np
import random as rnd
class TicTacToeGame:
    def __init__(self):
        self.app = Flask(__name__)#variable to store the flask instance 
        self.auth = HTTPBasicAuth()# a variable used to handle http basic authentication for logins
        self.app.secret_key = 'p9MZng6tpiEmHtcLSvWgKA=='# Secret key used by Flask to sign session cookies.
        self.gameBoardArray = np.zeros((8, 8, 3), dtype=int)#3d array used as the game board of the tictactoe game
        self.player1Colour = (255, 0, 0)#the colour that player 1 would use
        self.player2Colour = (0, 0, 255)#the colour that player 2 would use
        self.weekAiColour = (0, 125, 255)#the colour that the weekai would use
        self.gameBoardColour = (255, 255, 255)#the colour is used to create the image of a tictactoe game board        
        self.turns = 0#variable used to keep track of the amount of turns that have gone by and check if the game ended in a tie
        self.playerCheck = 0#check if the player is player 1 or player 2 this function may not be needed as playerNumber is the same thing
        self.aiCheck = 0#check if the ai is being used
        self.playerNumber =1#check if the player is player 1 or player 2
        self.ip_Address = [None]*2# an array of length 2 for the 2 people that will be playing on the webserver
        self.users = 0# a variable to see how many users are in the webserver
        self.aiTurn =0
        self.usernameCount = 0
        #these variables are used for the database and spreadsheet
        self.playerUsername = [None]*2
        self.playerPassword = None
        self.playerPosX = None
        self.playerPosY = None 
        self.player1Save = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.player2Save = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.playerAISave = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.moveLeft = [1,2,3,4,5,6,7,8,9]
        self.allplayedMoves = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.checkP1 = [-1]*9
        self.checkAI = [-1]*9

        self.arraySaveXP2 = [-1,-1,-1,-1,-1,-1,-1,-1,-1] #save the x for the player 2 position.
        self.arraySaveYP2 = [-1,-1,-1,-1,-1,-1,-1,-1,-1] #save the y for the player 2 position.
        self.arraySaveX = [-1,-1,-1,-1,-1,-1,-1,-1,-1]#save the x for the player 1 position.
        self.arraySaveY = [-1,-1,-1,-1,-1,-1,-1,-1,-1]#save the y for the player 1 position.
        self.arraySaveAIX = [-1,-1,-1,-1,-1,-1,-1,-1,-1]#save the x for the player 1 position.
        self.arraySaveAIY = [-1,-1,-1,-1,-1,-1,-1,-1,-1]#save the y for the player 1 position.

        self.winCode = 0
        self.countP1 = 0
        self.countP2 = 0
        self.countAI = 0
        self.played = 0
        self.countP1save = 0

        self.playerCount = 1
        self.turns = 0
        self.strong = 0

        self.email = [None]*2
        self.sheet = SpreadSheet()#create an instance of the spreadsheet class
        self.sheet.createSpreadsheet()# create a spreadsheet if it already exists dont need to create one   
        #self.db = Database()
        #self.db.CreateDataBase()
            
    
    def sendDataToSpreadSheet(self):        
        try:
            data = [None]*6 #a array to store the data to send to the database  
            if self.users == 1:
                if self.turns % 2 == 1:                              
                    data[0] = self.playerNumber
                    data[1] = self.playerUsername[0]
                    data[2] = self.email[0]
                    data[3] = self.playerPassword
                    data[4] = self.playerPosX 
                    data[5] = self.playerPosY                   
                    self.sheet.sendDataToSpreadSheet(data) 
                    
            else:
                if self.turns % 2 == 1: 
                    print(self.playerUsername[0])                    
                    data[0] = self.playerNumber
                    data[1] = self.playerUsername[0]
                    data[2] = self.playerPassword
                    data[3] = self.playerPosX 
                    data[4] = self.playerPosY                                                            
                else:  
                    print(self.playerUsername[1])                  
                    data[0] = self.playerNumber
                    data[1] = self.playerUsername[1]
                    data[2] = self.email[1]
                    data[3] = self.playerPassword
                    data[4] = self.playerPosX 
                    data[5] = self.playerPosY 
                    self.sheet.sendDataToSpreadSheet(data)                    
                 
                 
        except Exception as e:
            print(e)
    def getRandomNumber(self):            
            number = [0,3,6]
            value = rnd.choice(number)
            return value

    def weekAi(self):      
        positions = self.getPosition(3,0,0)        
        for x, y, color in positions:
            self.update_2x2_square(x, y, color)        
        return jsonify({"status": "AI turn completed"})

    def chooseAiPos(self,player):
        if player == 3:
            stop = 0
            posInputX = self.getRandomNumber()  
            posInputY = self.getRandomNumber()
                
            while True:
                if (self.checkSave(3,posInputX,posInputY) == False):
                    posInputX = self.getRandomNumber()  
                    posInputY = self.getRandomNumber()
                else:
                    stop = 1
                    break

            if stop == 1:
                if posInputX == 0 and posInputY == 0: 
                    pos = [(0,0),(1,1)]
                    self.positionSave(3,0,0)
                    #self.possibleMove(0,0)
                elif posInputX == 3 and posInputY == 0:
                    pos = [(3,0),(4,1)]
                    self.positionSave(3,3,0)
                    #self.possibleMove(3,0)
                elif posInputX == 6 and posInputY == 0:
                    pos = [(6,0),(7,1)]
                    self.positionSave(3,6,0)
                    #self.possibleMove(6,0)
                elif posInputX == 0 and posInputY == 3:
                    pos = [(0,3),(1,4)]
                    self.positionSave(3,0,3)
                    #self.possibleMove(0,3)
                elif posInputX == 3 and posInputY == 3:
                    pos = [(3,3),(4,4)]
                    self.positionSave(3,3,3)
                    #possibleMove(3,3)
                elif posInputX == 6 and posInputY == 3:
                    pos = [(6,3),(7,4)]
                    self.positionSave(3,6,3)
                    #possibleMove(6,3)
                elif posInputX == 0 and posInputY == 6:
                    pos = [(0,6),(1,7)]
                    self.positionSave(3,0,6)
                    #possibleMove(0,6)
                elif posInputX == 3 and posInputY == 6:
                    pos = [(3,6),(4,7)]
                    self.positionSave(3,3,6)
                    #possibleMove(3,6)
                elif posInputX == 6 and posInputY == 6:
                    pos = [(7,7),(6,6)]
                    self.positionSave(3,6,6)
                    #possibleMove(6,6) 
        elif player == 4:
            posInput = self.strongMove()
            
            if posInput == 1: 
                pos = [(0,0),(1,1)]
                self.positionSave(4,1,0)
                self.positionSave(3,0,0)
                self.removeMove(1)
            elif posInput == 2:
                pos = [(3,0),(4,1)]
                self.positionSave(4,2,0)
                self.positionSave(3,3,0)
                self.removeMove(2)
            elif posInput == 3:
                pos = [(6,0),(7,1)]
                self.positionSave(4,3,0)
                self.positionSave(3,6,0)
                self.removeMove(3)
            elif posInput == 4:
                pos = [(0,3),(1,4)]
                self.positionSave(4,4,0)
                self.positionSave(3,0,3)
                self.removeMove(4)
            elif posInput == 5:
                pos = [(3,3),(4,4)]
                self.positionSave(4,5,0)
                self.positionSave(3,3,3)
                self.removeMove(5)
            elif posInput == 6:
                pos = [(6,3),(7,4)]
                self.positionSave(4,6,0)
                self.positionSave(3,6,3)
                self.removeMove(6)
            elif posInput == 7:
                pos = [(0,6),(1,7)]
                self.positionSave(4,7,0)
                self.positionSave(3,0,6)
                self.removeMove(7)
            elif posInput == 8:
                pos = [(3,6),(4,7)]
                self.positionSave(4,8,0)
                self.positionSave(3,3,6)
                self.removeMove(8)
            elif posInput == 9:
                pos = [(7,7),(6,6)]
                self.positionSave(4,9,0)
                self.positionSave(3,6,6)
                self.removeMove(9)
        return pos

    def strongMove(self):
        bestScore = -float('inf')
        playsP1 = [-1]*9
        playsAI = [-1]*9
        
        for i in range(9):
            if self.moveLeft[i] != -1:
                moveAI = self.moveLeft[i]
                for j in range(9):
                    playsP1[j] = self.player1Save[j]
                    playsAI[j] = self.playerAISave[j]
                for g in range(9):
                    if playsAI[g] == -1:
                        playsAI[g] = moveAI
                        break
                #checking if the AI will win
                for u in range(9):
                    if playsP1[u] == -1:
                        playsP1[u] = moveAI
                        break               
                if self.checkWin(1,playsP1,playsAI):                    
                    return moveAI                
                for h in range(9):
                    if playsP1[h] == moveAI:
                        playsP1[u] = -1
                
                score = self.minMax(playsP1,playsAI, 0, True)
                if score > bestScore:
                    bestScore = score
                    print("bestScore", bestScore)
                    moveAI = self.moveLeft[i]
        return moveAI

    def minMax(self,play1,playA, depth, isMax):
    
        allmoves = [-1]*9
        for i in range(9):
            if playA[i] != -1:
                allmoves[i] = playA[i]
            else:
                if play1[i] != -1:
                    allmoves[i] = play1[i]
        
        if self.checkWin(1, play1, playA):
            return -1
        elif self.checkWin(3, play1, playA):
            return 1
        
        for i in range(9):
            if allmoves[i] == -1:
                break
            else:
                return 0
        
        if isMax: #AI point of view
            bestScore = -float('inf')
            playsP1 = [-1]*9
            playsAI = [-1]*9
            for t in range(9):
                if self.moveLeft[t] != play1[t] and self.moveLeft[t] != playA[t] and self.moveLeft[t] != -1:
                    for i in range(9):
                        playsP1[i] = play1[i]
                        playsAI[i] = playA[i]
                    score = self.minMax(playsP1, playsAI, depth + 1, False)
                    if score > bestScore :
                        bestScore = score
            return bestScore

        else: #player point of view
            bestScore = -float('inf')
            playsP1 = [-1]*9
            playsAI = [-1]*9
            for o in range(9):
                if self.moveLeft[o] != play1[o] and self.moveLeft[o] != playA[o] and self.moveLeft[o] != -1:
                    moveAI = self.moveLeft[o] 
                    for i in range(9):
                        playsP1[i] = play1[i]
                        playsAI[i] = playA[i]
                    for j in range(9):
                        if playsP1[j] == -1:
                            playsP1[j] = moveAI
                            break
                    score = self.minMax(playsP1, playsAI, depth + 1, True)
                    if score < bestScore:
                        bestScore = score
            return bestScore

    def strongAI(self):
        positions = self.getPosition(4,0,0)
        for x, y, color in positions:
            self.update_2x2_square(x, y, color)
        return jsonify({"status": "AI turn completed"})


    def checkWin(self,player, play1Move, playerAImove):

        winCombination1 = [1,2,3]  # 1 2 3
        winCombination2 = [1,4,7]  # 1 4 7
        winCombination3 = [2,5,8]   # 2 5 8
        winCombination4 = [3,6,9]   # 3 6 9
        winCombination5 = [4,5,6]  # 4 5 6
        winCombination6 = [7,8,9]   # 7 8 9
        winCombination7 = [1,5,9]   # 1 5 9
        winCombination8 = [3,5,7]   # 3 5 7
        
        win_combinations = [winCombination1, winCombination2, winCombination3,
                        winCombination4, winCombination5, winCombination6,
                        winCombination7, winCombination8,]

        if player ==1:
            print("sim player")
            for combination in win_combinations:
                if all(position in play1Move for position in combination):
                    print("sim player win")
                    return True
        
        if player ==3:
            print("sim AI")
            for combination in win_combinations:
                if all(position in playerAImove for position in combination):
                    print("sim AI win")
                    return True                                              
        
        return False

    def removeMove(self,move):
        count = 0
        while count < len(self.moveLeft):
            if move == self.moveLeft[count]:
                self.moveLeft[count] = -1
                break
            count += 1
        return True

    def positionSave(self,player,x,y):        
        if(player == 1):
            self.arraySaveX[self.countP1] = x
            self.arraySaveY[self.countP1] = y
            self.countP1 = self.countP1 + 1
        elif (player == 2):
            self.arraySaveXP2[self.countP2] = x
            self.arraySaveYP2[self.countP2] = y
            self.countP2 = self.countP2 + 1
        elif (player == 3):
            self.arraySaveAIX[self.countAI] = x
            self.arraySaveAIY[self.countAI] = y
            self.countAI = self.countAI + 1
        elif player == 4:
            self.playerAISave[self.countAI] = x
            self.countAI = self.countAI + 1
        elif player == 5:
            self.player1Save[self.countP1save] = y
            self.countP1save = self.countP1save + 1

    def checkSave(self,player,x,y):
        saveCount=0
        while saveCount < len(self.arraySaveX):
            if(player == 1):
                if (x == self.arraySaveX[saveCount] and y == self.arraySaveY[saveCount]) or (x == self.arraySaveXP2[saveCount] and y == self.arraySaveYP2[saveCount]) or (x == self.arraySaveAIX[saveCount] and y == self.arraySaveAIY[saveCount]):
                    return False
            elif(player == 2):
                if (x == self.arraySaveX[saveCount] and y == self.arraySaveY[saveCount]) or (x == self.arraySaveXP2[saveCount] and y == self.arraySaveYP2[saveCount]):
                    return False
            elif(player == 3):
                if (x == self.arraySaveX[saveCount] and y == self.arraySaveY[saveCount]) or (x == self.arraySaveAIX[saveCount] and y == self.arraySaveAIY[saveCount]) or (x == self.arraySaveXP2[saveCount] and y == self.arraySaveYP2[saveCount]):
                    return False
            saveCount+=1
        return True

    def Player1Turn(self,row,col):          
        positions = self.getPosition(1,row,col)
        for x, y, color in positions:
            self.update_2x2_square(x, y, color)
        return jsonify({"status": "Player 1's turn completed"})

    def Player2Turn(self,row,col):        
        positions = self.getPosition(2,row,col)        
        for x, y, color in positions:
            self.update_2x2_square(x, y, color)
        return jsonify({"status": "Player 1's turn completed"})

    def update_2x2_square(self,x, y, color):
        self.gameBoardArray[y:y + 2, x:x + 2] = color

    def choosePos(self, player, row, col):              
        if player == 1:
            if row == 0:
                if col == 0:
                    pos = [(0, 0), (1, 1)]
                    self.positionSave(1,0,0)
                    self.positionSave(5,0,1)
                elif col == 1:
                    pos = [(0, 0), (1, 1)]
                    self.positionSave(1,0,0)
                    self.positionSave(5,0,1)                    
                elif col == 3:
                    pos = [(3, 0), (4, 1)]
                    self.positionSave(1,3,0)
                    self.positionSave(5,0,2)  
                elif col == 4:
                    pos = [(3, 0), (4, 1)]
                    self.positionSave(1,3,0)
                    self.positionSave(5,0,2)        
                elif col == 6:                    
                    pos = [(6, 0), (7, 1)]
                    self.positionSave(1,6,0)
                    self.positionSave(5,0,3)     
                elif col == 7:
                    pos = [(6,0), (7,1)]
                    self.positionSave(1,6,0)
                    self.positionSave(5,0,3) 
                     
            if row == 1:
                if col == 0:
                    pos = [(0, 0), (1, 1)]
                    self.positionSave(1,0,0)
                    self.positionSave(5,0,1) 
                elif col == 1:
                    pos = [(0, 0), (1, 1)]
                    self.positionSave(1,0,0)
                    self.positionSave(5,0,1)                     
                elif col == 3:
                    pos = [(3, 0), (4, 1)]
                    self.positionSave(1,3,0)
                    self.positionSave(5,0,2)   
                elif col == 4:
                    pos = [(3, 0), (4, 1)]
                    self.positionSave(1,3,0)
                    self.positionSave(5,0,2)        
                elif col == 6:
                    pos = [(6,0),(7,1)]
                    self.positionSave(1,6,0)
                    self.positionSave(5,0,3)   
                elif col == 7:
                    pos = [(6,0),(7,1)]
                    self.positionSave(1,6,0)
                    self.positionSave(5,0,3)                       
            elif row == 3:
                if col == 0:
                    pos = [(0,3),(1,4)]
                    self.positionSave(1,0,3)
                    self.positionSave(5,0,4) 
                elif col == 1:
                    pos = [(0,3),(1,4)]
                    self.positionSave(1,0,3)
                    self.positionSave(5,0,4)                    
                elif col == 3:
                    pos = [(3,3),(4,4)]
                    self.positionSave(1,3,3)
                    self.positionSave(5,0,5)   
                elif col == 4:
                    pos = [(3,3),(4,4)]
                    self.positionSave(1,3,3)
                    self.positionSave(5,0,5)         
                elif col == 6:
                    pos = [(6,3),(7,4)]
                    self.positionSave(1,6,3)
                    self.positionSave(5,0,6)   
                elif col == 7:
                    pos = [(6,3),(7,4)]
                    self.positionSave(1,6,3)
                    self.positionSave(5,0,6)   
            elif row == 4:
                if col == 0:
                    pos = [(0,3),(1,4)]
                    self.positionSave(1,0,3)
                    self.positionSave(5,0,4)  
                elif col == 1:
                    pos = [(0,3),(1,4)]
                    self.positionSave(1,0,3)
                    self.positionSave(5,0,4)                    
                elif col == 3:
                    pos = [(3,3),(4,4)]
                    self.positionSave(1,3,3)
                    self.positionSave(5,0,5)   
                elif col == 4:
                    pos = [(3,3),(4,4)]
                    self.positionSave(1,3,3)
                    self.positionSave(5,0,5)         
                elif col == 6:
                    pos = [(6,3),(7,4)]
                    self.positionSave(1,6,3)
                    self.positionSave(5,0,6)    
                elif col == 7:
                    pos = [(6,3),(7,4)]
                    self.positionSave(1,6,3)
                    self.positionSave(5,0,6)    
            elif row == 6:
                if col == 0:
                    pos = [(0,6),(1,7)]
                    self.positionSave(1,0,6)
                    self.positionSave(5,0,7) 
                elif col == 1:
                    pos = [(0,6),(1,7)]
                    self.positionSave(1,0,6)
                    self.positionSave(5,0,7)                   
                elif col == 3:
                    pos = [(3,6),(4,7)]
                    self.positionSave(1,3,6)
                    self.positionSave(5,0,8) 
                elif col == 4:
                    pos = [(3,6),(4,7)]
                    self.positionSave(1,3,6)
                    self.positionSave(5,0,8)        
                elif col == 6:
                    pos = [(7,7),(6,6)]
                    self.positionSave(1,6,6)
                    self.positionSave(5,0,9)  
                elif col == 7:
                    pos = [(7,7),(6,6)]
                    self.positionSave(1,7,7)
                    self.positionSave(5,0,9)  
            elif row == 7:
                if col == 0:
                    pos = [(0,6),(1,7)]
                    self.positionSave(1,0,6) 
                    self.positionSave(5,0,7)
                elif col == 1:
                    pos = [(0,6),(1,7)]
                    self.positionSave(1,0,6)
                    self.positionSave(5,0,7)                   
                elif col == 3:
                    pos = [(3,6),(4,7)]
                    self.positionSave(1,3,6) 
                    self.positionSave(5,0,8)
                elif col == 4:
                    pos = [(3,6),(4,7)]
                    self.positionSave(1,3,6)
                    self.positionSave(5,0,8)        
                elif col == 6:
                    pos = [(7,7),(6,6)]
                    self.positionSave(1,7,7) 
                    self.positionSave(5,0,9) 
                elif col == 7:
                    pos = [(7,7),(6,6)]
                    self.positionSave(1,7,7)
                    self.positionSave(5,0,9) 

        elif player == 2:
            print("choose player 2")
            if row == 0:
                if col == 0:
                    pos = [(0, 1), (1, 0)]
                    self.positionSave(2,0,1)
                elif col == 1:
                    pos = [(0, 1), (1, 0)]  
                    self.positionSave(2,0,1)                  
                elif col == 3:
                    pos = [(3, 1), (4, 0)]
                    self.positionSave(2,3,1)  
                elif col == 4:
                    pos = [(3, 1), (4, 0)] 
                    self.positionSave(2,3,1)        
                elif col == 6:
                    pos = [(6,1),(7,0)]
                    self.positionSave(2,6,1)     
                elif col == 7:
                    pos = [(6,1), (7,0)] 
                    self.positionSave(2,6,1)  
            if row == 1:
                if col == 0:
                    pos = [(0, 1), (1, 0)]
                    self.positionSave(2,0,1)
                elif col == 1:
                    pos = [(0, 1), (1, 0)]  
                    self.positionSave(2,0,1)                  
                elif col == 3:
                    pos = [(3, 1), (4, 0)]
                    self.positionSave(2,3,1)  
                elif col == 4:
                    pos = [(3, 1), (4, 0)] 
                    self.positionSave(2,3,1)        
                elif col == 6:
                    pos = [(6,1),(7,0)]
                    self.positionSave(2,6,1)     
                elif col == 7:
                    pos = [(6,1), (7,0)] 
                    self.positionSave(2,6,1)                    
            elif row == 3:
                if col == 0:
                    pos = [(0,4),(1,3)]
                    self.positionSave(2,0,4) 
                elif col == 1:
                    pos = [(0,4),(1,3)]
                    self.positionSave(2,0,4)                  
                elif col == 3:
                    pos = [(3,4),(4,3)] 
                    self.positionSave(2,3,4)
                elif col == 4:
                    pos = [(3,4),(4,3)] 
                    self.positionSave(2,3,4)      
                elif col == 6:
                    pos = [(6,4),(7,3)] 
                    self.positionSave(2,6,4)
                elif col == 7:
                    pos = [(6,4),(7,3)] 
                    self.positionSave(2,6,4)
            elif row == 4:
                if col == 0:
                    pos = [(0,4),(1,3)]
                    self.positionSave(2,0,4) 
                elif col == 1:
                    pos = [(0,4),(1,3)]
                    self.positionSave(2,0,4)                  
                elif col == 3:
                    pos = [(3,4),(4,3)] 
                    self.positionSave(2,3,4)
                elif col == 4:
                    pos = [(3,4),(4,3)] 
                    self.positionSave(2,3,4)      
                elif col == 6:
                    pos = [(6,4),(7,3)] 
                    self.positionSave(2,6,4)
                elif col == 7:
                    pos = [(6,4),(7,3)] 
                    self.positionSave(2,6,4)
            elif row == 6:
                if col == 0:
                    pos = [(0,7),(1,6)]
                    self.positionSave(2,0,7)
                elif col == 1:
                    pos = [(0,7),(1,6)]
                    self.positionSave(2,0,7)                 
                elif col == 3:
                    pos = [(3,7),(4,6)]
                    self.positionSave(2,3,7)
                elif col == 4:
                    pos = [(3,7),(4,6)] 
                    self.positionSave(2,3,7)      
                elif col == 6:
                    pos = [(7,6),(6,7)] 
                    self.positionSave(2,6,7)
                elif col == 7:
                    pos = [(7,6),(6,7)]
                    self.positionSave(2,6,7) 
            elif row == 7:
                if col == 0:
                    pos = [(0,7),(1,6)]
                    self.positionSave(2,0,7)
                elif col == 1:
                    pos = [(0,7),(1,6)]
                    self.positionSave(2,0,7)                 
                elif col == 3:
                    pos = [(3,7),(4,6)]
                    self.positionSave(2,3,7)
                elif col == 4:
                    pos = [(3,7),(4,6)] 
                    self.positionSave(2,3,7)      
                elif col == 6:
                    pos = [(7,6),(6,7)] 
                    self.positionSave(2,6,7)
                elif col == 7:
                    pos = [(7,6),(6,7)]
                    self.positionSave(2,6,7)  
        print("choose player 2")
        return pos

    def getPosition(self, player, row, col):                
        if player == 1:
            player_updated_positions = self.choosePos(player, row, col)
        elif player == 2:            
            player_updated_positions = self.choosePos(player, row, col)            
        elif player == 3:
            player_updated_positions = self.chooseAiPos(3)
        elif player == 4:
            player_updated_positions = self.chooseAiPos(4)            
        else:
            updated_positions = [
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
                (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
                (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)
            ]
        all_positions = [(x, y) for x in range(8) for y in range(8)]
        if self.turns == 9:
            self.reset()
            self.sheet.openSpreadsheet()
            self.sheet.resetMoveIndex()         
        self.turns += 1
        self.playerPosX = row
        self.playerPosY = col
        self.sendDataToSpreadSheet()
       
        if self.win_condition(1):
            self.sheet.createSpreadsheet()#these are used to update the game id for everytime the user wins                      
            raise win()           
        elif self.win_condition(2):
            self.sheet.createSpreadsheet()             
            raise win()
        elif self.win_condition(3): 
            self.sheet.createSpreadsheet()             
            raise win()       
        elif self.win_condition(4): 
            self.sheet.createSpreadsheet()             
            raise win()
        
            

        if player == 1:
            return [(x, y, self.player1Colour) if (x, y) in player_updated_positions else (x, y, tuple(self.gameBoardArray[y, x])) for x, y in all_positions]
        elif player == 2:
            return [(x, y, self.player2Colour) if (x, y) in player_updated_positions else (x, y, tuple(self.gameBoardArray[y, x])) for x, y in all_positions]
        elif player == 3:
            return [(x, y, self.weekAiColour) if (x, y) in player_updated_positions else (x, y, tuple(self.gameBoardArray[y, x])) for x, y in all_positions]
        elif player == 4:
            return [(x, y, self.weekAiColour) if (x, y) in player_updated_positions else (x, y, tuple(self.gameBoardArray[y, x])) for x, y in all_positions]
        else:
            return [(x, y, self.gameBoardColour) if (x, y) in updated_positions else (x, y, tuple(self.gameBoardArray[y, x])) for x, y in all_positions]

    def win_condition(self,player):
    
        winCombination1player1 = [(0,0),(3,0),(6,0)]  # 1 2 3
        winCombination2player1 = [(0,0),(0,3),(0,6)]  # 1 4 7
        winCombination3player1 = [(3,0),(3,3),(3,6)]  # 2 5 8
        winCombination4player1 = [(6,0),(6,3),(6,6)]  # 3 6 9
        winCombination5player1 = [(0,3),(3,3),(6,3)]  # 4 5 6
        winCombination6player1 = [(0,6),(3,6),(6,6)]  # 7 8 9
        winCombination7player1 = [(0,0),(3,3),(6,6)]  # 1 5 9
        winCombination8player1 = [(6,0),(3,3),(0,6)]  # 3 5 7

        winCombination1player2 = [(0,0),(3,0),(6,0)]  # 1 2 3
        winCombination2player2 = [(0,0),(0,3),(0,6)]  # 1 4 7
        winCombination3player2 = [(3,0),(3,3),(3,6)]  # 2 5 8
        winCombination4player2 = [(6,0),(6,3),(6,6)]  # 3 6 9
        winCombination5player2 = [(0,3),(3,3),(6,3)]  # 4 5 6
        winCombination6player2 = [(0,6),(3,6),(6,6)]  # 7 8 9
        winCombination7player2 = [(0,0),(3,3),(6,6)]  # 1 5 9
        winCombination8player2 = [(6,0),(3,3),(0,6)]  # 3 5 7

        winCombination1 = [1,2,3]  # 1 2 3
        winCombination2 = [1,4,7]  # 1 4 7
        winCombination3 = [2,5,8]   # 2 5 8
        winCombination4 = [3,6,9]   # 3 6 9
        winCombination5 = [4,5,6]  # 4 5 6
        winCombination6 = [7,8,9]   # 7 8 9
        winCombination7 = [1,5,9]   # 1 5 9
        winCombination8 = [3,5,7]   # 3 5 7
        
        win_combinations = [winCombination1player1, winCombination2player1, winCombination3player1,
                        winCombination4player1, winCombination5player1, winCombination6player1,
                        winCombination7player1, winCombination8player1,]
        win_combinationsPlayer2= [winCombination1player2,
                        winCombination2player2, winCombination3player2, winCombination4player2,
                        winCombination5player2, winCombination6player2, winCombination7player2,
                        winCombination8player2]
        
        win_combinations_AI = [winCombination1, winCombination2, winCombination3, winCombination4,
                        winCombination5, winCombination6, winCombination7,
                        winCombination8]
        
        player_position1 = [(x, y) for x, y in zip(self.arraySaveX, self.arraySaveY) if (x, y) != (-1, -1)]
        player_position2 = [(x, y) for x, y in zip(self.arraySaveXP2, self.arraySaveYP2) if (x, y) != (-1, -1)]
        player_AI = [(x, y) for x, y in zip(self.arraySaveAIX, self.arraySaveAIY) if (x, y) != (-1, -1)]
        
        if player ==1:
            for combination in win_combinations:
                if all(position in player_position1 for position in combination):
                    self.reset()                   
                    return True

            return False
        
        elif player ==2:
            for combination in win_combinationsPlayer2:
                if all(position in player_position2 for position in combination):
                    self.reset()                    
                    return True
            return False
        
        elif player ==3:
            for combination in win_combinationsPlayer2:
                if all(position in player_AI for position in combination):
                    self.reset()                    
                    return True
            return False
        
        elif player == 4:
            for combination in win_combinations_AI:
                if all(position in player_AI for position in combination):
                    self.reset()                    
                    return True
            return False
        else:
            return False
        

    def reset(self):
        self.winCode = 0
        self.gameBoardArray[:] = 0 #reset all the indexes in the array to 0 and send back to html file
        self.player1Save = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.player2Save = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.playerAISave = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.moveLeft = [1,2,3,4,5,6,7,8,9]
        self.allplayedMoves = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.checkP1 = [-1]*9
        self.checkAI = [-1]*9

        self.arraySaveXP2 = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.arraySaveYP2 = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.arraySaveX = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.arraySaveY = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.arraySaveAIX= [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.arraySaveAIY= [-1,-1,-1,-1,-1,-1,-1,-1,-1]

        self.countP1 = 0
        self.countP2 = 0
        self.countAI = 0
        self.played = 0
        self.countP1save = 0

        self.playerCount = 1
        self.turns = 0
        self.strong = 0
        
    def set_routes(self):
        @self.app.route('/strongAi')
        def strongAi():
            try:
                if self.playerCheck == 1 and self.aiTurn == 0:
                    return jsonify({'error': 'Player 2 is playing'}), 400
                else:
                    if (self.users ==1):
                        return self.strongAI()                
            except OutOfBoundsError as e:
                return jsonify({'error': str(e)}), 400  
            except win as e:
                #self.db.playerInformation()
                return jsonify({'error': str(e)}), 300          
            except Exception as e:                
                return jsonify({'error': str(e)}), 500            
            
        @self.app.route('/open_spreadsheet')
        def openSpreadsheet():
            spreadsheet_url = self.sheet.openSpreadsheet()
            return jsonify({'url': spreadsheet_url})
        
        @self.app.route('/get_game_board')
        def get_game_board():
            return jsonify(self.gameBoardArray.tolist()) #return the gameboard as a json format to the html file         
        
        @self.app.route('/resetGameBoard')
        def resetGameBoard():            
            self.reset()
            return jsonify(self.gameBoardArray.tolist())        

        @self.app.route('/weekai')
        def week_ai():
            try:
                if self.playerCheck == 1 and self.aiTurn == 0:
                    return jsonify({'error': 'Player 2 is playing'}), 400
                else:
                    if (self.users ==1):
                        return self.weekAi()                
            except OutOfBoundsError as e:
                return jsonify({'error': str(e)}), 400
            except win as e:
                return jsonify({'error': str(e)}), 300            
            except Exception as e:                
                return jsonify({'error': str(e)}), 500
            

        @self.app.route('/select_position', methods=['POST'])
        def select_position():
            try:                
                data = request.json  # Get JSON data from request body
                row = int(data['row'])  # Convert row to integer
                col = int(data['col'])  # Convert col to integer
                
                while True:
                    if self.checkSave(self.playerNumber, row, col) == False:
                        raise InvalidPosition()  
                    else:                        
                        break
                                    
                #switch between player 1 and player 2 every time
                ip = request.access_route[-1] #get the "ip address" of the user that clicked on the screen                                                              
                print(f"users = {self.ip_Address}")
                if ip == self.ip_Address[0] and self.playerNumber == 1:# if the ip address is the same as the ip address of the first person to login                                  
                    print(f"users = {self.users}")
                    if self.users == 1:
                        if self.turns % 2 == 0:
                            self.winCode = 300 
                            self.Player1Turn(row, col)
                                                   
                    else: 
                        if self.turns % 2 == 0: 
                            self.winCode = 300                      
                            self.Player1Turn(row, col)# send them to the player1turn function                                  
                            self.playerNumber = 2# add 1 to playerNumber so that the second player can play 
                                                      
                elif ip == self.ip_Address[1] and self.playerNumber == 2:
                    if self.users == 1:                        
                        if self.turns % 2 == 0:
                            self.winCode = 301 
                            self.Player2Turn(row, col)                                                       
                    else:
                        if self.turns % 2 == 1:
                            self.winCode = 301                                                 
                            self.Player2Turn(row, col)                            
                            self.playerNumber = 1                
                # Convert numpy array to list before returning
                game_board_list = self.gameBoardArray.tolist()
                return jsonify(game_board_list)
            except InvalidPosition as e:
                self.turns -=1
                return jsonify({'error': str(e)}), 500
            except OutOfBoundsError as e:# if the error is that the user clicked somewhere that was not supposed to be clicked 
                return jsonify({'error': str(e)}), 400 #return error 400
            except win as e:                
                return jsonify({'error': str(e)}),self.winCode
            except Exception as e:# any other exception is error code 500
                print(e)
                return jsonify({'error': str(e)}), 501
            
            

        @self.auth.verify_password #function to verify the users password and username and also store the users ip address
        def verify_password(username, password):
            if self.usernameCount == 0:
                self.playerUsername[0] = username # store the username
                self.playerPassword = password # store the password 
                self.email[0] = request.form['Email']
                self.usernameCount+=1
            else:
                self.playerUsername[1] = username # store the username
                self.email[1] = request.form['Email']
                self.playerPassword = password # store the password  
            try: 
                print(self.email) 
                if password == 'Dylan':
                    session['logged_in'] = True #if the username and password are correct set the current session as true 
                    if self.ip_Address[0] == None and self.users == 1:#if there is a user logged in with no ip address 
                        self.users -=1 
                    self.ip_Address[self.users] = request.access_route[-1] # store the ip addresses of the users that login to the server
                    self.users +=1
                    if(self.users > 2): # make sure that only 2 people can login to the server at any time
                        return False
                    return True
                return False
            except Exception:
                return False

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            try:
                if request.method == 'POST': #if the html code sends a post message to the server
                    if verify_password(request.form['username'], request.form['password']):  #check if the username and password is true                                     
                        return redirect(url_for('index')) # send the user to the index.html file webserver
                    else:
                        return render_template('login.html', error='Invalid username or password') # if the credentials are incorrect
                                                                                                # Call the login.html again and display a error
                return render_template('login.html')
            except Exception:
                return render_template('login.html', error='Invalid username or password') 

        @self.app.route('/logout', methods=['POST'])#function to logout users from the server and delete their ip address from the server
        def logout():
            session.pop('logged_in', None)
            self.users -= 1
            ip = request.access_route[-1] # get the ip address of the user at the moment of logout            
            if ip == self.ip_Address[0]:# if the users ip address is the same as the first user that logged 
                self.ip_Address[0] = None # remove that users ip address from the server  
                self.playerNumber[0] = None                         
            elif ip == self.ip_Address[1]:
                self.ip_Address[1] = None 
                self.playerNumber[1] = None                            
            print(f"After deletion = {self.ip_Address}")
            return redirect(url_for('login'))

        @self.app.route('/')# Route to the homepage, which renders the login.html template when accessed 
        def index():
            if 'logged_in' in session and session['logged_in']: # if the seesion is logged in 
                return render_template('index.html') # send the user to the index.html file
            else:
                return redirect(url_for('login')) # if its not send the user to the login.html file  
                  
    def run(self):
        self.set_routes()
        self.app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)

if __name__ == '__main__':
    game = TicTacToeGame()    
    game.run()