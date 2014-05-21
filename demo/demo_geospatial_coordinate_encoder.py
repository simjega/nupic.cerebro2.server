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

import csv
import sys

import numpy

from cerebro2.patcher import Patcher
from nupic.encoders.base import defaultDtype
from nupic.encoders.geospatial_coordinate import GeospatialCoordinateEncoder



def run(dataPath):
  encoder = GeospatialCoordinateEncoder(30,
                                        60,
                                        n=999,
                                        w=25,
                                        name='geospatial_coordinate')
  Patcher().patchCoordinateEncoder(encoder, encoder.name)

  with open(dataPath) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      longitude = float(row[2])
      latitude = float(row[3])
      speed = float(row[5])
      encode(encoder, longitude, latitude, speed)



def encode(encoder, longitude, latitude, speed):
  output = numpy.zeros(encoder.getWidth(), dtype=defaultDtype)
  print ("===== " + str(latitude) + " / " + str(longitude) +
         " / " + str(speed) +  " =====")
  encoder.encodeIntoArray((longitude, latitude, speed), output)
  print output.nonzero()[0]
  print
  return output



if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage: {0} /path/to/data.csv".format(sys.argv[0])
    sys.exit(0)

  dataPath = sys.argv[1]
  run(dataPath)
