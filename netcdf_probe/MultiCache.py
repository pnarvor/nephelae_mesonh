import threading as th
import numpy as np
import time

class MultiCache(th.Thread):

    """
    MultiCache : allow asynchronous loading from array
                 (intended for array in which single value read are
                 as slow as bulk read, much like streaming)

    - public member functions :
        __init__(self, arrays)     : arrays=list of arrays to read from
        __getitem__                : get elements in self.buffers, thread safe
                                     returns a list of numpy arrays.
                                     WARNING : keys are expressed in the 
                                     self.data.shape, not self.buffer.shape
        load(self, keys, blocking) : keys=tuple used to read into arrays
                                     (self.buffer[i] = self.data[i][keys]
                                     if blocking == True, data is loaded
                                     from current thread. (default is False)

    - public attributes :
        data       : data to read from
        buffers    : list of numpy arrays already read from self.data
                     (empty at initialization)
        bufferLims : self.buffer location in self.data
                     equal to last key used in load(self, keys)
                     (self.buffer[i] = self.data[i][self.bufferLims]

    - private member functions :
        run(self)            : main loading thread, is always active but wait
                               for input (wait using self.__loadLock() until
                               self.__loadRequested is set to True).
                               Calls self.__doLoad()
        __doLoad(self, keys) : perform all the loading process
                               locks self.__bufferLock but can be called
                               outside self.run()

    - private attributes :
        __running       : boolean condition on thread main loop
        __bufferLock    : threading.lock() used to protect access to
                          self.buffers and self.bufferLims
        __loadLock      : threading.Condition(), used to make self.run()
                          wait for a load request
        __loadRequested : boolean. Set to true when self.load called.
                          True until data was loaded or error
                          occured during load
        __loadKeys      : set equal to keys in self.load(keys) to be used in
                          loading thread
        __bufferOrigin  : coordinates of "lower left" corner of self.buffer in
                          self.data. Used inside __getitem__ to translate keys
                          for read in buffers
    """

    # public member functions
    def __init__(self, arrays):
      
        # initialsation of base threading class
        super(MultiCache, self).__init__(name="MultiCache-{}".format(id(self)))

        # public attributes
        self.data       = arrays
        self.buffers    = [np.empty([])]*len(self.data)
        self.bufferLims = ()

        # private attributes
        self.__running       = False
        self.__bufferLock    = th.Lock()
        self.__loadLock      = th.Condition()
        self.__loadRequested = False
        self.__loadKeys      = ()
        self.__bufferOrigin  = []

        self.start()

    def __getitem__(self, keys):

        self.__bufferLock.acquire()

        newKeys = ()
        for key, origin in zip(keys, self.__bufferOrigin):
            if isinstance(key, slice):
                newKeys = newKeys + (slice(key.start - origin,
                                           key.stop  - origin, None),)
            else:
                newKeys = newKeys + (key - origin,)

        res = []
        for buf in self.buffers:
            res.append(buf[newKeys])

        self.__bufferLock.release()

        return res

    def load(self, keys, blocking=False):
        if not self.__loadLock.acquire(blocking=blocking):
            raise Exception("MultiCache.load() : Could not lock __loadLock, aborting")
        if blocking:
            self.__doLoad(keys)
        else:
            self.__loadKeys = keys
            self.__loadRequested = True
            self.__loadLock().notify()
        self.__loadLock.release()

    # private member functions  
    def run(self):

        self.__loadLock.acquire()
        self.__running = True
        while self.__running:

            while not self.__loadRequested:
                self.__loadLock.wait()
                if not self.__running:
                    self.__loadLock.release()
                    return
            
            try:
                self.__doLoad(self.__loadKeys)
            except error:
                print("Loading error :", error)

            self.__loadRequested = False
            
            # prevent potential deadLock, not used in nominal behavior
            if not self.__running:
                self.__loadLock.release()

                break

    def __doLoad(self, keys):
       
        # perfom load from self.data
        outputs = []
        for array in self.data:
            outputs.append(array[keys])

        # computing new self.__bufferOrigin
        bufferOrigin = []
        for key in self.bufferLims:
            if isinstance(key, slice):
                bufferOrigin.append(key.start)
            else:
                bufferOrigin.append(key)

        # perform buffer "swap"
        self.__bufferLock.acquire()
        self.buffers = []
        for out in outputs:
            self.buffers.append(out)
        self.bufferLims = keys
        self.__bufferOrigin = bufferOrigin
        self.__bufferLock.release()

