
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
    e = event.Event()                       # arrival    */
    e.t = START
    e.x = OFF
    monitoring_events.append(e)

    d = event.Event()                       # departure  */
    d.t = START
    d.x = OFF
    monitoring_events.append(d)


# **************************** Analyze&Plan area ************************
# *****************+** 1 MSQ (con priorità abstract) ********************

ANALYZE_PLANNING_SERVERS = 3
msq = msq.MSQ()
# ANALYZE_PLANNING_SERVERS + 1 because first event is the arrivals

# TO-DO
analyze_plan_events = [event.Event() for i in range(ANALYZE_PLANNING_SERVERS+1)]

# da 1 in poi perchè il primo evento è l'arrivo e coinciderà con una departure dalla prima area
for s in range(1, ANALYZE_PLANNING_SERVERS+1):
    analyze_plan_events[s].t = START          # this value is arbitrary because */
    analyze_plan_events[s].x = OFF            # all servers are initially idle  */
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

events = {                              # dictionary of lists of events         */
    "monitor": monitoring_events,
    "analyze&plan": analyze_plan_events,
    "execute": []
}

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
    #       area     += (t.next - t.current) * number       # update integral   */
    t.current = t.next                              # advance the clock */

    #if number > 0:                          # update integrals    */
    #    area.node += (t.next - t.current) * number
    #    area.queue += (t.next - t.current) * (number - 1)
    #    area.service += (t.next - t.current)
    # EndIf

    if e == 0 or e == 2 or e == 4:              # process an arrival to server 1 Monitor */
        number += 1                             # plus one job in the system             */
        ssqs[int(e/2)].number += 1              # plus one job in on of the ssq          */
        # prepares next arrival
        events[e].t = GetArrival()
        # checks if it's the last arrival
        if events[e].t > STOP:
            events[e].x = 0

        if ssqs[e].number <= SERVERS:
            service  = GetService()
            s = FindOne(events)
            sum[s].service += service
            sum[s].served += 1
            events[s].t = t.current + service
            events[s].x = 1

    #EndIf
    else:                                        # process a departure */
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

# C output:
# Enter a positive integer seed (9 digits or less) >> 123456789

# for 10025 jobs
#    average interarrival time =   1.99
#    average wait ............ =   4.11
#    average delay ........... =   2.62
#    average service time .... =   1.50
#    average # in the node ... =   2.06
#    average # in the queue .. =   1.31
#    utilization ............. =   0.75
