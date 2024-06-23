from .libs import rvms, rngs, rvgs
from .util import event

ON = 1                          # flag to signal active event          */
OFF = 0                         # flag to signal inactive event        */
START = 0.0                     # initial time                         */

# service times distribution:                                          */
#               X =  Lognormal(a, b)   x > 0                           */
# The mean and variance are                                            */
#               μ = mean = exp(a + 0.5*b*b)  = 0.55                    */
#               σ^2 = variance = (exp(b*b) - 1)*exp(2*a + b*b) = 0.45  */
# Follows that                                                         */
#               a = log(μ) - b^2/2                                     */
#               b = sqrt ( log( [σ^2 / log(μ)^2] + 1 ) )               */
a = -0.843414
b = 0.714951

# TRUNCATION                                                           */
# right tail cut at x = 3 seconds                                      */
#                  β = 1-Pr(X ≤ x) = 1-F(x)                            */
# determine left-tail and right-tail truncation probabilities α and β  */
# in our case only the right truncation is needed                      */
#   alpha = rvms.cdfLognormal(a, b, x=0.0)                     # α = 0 */
beta = 1.0 - rvms.cdfLognormal(a, b, x=3.0)                        # β */
# constrained inversion                                                */
u = rvgs.Uniform(0.0, 1.0 - beta)


class PlanningCentre:
    number = 0.0                # time integrated number in the node    */
    queue = []                  # time integrated number in the queue   */
    service = 0.0               # time integrated number in service     */
    departed = 0                # number served                         */

    def __init__(self) -> None:
        pass

    def get_events(self) -> list:

        planning_events = []
        # one arrival and one departure event for each ssq               */
        a = event.Event()  # arrival                                     */
        a.t = START
        a.x = OFF
        planning_events.append(a)

        d = event.Event()  # departure                                   */
        d.t = START
        d.x = OFF
        planning_events.append(d)

        return planning_events

    # ********************************************************************/
    # def get_arrival(self, stream) -> int:
    #    # ----------------------------------------------                */
    #    # * generate the next arrival time
    #    # * --------------------------------------------                */
    #    # */
    #    global arrivalTemp                                              */

    #    rngs.selectStream(stream)                                       */
    #    arrivalTemp += rvgs.Exponential(2.0)                            */
    #    return arrivalTemp                                              */
    # ********************************************************************/

    def get_service(self, stream) -> int:
        # ---------------------------------------------
        # * generate the next service time
        # * --------------------------------------------
        # */
        rngs.selectStream(stream)
        return rvms.idfLognormal(a, b, u)
