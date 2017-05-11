from saveable.composite import Composite
from saveable.saveableImage import SaveableImage
from saveable.saveableArray import array
from saveable.node import Node


class SalesmanConfig(Composite):
    """
    Represents the configuration of the salesman. Consists of a single background image and a list of nodes
    """
    background = SaveableImage
    nodes = array(Node)
