import numpy as np

from .NetCDFInterface   import NetCDFInterface
from .PeriodicContainer import PeriodicContainer
from .ScaledArray       import ScaledArray
from .DimensionHelper   import DimensionHelper

from nephelae_base.types import Position

class MesoNHVariable(ScaledArray):

    """MesoNHVariable

    Helper class to access MesoNH data using space coordinates
    instead of indexes

    /!\ Reading is done using this order : [t,z,y,x]

    """

    tvar = 'time'
    zvar = 'VLEV'
    yvar = 'S_N_direction'
    xvar = 'W_E_direction'


    def __init__(self, atm, var, origin=None, interpolation='linear'):

        # Getting dimensions of MesoNH array and conversion in SI units
        tdim = atm.variables[MesoNHVariable.tvar][:]
        xdim = 1000.0*atm.variables[MesoNHVariable.xvar][:]
        ydim = 1000.0*atm.variables[MesoNHVariable.yvar][:]
        zdim = 1000.0*np.squeeze(atm.variables[MesoNHVariable.zvar][:,0,0])

        # Seems more logical to start a simulation at time 0.0 in any case ?
        tdim = tdim - tdim[0]
        
        # Reset origin if given
        if origin is not None:
            tdim = tdim - tdim[0] + origin.t
            xdim = xdim - xdim[0] + origin.x
            ydim = ydim - ydim[0] + origin.y
            zdim = zdim - zdim[0] + origin.z
        
        dimHelper = DimensionHelper()
        dimHelper.add_dimension(tdim, 'LUT')
        dimHelper.add_dimension(zdim, 'LUT')
        dimHelper.add_dimension(ydim, 'linear')
        dimHelper.add_dimension(xdim, 'linear')

        # Creating a ScaledArray with a PeriodicContainer as base
        # (MesoNH x,y are periodic)
        super().__init__(PeriodicContainer(NetCDFInterface(atm, var), [2,3]),
                         dimHelper, interpolation)
    

    # CANNOT DO THIS BECAUSE SUBARRAY INHERITS DIMENSIONNAL STRUCTURE
    # def __getitem__(self, keys):

    #     # Had to overload ScaledArray.__getitem__ because of
    #     # weird MesoNH [t,z,y,x] access

    #     """Access array data, key order is [t,x,y,z]
    #         Return a non-periodic scaled array, or
    #         a single floating point number.
    #     """
    #     
    #     return super().__getitem__((keys[0],keys[3],keys[2],keys[1]))


