#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

from piece import Piece

class CSV(object):
	def __init__(self, filename='e2pieces.txt', directory='./project/', delimiter=';', have_header=True, **kwargs):
		self.filename = filename
		self.delimiter = delimiter
		self.directory = directory
		self.have_header = have_header

		self._header = self._read_header()
		self._datas = self._read_dataset()

	def header(self):
		return self._header

	def _read_header(self):
		with open(self.directory+self.filename, mode='r') as csv:
			return list(csv)[0].rstrip('\n'	).lower().split(';')

	def get_path(self):
		return self.directory + self.filename

	def _read_dataset(self):
		if self.have_header:
			return numpy.genfromtxt(self.get_path(), delimiter=self.delimiter, skip_header=True)
		return numpy.genfromtxt(self.get_path(), delimiter=self.delimiter)

	def get(self, row_ids=[]):
		if len(row_ids) == 0:
			return self._datas
		else:
			return self._datas[list(row_ids)]

class Board(object):
	def __init__(self, size_x=16, size_y=16, **kwargs):
		self.shape((size_x, size_y))
		self.board = numpy.zeros(self.shape, dtype='int')

	def shape(self, shape):
		if not isinstance(shape, tuple):
			print "Error : shape argument must be a tuple instance."
			return
		self.shape = shape

	def put(self, piece_id, coordinates):
		if not isinstance(piece_id, int):
			print "Error : piece_id argument must be an int."
			return
		if not isinstance(coordinates, tuple):
			print "Error ; coordinates argument ust be a tuple."
			return
		self.board[coordinates] = piece_id

	def print_board(self):
		for row in self.board:
			print " | ".join(row.astype(str))

	def get_piece(self, piece_coordinates):
		if not isinstance(piece_coordinates, (tuple, list, numpy.ndarray)):
			return
		return self.board[piece_coordinates[0], piece_coordinates[1]]

	def get_area(self, x_lim, y_lim):
		if not isinstance(x_lim, (tuple, list, numpy.ndarray)) or not isinstance(y_lim, (list, tuple, numpy.ndarray)):
			return
		return self.board[x_lim[0]:x_lim[1], y_lim[0]:y_lim[1]]

	def print_piece(self, piece_coordinates):
		if not isinstance(piece_coordinates, (tuple, list, numpy.ndarray)):
			return
		print self.board[piece_coordinates[0], piece_coordinates[1]]

	def print_area(self, x_lim, y_lim):
		if not isinstance(x_lim, (tuple, list, numpy.ndarray)) or not isinstance(y_lim, (list, tuple, numpy.ndarray)):
			return
		area = self.board[x_lim[0]:x_lim[1], y_lim[0]:y_lim[1]]
		for row in area:
			print " | ".join(row.astype(str))

def set_pieces(pieces_dataset, header):
	return [Piece(pieces_dataset[i], i+1, header) for i in range(len(pieces_dataset))]

# Entry point
if __name__ == '__main__':
	pieces_csv = CSV()
	pieces = set_pieces(pieces_csv.get(), pieces_csv.header())
	
	board = Board()
	board.put(pieces[0].id, (0,0))
	board.print_board()
	board.print_piece((0,0))
	board.print_area((0,4), (0,4))
