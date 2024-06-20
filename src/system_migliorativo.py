
from src.libs import rngs
from src.utils import event, clock
from src.subsystems import msq, ssq

ON = 1                                          # flag to signal active event            */
OFF = 0                                         # flag to signal inactive event          */
START = 0.0                                     # initial time                           */
STOP = 20000.0                                  # terminal time (close the door)         */
INFINITY = (100.0 * STOP)                       # must be much larger than STOP          */

# ************************************** Monitoring area **********************************
# */
# -----------------------------------------------------------------------------------------
# *                  Initialize 3 SSQs for the Monitoring Area
# * ---------------------------------------------------------------------------------------
# */

# sub-systems initialization: empty SSQs                                                 */
MONITORING_SERVERS = 3
ssqs = [ssq.SSQ() for i in range(MONITORING_SERVERS)]

# events initialization: from START with flag OFF                                        */
monitoring_events = []
# one arrival and one departure event for each ssq                                       */
for i in range(MONITORING_SERVERS):

    a = event.Event()                   # arrival                                        */
    a.t = START
    a.x = OFF
    monitoring_events.append(a)

    d = event.Event()                   # departure                                      */
    d.t = START
    d.x = OFF
    monitoring_events.append(d)

# *********************************** Analyze&Plan area ***********************************
# */
# -----------------------------------------------------------------------------------------
# *                  Initialize 1 MSQs with abstract priority classes
# * ---------------------------------------------------------------------------------------
# */

# sub-systems initialization: empty MSQs                                                */
ANALYZE_PLANNING_SERVERS = 3
msq = msq

# events initialization: from START with flag OFF                                       */
# one arrival event for the msq                                                         */
analyze_plan_events = []
a = event.Event()                       # arrival                                       */
a.t = START
a.x = OFF
monitoring_events.append(a)

# one departure event for each server of the msq                                        */
for i in range(1, ANALYZE_PLANNING_SERVERS+1):

    d = event.Event()                   # departure                                     */
    d.t = START
    d.x = OFF
    monitoring_events.append(d)


# ***************************************** System ***************************************

# SYSTEM VALUES
number = 0                                     # number in the system                   */
departed_jobs = 0                              # departed jobs from the system          */

# **************************************** Simulation ************************************
# plant initial seed
rngs.plantSeeds(123456789)

t = clock.Time()
t.current = START                               # set the clock                         */
t.completion = INFINITY                         # the first event can't be a completion */

events = monitoring_events+analyze_plan_events+[]

# QUA SERVIRANNO 3 streams diversi si ok

events[0].t = ssq.GetArrival()                  # first event is of course an arrival   */
events[0].x = ON                                # schedule the first arrival            */

events[2].t = ssq.GetArrival()                  # first event is of course an arrival   */
events[2].x = ON                                # schedule the first arrival            */

events[4].t = ssq.GetArrival()                  # first event is of course an arrival   */
events[4].x = ON                                # schedule the first arrival            */

while (events[0].x != 0) or (events[2].x != 0) or (events[4].x != 0) or (number != 0):

    # get the next event in the timeline                                                */

    e = event.next_event(events)  # next event                            */
    t.next = events[e].t                        # next event time                       */
    t.current = t.next                          # advance the clock                     */

    #area     += (t.next - t.current) * number      # update integral   */
    #if number > 0:                                 # update integrals  */
    #    area.node += (t.next - t.current) * number
    #    area.queue += (t.next - t.current) * (number - 1)
    #    area.service += (t.next - t.current)
    # EndIf

    # ------------------------------------------------------------------------------------
    # *                          Monitoring Area Events
    # * ----------------------------------------------------------------------------------
    # */
    if e == 0 or e == 2 or e == 4:              # process an arrival in the Monitoring  */
        number += 1                             # plus one job in the system            */
        ssqs[e/2].number += 1                   # plus one job in one of the ssq        */

        events[e].t = ssq.getArrival()          # prepares next arrival                 */
        if events[e].t > STOP:                  # if the arrival is out of time:        */
            events[e].x = OFF                   # turn off the arrivals                 */

        if ssqs[e/2].number == 1:               # prepares next departure               */
            events[e+1].t = t.current + ssq.getService()
            events[e+1].x = ON

    if e == 1 or e == 3 or e == 5:              # process a departure from the Monitor  */
        ssqs[(e-1)/2].departed += 1             # plus one job departed from of the ssq */
        ssqs[(e-1)/2].number -= 1               # minus one job in one of the ssq       */

        if ssqs[(e-1)/2].number > 0:            # prepares next departure               */
            events[e].t = t.current + ssq.getService()
        else:
            events[e].x = OFF

        events[6].x = ON                        # signal an arrival in the An&Plan area */
        events[6].t = t.current

    # ------------------------------------------------------------------------------------
    # *                          Analyze&Plan Area Events
    # * ----------------------------------------------------------------------------------
    # */

    if e == 6:                                  # process an arrival to server   An&Pla */
        msq.number += 1                         # plus one job in the msq               */

        if msq.number <= msq.SERVERS:           # prepares next departure               */
            s = msq.find_one(analyze_plan_events)
            events[e+s].t = t.current + msq.getService()
            events[e+s].x = ON

    if e == 7 and e == 8 and e == 9:
        msq.departed += 1                       # plus one departure from the An Area   */
        msq.number -= 1                         # minus one job in the msq              */

        if msq.number >= msq.SERVERS:           # prepares next departure               */
            events[e].t = t.current + msq.getService()
        else:
            events[e].x = OFF

        events[10].x = ON                        # signal an arrival in the Exec area   */
        events[10].t = t.current
    # * ----------------------------------------------------------------------------------
    # *                             Execute Area Events
    # * ----------------------------------------------------------------------------------
    # */

    # TO-DO

    else:
        departed_jobs += 1                                     # from server s         */
        number -= 1
        s = e
        if number >= SERVERS:
            service = GetService()
            sum[s].service += service
            sum[s].served += 1
            events[s].t = t.current + service
        else:
            events[s].x = 0
