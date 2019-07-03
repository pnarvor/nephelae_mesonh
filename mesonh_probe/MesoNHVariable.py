from .NetCDFInterface import NetCDFInterface
from .PeriodicContainer import PeriodicContainer

from nephelae_base.types import Position

class MesoNHVariable(PeriodicContainer):

    """MesoNHVariable

    Helper class to access MesoNH data using space coordinates
    instead of indexes

    """

    tvar = 'time'
    zvar = 'VLEV'
    xvar = 'W_E_direction'
    yvar = 'S_N_direction'

    def __init__(self, atm, var, origin=Position(0.0,0.0,0.0,0.0)):
        super().__init__(NetCDFInterface(atm, var), [2,3])
        
        self.mesonhOrigin = Position(atm.variables[tvar][0],
                                     atm.variables[xvar][0],
                                     atm.variables[yvar][0],
                                     0.0)
        self.origin = origin - self.mesonhOrigin

    # def __getitem__(self, keys): 

    #     """Get array of data. Keys are expressed in seconds and meters and
    #     relative to the origin Position given in __init__. A key element can 
    #     be a slice.
    #     """


