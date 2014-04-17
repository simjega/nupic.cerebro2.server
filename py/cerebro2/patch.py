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



DIRNAME_DIMENSIONS      = "dimensions"
DIRNAME_MODEL_STATES    = "states"
FILENAME_ACTIVE_COLUMNS = "active_columns.json"
FILENAME_ACTIVE_CELLS   = "active_cells.json"



class Patch:


  def __init__(self, model, params, dataDir="/tmp/cerebro2/model"):
    self.dataDir = dataDir
    self.params = params

    if not os.path.exists(dataDir):
      os.makedirs(dataDir)

    self._saveDimensions()

    self.inRegion = model._getSensorRegion()
    self.spRegion = model._getSPRegion()
    # self.tpRegion = model._getTPRegion()

    run = model.run
    self.iteration = 0

    def patchedRun(inputRecord):
      results = run(inputRecord)

      self._saveInputState()
      self._saveSPState()

      self.iteration += 1
      return results

    model.run = patchedRun


  def _saveDimensions(self):
    dimensions = [
      ("input",  self._getInputDimensions()),
      ("output", self._getOutputDimensions())
    ]

    for dimension in dimensions:
      dimensionDir = os.path.join(self.dataDir, DIRNAME_DIMENSIONS)
      if not os.path.exists(dimensionDir):
        os.makedirs(dimensionDir)

      filepath = os.path.join(dimensionDir, dimension[0]+".json")
      writeJSON(dimension[1], filepath)


  def _saveInputState(self):
    sdr = self.inRegion.getOutputData('dataOut').nonzero()[0].tolist()
    filepath = os.path.join(self._getStateDir("input"), FILENAME_ACTIVE_CELLS)
    writeJSON(sdr, filepath)


  def _saveSPState(self):
    activeCells = self.spRegion.getOutputData('bottomUpOut').nonzero()[0].tolist()
    filepath = os.path.join(self._getStateDir("output"), FILENAME_ACTIVE_CELLS)
    writeJSON(activeCells, filepath)


  def _getStateDir(self, layerType):
    currentDir = os.path.join(self.dataDir,
                              DIRNAME_MODEL_STATES,
                              str(self.iteration),
                              layerType)

    if not os.path.exists(currentDir):
      os.makedirs(currentDir)

    return currentDir


  def _getInputDimensions(self):
    n = 0
    encoders = self.params["sensorParams"]["encoders"]

    for key in encoders:
      if key == "_classifierInput":
        continue
      encoder = encoders[key]
      if encoder["type"] == "SDRCategoryEncoder":
        n += encoder["n"]

    return [n]


  def _getOutputDimensions(self):
    tpParams = self.params["tpParams"]
    return [tpParams["columnCount"], tpParams["cellsPerColumn"]]



def writeJSON(obj, filepath):
  with open(filepath, 'w') as outfile:
    json.dump(obj, outfile)
