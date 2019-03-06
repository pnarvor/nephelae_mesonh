import numpy as np
import time

from .MesoNHVariable import MesoNHVariable
from .MultiCache     import MultiCache

from .Fancy import Fancy

class MesoNHProbe:

    """
    MesoNHProbe : stream sample by sample data from a large collection of
                  MesoNH files. Also handles interpolation and cache updates.
                  MesoNH files are assumed to be periodic in the x,y axes.
                  Assumes the virtual probe will not go back in time.

    - public member functions :
        __init__(self, atm, variables, targetCacheShape=[0:10,-0.5:0.5, ...]) :
            atm = netcdf4.MFDataset ALREADY LOADED with MesoNH files.
            variables : list of variables to read from the MesoNH dataset
            targetCacheSpan : defines span of data to be read around the 
                              virtual probe at a given probe position
                              (expressed in the native MesoNH axes units)
    - public attributes :
        variables : list of variables read in the MesoNHFiles

    - private attributes :
        __atm             : netcdf4.MFDataSet MesoNHData
        __cache           : Cached data from which every read is done
        __targetCacheSpan : Target span of data to be read around the vitual
                            probe. Effective read span depends on the atm shape
                        
    """

    def __init__(self, atm, variables,
                 targetCacheShape=Fancy()[0:10.0,-0.5:0.5,-0.5:0.5,-0.5:0.5]):
    
        self.__atm = at m
        self.variables  = []
        tmpVarList = []
        for var in variables:
            if var in self.__atm.variables.keys():
                self.variables.append(var)
                tmpVarList.append(MesoNHVariable(self.__atm, var))
        self.__cache = MultiCache(tmpVarList)

    def getCache(self):
        return self.__cache

