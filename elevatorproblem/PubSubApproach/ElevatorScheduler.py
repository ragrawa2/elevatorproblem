from elevatorproblem.PubSubApproach.PublisherObserver import Subscriber, Publisher
from elevatorproblem.PubSubApproach.RequestCall import RequestCall
import random
import datetime
import time
import threading
import numpy as np
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)


class Direction(Enum):
    UP = 1
    DOWN = 2
    NONE = 3


class Elevator(threading.Thread):

    def __init__(self, num, loc=0, dir=Direction.NONE, validFloors=[0], lock=None):
        super(Elevator, self).__init__()
        self.num = num
        self.location = loc
        self.direction = dir

        self.validFloors = validFloors
        self.validFloors.sort()

        self.upStops = set()
        self.downStops = set()

        self.lock = lock

    def get_position(self):
        """
        gets position of elevator
        :return: location and direction
        """
        return self.location, self.direction

    def set_direction(self, direction):
        """
        set method on direction
        :return: void
        """
        self.direction = direction

    def can_go(self, floor):
        """
        is elevator eligible for the floor
        :param floor: int
        :return: true or false
        """
        return floor in self.validFloors

    def addStop(self, req):
        """
        stop is added for elevator
        :param req: Request
        :return: void
        """
        if req.direction == Direction.UP:
            self.upStops.add(req.floor)
        else:
            self.downStops.add(req.floor)

    def moveElevator(self, floor, directionOfRequests):
        """
        :param floor: int, floor number to move to
        :param directionOfRequests: which direction is elevator moving in
        :return: void
        """
        self.location = floor
        self.set_direction(directionOfRequests)
        logging.info(
            "{}  Elevator #{} is moving to floor : {} to process all direction={} which will take 2 seconds.".format(
                self.__class__.name, self.num, floor, directionOfRequests))
        time.sleep(2)

    def run(self):
        """
        start part of the code
        :return:
        """

        # direction can only be changed by set_direction for clean implementation
        while True:
            if self.direction == Direction.UP:
                self.processUPReq()
            elif self.direction == Direction.DOWN:
                self.processDownReq()
            else:
                self.processNoneReq()

            logging.info("Elevator # {}. current position : {}".format(self.num, self.get_position()))
            time.sleep(4)
            # if len(self.upStops) != 0 or len(self.downStops) != 0:
            #     req = self.

    def processUPReq(self):
        logging.info("UP UP Elevator #{} current position : {}".format(self.num, self.get_position()))
        logging.info(self.upStops)
        floorsReachableWithDirection = [x for x in self.upStops if x >= self.location]
        if len(floorsReachableWithDirection) == 0:
            self.set_direction(Direction.NONE)
        else:
            target = min(floorsReachableWithDirection)
            if target == self.location:
                with self.lock:
                    self.upStops.remove(target)
                    logging.info("removing {} from Elevator # {}".format(target, self.num))
                    newStop = self.addUserFloorReqFromInsideElevator(self.validFloors, self.location, Direction.UP)
                    if newStop is not None:
                        self.upStops.add(newStop)
                    logging.info("within our lock state")
                    logging.info("Sleeping for 5")
                    time.sleep(5)
            else:
                self.moveElevator(target, Direction.UP)

    def processDownReq(self):
        logging.info("DOWN DOWN Elevator #{} current position : {}".format(self.num, self.get_position()))
        logging.info(self.downStops)
        floorsReachableWithDirection = [x for x in self.downStops if x <= self.location]
        if len(floorsReachableWithDirection) == 0:
            self.set_direction(Direction.NONE)
        else:
            target = max(floorsReachableWithDirection)

            if target == self.location:
                with self.lock:
                    self.downStops.remove(target)
                    logging.info("removing {} from Elevator # {}".format(target, self.num))
                    newStop = self.addUserFloorReqFromInsideElevator(self.validFloors, self.location, Direction.DOWN)
                    if newStop is not None:
                        self.downStops.add(newStop)
                    logging.info("within our lock state")
                    logging.info("Sleeping for 5")
                    time.sleep(5)
            else:
                self.moveElevator(target, Direction.DOWN)

    @staticmethod
    def addUserFloorReqFromInsideElevator(validFloors, location, whichWay):
        if whichWay == Direction.DOWN:
            chooseFrom = [x for x in validFloors if x < location]
        else:
            chooseFrom = [x for x in validFloors if x > location]

        if len(chooseFrom) == 0:
            return None
        else:
            return random.choice(chooseFrom)

    @staticmethod
    def addValidInput(x, y):
        try:
            val = random.randint(x + 1, y)
        except:
            return None
        return val

    def processNoneReq(self):
        if len(self.upStops) == 0 and len(self.downStops) == 0:
            return
        # going with most number of request tie break with UP
        if len(self.downStops) > len(self.upStops):
            self.moveElevator(max(self.downStops), Direction.DOWN)
        else:
            self.moveElevator(min(self.upStops), Direction.UP)


class ElevatorScheduler(Subscriber):

    def __init__(self, numElevators, minFloor, maxFloor, name="dummyScheduler"):
        self.name = name
        self.numElevators = numElevators
        self.maxFloor = maxFloor
        self.minFloor = minFloor
        self.elevators = []
        self.locks = []
        self.numberOfRequestForHashing = 0
        for i in range(numElevators):
            myLock = threading.Lock()
            self.locks.append(myLock)
            logging.info(i)
            logging.info(list(np.arange(minFloor, maxFloor + 1)))
            self.elevators.append(Elevator(i, validFloors=list(np.arange(minFloor, maxFloor + 1)), lock=myLock))
            self.elevators[i].start()

    def update(self, message):
        directionRequest = message.direction
        fromFloorRequest = message.from_floor

        self.numberOfRequestForHashing = self.numberOfRequestForHashing + 1
        logging.info('{} got message "{}"'.format(self.name, str(message)))
        index = self.numberOfRequestForHashing % self.numElevators
        if directionRequest == Direction.UP:
            with self.locks[index]:
                self.elevators[index].upStops.add(fromFloorRequest)
        else:
            with self.locks[index]:
                self.elevators[index].downStops.add(fromFloorRequest)

    def getNumElevators(self):
        return self.numElevators

    def getMinFloor(self):
        return self.minFloor

    def getMaxFloor(self):
        return self.maxFloor


class RequestGenerator(Publisher):
    """
    generates button press requests from user
    """

    def __init__(self):
        super(RequestGenerator, self).__init__()

    def generateRequest(self, f=None):
        # self.register("ravi_scheduler")
        if f is not None:
            floor = f
        else:
            floor = random.randint(-2, 10)

        logging.info("{} - floor request is floor# {}".format(self.__class__.__name__, floor))
        self.dispatch(RequestCall(datetime.datetime.now(), floor, Direction.DOWN))


def main():
    b = RequestGenerator()
    scheduler = ElevatorScheduler(2, -2, 10)
    b.register(scheduler)
    for i in range(3):
        b.generateRequest()


if __name__ == "__main__":
    main()
