from elevatorproblem.classes.PublisherObserver import Publisher
from elevatorproblem.classes.RequestCall import RequestCall
import random
import time

class RequestGenertor(Publisher):
    """
    generates button press requests from user
    """

    def __init__(self):
        super()

    def generateRequest(self):
        self.register("ravi_scheduler")
        timeout = random.randint(1,10)
        print(timeout, " -- is the timeout")
        time.sleep(timeout)
        self.dispatch("go to number 7")

def main():
    b = RequestGenertor()


if __name__ == "__main__":
    main()


