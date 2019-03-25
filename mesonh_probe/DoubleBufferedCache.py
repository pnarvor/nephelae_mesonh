import threading as th
import numpy as np
import time

class DoubleBufferedCache(th.Thread):

    """
    DoubleBufferedCache : class to asynchronously read a numpy array like object
        - data : implements shape and _getitem__ returning numpy arrays
        - Use case : the data array is only an interface to a ressource with slow reading
          (originaly intended for reading large netcdf datasets)
        - This object behaves as a numpy array of the same size as the data interface,
          but hold only a subset of it in workBuffer
            - When accessing data, the indexes to use are the same one as the data interface
            - Behavior when requesting data not yet loaded in workBuffer is undefined
    """

    def __init__(self, data):
        
        """
        Constructor of DoubleBufferedCache:
            - data       : slow access array ressource
                           (must implement __getitem__ as numpy arrays)
            - shape      : convenience attribute for users, not used in implementation below
            - workBuffer : loaded buffer (quick access)
            - workOrigin : offset in indexes of __getitem__ to have same behavior
                           as the data ressource
            - loadKeys   : hold indexes (both integer and slices) of array to load from self.data
            - loadLock   : to prevent several successive calls to self.load()
                           from spawning several loading threads
            - workLock   : lock acces to workBuffer and workOrigin during
                           access (__getitem__) and update (run)
        """
      
        # initialsation of base threading class
        super(DoubleBufferedCache, self).__init__(
            name="DoubleBufferedCache-{}".format(id(self)))

        self.data              = data
        self.shape             = data.shape
        self.buffer            = np.array([])
        self.bufferOrigin      = []
        self.bufferLock        = th.Lock()
        self.loadKeys          = ()
        self.lastKeys          = ()
        self.loadRequestWaiter = th.Condition()
        self.mustLoad          = False

        self.start()

    def inBuffer(self, keys):
        
        for key, size in zip(keys, self.buffer.shape):
            if isinstance(key, slice):
                if key.start is not None and key.start < 0:
                    return False
                if key.stop is not None and key.stop > size:
                    return False
            else:
                if not (0 <= key < size):
                    return False

        return True

    def __getitem__(self, keys):

        # Generating keys to read in workBuffer as if in reading in self.data
        newKeys = ()
        res = [] 
        if not self.bufferLock.acquire(timeout = 3):
            raise Exception("Could read workBuffer : could not lock")

        for key, origin in zip(keys,self.bufferOrigin):
            if isinstance(key, slice):
                if key.start is None:
                    key_start = 0 - origin
                else:
                    key_start = key.start - origin
                if key.stop is None:
                    key_stop = 0 - origin
                else:
                    key_stop = key.stop - origin
                newKeys = newKeys + (slice(key_start, key_stop, None),)
            else:
                newKeys = newKeys + (key - origin,)
        
        # print("Checking keys :")
        # print("Keys  : ", keys)
        # print("Keys  : ", newKeys)
        # print("Shape : ", self.buffer.shape)
        if not self.inBuffer(newKeys):
            return []

        try:
            res = self.buffer[newKeys]
        except:
            res = []
        self.bufferLock.release()
        return res

    def get(self, keys):
        
        # keys assumed to be inside buffer shape
        res = [] 
        if not self.bufferLock.acquire(timeout = 3):
            raise Exception("Could read workBuffer : could not lock")
        try:
            res = self.buffer[tuple(keys)]
        except:
            res = []
        self.bufferLock.release()
        return res

    def load(self, keys, blocking=False):

        """
        Request load of data into workBuffer:
            - Load array part indexed by keys
            - Can be synchronous (blocking=True) or asynchrounous (blocking=False)
        """
        
        if not self.isAlive():
            raise Exception("Error : loading thread is not alive.")

        # print("Load requested : ", keys)
        self.loadRequestWaiter.acquire()
        # print("Main thread : Got lock")
        self.loadKeys = keys
        self.mustLoad = True
        self.loadRequestWaiter.notify()
        self.loadRequestWaiter.release()
        # print("Main thread : released lock")

        if blocking:
            self.loadRequestWaiter.acquire()
            while self.mustLoad:
                self.loadRequestWaiter.wait()
            self.loadRequestWaiter.release()

    # private member functions ###################################
    def run(self):

        """
        Perform asynchronous loading of self.data
            - Started on the constructor, wait for load requests
        """
        
        loadCount = 0;
        # print("Loading thread started")
        self.running = True
        while self.running:
            
            self.loadRequestWaiter.acquire()
            while not self.mustLoad:
                # print("    ", loadCount, " - Loading thread waiting...")
                self.loadRequestWaiter.wait()
            if not self.running:
                self.loadRequestWaiter.release()
                break

            # print("    ", loadCount, " - Load process started")
            # print("    ", loadCount,"-- keys               : ", self.loadKeys)
            # print("    ", loadCount,"-- last keys          : ", self.lastKeys)
            # print("    ", loadCount,"-- last buffer shape  : ", self.buffer.shape)
            # print("    ", loadCount,"-- last buffer origin : ", self.bufferOrigin)

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
            if not self.bufferLock.acquire(timeout = 3):
                self.mustLoad = False
                self.loadRequestWaiter.release()
                raise Exception("Could not update workBuffer : could not lock")

            self.buffer = newBuffer
            self.bufferOrigin = newOrigin
            self.lastKeys = self.loadKeys
            self.bufferLock.release()

            # print("    ", loadCount, "-- next keys          : ", self.lastKeys)
            # print("    ", loadCount, "-- next buffer shape  : ", self.buffer.shape)
            # print("    ", loadCount, "-- next buffer origin : ", self.bufferOrigin)

            self.mustLoad = False
            self.loadRequestWaiter.notify()
            self.loadRequestWaiter.release()
            # print("    ", loadCount, " - Load process finished")
            loadCount += 1



