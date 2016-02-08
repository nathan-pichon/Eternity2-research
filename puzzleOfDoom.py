#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *
from PIL import ImageTk, Image

import tkFileDialog
import copy
import os
import pickle
import csv
from datetime import datetime

from algorithm import algorithm
from island import IslandsAlgorithm

class LoggerCSV:
    def __init__(self, mainFolder):
        self.logsFolder = mainFolder + '/logs/'

    def init(self):
        # Log files
        self.generationCSV = open(self.logsFolder + 'generation.csv', 'a+')
        self.bestBoardCSV = open(self.logsFolder + 'bestBoard.csv', 'a+')

        # Writer with header
        fieldnamesGen = ['time', 'generation', 'note']
        self.generationWriter = csv.DictWriter(self.generationCSV, fieldnames=fieldnamesGen)
        self.generationWriter.writeheader()

        # Writer without header
        self.bestBoardWriter = csv.writer(self.bestBoardCSV)

    def writeGenerationCSV(self, data):
        self.generationWriter.writerow(data)

    def writeBestBoardCSV(self, data):
        self.bestBoardWriter.writerow(data)

class GenBackUp:
    def __init__(self, genCount, data):
        self.genCount = genCount
        self.data = data

    def save(self, mainFolder):
        with open(mainFolder + '/data/generation_' + str(self.genCount) + '.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

class PuzzleOfDoom:
    def __init__(self):
        self.windown = Tk()
        self.windown.resizable(width=FALSE, height=FALSE)
        self.windown.wm_title('Puzzle Of Doom')
        self.piecesIm = []
        self.inProcess = IntVar()
        self.inProcess.set(0)

        # Algorithms
        self.useIsland = False
        if self.useIsland:
            self.islands = IslandsAlgorithm(10, 4, 25)
        else:
            self.algorithm = algorithm(4)

        # Backup
        time = datetime.now()
        self.mainFolder = os.getcwd() + '/results/' + time.strftime('run-%Y-%m-%d_%H-%M-%S')
        self.sizeHistory = 25
        self.historyGen = []

        # Logger
        self.logger = LoggerCSV(self.mainFolder)

        # Board side
        self.cursorPosition = IntVar()
        self.cursorPosition.set(0)
        self.boardCount = IntVar()
        self.boardCount.set(0)

        self.nbrGen = IntVar()
        self.nbrGen.set(1)
        self.currentBoardLife = IntVar()
        self.currentBoardLife.set(0)
        self.currentBoardNote = IntVar()
        self.currentBoardNote.set(0)

        # Best side
        self.genCount = IntVar()
        self.genCount.set(1)

        self.currentBestLife = IntVar()
        self.currentBestLife.set(0)
        self.currentBestNote = IntVar()
        self.currentBestNote.set(0)

    def initUI(self):

        # Preload images
        for i in range(0, 256):
            im = Image.open("project/Eternity_resized/" + str(i + 1) + '.png')
            self.piecesIm.append(im.copy())
            im.close()
            self.piecesIm[i].thumbnail((25, 25), Image.ANTIALIAS)

        # Create results folders
        os.makedirs(self.mainFolder)
        os.makedirs(self.mainFolder + '/data/')
        os.makedirs(self.mainFolder + '/logs/')

        # Log fist gen
        self.logger.init()

        # Simple log
        self.logger.writeBestBoardCSV([self.genCount.get()] + self.algorithm.best.toArray())
        self.logger.writeGenerationCSV({'time': datetime.now().time(), 'generation': self.genCount.get(), 'note': self.algorithm.best.note})

        # Island log
        #

        if not self.useIsland:
            # Save gen data
            dataSaved = GenBackUp(self.genCount.get(), copy.deepcopy(self.algorithm));
            dataSaved.save(self.mainFolder);
            #self.historyGen.append(dataSaved);

            # Attach board to UI canvas
            self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
            self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)
        else:
            # Save gen data
            #
            #
            #

            # Attach board to UI canvas
            self.attachBoardToCanvas(self.islands.best.board, self.canvasBestFrame)
            self.attachBoardToCanvas(self.islands.islands[self.cursorPosition.get()].boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    def loadUI(self):
        self.note = Notebook(self.windown)

        self.loadTabGeneration()
        self.loadTabHistory()
        self.note.pack()

    def loadTabGeneration(self):
        self.tabGeneration = Frame(self.note)

        self.loadBestFrame()
        self.loadBoardFrame()

        self.loadMenu()
        self.note.add(self.tabGeneration, text="Generation")

    def loadTabHistory(self):
        self.tabHistory = Frame(self.note)
        self.note.add(self.tabHistory, text="History")

    def loadMenu(self):
        menubar = Menu(self.windown)

        menu1 = Menu(menubar, tearoff=0)
        #menu1.add_command(label="Save", command=self.save)
        menu1.add_command(label="Load", command=self.load)
        menu1.add_separator()
        menu1.add_command(label="Quit", command=self.windown.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=menu3)

        self.windown.config(menu=menubar)

    def loadBestFrame(self):
        # Left side, show best board for the current generation
        bestFrame = LabelFrame(self.tabGeneration, text=" Best board of the generation ")
        bestFrame.pack(side=LEFT, padx=15, pady=15)

        # Panel canvas & controllers + stats
        p = PanedWindow(bestFrame, orient=VERTICAL)
        p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        # Panel canvas + controllers
        panel1 = Label(p, text='Canvas + Controllers', anchor=CENTER)
        p.add(panel1)

        # Canvas = board
        self.canvasBestFrame = Canvas(panel1, width=400, height=400, background='black')
        self.canvasBestFrame.pack(side=TOP, padx=5, pady=5)

        # Button frame
        buttomFrame = Frame(panel1, relief=FLAT, borderwidth=1)
        buttomFrame.pack(side=BOTTOM, padx=5, pady=5)

        self.entree = Entry(buttomFrame, textvariable=self.nbrGen, width=10)
        self.entree.pack(side=LEFT)
        Button(buttomFrame, text="Generate", command=self.doNextGen).pack(side=LEFT, padx=5, pady=5)

        # Stats
        panel2 = Label(p, text='Statistiques', anchor=CENTER)
        p.add(panel2)

        statsFrame = LabelFrame(panel2, text=" Statistiques ")
        statsFrame.pack(fill=X, padx=15, pady=15)

        # Panel stats
        pstats = PanedWindow(statsFrame, orient=VERTICAL)
        pstats.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        pstats1 = Label(pstats, text='Generation n°', anchor=W)
        Label(pstats1, textvariable=self.genCount).pack()
        pstats.add(pstats1)

        pstats2 = Label(pstats, text='In process: ', anchor=W)
        Label(pstats2, textvariable=self.inProcess).pack()
        pstats.add(pstats2)

        pstats3 = Separator(pstats)
        pstats.add(pstats3)

        pstats4 = Label(pstats, text='Best Note: ', anchor=W)
        Label(pstats4, textvariable=self.currentBestNote).pack()
        pstats.add(pstats4)

        pstats4 = Label(pstats, text='Best Life: ', anchor=W)
        Label(pstats4, textvariable=self.currentBestLife).pack()
        pstats.add(pstats4)

    def loadBoardFrame(self):
        # Right side, show all boards for the current generation
        boardsFrame = LabelFrame(self.tabGeneration, text=" Boards ")
        boardsFrame.pack(side=RIGHT, padx=15, pady=15)

        # Panel canvas & controllers + stats
        p = PanedWindow(boardsFrame, orient=VERTICAL)
        p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        # Panel canvas + controllers
        panel1 = Label(p, text='Canvas + Controllers', anchor=CENTER)
        p.add(panel1)

        self.canvasBoardFrame = Canvas(panel1, width=400, height=400, background='black')
        self.canvasBoardFrame.pack(side=TOP, padx=5, pady=5)

        bottomFrame = Frame(panel1, relief=FLAT, borderwidth=1)
        bottomFrame.pack(side=BOTTOM, padx=5, pady=5)

        Button(bottomFrame, text="<<",command=self.PreviousBoard).pack(side=LEFT, padx=5, pady=5)
        Label(bottomFrame, textvariable=self.cursorPosition).pack(side=LEFT, padx=5, pady=5)
        if self.useIsland:
            self.boardCount.set(self.islands.islandNumber*self.islands.populationNb)
        else:
            self.boardCount.set(len(self.algorithm.boards) - 1)
        Label(bottomFrame, text='/').pack(side=LEFT, padx=5, pady=5)
        Label(bottomFrame, textvariable=self.boardCount).pack(side=LEFT, padx=5, pady=5)
        Button(bottomFrame, text=">>", command=self.NextBoard).pack(side=LEFT, padx=5, pady=5)

        # Stats
        panel2 = Label(p, text='Statistiques', anchor=CENTER)
        p.add(panel2)

        statsFrame = LabelFrame(panel2, text=" Statistiques ")
        statsFrame.pack(fill=X, padx=15, pady=15)

        # Panel stats
        pstats = PanedWindow(statsFrame, orient=VERTICAL)
        pstats.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        pstats1 = Label(pstats, text='Board n°', anchor=W)
        Label(pstats1, textvariable=self.cursorPosition).pack()
        pstats.add(pstats1)

        pstats2 = Separator(pstats)
        pstats.add(pstats2)

        pstats3 = Label(pstats, text='Note: ', anchor=W)
        Label(pstats3, textvariable=self.currentBoardNote).pack()
        pstats.add(pstats3)

        pstats4 = Label(pstats, text='Life: ', anchor=W)
        Label(pstats4, textvariable=self.currentBoardLife).pack()
        pstats.add(pstats4)

        pstats5 = Label(pstats, text='', anchor=W)
        pstats.add(pstats5)

    def about(self):
        showinfo("About", "Puzzle Of Doom - 2016, Epitech Project by:\n\nNathan Pichonwalchshofer\tpichon_b\nThibaut Coutard\t\tcoutar_t\nAurelien Dorey\t\tdorey_a\nArthur Leclerc\t\tlecler_h")

    #def save(self):
    #    filename = tkFileDialog.asksaveasfilename(defaultextension=".pkl")

    #    if filename:
    #        with open(filename, 'wb') as output:
    #            if self.useIsland:
    #                pickle.dump(self.islands.generationHistory, output, pickle.HIGHEST_PROTOCOL)
    #            else:
    #                pickle.dump(self.historyGen, output, pickle.HIGHEST_PROTOCOL)

    def load(self):
        # Check if algo is on process
        filepath = tkFileDialog.askopenfilename(title="Open history", filetypes=[('pkl files','.pkl')])

        save = pickle.load(open(filepath, "rb"))

        #if self.useIsland:
        #    self.islands = IslandsAlgorithm(len(save[len(save)-1].algorithms), save[len(save)-1].populationNb, save[len(save)-1].turnover)
        #    self.genCount.set(save[len(save)-1].genCount)
        #    self.boardCount.set(self.islands.islandNumber*self.islands.populationNb)
        #    self.attachBoardToCanvas(self.islands.best.board, self.canvasBestFrame)
        #    self.cursorPosition.set(0)
        #    self.attachBoardToCanvas(self.islands.islands[self.cursorPosition.get()].boards[self.cursorPosition.get()].board, self.canvasBoardFrame)
        #else:
        self.algorithm = save.data
        self.genCount.set(save.genCount)
        self.boardCount.set(len(self.algorithm.boards) - 1)
        self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
        self.cursorPosition.set(0)
        self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Next board button
    def NextBoard(self):
        if self.useIsland:
            if self.cursorPosition.get() < (self.islands.islandNumber*self.islands.populationNb):
                self.cursorPosition.set(self.cursorPosition.get() + 1)
                islandIdx = int((self.cursorPosition.get())/self.islands.populationNb)
                boardIdx = int(str(self.cursorPosition.get())[-1])-1%self.islands.populationNb
                print "{} --- {}".format(islandIdx, boardIdx)
                self.attachBoardToCanvas(self.islands.islands[islandIdx].boards[boardIdx].board, self.canvasBoardFrame)
        else:
            if (self.cursorPosition.get() < len(self.algorithm.boards) - 1):
                self.cursorPosition.set(self.cursorPosition.get() + 1)
                self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Previous board button
    def PreviousBoard(self):
        if self.useIsland:
            if (self.cursorPosition.get() > 0):
                self.cursorPosition.set(self.cursorPosition.get() - 1)
                self.attachBoardToCanvas(self.islands.islands[int(self.cursorPosition.get()/10)].boards[int(str(self.cursorPosition.get())[-1])%4].board, self.canvasBoardFrame)
        else:
            if (self.cursorPosition.get() > 0):
                self.cursorPosition.set(self.cursorPosition.get() - 1)
                self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Generate new gen button
    def doNextGen(self):
        if self.inProcess.get() == 0:
            if (self.nbrGen.get() >= 1):
                self.inProcess.set(self.nbrGen.get())
                while self.inProcess.get() > 0:
                    if self.useIsland:
                        self.islands.doOneGen()
                        self.genCount.set(self.islands.generationNumber)

                        # Island log
                        #
                        #

                        # Save gen data
                        #
                        #
                        #

                        # Attach board to UI canvas
                        self.boardCount.set(self.islands.islandNumber*self.islands.populationNb)
                        self.attachBoardToCanvas(self.islands.best.board, self.canvasBestFrame)
                        self.cursorPosition.set(0)
                        self.attachBoardToCanvas(self.islands.islands[self.cursorPosition.get()].boards[self.cursorPosition.get()].board, self.canvasBoardFrame)
                    else:
                        self.algorithm.doOneGen()
                        self.genCount.set(self.algorithm.genCount)

                        # Simple log
                        self.logger.writeBestBoardCSV([self.genCount.get()] + self.algorithm.best.toArray())
                        self.logger.writeGenerationCSV({'time': datetime.now().time(), 'generation': self.genCount.get(), 'note': self.algorithm.best.note})

                        # Save gen data
                        dataSaved = GenBackUp(self.genCount.get(), copy.deepcopy(self.algorithm));
                        dataSaved.save(self.mainFolder);
                        #self.historyGen.append(dataSaved);

                        # Attach board to UI canvas
                        self.boardCount.set(len(self.algorithm.boards) - 1)
                        self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
                        self.cursorPosition.set(0)
                        self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)
                    self.windown.update()
                    self.inProcess.set(self.inProcess.get() - 1)

    # Attach board to frame
    def attachBoardToCanvas(self, board, canvas):
        # Update UI val
        if self.useIsland:
            self.currentBoardLife.set(self.islands.islands[self.cursorPosition.get()].boards[self.cursorPosition.get()].life)
            self.currentBoardNote.set(self.islands.islands[self.cursorPosition.get()].boards[self.cursorPosition.get()].note)
            self.currentBestLife.set(self.islands.best.life)
            self.currentBestNote.set(self.islands.best.note)
        else:
            self.currentBoardLife.set(self.algorithm.boards[self.cursorPosition.get()].life)
            self.currentBoardNote.set(self.algorithm.boards[self.cursorPosition.get()].note)
            self.currentBestLife.set(self.algorithm.best.life)
            self.currentBestNote.set(self.algorithm.best.note)

        # Generate image
        im = Image.new("RGB", (400, 400))
        i = 1
        x = 0
        y = 0

        for piece in board:
            im.paste(self.piecesIm[piece.piece].rotate(piece.orientation), (x, y))
            x += 25
            if i % 16 == 0:
                y += 25
                x = 0
            i += 1

        canvas.image = ImageTk.PhotoImage(im)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')

def main():
    puzzleOfDoom = PuzzleOfDoom()

    puzzleOfDoom.loadUI()
    puzzleOfDoom.initUI()

    puzzleOfDoom.windown.mainloop()

if __name__ == '__main__':
    main()
