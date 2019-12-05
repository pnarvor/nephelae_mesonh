import threading
import numpy as np

t0 = 92

class MesonhInterface:

    """
    This class is a helper interface to access multiple MesoNH variables in a numpy-like fashion
    
    Is thread safe for array read when using __getitem__.
    """

    lock = threading.Lock()

    def __init__(self, mesonhDataset, mesonhVariables):

        """
        """

        self.mesonhDataset = mesonhDataset

        self.variables = {}
        self.varData   = []
        if isinstance(mesonhVariables, str):
            self.variables[mesonhVariables] = self.mesonhDataset.variables[mesonhVariables]
            self.varData.append(self.variables[mesonhVariables])
        elif isinstance(mesonhVariables, (list, tuple,)):
            for var in mesonhVariables:
                self.variables[var] = self.mesonhDataset.variables[var]
                self.varData.append(self.variables[var])
        else:
            raise TypeError("mesonhVariable must be a string or a tuple or strings")
            
        # shape = []
        # # for dim in self.varData[0].dimensions:
        # #     shape.append(len(self.mesonhDataset.dimensions[dim]))
        # for dim in self.mesonhDataset.dimensions:
        #     shape.append(len(dim['data']))
        shape = [len(dim['data']) for dim in self.mesonhDataset.dimensions]
        self.shape = (shape[0], shape[3], shape[2], shape[1], len(self.varData))



    def __getitem__(self, keys):

        keys, shape = self.process_keys(keys)
        output = []
        with MesonhInterface.lock:
            for var in self.varData:
                # output.append(np.array(var[keys]).reshape(shape))
                output.append(self.fixed_time_read(var, keys, shape).reshape(shape))
        return np.array(output).transpose((1,4,3,2,0)).squeeze()

    
    def fixed_time_read(self, var, keys, shape):
        keys = list(keys)
        keys[0] = t0
        keys = tuple(keys)
        output = np.array(var[keys])
        # print("output1", output.shape)
        output = np.array([[output]] * shape[0])
        # print("output2", output.shape)

        return output

    def process_keys(self, keys):

        if keys is None:
            keys = [slice(None), slice(None), slice(None), slice(None)]
        keys = list(keys)
        while len(keys) < 4:
            keys.append(slice(None))

        shape = []
        for key, dim in zip(keys, self.shape):
            if isinstance(key, slice):
                if key.step is not None and key.step != 1:
                    raise ValueError("Step value in slice not supported")
                if key.start is None:
                    key_start = 0
                else:
                    if key.start < 0:
                        key_start = key.start + dim
                    else:
                        key_start = key.start
                if key.stop is None:
                    key_stop = dim
                else:
                    if key.stop < 0:
                        key_stop = key.stop + dim
                    else:
                        key_stop = key.stop
                shape.append(key_stop - key_start)
            else:
                shape.append(1)

        return ( keys[0],  keys[3],  keys[2],  keys[1]),\
               (shape[0], shape[3], shape[2], shape[1])



