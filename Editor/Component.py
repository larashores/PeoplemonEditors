__author__ = 'Vincent'

from abc import ABCMeta, abstractmethod, abstractstaticmethod

class Component():
    """
    Represents a single component in an editor. It should a method to create a new object from a byte array, or return
    a byte array representing that component
    """
    __metaclass__ = ABCMeta


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

    @abstractmethod
    def load(self):
        """
        Returns all of the paramters involved in the component in a list

        :return:            List of values representing component
        """
        return []

    @abstractmethod
    def update(self,param):
        """
        Takes list of paramters an updates the components data

        :param param:      List of parameters with component data
        :return:
        """

