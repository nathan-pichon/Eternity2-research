#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import csv
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

    def init_algo(self):
        for i in range(self.numberOfBoards):
            self.boards.append(Board())

    def getBest(self):
        for i in self.boards:
            if (i.note > self.best.note):
                self.best = i

    def crossover(self):

    def mutate(self):

    def doAlgorithm(self):
        for i in self.boards:
            # crossover

            # mutate


            # substract life
            i.life -= 1
            # remove dead boards
            if (i.life == 0):
                self.boards.remove(i)
