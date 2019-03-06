import threading as th

class NetCDFInterface:

    """
    This class is a helper interface to access netCDF data in a numpy-like fashion
    """

    dataMutex = th.Lock()

    def __init__(self, netcdfData, netcdfVariable):

        """
        NetCDFInterface constructor:
            - netCDFData     : netCDF4.MFDataset type already loaded from netcdf files
            - netcdfVariable : variable to ouput from this class
        Will infer shape of the array from netCDF data
        """

        self.netcdfData = netcdfData
        self.varName = netcdfVariable
        self.varData = self.netcdfData.variables[netcdfVariable]
        shape = []
        for dim in self.varData.dimensions:
            shape.append(len(self.netcdfData.dimensions[dim]))
        self.shape = tuple(shape)

    def __getitem__(self, keys):
        
        res = []
        NetCDFInterface.dataMutex.acquire()
        res = self.varData[keys]
        NetCDFInterface.dataMutex.release()

        return res
