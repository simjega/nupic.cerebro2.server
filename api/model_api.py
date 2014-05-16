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

from cerebro2.paths import Paths



# TODO: make this a parameter
DATA_DIR = "/tmp/cerebro2/model"

urls = (
  r"/num_iterations", "NumIterations",
  r"/([-\w\/]*)", "Fetch",
)



class Fetch:


  def GET(self, path):
    components = (path + ".json").split("/")
    filepath = os.path.join(DATA_DIR, *components)
    return jsonResponse(readJSON(filepath))



class NumIterations:


  def GET(self):
    paths = Paths(DATA_DIR)
    statesDir = paths.states()
    states = os.listdir(statesDir)
    states = [state for state in states if not state.startswith(".")]
    return jsonResponse(len(states))



def readJSON(filepath, notFoundValue=None):
  try:
    with open(filepath, 'r') as infile:
      return json.load(infile)
  except IOError as error:
    if notFoundValue == None:
      raise error
    return notFoundValue


def jsonResponse(obj):
  callbackFn = web.input(callback=None).callback
  jsonStr = json.dumps(obj)
  web.header('Content-Type', 'application/json')
  return "%s(%s)" % (callbackFn, jsonStr) if callbackFn else jsonStr



app = web.application(urls, globals())
