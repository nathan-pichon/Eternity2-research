#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import ImageTk, Image

from algorithm import algorithm

class PuzzleOfDoom:
    def __init__(self):
        self.windown = Tk()
        self.algorithm = algorithm(4)
        self.cursorPosition = IntVar()
        self.cursorPosition.set(0)
        self.boardCount = IntVar()
        self.boardCount.set(0)
        self.nbrGen = IntVar()
        self.nbrGen.set(1)

    def loadBestFrame(self):
        # Left side, show best board for the current generation
        bestFrame = Frame(self.windown, relief=GROOVE)
        bestFrame.pack(side=LEFT, padx=15, pady=15)

        self.canvasBestFrame = Canvas(bestFrame, width=400, height=400, background='black')
        self.canvasBestFrame.pack(side=TOP, padx=5, pady=5)

        self.entree = Entry(bestFrame, textvariable=self.nbrGen, width=30)
        self.entree.pack()

        Button(bestFrame, text="Generate", command=self.doNextGen).pack(side=LEFT, padx=5, pady=5)

    def loadBoardFrame(self):
        # Right side, show all boards for the current generation
        boardsFrame = Frame(self.windown, relief=GROOVE)
        boardsFrame.pack(side=RIGHT, padx=15, pady=15)

        self.canvasBoardFrame = Canvas(boardsFrame, width=400, height=400, background='black')
        self.canvasBoardFrame.pack(side=TOP, padx=5, pady=5)

        Button(boardsFrame, text="<<", command=self.PreviousBoard).pack(side=LEFT, padx=5, pady=5)
        Label(boardsFrame, textvariable=self.cursorPosition).pack()
        self.boardCount.set(len(self.algorithm.boards) - 1)
        Label(boardsFrame, textvariable=self.boardCount).pack()
        Button(boardsFrame, text=">>", command=self.NextBoard).pack(side=RIGHT, padx=5, pady=5)

    # Next board button
    def NextBoard(self):
        if (self.cursorPosition.get() < len(self.algorithm.boards) - 1):
            self.cursorPosition.set(self.cursorPosition.get() + 1)
            self.attachBoardToFrame(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Previous board button
    def PreviousBoard(self):
        if (self.cursorPosition.get() > 0):
            self.cursorPosition.set(self.cursorPosition.get() - 1)
            self.attachBoardToFrame(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Generate new gen button
    def doNextGen(self):
        if (self.nbrGen.get() >= 1):
            i = self.nbrGen.get()
            while i > 0:
                self.algorithm.doOneGen()
                print i
                i -= 1
        else:
            self.algorithm.doOneGen()
        self.boardCount.set(len(self.algorithm.boards) - 1)
        self.attachBoardToFrame(self.algorithm.best.board, self.canvasBestFrame)
        self.cursorPosition.set(0)
        self.attachBoardToFrame(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Attach board to frame
    def attachBoardToFrame(self, board, canvas):
        # Generate image
        im = Image.new("RGB", (400, 400))
        i = 1
        x = 0
        y = 0

        for piece in board:
            piece = Image.open("project/Eternity/" + str(piece.piece + 1) + '.png')
            piece.thumbnail((25, 25), Image.ANTIALIAS)

            im.paste(piece, (x, y))
            x += 25
            if i % 16 == 0:
                y += 25
                x = 0
            i += 1

        canvas.image = ImageTk.PhotoImage(im)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')

def main():
    puzzleOfDoom = PuzzleOfDoom()

    puzzleOfDoom.loadBestFrame()
    puzzleOfDoom.loadBoardFrame()

    puzzleOfDoom.attachBoardToFrame(puzzleOfDoom.algorithm.best.board, puzzleOfDoom.canvasBestFrame)
    puzzleOfDoom.attachBoardToFrame(puzzleOfDoom.algorithm.boards[puzzleOfDoom.cursorPosition.get()].board, puzzleOfDoom.canvasBoardFrame)

    puzzleOfDoom.windown.mainloop()

main()