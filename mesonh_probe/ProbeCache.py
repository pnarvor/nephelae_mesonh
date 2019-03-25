import numpy as np

from .DoubleBufferedCache import DoubleBufferedCache

class ProbeCache:

    """
    ProbeCache
    Manage updates of a DoubleBufferedCache according to input
    - Input supposed to behave like a "physical probe", exploring the data array
        - Succesive read are supposed to rest within a given range of each other.
        - Cache loading is asynchronous (in another thread) to not impact read latency 
    - Managed data array can be periodic on some dimensions
        - only if input implementing a periodicShape attribute
        - data.dimension[i] is periodic if data.periodicShape[i] < 0
    """

    def __init__(self, data, targetCacheShape,
                 updateTriggerThreshold=0.5, initPosition=[]):

        self.buffer = DoubleBufferedCache(data)
        if hasattr(self.buffer.data, 'periodicShape'):
            self.dataShape = self.buffer.data.periodicShape
        else:
            self.dataShape = self.buffer.shape
        self.targetShape = (np.array(targetCacheShape)[np.newaxis]).T
        self.updateTriggerThreshold = updateTriggerThreshold
        self.lastCachePosition = np.array([])

        # load first time
        if len(initPosition) == 0:
            initPosition = [0.0]*len(data.shape)
        # print("Init position : ", initPosition)
        self.update_cache(initPosition, blocking=True)

    def __getitem__(self, keys):
        # Generating keys to read in workBuffer as if in reading in self.data

        position = [] # set at center of array delimited by keys
        for i,key in enumerate(keys):
            if isinstance(key, slice):
                if key.start is None:
                    key_start = 0
                else:
                    key_start = key.start
                if key.stop is None:
                    key_stop = self.buffer.shape[i]
                else:
                    key_stop = key.stop
                position.append((key_start + key_stop - 1) / 2)
            else:
                position.append(key)
        self.update_cache(position)
        return self.buffer[keys]

    def update_cache(self, position, blocking=False):

        """
        Check and update cache if necessary
        """
        position = (np.floor(np.array(position))[np.newaxis]).T

        if len(position) == len(self.lastCachePosition): 
            if (position == self.lastCachePosition).all():
                return

        if len(self.lastCachePosition) != 0:
            # print("Position       : ", position.T)
            # print("Last position  : ", self.lastCachePosition.T)
            # print("Criterion      : ", 2.0*((position - self.lastCachePosition) / self.targetShape).T)
            # print("Criterion eval : ", (2.0*((position - self.lastCachePosition) / self.targetShape) < self.updateTriggerThreshold).T)
            if 2.0*np.amax((position-self.lastCachePosition) / self.targetShape) < \
                    self.updateTriggerThreshold:
                return

        newCacheKeys = self.__compute_new_cache_keys(position)
        if np.array_equal(newCacheKeys, self.buffer.lastKeys):
            return
        
        self.buffer.load(newCacheKeys, blocking)
        self.lastCachePosition = position

    # private functions #############################################
    def __compute_new_cache_keys(self, position):

        """
        Generates bounds of an array of initial size self.targetShape
        centered on position parameter and clipped to stay within self.dataShape
        """
        
        newCacheLims = np.hstack([position - np.floor(0.5*self.targetShape),
                                  position + np.floor(0.5*self.targetShape)])
        # print("newCacheLims :\n", newCacheLims)
        newCacheKeys = []
        for i in range(newCacheLims.shape[0]):
            if self.dataShape[i] > 0:
                if newCacheLims[i,0] < 0:
                    newCacheLims[i,0] = 0
                if newCacheLims[i,0] > self.dataShape[i]:
                    newCacheLims[i,0] = self.dataShape[i]
            newCacheKeys.append(slice(int(newCacheLims[i,0]), int(newCacheLims[i,1] + 1), None))

        return tuple(newCacheKeys)

