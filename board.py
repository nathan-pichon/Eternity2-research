#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import csv
from piece import Piece

## BOARD OF THE GAME
## self.board is the board
## self.note is the note of the board
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

    # Get Note for the board
    # We add +1 for each faces that match
    def notate(self):
        self.note = 0
        i = 0
        for i in range(len(self.board)):
            if (i > 16): #NOT TOP
                if (random_pieces[i].faces[0] == random_pieces[i-16].faces[0]):
                    self.note += 1
            else: #TOP
                self.note += 0
            if (i < 240): #NOT BOT
                if (random_pieces[i].faces[1] == random_pieces[i+16].faces[1]):
                    self.note += 1
            else: #BOT
                self.note += 0
            if (i % 16==0): #LEFT
                if (random_pieces[i].faces[2] == random_pieces[i+1].faces[2]):
                    self.note += 1
            elif (i % 16==15): #RIGT
                if (random_pieces[i].faces[3] == random_pieces[i-1].faces[3]):
                    self.note += 1
            else: #MIDDLE
                if (random_pieces[i].faces[3] == random_pieces[i+1].faces[3]):
                    self.note += 1
                if (random_pieces[i].faces[2] == random_pieces[i-1].faces[2]):
                    self.note += 1
            i+=1

    # Helper to print board
    def printBoard(self):
        i = 0
        while i < len(self.board):
            print str(self.board[i].piece) + " " + str(self.board[i+1].piece) + " " + str(self.board[i+2].piece) + " " + str(self.board[i+3].piece) + " " + str(self.board[i+4].piece) + " " + str(self.board[i+5].piece) \
            + " " + str(self.board[i+6].piece) + " " + str(self.board[i+7].piece) + " " + str(self.board[i+8].piece) + " " + str(self.board[i+9].piece) + " " + str(self.board[i+10].piece) + " " + str(self.board[i+11].piece) \
            + " " + str(self.board[i+12].piece) + " " + str(self.board[i+13].piece) + " " + str(self.board[i+14].piece)+ " " + str(self.board[i+15].piece) + "\n"
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
        

def main():
    b = Board()
    b.printBoard()
main()
