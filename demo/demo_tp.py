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
# This is the class corresponding to the C++ optimized Temporal Pooler
from nupic.research.TP10X2 import TP10X2 as TP



def run():
  tp = TP(numberOfCols=121, cellsPerColumn=4,
              initialPerm=0.5, connectedPerm=0.5,
              minThreshold=11, newSynapseCount=11,
              permanenceInc=0.1, permanenceDec=0.05,
              activationThreshold=2,
              globalDecay=0, burnIn=1,
              checkSynapseConsistency=False,
              pamLength=3)
  Patcher().patchTP(tp)

  inputArray = numpy.zeros(tp.numberOfCols, dtype='int32')

  for i in range(100):
    generateInput(inputArray)
    tp.compute(inputArray, enableLearn = True, computeInfOutput = True)
    print "Ran iteration:\t{0}".format(i)


def generateInput(inputArray):
  inputArray[0:] = 0
  for i in range(inputArray.size):
    inputArray[i] = randrange(2)



if __name__ == "__main__":
  run()
