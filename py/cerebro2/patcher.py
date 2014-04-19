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



class Patcher:


  def __init__(self, dataDir="/tmp/cerebro2/model"):
    self.paths = Paths(dataDir)


  def patchCLAModel(self, model):
    encoder = model._getSensorRegion().getSelf().encoder
    self.patchEncoder(encoder, "input")

    sp = model._getSPRegion().getSelf()._sfdr
    self.patchSP(sp, "output")

    tp = model._getTPRegion().getSelf()._tfdr
    self.patchTP(tp, "output")


  def patchEncoder(self, encoder, layer):
    EncoderPatch(self, layer).patch(encoder)


  def patchSP(self, sp, layer):
    SPPatch(self, layer).patch(sp)


  def patchTP(self, tp, layer):
    TPPatch(self, layer).patch(tp)


  def saveDimensions(self, dimensions, layer):
    writeJSON(dimensions, self.paths.dimensions(layer))


  def saveActiveColumns(self, activeColumns, layer, iteration):
    writeJSON(activeColumns, self.paths.activeColumns(layer, iteration))


  def saveActiveCells(self, activeCells, layer, iteration):
    writeJSON(activeCells, self.paths.activeCells(layer, iteration))



class Patch:


  def __init__(self, patcher, layer):
    self.patcher = patcher
    self.layer = layer
    self.iteration = 0



class EncoderPatch(Patch):


  def patch(self, encoder):
    self.encoder = encoder
    self.saveDimensions()

    encodeIntoArray = encoder.encodeIntoArray

    def patchedEncodeIntoArray(inputData, output):
      results = encodeIntoArray(inputData, output)
      self.saveState(output)
      self.iteration += 1
      return results

    encoder.encodeIntoArray = patchedEncodeIntoArray


  def saveDimensions(self):
    dimensions = [self.encoder.getWidth(), 1, 1]
    self.patcher.saveDimensions(dimensions, self.layer)


  def saveState(self, output):
    activeCells = output.nonzero()[0].tolist()
    self.patcher.saveActiveCells(activeCells, self.layer, self.iteration)



class SPPatch(Patch):


  def patch(self, sp):
    self.sp = sp
    self.saveDimensions()

    compute = sp.compute

    def patchedCompute(inputVector, learn, activeArray):
      results = compute(inputVector, learn, activeArray)
      self.saveState(activeArray)
      self.iteration += 1
      return results

    sp.compute = patchedCompute


  def saveDimensions(self):
    dimensions = [self.sp.getNumColumns(), 1, 1]
    self.patcher.saveDimensions(dimensions, self.layer)


  def saveState(self, activeArray):
    activeColumns = activeArray.nonzero()[0].tolist()
    self.patcher.saveActiveColumns(activeColumns, self.layer, self.iteration)



class TPPatch(Patch):


  def patch(self, tp):
    self.tp = tp
    self.saveDimensions()

    compute = tp.compute

    def patchedCompute(bottomUpInput, enableLearn, computeInfOutput=None):
      results = compute(bottomUpInput, enableLearn, computeInfOutput=computeInfOutput)
      self.saveState()
      self.iteration += 1
      return results

    tp.compute = patchedCompute


  def saveDimensions(self):
    dimensions = [self.tp.numberOfCols, 1, self.tp.cellsPerColumn]
    self.patcher.saveDimensions(dimensions, self.layer)


  def saveState(self):
    activeCells = self.tp.getActiveState().nonzero()[0].tolist()
    self.patcher.saveActiveCells(activeCells, self.layer, self.iteration)



def writeJSON(obj, filepath):
  with open(filepath, 'w') as outfile:
    json.dump(obj, outfile)
