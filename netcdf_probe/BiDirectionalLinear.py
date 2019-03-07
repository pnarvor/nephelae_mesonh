import numpy as np

class BiDirectionalLinear:

    """
    BidirectionalLinear : map input 1D space to output 1D space through
                          linear operation
    """

    def __init__(self, inputToOutput, inputRange=[]):

        self.N = len(inputToOutput)
        if not inputRange:
            self.inputRange = [0, self.N - 1]
        else:
            self.inputRange = inputRange
        self.outputRange = [inputToOutput[0], inputToOutput[-1]]

        p1 = [self.inputRange[0], self.outputRange[0]]
        p2 = [self.inputRange[1], self.outputRange[1]]

        self.toOutputAlpha = (p2[1] - p1[1]) / (p2[0] - p1[0])
        self.toOutputBeta  = p1[1] - self.toOutputAlpha * p1[0]

        self.toInputAlpha = (p2[0] - p1[0]) / (p2[1] - p1[1])
        self.toInputBeta  = p1[0] - self.toOutputAlpha * p1[1]

    def toOutputSpace(self, data):
        return self.toOutputAlpha * data + self.toOutputBeta

    def toInputSpace(self, data):
        return self.toInputAlpha * data + self.toInputBeta
