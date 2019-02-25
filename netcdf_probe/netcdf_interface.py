# This class is intended to provide a fast single data read in a collection of mesonh files
# by mean of putting part of the files in cache 
# under the assumption that successive read for the file are not far from each other.
# (primary application is a simulation of a UAV flight into MesoNH files

import numpy as np

class NetCDFInterface:

    # self.netcdf : handle to already opened netCDF files (either netCDF4.MFDataset or netCDF4.Dataset types)

    def __init__(self, netcdfData, netcdfVariableName, periodicVariables=[]):

        self.netcdfData = netcdfData
        self.varName = netcdfVariableName
        self.varData = self.netcdfData.variables[netcdfVariableName]
        shape = []
        self.isPeriodic = []
        for dim in self.varData.dimensions:
            print(dim)
            shape.append(len(self.netcdfData.dimensions[dim]))
            if any(dim in var for var in periodicVariables):
                self.isPeriodic.append(True)
            else:
                self.isPeriodic.append(False)
        self.shape = tuple(shape)
        self.outputShape = ()
        self.readTuples = []
        self.writeTuples = []

    def format_keys(self, keys):
        checkedKeys = []
        for i, key in enumerate(keys):

            if isinstance(key, slice):
                if key.start == None:
                    key_start = 0
                else:
                    key_start = key.start
                if key.stop == None:
                    key_stop = self.shape[i] - 1
                else:
                    key_stop = key.stop
                key = slice(key_start, key_stop, key.step)

                if key.start > key.stop:
                    raise Exception("Error : slice must have positive length")

                if self.isPeriodic[i]: # if dim is periodic set key.start into shape bounds
                    t = self.shape[i] * (key.start // self.shape[i])
                    checkedKeys.append(slice(key.start - t, key.stop - t, key.step))
                else:
                    if key.start < 0 or key.start >= self.shape[i]:
                        raise Exception("Error : index not inside shape")
                    if key.stop < 0 or key.stop >= self.shape[i]:
                        raise Exception("Error : index not inside shape")
                    checkedKeys.append(key)
            else:
                if self.isPeriodic[i]:
                    key = key - self.shape[i] * (key // self.shape[i])
                else:
                    if key < 0 or key >= self.shape[i]:
                        raise Exception("Error : index not inside shape")
                checkedKeys.append(slice(key, key, None))

        return tuple(checkedKeys)

    def expandTuples(tuples):
        out = []
        if len(tuples) <=  1:
            for tu in tuples[0]:
                out.append((tu,))
        else:
            others = NetCDFInterface.expandTuples(tuples[1:])
            for tu0 in tuples[0]:
                for tu1 in others:
                    out.append((tu0,) + tu1)
        return out

    def compute_read_write_tuples(self, keys):
        shape = []
        for key in keys:
            shape.append(key.stop - key.start + 1)
        self.outputShape = tuple(shape)

        readTuples  = []
        writeTuples = []
        for key, inDimLen, outDimLen in zip(keys, self.shape, self.outputShape):

            Ntuples = 1 + key.stop // inDimLen
            print(Ntuples, key, inDimLen, outDimLen)

            ituples = []
            if Ntuples <= 1:
                ituples = [key]
            else:
                ituples = [slice(0, inDimLen-1)] * (Ntuples - 2)
                ituples.insert(0, slice(key.start, inDimLen-1))
                ituples.append(slice(0, key.stop % inDimLen))
            index0 = 0
            otuples = []
            for tu in ituples:
                otuples.append(slice(index0, index0 + tu.stop - tu.start))
                index0 += tu.stop - tu.start + 1

            readTuples.append(ituples)
            writeTuples.append(otuples)

            print("--- ", ituples)
            print("--- ", otuples)
        
        self.readTuples = NetCDFInterface.expandTuples(readTuples)
        self.writeTuples = NetCDFInterface.expandTuples(writeTuples)

        print("readTuples len  : ", len(readTuples))
        for tu in self.readTuples:
            print(tu)
        print("writeTuples len : ", len(writeTuples))
        for tu in self.writeTuples:
            print(tu)
        

    def __getitem__(self, keys):
    
        self.compute_read_write_tuples(self.format_keys(keys))
        res = np.empty(self.outputShape)
        print(res.shape)

        for readIndex, writeIndex in zip(self.readTuples, self.writeTuples):
            print("Read index  :", readIndex)
            print("Write index :", writeIndex, "\n")
            res[writeIndex] = self.varData[list(readIndex)]



