#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import collections

## PIECE OF THE Board
## self.piece is the id of the piece
## self.faces is the array of the faces
class Piece(object):
	def __init__(self, faces, piece, orient = 0):
		self.faces = np.append(faces, orient)
		self.rotatedFaces = np.append(faces, orient)
		self.piece = piece
		self.orientation = orient
