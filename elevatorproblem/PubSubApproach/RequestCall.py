import datetime


class RequestCall(object):
    """
    Lift calling request
    """

    def __init__(self, time, from_floor, direction, to_floor=None):
        self.time_created = time
        self.from_floor = from_floor
        self.direction = direction
        self.time_processed = None
        self.to_floor = to_floor

    def __str__(self):
        s = "Created time : " + self.time_created.strftime(
            "%m/%d/%Y, %H:%M:%S") + ". From Floor : " + str(self.from_floor) + ". Direction :" + str(self.direction)
        print("RequestCall is : ", s)
        return s
