* ElevatorProblem version:
* Python version:
* Operating System:

### Description

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


Evaluation on the basis of:

    Problem solution design - the way the solution is approached/ design patterns applied/prioritization of the core vs
     peripheral parts of the problem given the time constraints etc.
    Testability.

### What I Did

```
Paste the command(s) you ran and the output.
If there was a crash, please include the traceback here.
```
