# -------------------------------------------------------------------------
# * This program is a next-event simulation of a single-server FIFO service
# * node using Exponentially distributed interarrival times and Erlang
# * distributed service times (i.e., a M/E/1 queue).  The service node is
# * assumed to be initially idle, no arrivals are permitted after the
# * terminal time STOP, and the node is then purged by processing any
# * remaining jobs in the service node.
# *
# * Name            : ssq4.c  (Single Server Queue, version 4)
# * Author          : Steve Park & Dave Geyer
# * Language        : ANSI C
# * Latest Revision : 11-09-98
#  # Translated by   : Philip Steele
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
# * -------------------------------------------------------------------------
# */
from src.libs import rngs as rngs
from src.libs import rvgs as rvgs
from src.utils import event

ON = 1  # flag to signal active event            */
OFF = 0  # flag to signal inactive event          */
START = 0.0  # initial time                           */


class PlanningCentre:
    number = 0.0  # time integrated number in the node    */
    queue = 0.0  # time integrated number in the queue   */
    service = 0.0  # time integrated number in service     */
    departed = 0  # number served                         */

    def __init__(self) -> None:
        pass

    def get_events(self) -> list:

        planning_events = []
        # one arrival and one departure event for each ssq                                       */
        a = event.Event()  # arrival                                            */
        a.t = START
        a.x = OFF
        planning_events.append(a)

        d = event.Event()  # departure                                          */
        d.t = START
        d.x = OFF
        planning_events.append(d)

        return planning_events

    def get_arrival(self, stream) -> int:
        # ----------------------------------------------
        # * generate the next arrival time, with rate 1/2
        # * --------------------------------------------
        # */
        global arrivalTemp

        rngs.selectStream(stream)
        arrivalTemp += rvgs.Exponential(2.0)
        return arrivalTemp

    def get_service(self, stream) -> int:
        # ---------------------------------------------
        # * generate the next service time with rate 2/3
        # * --------------------------------------------
        # */
        rngs.selectStream(stream)
        return rvgs.Erlang(5, 0.3)
