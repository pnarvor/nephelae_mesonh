import threading as th
import numpy as np
import time

class DoubleBufferedCache(th.Thread):

    """
    DoubleBufferedCache : class to asynchronously read a numpy array like object (data : implements shape and _getitem__ returning numpy arrays)
        - Use case : the data array is only an interface to a ressource with slow reading (originaly intended for reading large netcdf datasets)
        - This object behaves as a numpy array of the same size as the data interface, but hold only a subset of it in workBuffer
            - When accessing data, the indexes to use are the same one as the data interface
            - Behavior when requesting data not yet loaded in workBuffer is undefined
    """

    def __init__(self, data):
        
        """
        Constructor of DoubleBufferedCache:
            - data       : slow access array ressource (must implement __getitem__ as numpy arrays)
            - shape      : convenience attribute for users, not used in implementation below
            - workBuffer : loaded buffer (quick access)
            - workOrigin : offset in indexes of __getitem__ to have same behavior as the data ressource
            - loadKeys   : hold indexes (both integer and slices)  of array to load from self.data
            - loadLock   : to prevent several successive calls to self.load() from spawning several loading threads
            - workLock   : lock acces to workBuffer and workOrigin during access (__getitem__) and update (run)
        """
      
        # initialsation of base threading class
        super(DoubleBufferedCache, self).__init__(name="DoubleBufferedCache-{}".format(id(self)))

        self.data       = data
        self.shape      = data.shape
        self.workBuffer = np.array([])
        self.workOrigin = []
        self.loadKeys   = ()
        self.loadLock   = th.Lock()
        self.workLock   = th.Lock()

    def __getitem__(self, keys):

        newKeys = []
        if not self.workLock.acquire(timeout = 3):
            raise Exception("Could read workBuffer : could not lock")
        
        # Generating to read in worBuffer as if in reading in self.data
        for key, origin in zip(keys,workOrigin):
            if isinstance(key, slice):
                if key.start is None:
                    key_start = 0 - origin
                else:
                    key_start = key.start - origin
                if key.stop is None:
                    key_stop = 0 - origin
                else:
                    key_stop = key.stop - originA
                newKeys.append(slice(key_start, key_stop, None))
            else:
                newKeys.append(key - origin)
        
        res = workBuffer[tuple(newKeys)]
        self.workLock.release()
        return res

    def load(self, keys, blocking=False):

        """
        Request load of data into workBuffer:
            - Load array part indexed by keys
            - Can be synchronous (blocking=True) or asynchrounous (blocking=False)
        """
        
        print("Load requested : ", keys)
        if blocking:
            if not self.loadLock.acquire(blocking=False):
                print("Loading still in progress : cannot call load function")
                return
            self.loadKeys = keys
            self.loadLock.release() # release lock, is locked again in self.run()
            self.run()              # if blocking, not spawning a thread to load data
        else:
            if not self.loadLock.acquire(blocking=False):
                print("Loading still in progress : cannot call load function")
                return
            self.loadKeys = keys
            self.start()
            self.loadLock.release() # release lock, is locked again in self.run()

    # private member functions ###################################
    def run(self):

        """
        Perform asynchronous loading of self.data
            - Will be called by self.load() in a new thread
        """
        print("Load process started")
        print("-- keys : ", self.loadKeys)
        if not self.loadLock.acquire(timeout=3):
            raise Exception("Error : could not lock loadingLock, aborting !")

        newBuffer = self.data[self.loadKeys]
        newOrigin = []
        for key in self.loadKeys:
            if isinstance(key, slice):
                if key.start is None:
                    newOrigin.append(0)
                else:
                    newOrigin.append(key.start)
            else:
                newOrigin.append(key)
       
        # Data is loaded in newBuffer, updating workBuffer
        if not self.workLock.acquire(timeout = 3):
            loadLock.release()
            raise Exception("Could not update workBuffer : could not lock")

        self.workBuffer = newBuffer
        self.workOrigin = newOrigin

        self.workLock.release()
        self.loadLock.release()
        print("Load process finished")



