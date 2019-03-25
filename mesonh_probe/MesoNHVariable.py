from .NetCDFInterface import NetCDFInterface
from .PeriodicContainer import PeriodicContainer

class MesoNHVariable(PeriodicContainer):

    def __init__(self, atm, var):
        super(MesoNHVariable, self).__init__(NetCDFInterface(atm, var), [2,3])
