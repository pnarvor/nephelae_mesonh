from .ProbeCache import ProbeCache
import numpy as np

class MesoNHProbe:

    """
    MesoNHProbe
    Gives efficient acces to a large collection of MesoNH files
        - Intended to simulate a flight inside MesoNH data
    """

    def __init__(self, atm, variables, maxVelocity=25, frequency=4):

        """
        - atm         : MFDataset from netCDF4 package ALREADY LOADED with
                        a set of mesonh files
        - maxVelocity : Max espected flight velocity (in m/s), Used to compute
                        cache parameters (caution, too high cause large cache
                        loadings and may severe simulation speed)
        - frequency   : Extimated sampling frequency (in Hz) of data queries.
                        used to compute cache parameters (too low may
                        cause large cache buffers, too high may cause
                        too often occurring cache update)
        """

        self.atm = atm
        self.variables = variables
        self.probes = []

