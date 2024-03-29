#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *
from PIL import ImageTk, Image

import tkFileDialog
import copy
import pickle

from algorithm import algorithm

class GenBackUp:
    def __init__(self, genCount, algorithm):
        self.genCount = genCount
        self.algorithm = algorithm

class PuzzleOfDoom:
    def __init__(self):
        self.windown = Tk()
        self.windown.resizable(width=FALSE, height=FALSE)
        self.windown.wm_title('Puzzle Of Doom')
        self.algorithm = algorithm(4)

        self.inProcess = IntVar()
        self.inProcess.set(0)

        self.historyGen = []

        self.piecesIm = []

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

        for i in range(1, 256):
            self.piecesIm.append(Image.open("project/Eternity_resized/" + str(i) + '.png'))
            self.piecesIm[i - 1].thumbnail((25, 25), Image.ANTIALIAS)

        # Capture gen state
        self.historyGen.append(GenBackUp(self.genCount.get(), copy.deepcopy(self.algorithm)))

        self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
        self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    def loadUI(self):
        self.note = Notebook(self.windown)

        self.loadTabGeneration()
        self.loadTabHistory()
        self.note.pack()

    #\
    #   TOP MENU
    #/
    def loadMenu(self):
        menubar = Menu(self.windown)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Save", command=self.save)
        menu1.add_command(label="Load", command=self.load)
        menu1.add_separator()
        menu1.add_command(label="Quit", command=self.windown.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=menu3)

        self.windown.config(menu=menubar)

    def about(self):
        showinfo("About", "Puzzle Of Doom - 2016, Epitech Project by:\n\nNathan Pichonwalchshofer\tpichon_b\nThibaut Coutard\t\tcoutar_t\nAurelien Dorey\t\tdorey_a\nArthur Leclerc\t\tlecler_h")

    def save(self):
        filename = tkFileDialog.asksaveasfilename(defaultextension=".pkl")

        if filename:
            with open(filename, 'wb') as output:
                pickle.dump(self.historyGen, output, pickle.HIGHEST_PROTOCOL)

    def load(self):
        # Check if algo is on process
        filepath = tkFileDialog.askopenfilename(title="Open history", filetypes=[('pkl files','.pkl')])

        if filepath:
            save = pickle.load(open(filepath, "rb"))

            self.historyGen = save

            self.algorithm = self.historyGen[len(save) - 1].algorithm
            self.genCount.set(self.historyGen[len(save) - 1].genCount)

            self.boardCount.set(len(self.algorithm.boards) - 1)
            self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
            self.cursorPosition.set(0)
            self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

        # Update history tab
        self.updateHistoryList()

    #\
    #   HISTORY TAB
    #/
    def loadTabHistory(self):
        tabHistory = Frame(self.note)

        historyFrame = Label(tabHistory)
        historyFrame.pack(side=LEFT, padx=15, pady=15)
        self.loadHistoryList(historyFrame)

        previewFrame = LabelFrame(tabHistory, text=" Preview ")
        previewFrame.pack(side=RIGHT, padx=15, pady=15)
        self.loadPreview(previewFrame)

        self.note.add(tabHistory, text="History")

    def selectionHistory(self, event):
        w = event.widget
        index = int(w.curselection()[0])

        if index in range(0, len(self.historyGen)):
            self.attachBoardToCanvas(self.historyGen[index].algorithm.best.board, self.canvasPreviewFrame)

    def loadHistoryList(self, historyFrame):
        self.historybox = Listbox(historyFrame, width=75, height=25)
        self.historybox.pack()

        self.historybox.bind('<<ListboxSelect>>', self.selectionHistory)

        self.updateHistoryList()

    def loadPreview(self, previewFrame):
        self.canvasPreviewFrame = Canvas(previewFrame, width=400, height=400, background='black')
        self.canvasPreviewFrame.pack(side=TOP, padx=5, pady=5)

    def updateHistoryList(self):
        for gen in self.historyGen:
            self.historybox.insert(END, gen)

    #\
    #   MAIN TAB
    #/
    def loadTabGeneration(self):
        self.tabGeneration = Frame(self.note)

        self.loadBestFrame()
        self.loadBoardFrame()

        self.loadMenu()
        self.note.add(self.tabGeneration, text="Generation")

    #\
    #   MAIN TAB - LEFT SIDE
    #/
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

    # Generate new gen button
    def doNextGen(self):
        if self.inProcess.get() == 0:
            if (self.nbrGen.get() >= 1):
                self.inProcess.set(self.nbrGen.get())
                while self.inProcess.get() > 0:
                    self.algorithm.doOneGen()
                    self.genCount.set(self.algorithm.genCount)

                    # Capture gen state
                    self.historyGen.append(GenBackUp(self.genCount.get(), copy.deepcopy(self.algorithm)))

                    self.boardCount.set(len(self.algorithm.boards) - 1)
                    self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
                    self.cursorPosition.set(0)
                    self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)
                    self.windown.update()
                    self.inProcess.set(self.inProcess.get() - 1)
            else:
                self.inProcess.set(1)
                self.algorithm.doOneGen()
                self.genCount.set(self.algorithm.genCount)

                # Capture gen state
                self.historyGen.append(GenBackUp(self.genCount.get(), copy.deepcopy(self.algorithm)))

                self.boardCount.set(len(self.algorithm.boards) - 1)
                self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
                self.cursorPosition.set(0)
                self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)
                self.inProcess.set(0)

    #\
    #   MAIN TAB - RIGHT SIDE
    #/
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

    # Next board button
    def NextBoard(self):
        if (self.cursorPosition.get() < len(self.algorithm.boards) - 1):
            self.cursorPosition.set(self.cursorPosition.get() + 1)
            self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Previous board button
    def PreviousBoard(self):
        if (self.cursorPosition.get() > 0):
            self.cursorPosition.set(self.cursorPosition.get() - 1)
            self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    #\
    #   UTILS
    #/

    # Attach board to frame
    def attachBoardToCanvas(self, board, canvas):
        # Update UI val
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
            im.paste(self.piecesIm[piece.piece - 1].rotate(piece.orientation), (x, y))
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
