from elevatorproblem.PubSubApproach.ElevatorScheduler import *


def test_addUserFloorReqFromInsideElevator_1():
    # e = Elevator(1, loc=2, dir=Direction.UP, validFloors=[0, 1, 2, 3, 4, 5, 6])
    for i in range(1000):
        generatedStop = Elevator.addUserFloorReqFromInsideElevator([0, 1, 2, 3, 4, 5, 6], 4, Direction.UP)
        if generatedStop not in [5, 6]:
            assert False
    assert True


def test_addUserFloorReqFromInsideElevator_2():
    # e = Elevator(1, loc=2, dir=Direction.UP, validFloors=[0, 1, 2, 3, 4, 5, 6])
    for i in range(1000):
        generatedStop = Elevator.addUserFloorReqFromInsideElevator([0, 1, 2, 3, 4, 5, 6], 5, Direction.UP)
        if generatedStop != 6:
            assert False
    assert True


def test_addUserFloorReqFromInsideElevator_3():
    # e = Elevator(1, loc=2, dir=Direction.UP, validFloors=[0, 1, 2, 3, 4, 5, 6])
    for i in range(1000):
        generatedStop = Elevator.addUserFloorReqFromInsideElevator([-1, 0, 1, 2, 3, 4, 5, 6], 6, Direction.UP)
        if generatedStop is not None:
            assert False
    assert True


def test_addUserFloorReqFromInsideElevator_4():
    # e = Elevator(1, loc=2, dir=Direction.UP, validFloors=[0, 1, 2, 3, 4, 5, 6])
    for i in range(1000):
        generatedStop = Elevator.addUserFloorReqFromInsideElevator([-1, 0, 1, 2, 3, 4, 5, 6], 0, Direction.DOWN)
        if generatedStop != -1:
            assert False
    assert True
