
from src.libs import rngs
from src.libs import rvgs
from src.utils import event, clock, ssq, msq

ON = 1                              # flag to signal active event                */
OFF = 0                             # flag to signal inactive event              */
START = 0.0                         # initial time                               */
STOP = 20000.0                      # terminal time (close the door)             */
INFINITY = (100.0 * STOP)           # must be much larger than STOP              */

# ********************************** Monitoring area ******************************
# */
# ---------------------------------------------------------------------------------
# *                  Initialize 3 SSQs for the Monitoring Area
# * -------------------------------------------------------------------------------
# */

# sub-systems initialization: empty SSQs                                        */
MONITORING_SERVERS = 3
ssqs = [ssq.SSQ() for i in range(MONITORING_SERVERS)]

# events initialization: from START with flag OFF                               */
monitoring_events = []
# one arrival and one departure event for each ssq                              */
for i in range(MONITORING_SERVERS):

    a = event.Event()                 # arrival                                 */
    a.t = START
    a.x = OFF
    monitoring_events.append(a)

    d = event.Event()                 # departure                               */
    d.t = START
    d.x = OFF
    monitoring_events.append(d)

# ******************************* Analyze&Plan area ******************************
# */
# --------------------------------------------------------------------------------
# *                  Initialize 1 MSQs with abstract priority classes
# * ------------------------------------------------------------------------------
# */

# sub-systems initialization: empty MSQs                                        */
ANALYZE_PLANNING_SERVERS = 3
msq = msq.MSQ()

# events initialization: from START with flag OFF                               */
# one arrival event for the msq                                                 */
analyze_plan_events = []
a = event.Event()                     # arrival                                 */
a.t = START
a.x = OFF
monitoring_events.append(a)

# one departure event for each server of the msq                                */
for i in range(1, ANALYZE_PLANNING_SERVERS+1):

    d = event.Event()                # departure                                */
    d.t = START
    d.x = OFF
    monitoring_events.append(d)


# ******************************** Execution area ******************************
# */
# ------------------------------------------------------------------------------
# *                          Initialize 1 Infinite Server
# * ----------------------------------------------------------------------------
# */

# TO-DO


# ************************************ System **********************************

# SYSTEM VALUES
number = 0                              # number in the system                */
departed_jobs = 0                       # departed jobs from the system       */

# ********************************* Simulation *********************************
# plant initial seed
rngs.plantSeeds(123456789)

t = clock.Time()
t.current = START                       # set the clock                         */
t.completion = INFINITY                 # the first event can't be a completion */

events = monitoring_events+analyze_plan_events+[]

# QUA SERVIRANNO 3 streams diversi si ok

events[0].t = ssq.GetArrival()          # first event is of course an arrival   */
events[0].x = ON                        # schedule the first arrival            */

events[2].t = ssq.GetArrival()          # first event is of course an arrival   */
events[2].x = ON                        # schedule the first arrival            */

events[4].t = ssq.GetArrival()          # first event is of course an arrival   */
events[4].x = ON                        # schedule the first arrival            */

while (events[0].x != 0) or (events[2].x != 0) or (events[4].x != 0) or (number != 0):

    # get the next event in the timeline

    e = event.NextEvent(events)                     # next event        */
    t.next = events[e].t                            # next event time   */
    t.current = t.next                              # advance the clock */

    #area     += (t.next - t.current) * number      # update integral   */
    #if number > 0:                                 # update integrals  */
    #    area.node += (t.next - t.current) * number
    #    area.queue += (t.next - t.current) * (number - 1)
    #    area.service += (t.next - t.current)
    # EndIf

    # -----------------------------------------------------------------------------
    # *                          Monitoring Area Events
    # * ---------------------------------------------------------------------------
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

        departed_jobs += 1
        ssqs[(e-1)/2].number -= 1               # minus one job in one of the ssq         */

        if ssqs[(e-1)/2].number > 0:            # prepares next departure                 */
            events[e].t = t.current + ssq.GetService()
        else:
            events[e].x = OFF

        # signal arrival to AN&Plan area                                                  */
        events[6].x = ON
        events[6].t = t.current

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

