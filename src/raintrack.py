#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
# Raintrack 
# --------------------------------------------------------------------------- #
class Raintrack:

    # ----------------------------------------------------------------------- #
    # Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, query):
      raise NotImplementedError('Implement a concrete Raintrack subclass.')
    
    # ----------------------------------------------------------------------- #
    # createREST
    # ----------------------------------------------------------------------- #
    def createREST(self):
      raise NotImplementedError('Implement a concrete Raintrack subclass.')
    
    # ----------------------------------------------------------------------- #
    # getResults
    # ----------------------------------------------------------------------- #
    def getResults(self):
      raise NotImplementedError('Implement a concrete Raintrack subclass.')
      
    # ----------------------------------------------------------------------- #
    # getPlaces
    # ----------------------------------------------------------------------- #
    def getPlaces(self):
      raise NotImplementedError('Implement a concrete Raintrack subclass.')