from typing import Tuple, Any

from src.libs import rngs as rngs
from src.libs import rvgs as rvgs
from src.utils import event

ON = 1  # flag to signal active event            */
OFF = 0  # flag to signal inactive event          */
START = 0.0  # initial time                           */

# routing probabilities
FATAL = 0.12
ERROR = 0.16
WARNING = 1 - FATAL - ERROR


# rates
LAMBDA = 1.446761181


class MonitoringCentre:
    number = []       # time integrated number in the node    */
    queue = []        # time integrated number in the queues  */
    service = 0.0     # time integrated number in service     */
    departed = []     # number served                         */
    servers = 0       # number of servers                     */

    def __init__(self, servers) -> None:
        self.servers = servers
        self.number = [0 for i in range(servers)]
        self.queue = [0 for i in range(servers)]
        self.departed = [0 for i in range(servers)]
        pass

    def get_events(self) -> list:
        monitoring_events = []
        # one arrival event for each ssq                                        */
        for i in range(self.servers):
            a = event.Event()  # arrival                                        */
            a.t = START
            a.x = OFF
            monitoring_events.append(a)

        # one departure event for each ssq                                      */
        for i in range(self.servers):
            d = event.Event()  # departure                                      */
            d.t = START
            d.x = OFF
            monitoring_events.append(d)

        return monitoring_events

    def route_arrival(self) -> int:
        r = rngs.random()
        if r == FATAL:
            return 0
        elif r == ERROR:
            return 1
        else:
            return 2

    def get_arrival(self, stream) -> tuple[Any, int]:
        # ----------------------------------------------
        # * generate the next arrival time, with rate 1/2
        # * --------------------------------------------
        # */
        global arrivalTemp

        rngs.selectStream(stream)
        arrivalTemp += rvgs.Exponential(LAMBDA)

        centre = self.route_arrival()
        return arrivalTemp, centre

    def get_service(self, stream_index) -> int:
        # ---------------------------------------------
        # * generate the next service time with rate 2/3
        # * --------------------------------------------
        # */
        rngs.selectStream(stream_index)
        return rvgs.Erlang(5, 0.3)
