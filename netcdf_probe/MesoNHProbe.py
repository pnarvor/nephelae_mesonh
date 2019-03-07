import numpy as np
import time

from .MesoNHVariable        import MesoNHVariable
from .MultiCache            import MultiCache
from .MesoNHDimensionHelper import MesoNHDimensionHelper

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
                 targetCacheSpan=Fancy()[10.0,-0.5:0.5,-0.5:0.5,-0.5:0.5]):
    
        self.__atm = atm
        self.variables  = []
        tmpVarList = []
        for var in variables:
            if var in self.__atm.variables.keys():
                self.variables.append(var)
                tmpVarList.append(MesoNHVariable(self.__atm, var))
        self.__cache = MultiCache(tmpVarList)
        self.__dimHelper = MesoNHDimensionHelper(atm)
        self.__targetCacheSpan = targetCacheSpan

        self.__updateThreshold = 0.5
        self.__lastLoadPosition = np.empty([])

    def check_position(self, position):

        if not self.__lastLoadPosition:
            return True

        cachePos = position - self.__lastLoadPosition
        for pos, span in zip(cachePos, self.__targetCacheSpan):
            if isinstance(span, slice):
                if pos < 0:
                    if pos / span.start > self.__updateThreshold:
                        return True
                else:
                    if pos / span.stop > self.__updateThreshold:
                        return True
            else:
                if pos / span > self.__updateThreshold:
                    return True
        return False

    def update_cache(self, position):
        
        if not self.check_position(position):
            return

        newCacheKeys = ()
        for pos, span in zip(position, self.__targetCacheSpan):
            if isinstance(span, slice):
                newCacheKeys = newCacheKeys + (slice(pos + span.start,
                                                     pos + span.stop, None),)
            else:
                newCacheKeys = newCacheKeys + (slice(pos, pos + span, None),)
        newCacheKeys = self.__dimHelper.to_indexes(newCacheKeys)

        # TODO check boundaries !!!!!

    def __getitem__(self, keys):
        
        indexes = self.__dimhelper.to_indexes(keys).astype(nt)
        # TODO check cache boundaries
        return self.__cache[indexes]

    def getCache(self):
        return self.__cache

