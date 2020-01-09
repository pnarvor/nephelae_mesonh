import threading
import time

from nephelae.types import Bounds

class MesonhCachedProbe:

    """MesoNHCachedProbe

    This is a class to handle quick successive reads in a MesoNH array.

    Original goal was to make a virtual UAV fly in real time in a 
    MesoNH dataset while reading a single variable (sensor)

    This class in maintaining a cached buffer. All read are done in the 
    cache. A new buffer is loaded in another thread.
    """

    def __init__(self, mesonhVariable, cacheBounds, triggerThreshold = 0.5):

        self.var = mesonhVariable
        self.cacheBounds = [Bounds(b[0],b[-1]) for b in cacheBounds]
        self.thresholdValues = [triggerThreshold*(b.max-b.min) for b in self.cacheBounds]

        self.cache      = None
        self.updateKeys = None

        self.running      = False
        self.updateLock   = threading.Condition(threading.Lock())
        self.updateThread = threading.Thread(target=self.update_work)
    

    def request_cache_update(self, keys, block=False):

        if self.updateLock.acquire(blocking=block):
            try:
                self.updateKeys = self.var.crop_keys(
                    (slice(self.cacheBounds[0].min + keys[0],
                           self.cacheBounds[0].max + keys[0], None),
                     slice(self.cacheBounds[1].min + keys[1],
                           self.cacheBounds[1].max + keys[1], None),
                     slice(self.cacheBounds[2].min + keys[2],
                           self.cacheBounds[2].max + keys[2], None),
                     slice(self.cacheBounds[3].min + keys[3],
                           self.cacheBounds[3].max + keys[3], None)))

                # Direct load if block == True
                # for initialization purposes
                if block:
                    self.cache = self.var[self.updateKeys]
                    self.updateKeys = None
                    return

                if not self.must_update_cache(self.updateKeys):
                    return
                self.updateLock.notifyAll()
            finally:
                self.updateLock.release()


    def must_update_cache(self, keys):
        
        """
        Return True if an update of cache is necessary given the cache bounds
        and threshold given in __init__.
        """
        if self.cache is None:
            return True

        if any([b.min - key.start > th or key.stop - b.max > th
               for b,key,th in zip(self.cache.bounds, keys, self.thresholdValues)]):
            return True
        else:
            return False


    def update_work(self):

        """
        This is the main cache update fonction which is running in another
        thread. Stays idle until self.updateLock is notified and 
        self.updateKeys is not None.
        """
        
        self.running = True
        while self.running:
            with self.updateLock:
                if self.updateKeys is not None:
                    # if there is something to load do:
                    self.cache = self.var[self.updateKeys]
                    self.updateKeys = None
                # will wait until notified by self.cache_update
                self.updateLock.wait()
    
    def start(self):

        self.updateThread.start()


    def stop(self):

        self.running = False
        with self.updateLock:
            self.updateLock.notifyAll()
        self.updateThread.join()


    def __getitem__(self, keys):
        
        self.request_cache_update(keys, block=False)
        return self.cache[keys]


