
from src.libs import rngs
from src.libs import rvgs
from src.utils import event, clock, ssq, msq

ON = 1
OFF = 0
START = 0.0  # initial time                                 */
STOP = 20000.0  # terminal (close the door) time            */
INFINITY = (100.0 * STOP)  # must be much larger than STOP  */
arrivalTemp = START

# ***************************** Monitoring area *************************
# ************************+** 3 SSQ 'parallele' *************************

MONITORING_SERVERS = 3
ssqs = []
monitoring_events = []
for i in range(MONITORING_SERVERS):

    # creates the ssqs for the monitoring areas
    q = ssq.SSQ()
    ssqs.append(q)

    # prepares empty events for the monitoring area:
    # all starting at START with the flag off
    a = event.Event()                       # arrival    */
    a.t = START
    a.x = OFF
    monitoring_events.append(a)

    d = event.Event()                       # departure  */
    d.t = START
    d.x = OFF
    monitoring_events.append(d)


# **************************** Analyze&Plan area ************************
# *****************+** 1 MSQ (con priorità abstract) ********************

ANALYZE_PLANNING_SERVERS = 3
msq = msq.MSQ()

analyze_plan_events = []
a = event.Event()                           # arrival    */
a.t = START
a.x = OFF
monitoring_events.append(a)

# (1, ANALYZE_PLANNING_SERVERS + 1) because first event is the arrival
for s in range(1, ANALYZE_PLANNING_SERVERS+1):

    d = event.Event()                       # departure  */
    d.t = START
    d.x = OFF
    monitoring_events.append(d)

    sum[s].service = 0.0
    sum[s].served = 0


# **************************** Execution area ************************
# TO-DO


# ****************************** System *******************************

# SYSTEM VALUES
departed_jobs = 0                       # used to count departed jobs          */
number = 0                              # number in the system                 */

# ****************************** Simulation *******************************
# initial seed
rngs.plantSeeds(123456789)

t = clock.Time()
t.current = START                       # set the clock                         */
t.completion = INFINITY                 # the first event can't be a completion */

events = monitoring_events+analyze_plan_events+[]

# QUA SERVIRANNO 3 streams diversi si ok

events[0].t = ssq.GetArrival()              # first event is of course an arrival   */
events[0].x = ON                        # schedule the first arrival            */

events[2].t = ssq.GetArrival()              # first event is of course an arrival   */
events[2].x = ON                        # schedule the first arrival            */

events[4].t = ssq.GetArrival()              # first event is of course an arrival   */
events[4].x = ON                        # schedule the first arrival            */

while (events[0].x != 0) or (events[2].x != 0) or (events[4].x != 0) or (number != 0):

    e = event.NextEvent(events)                     # next event        */
    t.next = events[e].t                            # next event time   */
    t.current = t.next                              # advance the clock */

    #area     += (t.next - t.current) * number      # update integral   */
    #if number > 0:                                 # update integrals  */
    #    area.node += (t.next - t.current) * number
    #    area.queue += (t.next - t.current) * (number - 1)
    #    area.service += (t.next - t.current)
    # EndIf

    # ----------------------------------------------
    # *           Monitoring Area Events
    # * --------------------------------------------
    # */
    if e == 0 or e == 2 or e == 4:              # process an arrival to server   Monitor  */
        number += 1                             # plus one job in the system              */
        ssqs[e/2].number += 1                   # plus one job in one of the ssq          */
        # prepares next arrival
        events[e].t = ssq.GetArrival()
        # checks if it's the last arrival
        if events[e].t > STOP:
            events[e].x = OFF

        if ssqs[e/2].number == 1:
            # prepares next departure
            events[e+1].t = t.current + ssq.GetService()
            events[e+1].x = ON

    if e == 1 or e == 3 or e == 5:              # process a departure from server Monitor */

        # signal arrival to AN&Plan area
        events[6].x = ON
        events[6].t = t.current

        departed_jobs += 1
        ssqs[(e-1)/2].number -= 1               # minus one job in one of the ssq         */
        # prepares next departure
        if ssqs[(e-1)/2].number > 0:
            events[e].t = t.current + ssq.GetService()
        else:
            events[e].x = OFF

    # ----------------------------------------------
    # *           Analyze&Plan Area Events
    # * --------------------------------------------
    # */
    # TO-DO

    if e == 6:                                  # process an arrival to server   An&Pla   */
        msq.number += 1                         # plus one job in one of the msq          */

        # TO-DO: generate departure from the area

    # TO-DO

    # ----------------------------------------------
    # *             Execute Area Events
    # * --------------------------------------------
    # */

    # TO-DO

    else:
        departed_jobs += 1                                     # from server s       */
        number -= 1
        s = e
        if number >= SERVERS:
            service = GetService()
            sum[s].service += service
            sum[s].served += 1
            events[s].t = t.current + service
        else:
            events[s].x = 0

# EndWhile

print("\nfor {0} jobs".format(index))
print("   average interarrival time = {0:6.2f}".format(t.last / index))
print("   average wait ............ = {0:6.2f}".format(area.node / index))
print("   average delay ........... = {0:6.2f}".format(area.queue / index))
print("   average service time .... = {0:6.2f}".format(area.service / index))
print("   average # in the node ... = {0:6.2f}".format(area.node / t.current))
print("   average # in the queue .. = {0:6.2f}".format(area.queue / t.current))
print("   utilization ............. = {0:6.2f}".format(area.service / t.current))

