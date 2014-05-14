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
import numpy
import os

from nupic.bindings.math import GetNTAReal

from cerebro2.paths import Paths



realType = GetNTAReal()



class Patcher:


  def __init__(self, dataDir="/tmp/cerebro2/model"):
    self.paths = Paths(dataDir, deleteExisting=True)


  def patchCLAModel(self, model):
    sp = model._getSPRegion().getSelf()._sfdr
    self.patchSP(sp)

    tp = model._getTPRegion().getSelf()._tfdr
    self.patchTP(tp, sp=sp)


  def patchSP(self, sp):
    SPPatch(self).patch(sp)


  def patchTP(self, tp, sp=None):
    TPPatch(self).patch(tp, sp=sp)


  def saveDimensions(self, dimensions, layer):
    writeJSON(dimensions, self.paths.dimensions(layer))


  def saveActiveColumns(self, activeColumns, layer, iteration):
    writeJSON(activeColumns, self.paths.activeColumns(layer, iteration))


  def saveActiveCells(self, activeCells, layer, iteration):
    writeJSON(activeCells, self.paths.activeCells(layer, iteration))


  def savePredictedCells(self, predictedCells, layer, iteration):
    writeJSON(predictedCells, self.paths.predictedCells(layer, iteration))


  def saveProximalSynapses(self, proximalSynapses, layer, iteration):
    writeJSON(proximalSynapses, self.paths.proximalSynapses(layer, iteration))

  def saveDistalSynapses(self, distalSynapses, layer, iteration):
        writeJSON(distalSynapses, self.paths.distalSynapses(layer, iteration))



class Patch:


  def __init__(self, patcher):
    self.patcher = patcher
    self.iteration = 1



class SPPatch(Patch):


  def patch(self, sp):
    self.sp = sp
    self.saveInputDimensions()
    self.saveColumnDimensions()

    compute = sp.compute

    def patchedCompute(inputVector, learn, activeArray):
      results = compute(inputVector, learn, activeArray)
      self.saveState(inputVector, activeArray)
      self.iteration += 1
      return results

    sp.compute = patchedCompute


  def saveInputDimensions(self):
    dimensions = list(self.sp.getInputDimensions())
    self.patcher.saveDimensions(dimensions, "input")


  def saveColumnDimensions(self):
    dimensions = list(self.sp.getColumnDimensions())
    self.patcher.saveDimensions(dimensions, "output")


  def saveState(self, inputVector, activeArray):
    activeCells = inputVector.nonzero()[0].tolist()
    self.patcher.saveActiveCells(activeCells, "input", self.iteration)

    activeColumns = activeArray.nonzero()[0].tolist()
    self.patcher.saveActiveColumns(activeColumns, "output", self.iteration)

    numColumns = self.sp.getNumColumns()
    numInputs = self.sp.getNumInputs()
    permanence = numpy.zeros(numInputs).astype(realType)
    proximalSynapses = []

    """ Proximal synapses storage format:
        A list of proximal connections, each represented by a list: [toIndex, fromIndex, permanence]
            ...where fromIndex is the index of a cell in the input layer,
                     toIndex is the index of a column in the SP layer,
                     permanence is the permanence value of the proximal connection.
    """
    for column in range(numColumns):
      self.sp.getPermanence(column, permanence)

      for input in permanence.nonzero()[0]:  # TODO: can this be optimized?
        proximalSynapses.append([column, input, permanence[input].tolist()])

    self.patcher.saveProximalSynapses(proximalSynapses, "output", self.iteration)


class TPPatch(Patch):


  def patch(self, tp, sp=None):
    self.tp = tp
    self.sp = sp
    self.saveDimensions()

    compute = tp.compute

    def patchedCompute(bottomUpInput, enableLearn, computeInfOutput=None):
      results = compute(bottomUpInput, enableLearn, computeInfOutput=computeInfOutput)
      self.saveState()
      self.iteration += 1
      return results

    tp.compute = patchedCompute


  def saveDimensions(self):
    if self.sp:
      columnDimensions = list(self.sp.getColumnDimensions())
      if len(columnDimensions) < 2:
        columnDimensions.append(1)
      dimensions =  columnDimensions + [self.tp.cellsPerColumn]
    else:
      dimensions = [self.tp.numberOfCols, 1, self.tp.cellsPerColumn]

    self.patcher.saveDimensions(dimensions, "output")


  def saveState(self):
    activeCells = self.tp.getActiveState().nonzero()[0].tolist()
    self.patcher.saveActiveCells(activeCells, "output", self.iteration)

    predictedCells = self.tp.getPredictedState().reshape(-1).nonzero()[0].tolist()
    self.patcher.savePredictedCells(predictedCells, "output", self.iteration)
    allCells = self.tp.cells
    distalSynapses = []

    """ Distal synapses storage format:
        A list of distal connections, each represented by a list: 
        [srcCol, srcCellIdx, destCol, destCellIdx, permanence]
            ...where  srcColis the id of the source column,
                      srcCellIdx is the id of the source cell in the column,
                      destCol is the id of the destination column,
                      destCellIdx is the id of the destination cell in the column,
                      permanence is permancence value of the distal connection
    """

    allCells = self.tp.cells
    for destCol in xrange(len(allCells)):
        for destCellIdx in xrange(len(allCells[destCol])):
            connections = []
            for segi in xrange(self.tp.getNumSegmentsInCell(destCol, destCellIdx)):
                syns = self.tp.getSegmentOnCell(destCol, destCellIdx, segi)[1:]
                for syn in syns:
                  [srcCol, srcCellIdx, permanence] = syn
                  connections.append([srcCol, srcCellIdx, destCol, destCellIdx, permanence])

            distalSynapses += connections

    self.patcher.saveDistalSynapses(distalSynapses, "output", self.iteration)


def writeJSON(obj, filepath):
  with open(filepath, 'w') as outfile:
    json.dump(obj, outfile)
