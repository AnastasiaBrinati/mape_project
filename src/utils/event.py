import math


class Event:
    t = None  # next event time         */
    x = None  # event status, 0 or 1    */


def NextEvent(events):

    # return the next event */

    i = 0
    event = None
    imminent = math.inf
    while i < len(events):
        e = events[i]
        if e.x == 1 and e.t < imminent:     # element in the event list that is ON */
            imminent = e.t                  # and the most imminent                */
            event = e

    return event
