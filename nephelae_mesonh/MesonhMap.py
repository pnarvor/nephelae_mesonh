from nephelae.mapping import MapInterface
from nephelae.types   import Bounds

from .MesonhVariable  import MesonhVariable

class MesonhMap(MapInterface):

    """MapInterface
    
    Implementation of MapInterface to MesonhVariable
    """

    def __init__(self, name, atm, mesonhVar, origin=None, interpolation='linear'):
        super().__init__(name)
        # attribute and not a subclass because python multiple inheritance system
        # seems fragile
        self.mesonh    = MesonhVariable(atm, mesonhVar, origin, interpolation)
        self.dataRange = self.mesonh.actual_range

    
    def at_locations(self, locations, returnStddev=False):
        # Will be awfuly slow, made to match the interface
        res = np.array([self.mesonh[p[0],p[1],p[2],p[3]] for p in locations]).squeeze()
        if returnStddev:
            return (res, np.zeros(res.shape))
        else:
            return res


    def shape(self):
        return self.mesonh.shape


    def span(self):
        return self.mesonh.span


    def bounds(self):
        return self.mesonh.bounds


    def resolution(self):
        return self.mesonh.resolution


    def range(self):
        return self.dataRange

    
    def computes_stddev(self):
        return False


    def __getitem__(self, keys):
        return self.mesonh[keys]




