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
import web

from cerebro2.fetcher import Fetcher



# TODO: make this a parameter
DATA_DIR = "/tmp/cerebro2/model"

fetcher = Fetcher(DATA_DIR)

urls = (
  r"/num_iterations", "NumIterations",
  r"/([-\w]*)/dimensions", "Dimensions",
  r"/([-\w]*)/(\d+)/active_columns", "ActiveColumns",
  r"/([-\w]*)/(\d+)/active_cells", "ActiveCells",
  r"/([-\w]*)/(\d+)/predicted_cells", "PredictedCells",
  r"/([-\w]*)/(\d+)/proximal_synapses", "ProximalSynapses",
)



class NumIterations:


  def GET(self):
    return jsonResponse(fetcher.getNumIterations())



class Dimensions:


  def GET(self, layer):
    return jsonResponse(fetcher.getDimensions(layer))



class ActiveColumns:


  def GET(self, layer, iteration):
    return jsonResponse(fetcher.getActiveColumns(layer, iteration))



class ActiveCells:


  def GET(self, layer, iteration):
    return jsonResponse(fetcher.getActiveCells(layer, iteration))



class PredictedCells:


  def GET(self, layer, iteration):
    return jsonResponse(fetcher.getPredictedCells(layer, iteration))



class ProximalSynapses:


  def GET(self, layer, iteration):
    return jsonResponse(fetcher.getProximalSynapses(layer, iteration))



class DistalSynapses:


  def GET(self, layer, iteration):
    return jsonResponse(fetcher.getDistalSynapses(layer, iteration))



def jsonResponse(obj):
  callbackFn = web.input(callback=None).callback
  jsonStr = json.dumps(obj)
  web.header('Content-Type', 'application/json')
  return "%s(%s)" % (callbackFn, jsonStr) if callbackFn else jsonStr



app = web.application(urls, globals())
