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


def get_arrival():
    # ----------------------------------------------
    # * generate the next arrival time, with rate 1/2
    # * --------------------------------------------
    # */
    global arrivalTemp

    rngs.selectStream(0)
    arrivalTemp += rvgs.Exponential(2.0)
    return arrivalTemp


def get_service():
    # ---------------------------------------------
    # * generate the next service time with rate 2/3
    # * --------------------------------------------
    # */
    rngs.selectStream(1)
    return rvgs.Erlang(5, 0.3)


class SSQ:
    number = 0.0    # time integrated number in the node    */
    queue = 0.0     # time integrated number in the queue   */
    service = 0.0   # time integrated number in service     */
    departed = 0    # number served                         */

