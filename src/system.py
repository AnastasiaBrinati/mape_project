
from src.libs import rngs
from src.subsystems.monitoring import MonitoringCentre
from src.subsystems.planning import PlanningCentre
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
# *                        Initialize 3 SSQs for the Monitoring Area
# * ---------------------------------------------------------------------------------------
# */

# sub-systems initialization: empty SSQs                                                 */
MONITORING_SERVERS = 3
monitoringCentre = MonitoringCentre(MONITORING_SERVERS)

# events initialization: from START with flag OFF                                        */
monitoring_events = monitoringCentre.get_events()

# *********************************** Analyze&Plan area ***********************************
# */
# -----------------------------------------------------------------------------------------
# *                                  Initialize 1 SSQ
# * ---------------------------------------------------------------------------------------
# */

# sub-systems initialization: empty SSQ                                                  */
planningCentre = PlanningCentre()

# events initialization: from START with flag OFF                                        */
planning_events = planningCentre.get_events()


# ***************************************** System ****************************************

# SYSTEM VALUES
number = 0                                     # number in the system                    */
departed_jobs = 0                              # departed jobs from the system           */

# **************************************** Simulation *************************************
# plant initial seed
rngs.plantSeeds(123456789)
ARRIVALS_STREAM = 0
t = clock.Time()
t.current = START                               # set the clock                          */
t.completion = INFINITY                         # the first event can't be a completion  */

events = monitoring_events+planning_events
arrival, e = monitoringCentre.get_arrival(ARRIVALS_STREAM)
events[e].t = arrival                           # first event is of course an arrival    */
events[e].x = ON                                # schedule first arrival                 */

while (events[0].x != 0) or (events[1].x != 0) or (events[2].x != 0) or (number != 0):

    # get the next event in the timeline                                                 */
    e = event.next_event(events)                # next event                             */
    t.next = events[e].t                        # next event time                        */
    t.current = t.next                          # advance the clock                      */

    #area     += (t.next - t.current) * number      # update integral   */
    #if number > 0:                                 # update integrals  */
    #    area.node += (t.next - t.current) * number
    #    area.queue += (t.next - t.current) * (number - 1)
    #    area.service += (t.next - t.current)
    # EndIf

    # -------------------------------------------------------------------------------------
    # *                          Monitoring Area Events
    # * -----------------------------------------------------------------------------------
    # */
    if e in range(0, MONITORING_SERVERS-1):     # process an arrival in the MonitoringC  */
        number += 1                             # plus one job in the system             */
        monitoringCentre.number[e] += 1         # plus one job in one of the ssqs        */
        monitoringCentre.queue[e] += 1          # plus one job in one of the queues      */

        arrival, w = monitoringCentre.get_arrival(ARRIVALS_STREAM)
        events[w].t = arrival                   # generate next arrival                  */
        events[w].x = ON                        # schedule the arrival                   */

        if events[w].t > STOP:                  # if the arrival is out of time:         */
            events[w].x = OFF                   # turn off the arrivals                  */

        if monitoringCentre.number[e] == 1:     # prepares next departure                */
            events[e+MONITORING_SERVERS].t = t.current + monitoringCentre.get_service(e+MONITORING_SERVERS)
            events[e+MONITORING_SERVERS].x = ON

    if e in range(MONITORING_SERVERS, MONITORING_SERVERS*2-1):     # process a departure from the Monitor   */
        monitoringCentre.departed[e-MONITORING_SERVERS] += 1       # plus one job departed from of the ssq  */
        monitoringCentre.number[e-MONITORING_SERVERS] -= 1         # minus one job in one of the ssq        */

        if monitoringCentre.number[e-MONITORING_SERVERS] > 0:      # prepares next departure                */
            events[e].t = t.current + monitoringCentre.get_service(e)
        else:
            events[e].x = OFF

        events[MONITORING_SERVERS*2].x = ON                        # signal an arrival in the An&Plan area  */
        events[MONITORING_SERVERS*2].t = t.current

    # -------------------------------------------------------------------------------------
    # *                          Analyze&Plan Area Events
    # * -----------------------------------------------------------------------------------
    # */

    if e == MONITORING_SERVERS*2:               # process an arrival to server   An&Pla  */
        planningCentre.number += 1              # plus one job in the area               */
        planningCentre.queue += 1               # plus one job in the queue              */
        arrival, w = planningCentre.get_arrival(e)
        events[w].t = arrival                   # generate next arrival                  */
        events[w].x = ON                        # schedule the arrival                   */

        if events[w].t > STOP:                  # if the arrival is out of time:         */
            events[w].x = OFF                   # turn off the arrivals                  */

        if planningCentre.number == 1:       # prepares next departure                */
            events[e+1].t = t.current + monitoringCentre.get_service(e+1)
            events[e+1].x = ON

    if e == MONITORING_SERVERS*2+1:
        planningCentre.number -= 1                         # minus one job in the area              */
        planningCentre.departed += 1                       # plus one departure from the PArea      */
        number -= 1                                        # minus one job in the system            */
        departed_jobs += 1                                 # plus one departed job from the system  */

        if planningCentre.number > 0:                      # prepares next departure                */
            events[e].t = t.current + planningCentre.get_service(e)
        else:
            events[e].x = OFF
