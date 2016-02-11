#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import copy
import random
import pickle
from datetime import datetime

from algorithm import algorithm

class IslandGenBackup:
	def __init__(self, genCount, algorithms, migrationsTurnover, populationNb, boardsNb, bestBoard):
		self.genCount = genCount
		self.algorithms = algorithms
		self.populationNb = populationNb
		self.turnover = migrationsTurnover

		self.boardsNumber = boardsNb
		self.best = bestBoard

	def save(self, folder):
		with open(folder + '/data/generation_' + str(self.genCount) + '.pkl', 'wb') as output:
			pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

class IslandsAlgorithm(object):
	def __init__(self, islandNb, populationNb, migrationsTurnover, saveFolder):
		self.generationNumber = 0
		self.generationHistory = []

		self.populationNb = populationNb
		self.turnover = migrationsTurnover

		self.islands = self.initIsland(islandNb, populationNb)
		self.islandNumber = len(self.islands)

		self.best = self.islands[0].best

		self.mainFolder = saveFolder

		self.migrations = []


	def initIsland(self, islandNb, populationNb):
		return [algorithm(populationNb) for i in range(islandNb)]

	def doOneGen(self):
		self.migrations = []
		islands_algorithms = []
		for i in range(len(self.islands)):
			self.islands[i].doOneGen()
			islands_algorithms.append(copy.deepcopy(self.islands[i]))

		if (self.generationNumber % self.turnover) == 0:
			# self._randomizeMigration()
			self._linearMigration(random.randrange(0, int(self.populationNb/2)))
		self.getBest()
		self.generationHistory.append(IslandGenBackup(self.generationNumber, islands_algorithms, self.turnover, self.populationNb, self.getBoardsNumber(), self.best))
		self.generationHistory[self.generationNumber].save(self.mainFolder)
		self.generationNumber += 1

	def getRandom(self, limits, exclude=[]):
		randInt = random.randint(limits[0], limits[1])
		if randInt in exclude:
			self.getRandom(limits, exclude)
		return randInt

	def _linearMigration(self, toMigrateNb=1):
		for i in range(len(self.islands)):
			toMigrateIdxs = [self.getRandom((0, len(self.islands[i].boards)-1)) for j in range(toMigrateNb)]
			if i == len(self.islands)-1:
				[self.islands[0].boards.append(self.islands[i].boards[idx]) for idx in toMigrateIdxs]
				self.migrations.append({'time': datetime.now().time(), 'generation': self.generationNumber, 'from': i, 'to': 0, 'migrated_boards_idx': toMigrateIdxs})
				print "Migrate ({}) from island {} to island {}".format(toMigrateIdxs, i, 0)
			else:
				[self.islands[i+1].boards.append(self.islands[i].boards[idx]) for idx in toMigrateIdxs]
				self.migrations.append({'time': datetime.now().time(), 'generation': self.generationNumber, 'from': i, 'to': i+1, 'migrated_boards_idx': toMigrateIdxs})
				print "Migrate ({}) from island {} to island {}".format(toMigrateIdxs, i, i+1)
			self.islands[i].boards = [item for j, item in enumerate(self.islands[i].boards) if j not in toMigrateIdxs]

	def _randomizeMigration(self):
		prev_migrations = []
		for i in range(len(self.islands)):
			toMigrateIdxs = list(set([self.getRandom((0, len(self.islands[i].boards)-1)) for j in range(self.getRandom((0, len(self.islands[i].boards)-2)))]))
			toExclude = prev_migrations + [i]
			toMigrateIslandIdx = self.getRandom((0, len(self.islands)-1), toExclude)
			prev_migrations.append(toMigrateIslandIdx)
			[self.islands[toMigrateIslandIdx].boards.append(self.islands[i].boards[idx]) for idx in toMigrateIdxs]
			self.migrations.append({'time': datetime.now().time(), 'generation': self.generationNumber, 'from': i, 'to': toMigrateIslandIdx, 'migrated_boards_idx': toMigrateIdxs})
			print "Migrate ({}) from island {} to island {}".format(toMigrateIdxs, i, toMigrateIslandIdx)
			self.islands[i].boards = [item for j, item in enumerate(self.islands[i].boards) if j not in toMigrateIdxs]

	def getBest(self):
		for i in range(len(self.islands)):
			if self.islands[i].best.note > self.best.note:
				self.best = self.islands[i].best

	def getBoardsNumber(self):
		boardsNumber = 0
		for island in self.islands:
			boardsNumber += len(island.boards)
		return boardsNumber