#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import csv, random, copy
from piece import Piece
from board import Board

## algorithm
## for our program it's like one island
## self.boards is an array of boards
## self.best is the best board

class algorithm:
    def __init__(self, numberOfBoards):
        self.boards = []
        self.numberOfBoards = numberOfBoards
        self.init_algo()
        self.best = self.boards[0]
        self.getBest()
        self.genCount = 1

    # Init algo with numberOfBoards boards in the list
    def init_algo(self):
        for i in range(self.numberOfBoards):
            self.boards.append(Board())

    # Get the best board
    def getBest(self):
        for i in self.boards:
            if (i.note > self.best.note):
                self.best = i

    # crossover between two boards and add it to the list
    def crossoverOne(self, first, second):
        num = random.randrange(0, 16*16-1)
        t = second.board[num]
        second2 = copy.copy(second)
        first2 = copy.copy(first)
        second2.life = random.randrange(7, 12)
        first2.life = random.randrange(7, 12)
        second2.change(num, first.board[num])
        first2.change(num, t)
        self.boards.append(second2)
        self.boards.append(first2)

    # crossover
    # we cross half population with a wheel selection
    def crossover(self):
        numToCross = self.numberOfBoards / 2
        sortedBoards = sorted(self.boards, key=lambda board: board.note, reverse=True)
        maximum = 0
        for i in sortedBoards:
            maximum += i.note
        for u in range(0, numToCross):
            np = random.randrange(0,maximum)
            first = sortedBoards[0]
            second = sortedBoards[0]
            for i in sortedBoards:
                np -= i.note
                if (np <= 0):
                    np += maximum
                    first = i
            np = random.randrange(0,maximum)
            for i in sortedBoards:
                np -= i.note
                if (i == first):
                    np += i.note
                if (np <= 0):
                    np += maximum
                    second = i
            self.crossoverOne(first, second)

    # mutate
    # call mutate of the board
    def mutate(self):
        n = random.randrange(0, len(self.boards)-1)
        self.boards[n].mutate(random.randrange(0, 16*16-1))


    # One Generation
    # Call it for each generation
    def doOneGen(self):
        self.genCount += 1
        # crossover

        self.crossover()
        # mutate
        self.mutate()
        maximum = 0
        for i in self.boards:
            if (i.note > maximum):
                maximum = i.note
        print maximum
        for i in self.boards:
            # substract life
            i.life -= 1
            print "life = " + str(i.life)
            # remove dead boards
            if (i.life <= 0):
                self.boards.remove(i)
        self.getBest()