__author__ = 'Vincent'

from abc import ABCMeta, abstractmethod, abstractstaticmethod

class Component():
    """
    Represents a single component in an editor. It should a method to create a new object from a byte array, or return
    a byte array representing that component
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.paramDict = {}

    @abstractmethod
    def fromByteArray(self,byteArray):
        """
        Makes a new Component object from a bytearray

        :param byteArray:   The bytearray representing the object
        :return:            A Component object
        """
        return Component()

    @abstractmethod
    def toByteArray(self):
        """
        Return a bytearray representation of the Component

        :return:            The bytearray
        """
        return bytearray()

    def load(self,params,options=None):
        """
        Lists any parameters requested

        :return:            List of values representing component
        """
        values = []
        for param in params:
            if param in self.paramDict.keys():
                values.append(self.paramDict[param])
            else:
                raise Exception('Unknown parameter')
        return values

    def update(self,paramdict,options=None):
        """
        Takes dictionary of paramters mapped to values and updates the components data

        :param param:      List of parameters with component data
        :return:
        """
        for key,val in paramdict.items():
            if not key in self.paramDict:
                raise Exception('Invalid parameter')
            self.paramDict[key] = val

    def addParam(self,name,val):
        """
        Adds a parameter to the component
        :param name: The name of the parameter
        :param val:  The initial value of the parameter
        :return:
        """
        self.paramDict[name] = val

