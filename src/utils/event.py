import math

class Event:
    t = None                        # next event time               */
    x = None                        # event status, 0 or 1          */

def NextEvent(events):
    # ---------------------------------------
    # * return the index of the next event type
    # * ---------------------------------------
    # */

    i = 0
    imminent = math.inf
    while i < len(events):
        # filter active events and check for the most imminent      */
        if events[i].x == 1 and events[i].t < imminent:
            imminent = events[i].t

    # in case of a draw return the first most imminent              */
    return i
