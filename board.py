#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import csv, random
from piece import Piece

## BOARD OF THE GAME
## self.board is the board
## self.note is the note of the board
TOP = 0
BOT = 1
LEFT = 2
RIGHT = 3

BORDER = 0

class Board:

    #ctr
    def __init__(self):
        self.board = []
        self.note = 0
        self.life = random.randrange(7, 12)
        self.init_board()
        self.notate()

    # Initialize Board with random pieces
    def init_board(self):
        random_pieces = np.arange(16*16)
        np.random.shuffle(random_pieces)
        all_pieces = []
        with open('project/e2pieces.txt', 'rb') as csvFile:
            e2pieces = csv.reader(csvFile, delimiter=';', quotechar='|')
            for row in e2pieces:
                if (row[0] != "Top"):
                    all_pieces.append(np.asarray(row).astype(int))
        for i in random_pieces:
            self.board.append(Piece(all_pieces[i], i))


    # Mutate the element mut to a random mutated2
    # We have to change the place where mutated2 was before with mutated1
    def mutate(self, mut):
        mutated1 = self.board[mut]
        mutated2 = random.randrange(0, 16*16)
        for i in range(0, len(self.board)):
            if (self.board[i].piece == mutated2):
                self.board[mut]=self.board[i]
                self.board[i]=mutated1
                mutated2 = -1
        self.notate()

    def change(self, num, numm):
        tmp = self.board[num]
        for i in range(0, len(self.board)):
            if (self.board[i].piece == tmp):
                self.board[num]=numm
                self.board[i]=tmp
                mutated2 = -1
        self.notate()


    # Get Note for the board
    # We add +1 for each faces that match
    def notate(self):
        self.note = 0
        i = 0
        for i in range(len(self.board)):
            if (i > 16): #NOT TOP
                if (self.board[i].faces[TOP] == self.board[i-16].faces[BOT]):
                    self.note += 1
            else: #TOP
                if self.board[i].faces[TOP] == BORDER:
                    self.note += 1
            if (i < 240): #NOT BOT
                if (self.board[i].faces[BOT] == self.board[i+16].faces[TOP]):
                    self.note += 1
            else: #BOT
                if self.board[i].faces[BOT] == BORDER:
                    self.note += 1
            if (i % 16==0): #LEFT
                if (self.board[i].faces[RIGHT] == self.board[i+1].faces[LEFT]):
                    self.note += 1
                elif self.board[i].faces[LEFT] == BORDER:
                    self.note += 1
            elif (i % 16==15): #RIGT
                if (self.board[i].faces[LEFT] == self.board[i-1].faces[RIGHT]):
                    self.note += 1
                elif self.board[i].faces[RIGHT] == BORDER:
                    self.note += 1
            else: #MIDDLE
                if (self.board[i].faces[RIGHT] == self.board[i+1].faces[LEFT]):
                    self.note += 1
                if (self.board[i].faces[LEFT] == self.board[i-1].faces[RIGHT]):
                    self.note += 1
            i+=1

    # Helper to print board
    def printBoard(self):
        i = 0
        while i < len(self.board):
            print str(self.board[i].piece) + "\t" + str(self.board[i+1].piece) + "\t" + str(self.board[i+2].piece) + "\t" + str(self.board[i+3].piece) + "\t" + str(self.board[i+4].piece) + "\t" + str(self.board[i+5].piece) \
            + "\t" + str(self.board[i+6].piece) + "\t" + str(self.board[i+7].piece) + "\t" + str(self.board[i+8].piece) + "\t" + str(self.board[i+9].piece) + "\t" + str(self.board[i+10].piece) + "\t" + str(self.board[i+11].piece) \
            + "\t" + str(self.board[i+12].piece) + "\t" + str(self.board[i+13].piece) + "\t" + str(self.board[i+14].piece)+ "\t" + str(self.board[i+15].piece)
            i+=16

    def toString(self):
        i = 0
        mystr = ""
        while i < len(self.board):
            mystr = str(self.board[i].piece) + " " + str(self.board[i+1].piece) + " " + str(self.board[i+2].piece) + " " + str(self.board[i+3].piece) + " " + str(self.board[i+4].piece) + " " + str(self.board[i+5].piece) \
            + " " + str(self.board[i+6].piece) + " " + str(self.board[i+7].piece) + " " + str(self.board[i+8].piece) + " " + str(self.board[i+9].piece) + " " + str(self.board[i+10].piece) + " " + str(self.board[i+11].piece) \
            + " " + str(self.board[i+12].piece) + " " + str(self.board[i+13].piece) + " " + str(self.board[i+14].piece)+ " " + str(self.board[i+15].piece) + "\n"
            i+=16
        return mystr
    
    def toArray(self):
        i = 0
        array = []
        while i < len(self.board):
            array.append(self.board[i].piece)
            array.append(self.board[i+1].piece)
            array.append(self.board[i+2].piece)
            array.append(self.board[i+3].piece)
            array.append(self.board[i+4].piece)
            array.append(self.board[i+5].piece)
            array.append(self.board[i+6].piece)
            array.append(self.board[i+7].piece)
            array.append(self.board[i+8].piece)
            array.append(self.board[i+9].piece)
            array.append(self.board[i+10].piece)
            array.append(self.board[i+11].piece)
            array.append(self.board[i+12].piece)
            array.append(self.board[i+13].piece)
            array.append(self.board[i+14].piece)
            array.append(self.board[i+15].piece)
            i+=16
        return array
