#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from tkMessageBox import *
from PIL import ImageTk, Image

from algorithm import algorithm

class PuzzleOfDoom:
    def __init__(self):
        self.windown = Tk()
        self.windown.resizable(width=FALSE, height=FALSE)
        self.windown.wm_title('Puzzle Of Doom')
        self.algorithm = algorithm(4)
        self.cursorPosition = IntVar()
        self.cursorPosition.set(0)
        self.boardCount = IntVar()
        self.boardCount.set(0)
        self.nbrGen = IntVar()
        self.nbrGen.set(1)

    def about(self):
        showinfo("About", "Puzzle Of Doom - 2016, Epitech Project by:\n\nNathan Pichonwalchshofer\tpichon_b\nThibaut Coutard\t\tcoutar_t\nAurelien Dorey\t\tdorey_a\nArthur Leclerc\t\tlecler_h")

    def loadMenu(self):
        menubar = Menu(self.windown)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Save")
        menu1.add_command(label="Load")
        menu1.add_separator()
        menu1.add_command(label="Quit", command=self.windown.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=menu3)

        self.windown.config(menu=menubar)

    def loadBestFrame(self):
        # Left side, show best board for the current generation
        bestFrame = LabelFrame(self.windown, text=" Best board of the generation ", padx=20, pady=20)
        bestFrame.pack(side=LEFT, padx=15, pady=15)

        self.canvasBestFrame = Canvas(bestFrame, width=400, height=400, background='black')
        self.canvasBestFrame.pack(side=TOP, padx=5, pady=5)

        bottomFrame = Frame(bestFrame, relief=FLAT, borderwidth=1)
        bottomFrame.pack(side=BOTTOM, padx=5, pady=5)

        self.entree = Entry(bottomFrame, textvariable=self.nbrGen, width=10)
        self.entree.pack(side=LEFT)
        Button(bottomFrame, text="Generate", relief=RAISED, command=self.doNextGen).pack(side=LEFT, padx=5, pady=5)

    def loadBoardFrame(self):
        # Right side, show all boards for the current generation
        boardsFrame = LabelFrame(self.windown, text=" Boards ", padx=20, pady=20)
        boardsFrame.pack(side=RIGHT, padx=15, pady=15)

        self.canvasBoardFrame = Canvas(boardsFrame, width=400, height=400, background='black')
        self.canvasBoardFrame.pack(side=TOP, padx=5, pady=5)

        bottomFrame = Frame(boardsFrame, relief=FLAT, borderwidth=1)
        bottomFrame.pack(side=BOTTOM, padx=5, pady=5)

        Button(bottomFrame, text="<<", relief=RAISED, command=self.PreviousBoard).pack(side=LEFT, padx=5, pady=5)
        Label(bottomFrame, textvariable=self.cursorPosition).pack(side=LEFT, padx=5, pady=5)
        self.boardCount.set(len(self.algorithm.boards) - 1)
        Label(bottomFrame, text='/').pack(side=LEFT, padx=5, pady=5)
        Label(bottomFrame, textvariable=self.boardCount).pack(side=LEFT, padx=5, pady=5)
        Button(bottomFrame, text=">>", relief=RAISED, command=self.NextBoard).pack(side=LEFT, padx=5, pady=5)

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
        self.attachBoardToCanvas(self.algorithm.best.board, self.canvasBestFrame)
        self.cursorPosition.set(0)
        self.attachBoardToCanvas(self.algorithm.boards[self.cursorPosition.get()].board, self.canvasBoardFrame)

    # Attach board to frame
    def attachBoardToCanvas(self, board, canvas):
        # Generate image
        im = Image.new("RGB", (400, 400))
        i = 1
        x = 0
        y = 0

        for piece in board:
            pieceIm = Image.open("project/Eternity/" + str(piece.piece + 1) + '.png')
            pieceIm.thumbnail((25, 25), Image.ANTIALIAS)

            im.paste(pieceIm, (x, y))
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
    puzzleOfDoom.loadMenu()

    puzzleOfDoom.attachBoardToCanvas(puzzleOfDoom.algorithm.best.board, puzzleOfDoom.canvasBestFrame)
    puzzleOfDoom.attachBoardToCanvas(puzzleOfDoom.algorithm.boards[puzzleOfDoom.cursorPosition.get()].board, puzzleOfDoom.canvasBoardFrame)

    puzzleOfDoom.windown.mainloop()

if __name__ == '__main__':
    main()