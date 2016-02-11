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
        all_pieces = []
        corner_counter = 0        
        board = [0 for i in range(16*16)]
        random_pieces = np.arange(16*16)
        np.random.shuffle(random_pieces)
        with open('project/e2pieces.txt', 'rb') as csvFile:
            e2pieces = csv.reader(csvFile, delimiter=';', quotechar='|')
            for row in e2pieces:
                if (row[0] != "Top"):
                    all_pieces.append(np.asarray(row).astype(int))
        for i in random_pieces:
            self.board.append(Piece(all_pieces[i], i))

        # print(len(self._get_exclude(16)))

        # for i in range(len(all_pieces)):
        #     if list(all_pieces[i]).count(BORDER) == 2:
        #         if corner_counter == 0:
        #             board[0] = Piece(all_pieces[i], i)
        #         elif corner_counter == 1:
        #             board[15] = Piece(all_pieces[i], i)
        #         elif corner_counter == 2:
        #             board[240] = Piece(all_pieces[i], i)
        #         elif corner_counter == 3:
        #             board[255] = Piece(all_pieces[i], i)
        #     elif list(all_pieces[i]).count(BORDER) == 1:
        #         board[self._get_first_border_free(board)] = Piece(all_pieces[i], i)
        #     else:
        #         print(self._get_randomize_free_place(board))
        #         board[self._get_randomize_free_place(board)] = Piece(all_pieces[i], i)
        # print(board)

    def _get_first_border_free(self, board):
        exclude = [0,15,240,255]
        for i in range(len(board)):
            if (i < 16 and board[i] == BORDER) and i not in exclude:
                return i
            elif i%16 == 0 and board[i] == BORDER:
                return i
            elif i%16 == 15 and board[i] == BORDER:
                return i
            elif (i > 239 and board[i] == BORDER) and i not in exclude:
                return i
        return None

    def _get_exclude(self, size):
        exclude = [i for i in range(size)]
        exclude += [i for i in range((size*(size-1)), ((size*size)-1))]
        exclude += [i for i in range(16, (size*(size-1)), 16)]
        exclude += [i for i in range((size*2)-1, ((size*size)-1), 16)]
        return exclude

    def _get_randomize_free_place(self, board):
        rand = random.randrange(0, 16*16)
        if not rand in self._get_exclude(16):
            if board[rand] == 0:
                return rand
            else:
                self._get_randomize_free_place(board)
        else:
            self._get_randomize_free_place(board)


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
