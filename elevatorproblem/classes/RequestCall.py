import datetime


class RequestCall(object):
    """
    Lift calling request
    """

    def __init__(self, time, floor, direction):
        self.time = time
        self.floor = floor
        self.direction = direction

    def __str__(self):
        s = "At time : " + self.time.strftime(
            "%m/%d/%Y, %H:%M:%S") + ". From Floor : " + str(self.floor) + ". Direction :" + str(self.direction)
        print("here s is : ", s)
        return s
