from .libs import rngs
from .monitoring import MonitoringCentre
from .planning import PlanningCentre

from .util import event, clock

ON = 1                                                                          # flag to signal active event         */
OFF = 0                                                                         # flag to signal inactive event       */
START = 0.0                                                                     # initial time                        */
STOP = 2000.0                                                                   # terminal time (close the door)      */
INFINITY = (100.0 * STOP)                                                       # must be much larger than STOP       */

MONITORING_SERVERS = 3
ARRIVALS_STREAM = 0


def simulation() -> list:
    # ***************************************************** Monitoring area ********************************************
    # */
    # ------------------------------------------------------------------------------------------------------------------
    # *                                     Initialize 3 SSQs for the Monitoring Area
    # * ----------------------------------------------------------------------------------------------------------------
    # */

    waiting_times_monitor = []
    response_times_monitor = []

    waiting_times_plan = []
    response_times_plan = []

    # sub-systems initialization: empty SSQs                                                                          */
    monitoring_centre = MonitoringCentre(MONITORING_SERVERS)

    # events initialization: from START with flag OFF                                                                 */
    monitoring_events = monitoring_centre.get_events()

    # ***************************************************** Analyze&Plan area ******************************************
    # */
    # ------------------------------------------------------------------------------------------------------------------
    # *                                                  Initialize 1 SSQ
    # * ----------------------------------------------------------------------------------------------------------------
    # */

    # sub-systems initialization: empty SSQ                                                                           */
    planning_centre = PlanningCentre()

    # events initialization: from START with flag OFF                                                                 */
    planning_events = planning_centre.get_events()

    # ****************************************************** System ****************************************************
    # SYSTEM VALUES
    number = 0                                                                  # number in the system                */
    departed_jobs = 0                                                           # departed jobs from the system       */

    # **************************************************** Simulation **************************************************
    # monitoring area services will have the streams in range (MONITORING_SERVERS, MONITORING_SERVERS*2-1)
    # planning area service will have the stream MONITORING_SERVERS*2+1

    # SYSTEM CLOCK
    t = clock.Time()
    t.current = START                                                            # set the clock                      */
    t.completion = INFINITY                                                      # first event can't be a completion  */

    events = monitoring_events+planning_events
    arrival, e = monitoring_centre.get_arrival(ARRIVALS_STREAM)
    events[e].t = arrival                                                        # first event is of course an arrival*/
    events[e].x = ON                                                             # schedule first arrival             */

    while (events[0].x == ON) or (events[1].x == ON) or (events[2].x == ON) or (number != 0):

        # get the next event in the timeline                                                                          */
        e = event.next_event(events)                                             # next event                         */
        t.next = events[e].t                                                     # next event time                    */
        t.current = t.next                                                       # advance the clock                  */

        # --------------------------------------------------------------------------------------------------------------
        # *                                         Monitoring Area Events
        # * ------------------------------------------------------------------------------------------------------------
        # */
        if e in range(0, MONITORING_SERVERS):                                    # process an arrival at MonitoringC  */

            number += 1                                                          # plus one job in the system         */
            monitoring_centre.number[e] += 1                                     # plus one job in one of the ssqs    */
            events[e].x = OFF                                                    # turn off arrivals at this centre   */

            arrived = events[e].t
            arrival, w = monitoring_centre.get_arrival(ARRIVALS_STREAM)          # generate next arrival              */
            events[w].t = arrival                                                # prepare event arrival              */
            events[w].x = ON                                                     # schedule the arrival               */

            if events[w].t > STOP:                                               # if the arrival is out of time:     */
                events[w].x = OFF                                                # turn off the arrivals              */

            if monitoring_centre.number[e] == 1:                                 # prepares next departure            */
                served = t.current + monitoring_centre.get_service(e+MONITORING_SERVERS)
                events[e+MONITORING_SERVERS].t = served
                events[e+MONITORING_SERVERS].x = ON
                waiting_times_monitor.append(0.0)                                # update integrals                   */
                response_times_monitor.append(served - arrived)                  # update integrals                   */
            else:
                # save the timestamp of the arrival as token for the job                                              */
                monitoring_centre.queue[e].append(t.current)                     # plus one job in one of the queues  */

        if e in range(MONITORING_SERVERS, MONITORING_SERVERS*2):                 # process a departure from MonitorC  */
            monitoring_centre.departed[e-MONITORING_SERVERS] += 1                # plus one j departed from the ssq   */
            monitoring_centre.number[e-MONITORING_SERVERS] -= 1                  # minus one job in one of the ssq    */

            if len(monitoring_centre.queue[e-MONITORING_SERVERS]) > 0:           # prepares next departure            */
                arrived = monitoring_centre.queue[e-MONITORING_SERVERS].pop(0)
                waiting_times_monitor.append(t.current - arrived)                # update integrals                   */
                served = t.current + monitoring_centre.get_service(e)
                events[e].t = served                                             # prepares next departure            */
                response_times_monitor.append(served - arrived)                  # update integrals                   */
            else:
                events[e].x = OFF

            events[MONITORING_SERVERS*2].x = ON                                  # signal an arrival in the An&PlanC  */
            events[MONITORING_SERVERS*2].t = t.current

        # --------------------------------------------------------------------------------------------------------------
        # *                                          Analyze&Plan Area Events
        # * ------------------------------------------------------------------------------------------------------------
        # */

        if e == MONITORING_SERVERS*2:                                            # process an arrival to An&PlaC      */
            planning_centre.number += 1                                          # plus one job in the area           */
            events[e].x = OFF                                                    # turn off the arrival               */
            if planning_centre.number == 1:                                      # prepares next departure            */
                s = planning_centre.get_service(e+1)
                served = t.current + s
                events[e+1].t = served
                events[e+1].x = ON
                waiting_times_plan.append(0.0)                                   # update integrals                   */
                response_times_plan.append(served - t.current)                   # update integrals                   */
            else:
                planning_centre.queue.append(t.current)                          # plus one job in the queue          */

        if e == MONITORING_SERVERS*2+1:
            planning_centre.number -= 1                                          # minus one job in the area          */
            planning_centre.departed += 1                                        # plus one departure from the PArea  */
            number -= 1                                                          # minus one job in the system        */
            departed_jobs += 1                                                   # plus one departed job from system  */

            if len(planning_centre.queue) > 0:                                   # prepares next departure            */
                arrived = planning_centre.queue.pop(0)
                waiting_times_plan.append(t.current - arrived)                   # update integrals                   */
                served = t.current + planning_centre.get_service(e)
                events[e].t = served
                response_times_plan.append(served - arrived)                     # update integrals                   */

            else:
                events[e].x = OFF

    return [response_times_monitor, waiting_times_monitor, response_times_plan, waiting_times_plan]
