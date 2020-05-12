from elevatorproblem.PubSubApproach.PublisherObserver import Subscriber, Publisher
from elevatorproblem.PubSubApproach.RequestCall import RequestCall
import random
import datetime
import time
import threading
import numpy as np
from enum import Enum
import logging


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
        # assumed to be sorted validFloors
        self.validFloors = validFloors
        self.upStops = set()
        self.downStops = set()
        self.lock = lock

    def get_position(self):
        return self.location, self.direction

    def set_direction(self, direction):
        self.direction = direction

    def can_go(self, floor):
        return floor in self.validFloors

    def addStop(self, req):
        if req.direction == Direction.UP:
            self.upStops.add(req.floor)
        else:
            self.downStops.add(req.floor)

    def moveElevator(self, floor, directionOfRequests):
        """
        :param floor:
        :param directionOfRequests:
        :return:
        """
        self.location = floor
        self.set_direction(directionOfRequests)
        logging.info("Elevator ", self.num, " is moving to floor : ", floor, " to process all direction=",
              directionOfRequests)
        time.sleep(2)

    def run(self):
        while True:
            if self.direction == Direction.UP:
                self.processUPReq()
            elif self.direction == Direction.DOWN:
                self.processDownReq()
            else:
                self.processNoneReq()

            logging.info("Elevator ", self.num, " current position : ", self.get_position())
            time.sleep(4)
            # if len(self.upStops) != 0 or len(self.downStops) != 0:
            #     req = self.

    def processUPReq(self):
        logging.info("UP UP Elevator ", self.num, " current position : ", self.get_position())
        logging.info("UP UP Elevator ", self.num, " current position : ", self.get_position())
        logging.info(self.upStops)
        floorsReachableWithDirection = [x for x in self.upStops if x >= self.location]
        if len(floorsReachableWithDirection) == 0:
            self.direction = Direction.NONE
        else:
            target = min(floorsReachableWithDirection)
            if target == self.location:
                with self.lock:
                    self.upStops.remove(target)
                    logging.info("removing ", target, " from Elevator ", self.num)
                    newStop = self.addUserFloorReqFromInsideElevator(self.validFloors, self.location, Direction.UP)
                    if newStop is not None:
                        self.upStops.add(newStop)
                    logging.info("within our lock state")
                    logging.info("Sleeping for 5")
                    time.sleep(5)
            else:
                self.moveElevator(target, Direction.UP)

    def processDownReq(self):
        floorsReachableWithDirection = [x for x in self.downStops if x <= self.location]
        if len(floorsReachableWithDirection) == 0:
            self.direction = Direction.NONE
        else:
            target = max(floorsReachableWithDirection)

            if target == self.location:
                with self.lock:
                    self.downStops.remove(target)
                    logging.info("removing ", target, " from Elevator ", self.num)
                    newStop = self.addUserFloorReqFromInsideElevator(self.validFloors, self.location, Direction.DOWN)
                    if newStop is not None:
                        self.downStops.add(newStop)

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
        self.numberOfRequestForHashing = self.numberOfRequestForHashing + 1
        logging.info('{} got message "{}"'.format(self.name, str(message)))
        index = self.numberOfRequestForHashing % self.numElevators
        if message.direction == Direction.UP:
            with self.locks[index]:
                self.elevators[index].upStops.add(message.floor)
        else:
            with self.locks[index]:
                self.elevators[index].downStops.add(message.floor)

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

    def generateRequest(self):
        # self.register("ravi_scheduler")
        floor = random.randint(-2, 10)
        logging.info(floor, " -- is the floor, sleep 1 sec")

        # time.sleep(2)
        self.dispatch(RequestCall(datetime.datetime.now(), floor, Direction.DOWN))


def main():
    b = RequestGenerator()
    scheduler = ElevatorScheduler(5, -2, 10)
    b.register(scheduler)
    for i in range(20):
        b.generateRequest()


if __name__ == "__main__":
    main()
