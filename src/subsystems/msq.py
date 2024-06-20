from src.libs import rngs as rngs
from src.libs import rvgs as rvgs


def get_arrival():
    # ---------------------------------------------
    # * generate the next arrival time, with rate 1/2
    # * ---------------------------------------------
    # */
    global arrivalTemp

    rngs.selectStream(0)
    arrivalTemp += rvgs.Exponential(2.0)
    return arrivalTemp


def get_service():
    # --------------------------------------------
    # * generate the next service time with rate 1/6
    # * --------------------------------------------
    # */
    rngs.selectStream(1)
    return rvgs.Uniform(2.0, 10.0)


def find_one(events):
    # -------------------------------------------------------
    # * return the index of the first available server
    # * -----------------------------------------------------
    # */
    for i in range(1, len(events)):
        if events[i].x == 1:
            return i

    return -1


class MSQ:
    def __init__(self, num_servers):
        self.SERVERS = num_servers

    number = 0             # time integrated number in the node   */
    queue = 0.0            # time integrated number in the queue  */
    service = 0.0          # service times                        */
    departed = 0           # number served                        */


########################### Main Program ##################################

SERVERS = 10
t = time()
events = [event() for i in range(SERVERS + 1)]
number = 0             # number in the node                 */
index = 0              # used to count processed jobs       */
area = 0.0             # time integrated number in the node */
sum = [accumSum() for i in range(SERVERS + 1)]

rngs.plantSeeds(0)

t.current = START
events[0].t = GetArrival()
events[0].x = 1
for s in range(1, SERVERS+1):
    events[s].t = START          # this value is arbitrary because */
    events[s].x = 0              # all servers are initially idle  */
    sum[s].service = 0.0
    sum[s].served = 0


while (events[0].x != 0) or (number != 0):
    e         = Event.next_event(events)  # next event index   */
    t.next    = events[e].t                        # next event time    */
    area     += (t.next - t.current) * number      # update integral    */
    t.current = t.next                             # advance the clock  */

    if e == 0:                                     # process an arrival */
        number += 1
        events[0].t = GetArrival()
        if events[0].t > STOP:
            events[0].x = 0
        #EndIf
        if number <= SERVERS:
            service  = GetService()
            s = MSQ.FindOne(events)
            sum[s].service += service
            sum[s].served += 1
            events[s].t = t.current + service
            events[s].x = 1
        #EndIf
    #EndIf
    else:                                          # process a departure */
        index += 1                                     # from server s       */
        number -= 1
        s = e
        if number >= SERVERS:
            service = get_service()
            sum[s].service += service
            sum[s].served += 1
            events[s].t = t.current + service
        else:
            events[s].x = 0
    #EndElse
#EndWhile
