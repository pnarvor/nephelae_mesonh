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

    def __init__(self, data, targetCacheShape, updateTriggerThreshold=0.5)

        self.buffer = DoubleBufferedCache(data)
        if hasattr(self.buffer.data, 'periodicShape'):
            self.dataShape = self.data.periodicShape
        else:
            self.dataShape = self.data.shape
        self.targetShape = np.array(targetCacheShape)
        self.updateTriggerThreshold = updateTriggerThreshold

    def update_cache(self, position, blocking=False):

        """
        Check and update cache if necessary
        """
        
        position = floor(position)
        if np.amax((position - self.lastCachePosition) / targetShape) < \
                self.updateTriggerThreshold:
            return

        newCacheKeys = self.compute_new_cache_keys(position)
        if np.array_equal(newCacheLims, self.lastKeys)
            return

        try:
            self.buffer.load(newCacheTuple, blocking)
        except:
            print("Could not update cache")

    def conpute_new_cache_keys(self, position):

        """
        Generates bounds of an array of initial size self.targetShape
        centered on position parameter and clipped to stay within self.dataShape
        """

        newCacheLims = np.hstack(position - floor(0.5*self.targetShape),
                                 position + floor(0.5*self.targetShape))
        
        newCacheKeys = []
        for i in range(newCacheLims.shape[0]):
            if self.dataShape[i] < 0:
                continue
            if newCacheLims[i,0] < 0:
                newCacheLims[i,0] = 0
            if newCacheLims[i,0] > self.dataShape[i]:
                newCacheLims[i,0] = self.dataShape[i]
            newCacheKeys.append(slice(newCacheLims[i,0], newCacheLims[i,1], None))

        return tuple(newCacheKeys)

