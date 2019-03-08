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
                 targetCacheSpan=Fancy()[20.0,-0.5:0.5,-0.5:0.5,-0.5:0.5],
                 updateThreshold = 0.5):
    
        self.__atm       = atm
        self.__dimHelper = MesoNHDimensionHelper(atm)
        self.__atmShape  = self.__dimHelper.atmShape
        self.t0          = self.__atm.variables['time'][0]
        self.variables   = []
        tmpVarList       = []
        for var in variables:
            if var in self.__atm.variables.keys():
                self.variables.append(var)
                tmpVarList.append(MesoNHVariable(self.__atm, var))

        self.__cache             = MultiCache(tmpVarList)
        self.__targetCacheSpan   = targetCacheSpan
        self.__updateThreshold   = updateThreshold

    def check_position(self, position):

        lastCachePosition = self.__cache.get_user_data()
        if not lastCachePosition:
            return True

        cachePos = []
        for pos, lpos in zip(position, lastCachePosition):
            cachePos.append(float(pos - lpos))
        print(" - cache position : ", cachePos)
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

    def update_cache(self, position, blocking=False):
       
        if not self.check_position(position):
            return
        
        newCacheKeys = ()
        for pos, span in zip(position, self.__targetCacheSpan):
            if isinstance(span, slice):
                newCacheKeys = newCacheKeys + (slice(pos + span.start,
                                                     pos + span.stop, None),)
            else:
                newCacheKeys = newCacheKeys + (slice(pos, pos + span, None),)

        indexKeys = self.__dimHelper.clip_units(newCacheKeys)
        indexKeys = self.__dimHelper.to_indexes(indexKeys)
        self.__cache.set_user_data(position)
        try:
            self.__cache.load(indexKeys, blocking=blocking)
        except:
            pass
        print(self.__cache.get_user_data())

    def __getitem__(self, position):
        
        # check if update required and update if necessary
        self.update_cache(position, blocking=False)

        indexes = self.__dimHelper.to_indexes(position)
        indexes = self.__dimHelper.clip_keys(indexes)
        return self.__cache[indexes]

    def getCache(self):
        return self.__cache





