#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import numpy

from cerebro2.patcher import Patcher
from nupic.encoders.base import defaultDtype
from nupic.encoders.coordinate import CoordinateEncoder



def run():
  n = 999
  w = 25
  encoder = CoordinateEncoder(name='coordinate',
                              n=n,
                              w=w)
  Patcher().patchCoordinateEncoder(encoder, encoder.name)

  encode(encoder, numpy.array([-149, 24]), 3)
  encode(encoder, numpy.array([-148, 24]), 3)
  encode(encoder, numpy.array([-147, 24]), 3)
  encode(encoder, numpy.array([-146, 24]), 3)
  encode(encoder, numpy.array([-145, 24]), 3)
  encode(encoder, numpy.array([-144, 24]), 3)
  encode(encoder, numpy.array([-142, 24]), 4)
  encode(encoder, numpy.array([-140, 24]), 4)
  encode(encoder, numpy.array([-138, 24]), 4)
  encode(encoder, numpy.array([-136, 24]), 4)
  encode(encoder, numpy.array([-134, 24]), 4)
  encode(encoder, numpy.array([-132, 24]), 4)
  encode(encoder, numpy.array([-130, 22]), 4)
  encode(encoder, numpy.array([-128, 20]), 4)
  encode(encoder, numpy.array([-126, 18]), 5)
  encode(encoder, numpy.array([-122, 16]), 5)
  encode(encoder, numpy.array([-118, 14]), 6)
  encode(encoder, numpy.array([-114, 12]), 7)
  encode(encoder, numpy.array([-110, 10]), 8)
  encode(encoder, numpy.array([-108, 8]),  9)
  encode(encoder, numpy.array([-104, 6]), 10)
  encode(encoder, numpy.array([-100, 6]), 11)
  encode(encoder, numpy.array([-96, 6]),  12)
  encode(encoder, numpy.array([-92, 6]),  13)
  encode(encoder, numpy.array([-86, 6]),  13)
  encode(encoder, numpy.array([-82, 6]),  13)
  encode(encoder, numpy.array([-78, 6]),  13)
  encode(encoder, numpy.array([-74, 6]),  13)
  encode(encoder, numpy.array([-70, 5]),  13)
  encode(encoder, numpy.array([-66, 5]),  13)
  encode(encoder, numpy.array([-62, 3]),  13)
  encode(encoder, numpy.array([-56, 1]),  13)
  encode(encoder, numpy.array([-52, 0]),  13)
  encode(encoder, numpy.array([-48, 0]),  13)
  encode(encoder, numpy.array([-44, 0]),  13)
  encode(encoder, numpy.array([-40, 0]),  13)
  encode(encoder, numpy.array([-36, 0]),  13)
  encode(encoder, numpy.array([-32, 0]),  13)
  encode(encoder, numpy.array([-28, 0]),  10)
  encode(encoder, numpy.array([-26, 0]),  8)
  encode(encoder, numpy.array([-24, 0]),  6)
  encode(encoder, numpy.array([-22, 0]),  4)
  encode(encoder, numpy.array([-20, 0]),  4)
  encode(encoder, numpy.array([-18, 0]),  4)
  encode(encoder, numpy.array([-16, 0]),  4)
  encode(encoder, numpy.array([-14, 0]),  4)



def encode(encoder, coordinate, radius):
  output = numpy.zeros(encoder.getWidth(), dtype=defaultDtype)
  encoder.encodeIntoArray((coordinate, radius), output)
  print "===== " + str(coordinate) + " / " + str(radius) + " ====="
  print output.nonzero()[0]
  print
  return output



if __name__ == "__main__":
  run()
