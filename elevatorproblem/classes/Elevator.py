from enum import Enum


class Elevator(object):
    class Direction(Enum):
        UP = 1
        DOWN = 2
        NOTMOVING = 3

    def __init__(self, loc=0, dir=Direction.NOTMOVING, validFloors=[0]):
        self.location = loc

