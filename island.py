#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import random

from algorithm import algorithm

class IslandGenBackup:
	def __init__(self, genCount, algorithms):
		self.genCount = genCount
		self.algorithms = algorithms

class IslandsAlgorithm(object):
	def __init__(self, islandNb, populationNb, migrationsTurnover):
		self.generationNumber = 0
		self.generationHistory = []
		self.populationNb = populationNb
		self.turnover = migrationsTurnover
		self.islands = self.initIsland(islandNb, populationNb)

	def initIsland(self, islandNb, populationNb):
		return [algorithm(populationNb) for i in range(islandNb)]

	def doNextGen(self):
		islands_algorithms = []
		for i in range(len(self.islands)):
			self.islands[i].doOneGen()
			islands_algorithms.append(copy.deepcopy(self.islands[i]))
			if (self.generationNumber % self.turnover) == 0:
				self.linear_migration(random.randrange(0, int(self.populationNb/2)))
		self.generationHistory.append(IslandGenBackup(self.generationNumber, islands_algorithms))
		self.generationNumber += 1

	def linear_migration(self, toMigrateNb=1):
		for i in range(len(self.islands)):
			toMigrateIdxs = [random.randrange(0, self.populationNb-1) for j in range(toMigrateNb)]
			if i == len(self.islands)-1:
				[self.islands[0].boards.append(self.islands[i].boards[idx]) for idx in toMigrateIdxs]
			else:
				[self.islands[i+1].boards.append(self.islands[i].boards[idx]) for idx in toMigrateIdxs]
			[self.islands[i].boards.pop(idx) for idx in toMigrateIdxs]


if __name__ == '__main__':
	gen_nb = 1000
	islands = IslandsAlgorithm(3, 30, 20)
	for i in range(gen_nb):
		islands.doNextGen()

	max_note = None

	for i in range(gen_nb):
		for j in range(len(islands.generationHistory[i].algorithms)):
			for e in range(len(islands.generationHistory[i].algorithms[j].boards)):
				if max_note == None or max_note < islands.generationHistory[i].algorithms[j].boards[e].note:
					max_note = islands.generationHistory[i].algorithms[j].boards[e].note
				# print "Generation {} -- Ile {} -- Board {} -- Note {} -- Life {}".format(i, 
				# 															 		     j,
				# 															   			 e,
				# 															   			 islands.generationHistory[i].algorithms[j].boards[e].note,
				# 															   			 islands.generationHistory[i].algorithms[j].boards[e].life
				# 															  			)

	print "Le meilleur score est : {}".format(max_note)