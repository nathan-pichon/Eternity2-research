#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import collections

class Piece(object):
	ALLOW_ANGLES = [0, 90, 180, 270]

	FACES_ORIENTATION_POS = {
		'top': 0,
		'left': 3,
		'right': 1,
		'bottom': 2
	}

	def __init__(self, faces, piece_id, orientations, **options):
		self.id = piece_id
		self.rotation_angle = 0
		self.actual_faces = self._set_faces(faces, orientations)
		self.default_faces = self.actual_faces

		self._is_corner = self._check_if_corner()
		self._is_border = self._check_if_border()
		self._picture_path = options.pop("picture_path", None)

	def _set_faces(self, faces, orientations):
		final_faces = numpy.zeros(len(orientations))
		for i in range(len(orientations)):
			numpy.put(final_faces, self.FACES_ORIENTATION_POS[orientations[i]], faces[i])
		return final_faces

	def is_border(self):
		return self._is_border

	def is_corner(self):
		return self._is_corner

	def _check_if_border(self):
		counter = collections.Counter(self.default_faces)
		if counter[0] > 0:
			return True
		return False

	def _check_if_corner(self):
		counter = collections.Counter(self.default_faces)
		if counter[0] == 2:
			return True
		return False

	def picture_path(self):
		return self.picture_path

	def rotate(self, angle):
		if not angle in self.ALLOW_ANGLES:
			print "Error : angle argument invalid."
			return
		self.rotation_angle = angle
		if angle == 0:
			self.actual_faces = self.default_faces
		elif angle == 90:
			self.actual_faces = numpy.roll(self.default_faces, 1)
		elif angle == 180:
			self.actual_faces = numpy.roll(self.default_faces, 2)
		elif angle == 270:
			self.actual_faces = numpy.roll(self.default_faces, 3)