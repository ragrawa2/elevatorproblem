from elevatorproblem.classes import Elevator


class Building(object):

    def __init__(self, numElevators, maxFloor, minFloor):
        self.numElevators = numElevators
        self.maxFloor = maxFloor
        self.minFloor = minFloor
        self.elevators = []
        for i in range(numElevators):
            self.elevators[i] =Elevator()


if __name__ == "__main__":
    main()


def main():
    b = Building(2, 10, -3)
