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
import os
import shutil

DIRNAME_DIMENSIONS         = "dimensions"
DIRNAME_MODEL_STATES       = "states"
FILENAME_ACTIVE_COLUMNS    = "active_columns.json"
FILENAME_ACTIVE_CELLS      = "active_cells.json"
FILENAME_PREDICTED_CELLS   = "predicted_cells.json"
FILENAME_PROXIMAL_SYNAPSES = "proximal_synapses.json"
FILENAME_DISTAL_SYNAPSES   = "distal_synapses.json"


class Paths:


  def __init__(self, dataDir, deleteExisting=False):
    self.dataDir = dataDir

    if deleteExisting and os.path.exists(dataDir):
      shutil.rmtree(dataDir)

    if not os.path.exists(dataDir):
      os.makedirs(dataDir)


  def states(self):
    directory = os.path.join(self.dataDir, DIRNAME_MODEL_STATES)
    return getDirectory(directory)


  def dimensions(self, layer):
    directory = os.path.join(self.dataDir, DIRNAME_DIMENSIONS)

    return getPath(directory, layer+".json")


  def activeColumns(self, layer, iteration):
    directory = os.path.join(self.dataDir,
                              DIRNAME_MODEL_STATES,
                              str(iteration),
                              layer)

    return getPath(directory, FILENAME_ACTIVE_COLUMNS)


  def activeCells(self, layer, iteration):
    directory = os.path.join(self.dataDir,
                              DIRNAME_MODEL_STATES,
                              str(iteration),
                              layer)

    return getPath(directory, FILENAME_ACTIVE_CELLS)


  def predictedCells(self, layer, iteration):
    directory = os.path.join(self.dataDir,
                              DIRNAME_MODEL_STATES,
                              str(iteration),
                              layer)

    return getPath(directory, FILENAME_PREDICTED_CELLS)


  def proximalSynapses(self, layer, iteration):
    directory = os.path.join(self.dataDir,
                              DIRNAME_MODEL_STATES,
                              str(iteration),
                              layer)

    return getPath(directory, FILENAME_PROXIMAL_SYNAPSES)

  def distalSynapses(self, layer, iteration):
    directory = os.path.join(self.dataDir, 
                              DIRNAME_MODEL_STATES,
                              str(iteration),
                              layer)

    return getPath(directory, FILENAME_DISTAL_SYNAPSES)


def getDirectory(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

  return directory


def getPath(directory, filename):
  return os.path.join(getDirectory(directory), filename)
