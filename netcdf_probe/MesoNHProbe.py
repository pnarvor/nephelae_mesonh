import numpy as np
import time

from .MesoNHVariable import MesoNHVariable
from .ProbeCache     import ProbeCache

class MesoNHProbe:

    """
    MesoNHProbe
    Gives efficient acces to a large collection of MesoNH files
        - Intended to simulate a flight inside MesoNH data
    """


    def __init__(self, atm, variables, cacheSize, initPosition=[0,0,0,0]):

        """
        - atm         : MFDataset from netCDF4 package ALREADY LOADED with
                        a set of mesonh files
        - variables   : Variables names to read in the MesoNH files
                        too many will cause load stall
        - maxVelocity : Max espected flight velocity (in m/s), Used to compute
                        cache parameters (caution, too high cause large cache
                        loadings and may severe simulation speed)
        - frequency   : Extimated sampling frequency (in Hz) of data queries.
                        used to compute cache parameters (too low may
                        cause large cache buffers, too high may cause
                        too often occurring cache update)
        """

        self.atm = atm
        
        self.variables = []
        self.probes = []
        for var in variables:
            if not var in self.atm.variables.keys():
                print("Warning : variable ", var, " is not in dataset. Discarding.")
                continue
            self.variables.append(var)
            self.probes.append(ProbeCache(MesoNHVariable(atm, var),
                                          targetCacheShape=cacheSize,
                                          initPosition=initPosition))

    def __getitem__(self, keys):
        
        print("Request : ", keys)
        res = []
        for probe in self.probes:
            res.append(probe[keys])
        return res


        





