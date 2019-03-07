import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import RegularGridInterpolator

class BiDirectionalLUT:

    """
    BidirectionalLUT : map input 1D space to output 1D space through an array
                       defining a stricly monotonous function
    """

    def __init__(self, inputToOutput, inputRange=[]):

        self.N = len(inputToOutput)
        if not inputRange:
            self.inputRange = [0, self.N - 1]
        else:
            self.inputRange = inputRange
        self.outputRange = [inputToOutput[0], inputToOutput[-1]]

        x_in = np.linspace(self.inputRange[0],
                           self.inputRange[1],
                           len(inputToOutput))

        self.toOutputInterpolator = RegularGridInterpolator((x_in,),
                                                            inputToOutput)
        self.toInputInterpolator = RegularGridInterpolator((inputToOutput,),
                                                           x_in)

    def to_output_space(self, data):
        return self.toOutputInterpolator(data)

    def to_input_space(self, data):
        return self.toInputInterpolator(data)

