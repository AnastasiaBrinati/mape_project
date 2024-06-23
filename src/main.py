import sys
import subsystems.system as system
import subsystems.libs as libs
import numpy as np

RESPONSE_TIME_MONITOR = []
WAITING_TIME_MONITOR = []
RESPONSE_TIME_PLAN = []
WAITING_TIME_PLAN = []

ALPHA = 0.05


def confidence_interval(alpha, n, l) -> float:
    sigma = np.std(l)
    mu = np.mean(l)
    t = libs.rvms.idfStudent(n-1, 1-ALPHA/2)
    return (t*sigma)/np.sqrt(n-1)


def main(n):
    libs.rngs.plantSeeds(123456789)
    for i in range(n):
        try:
            res = system.simulation()
            r_m, w_m, r_p, w_p = res[0], res[1], res[2], res[3]

            r_m_avg = sum(r_m) / float(len(r_m))
            w_m_avg = sum(w_m) / float(len(w_m))
            r_p_avg = sum(r_p) / float(len(r_p))
            w_p_avg = sum(w_p) / float(len(w_p))

            RESPONSE_TIME_MONITOR.append(r_m_avg)
            WAITING_TIME_MONITOR.append(w_m_avg)
            RESPONSE_TIME_PLAN.append(r_p_avg)
            WAITING_TIME_PLAN.append(w_p_avg)

        except Exception as e:
            print(f"An error occurred during execution {i + 1}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <number_of_times>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        main(n)
        response_time_monitor_interval = confidence_interval(ALPHA, n, RESPONSE_TIME_MONITOR)
        waiting_time_monitor_interval = confidence_interval(ALPHA, n, WAITING_TIME_MONITOR)
        response_time_plan_interval = confidence_interval(ALPHA, n, RESPONSE_TIME_PLAN)
        waiting_time_plan_interval = confidence_interval(ALPHA, n, WAITING_TIME_PLAN)
        print("Monitor Centre")
        print(f"E[Ts] = {np.mean(RESPONSE_TIME_MONITOR)}", f"+/- {response_time_monitor_interval}")
        print(f"E[Tq] = {np.mean(WAITING_TIME_MONITOR)}", f"+/- {waiting_time_monitor_interval}")
        print("Plan Centre")
        print(f"E[Ts] = {np.mean(RESPONSE_TIME_PLAN)}", f"+/- {response_time_plan_interval}")
        print(f"E[Tq] = {np.mean(WAITING_TIME_PLAN)}", f"+/- {waiting_time_plan_interval}")
    except ValueError:
        print("The argument must be an integer.")
        sys.exit(1)
