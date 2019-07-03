import numpy as np
import time
import scipy.interpolate as interp
import math as m

from nephelae_simulation.mesonh_interface import MesoNHVariable

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
                 updateThreshold = 0.2):
    
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
        # print(" - cache position : ", cachePos)
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
            return

    def __getitem__(self, position):
        
        """
        position must be a tuple of single floating point values
        """
        
        # check if update required and update if necessary
        self.update_cache(position, blocking=False)

        indexes = self.__dimHelper.to_indexes(position)

        readIndexes = ()
        for key in indexes:
            readIndexes = readIndexes + (slice(int(m.floor(key)),
                                               int(m.floor(key)) + 2,
                                               None),)
        readUnits = self.__dimHelper.to_units(readIndexes)
        try:
            gridData = self.__cache[readIndexes]
        except Exception as e:
            print("Warning : could not read from cache. "
                  "Your probe is probably moving too fast or "
                  "you didn't initialize probe buffer before read.\n"
                  " - If the former consider lowering the probe speed.\n"
                  " - If the later, call :\n"
                  "     MesoNHProbe.update_cache(posistion, blocking=True)\n"
                  "   After MesoNHProbe object build (position argument must "
                     "be the start position of the probe)\n"
                  "Exception feedback : ", e)
            return []
        
        points = np.empty([16, 4])
        ru = readUnits
        points[ 0,:] = [ru[0].start, ru[1].start, ru[2].start, ru[3].start]
        points[ 1,:] = [ru[0].start, ru[1].start, ru[2].start, ru[3].stop ]
        points[ 2,:] = [ru[0].start, ru[1].start, ru[2].stop , ru[3].start]
        points[ 3,:] = [ru[0].start, ru[1].start, ru[2].stop , ru[3].stop ]
        points[ 4,:] = [ru[0].start, ru[1].stop , ru[2].start, ru[3].start]
        points[ 5,:] = [ru[0].start, ru[1].stop , ru[2].start, ru[3].stop ]
        points[ 6,:] = [ru[0].start, ru[1].stop , ru[2].stop , ru[3].start]
        points[ 7,:] = [ru[0].start, ru[1].stop , ru[2].stop , ru[3].stop ]
        points[ 8,:] = [ru[0].stop , ru[1].start, ru[2].start, ru[3].start]
        points[ 9,:] = [ru[0].stop , ru[1].start, ru[2].start, ru[3].stop ]
        points[10,:] = [ru[0].stop , ru[1].start, ru[2].stop , ru[3].start]
        points[11,:] = [ru[0].stop , ru[1].start, ru[2].stop , ru[3].stop ]
        points[12,:] = [ru[0].stop , ru[1].stop , ru[2].start, ru[3].start]
        points[13,:] = [ru[0].stop , ru[1].stop , ru[2].start, ru[3].stop ]
        points[14,:] = [ru[0].stop , ru[1].stop , ru[2].stop , ru[3].start]
        points[15,:] = [ru[0].stop , ru[1].stop , ru[2].stop , ru[3].stop ]

        values = np.empty([gridData.shape[0], 16])
        for i in range(gridData.shape[0]):
            values[i, 0] = gridData[i, 0, 0, 0, 0]
            values[i, 1] = gridData[i, 0, 0, 0, 1]
            values[i, 2] = gridData[i, 0, 0, 1, 0]
            values[i, 3] = gridData[i, 0, 0, 1, 1]
            values[i, 4] = gridData[i, 0, 1, 0, 0]
            values[i, 5] = gridData[i, 0, 1, 0, 1]
            values[i, 6] = gridData[i, 0, 1, 1, 0]
            values[i, 7] = gridData[i, 0, 1, 1, 1]
            values[i, 8] = gridData[i, 1, 0, 0, 0]
            values[i, 9] = gridData[i, 1, 0, 0, 1]
            values[i,10] = gridData[i, 1, 0, 1, 0]
            values[i,11] = gridData[i, 1, 0, 1, 1]
            values[i,12] = gridData[i, 1, 1, 0, 0]
            values[i,13] = gridData[i, 1, 1, 0, 1]
            values[i,14] = gridData[i, 1, 1, 1, 0]
            values[i,15] = gridData[i, 1, 1, 1, 1]

        pos = np.array(position)
        dist = points - pos
        mu = np.linalg.norm(points - pos, axis=1)
        return np.dot(values, mu / np.sum(mu))

        # return interp.griddata(points, values, position, method='nearest')
        # return interp.griddata(points, values, position, method='linear') # does not work

    def get_cache(self):
        return self.__cache

    def stop(self):
        self.__cache.stop()





