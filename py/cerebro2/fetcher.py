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
import json
import os

from cerebro2.paths import Paths



class Fetcher:


  def __init__(self, dataDir):
    self.paths = Paths(dataDir)


  def getNumIterations(self):
    statesDir = self.paths.states()
    states = os.listdir(statesDir)
    states = [state for state in states if not state.startswith(".")]
    return len(states)


  def getDimensions(self, layer):
    return readJSON(self.paths.dimensions(layer))


  def getActiveColumns(self, layer, iteration):
    return readJSON(self.paths.activeColumns(layer, iteration),
                    notFoundValue=[])


  def getActiveCells(self, layer, iteration):
    return readJSON(self.paths.activeCells(layer, iteration),
                    notFoundValue=[])


  def getPredictedCells(self, layer, iteration):
    return readJSON(self.paths.predictedCells(layer, iteration),
                    notFoundValue=[])


  def getProximalSynapses(self, layer, iteration):
    return readJSON(self.paths.proximalSynapses(layer, iteration),
                    notFoundValue=[])

  def getDistalSynapses(self, layer, iterations):
    return readJSON(self.paths.DistalSynapses(layers, iteration), 
                    notFoundValue=[])



def readJSON(filepath, notFoundValue=None):
  try:
    with open(filepath, 'r') as infile:
      return json.load(infile)
  except IOError as error:
    if notFoundValue == None:
      raise error
    return notFoundValue
