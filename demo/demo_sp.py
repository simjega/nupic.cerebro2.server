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
from random import randrange

from cerebro2.patcher import Patcher
from nupic.research.spatial_pooler import SpatialPooler



def run():
  sp = SpatialPooler(
    inputDimensions=[10, 15],
    columnDimensions=[5, 10],
    potentialRadius=2,
    potentialPct=0.5,
    synPermInactiveDec=0.1,
    synPermActiveInc=0.1,
    synPermConnected=0.1,
    localAreaDensity=0.1,
    numActiveColumnsPerInhArea=-1,
    globalInhibition=True
  )
  inputArray = numpy.zeros(sp.getNumInputs())
  activeArray = numpy.zeros(sp.getNumColumns())

  Patcher().patchSP(sp)

  for i in range(100):
    generateInput(inputArray)
    sp.compute(inputArray, True, activeArray)
    print "Ran iteration:\t{0}".format(i)


def generateInput(inputArray):
  inputArray[0:] = 0
  for i in range(inputArray.size):
    inputArray[i] = randrange(2)



if __name__ == "__main__":
  run()
