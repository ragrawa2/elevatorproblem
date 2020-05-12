===============
ElevatorProblem
===============


.. image:: https://img.shields.io/pypi/v/elevatorproblem.svg
        :target: https://pypi.python.org/pypi/elevatorproblem

.. image:: https://img.shields.io/travis/ragrawa2/elevatorproblem.svg
        :target: https://travis-ci.com/ragrawa2/elevatorproblem

.. image:: https://readthedocs.org/projects/elevatorproblem/badge/?version=latest
        :target: https://elevatorproblem.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Design a Lift simulator system with some properties and constraints.

Multiple Elevator Scheduler and Simulator

The idea is to build a multithreaded system where different independent systems interact with each other through messaging system. I explored publisher subscriber systems and also explored pykka (python akka model) for this project.

These 2 methods would help decoupling logic and hence help in maintaining and debugging in case of issues.


Problem Statement

Design a Lift simulator system with the following properties and constraints:

There is one building with multiple lifts ( number of lifts = K).
The building has floors ranging from -N < 0 < M where -N is the lowest basement and M is the top floor.
All lifts stop at ground floor( floor number= 0).

Each lift works on the following algorithm:
A lift continues to move in its current direction as long as it has stops in that direction.
If no more stops in the current direction then it moves in the opposite direction if it has stops in the opposite direction.
If no more stops in any direction then it stops at the current floor and waits for next request.

A user standing in the lift bay on any floor can send request to go up or go down. (input = UP or DOWN)
A user inside a lift can send a request to go to any allowed floor.  (input = allowed floor number)

A constraint can be applied by the building admin on each lift - any one of the following constraints would apply :
Allowed floors = range ( x,y) where  x<y and lies within the range -N to M.
Allowed floor = Even floors only.
Allowed floor = Odd floor only.

The overall lift system should be efficient i.e. not all lifts should try and service all requests.

This will involve multithreaded consumers and producers using messaging queues to contruct a running system.
complexity is also involved in Writing proper test cases for this system.
Some thought needs to be put on Design Patterns. Will producer consumer work well or actor model or some messaging system.
