import math


class Event:
    t = None  # next event time         */
    x = None  # event status, 0 or 1    */


def NextEvent(events):

    # return the next event index */

    i = 0
    imminent = math.inf
    while i < len(events):
        if events[i].x == 1 and events[i].t < imminent:    # element in the event list that is ON */
            imminent = events[i].t                         # and the most imminent                */

    # in case of a draw return the first most imminent
    return i
