import xarray as xr
from glob import glob
import numpy as np

class MesonhDataset:
    """
    MesonhDataset

    Class to interface with MesoNH files.

    This is to easilly cope with different MesoNH formats.

    Attributes
    ----------
    
    dataFilenames : str or list(str,...)
        List of opened filenames.

    data : opened with xarray.open_mfdataset
        Data as opened by xarray

    variables : dictionary like object
        Reference to self.data.variables

    dimensions : list(dict('name':str, 'data':numpy.array), ...)
        List of dimension of data. Each dimension has a name and a scale.
        To abstract dimensions given by xarray, can be ambiguous.
    """

    defaultTimeVariable = 'time'

    def __init__(self, dataFilenames, dimensionNames=None):

        """
        Parameters
        ----------
        dataFilenames : str or list(str,...)
            Path of file(s) to be opened.

        dimensionNames : None or list(str,...)
            Names of dimensions of data. If None, will be inferred from dataset
            reading the dimension of the RCT variable.
        """
        
        if type(dataFilenames) is str:
            if '*' in dataFilenames:
                dataFilenames = glob(dataFilenames)
        if type(dataFilenames) is list:
            dataFilenames.sort()

        self.dataFilenames = dataFilenames
        self.data          = xr.open_mfdataset(self.dataFilenames)
        self.variables     = self.data.variables
        self.dimensions    = []

        if dimensionNames is None:
            try:
                # Inferring dimensions from the RCT field dimensions
                dimensionNames = self.data.RCT.dims
            except AttributeError as e:
                print("Failed to infer dimensions from data. " +
                      "AttributeError feedback :", e)

        if dimensionNames is not None:
            for dimName in dimensionNames:
                data = self.variables[dimName]
                if dimName == MesonhDataset.defaultTimeVariable:
                    # Dimension is time. Conversion to float(seconds)
                    # Any idea on simpler way to do this is welcome
                    # (why so complicated ???)A
                    # Also time origin set to 0
                    data = (data - data[0]) / np.array([1], dtype='m8[s]')
                self.dimensions.append({'name':dimName, 'data':data})

