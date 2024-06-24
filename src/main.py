import sys
import subsystems.system as system
import subsystems.libs as libs
import numpy as np

RESPONSE_TIME_MONITOR = []
WAITING_TIME_MONITOR = []
RESPONSE_TIME_PLAN = []
WAITING_TIME_PLAN = []

RHO_MONITOR_1 = []
RHO_MONITOR_2 = []
RHO_MONITOR_3 = []
RHO_PLAN = []

ALPHA = 0.05

RESPONSE_TIME_MONITOR_CUMULATIVE_AVG = [[] for i in range(50)]


def confidence_interval(alpha, n, l) -> float:
    sigma = np.std(l)
    mu = np.mean(l)
    if n > 1:
        t = libs.rvms.idfStudent(n - 1, 1 - ALPHA / 2)
    else:
        return 0.0
    return (t * sigma) / np.sqrt(n - 1)


def main(n, STOP):
    libs.rngs.plantSeeds(123456789)
    for i in range(n):
        try:
            res = system.simulation(STOP)
            response_times_monitor, waiting_times_monitor, response_times_plan, waiting_times_plan = res[0], res[1], res[2], res[3]

            for k in range(1, len(response_times_monitor)):
                RESPONSE_TIME_MONITOR_CUMULATIVE_AVG[i].append(np.mean(response_times_monitor[0:k]))

            response_times_monitor_avg = np.mean(response_times_monitor)
            waiting_times_monitor_avg = np.mean(waiting_times_monitor)
            response_times_plan_avg = np.mean(response_times_plan)
            waiting_times_plan_avg = np.mean(waiting_times_plan)

            RESPONSE_TIME_MONITOR.append(response_times_monitor_avg)
            WAITING_TIME_MONITOR.append(waiting_times_monitor_avg)
            RESPONSE_TIME_PLAN.append(response_times_plan_avg)
            WAITING_TIME_PLAN.append(waiting_times_plan_avg)

            RHO_MONITOR_1.append(res[4])
            RHO_MONITOR_2.append(res[5])
            RHO_MONITOR_3.append(res[6])
            RHO_PLAN.append(res[7])

        except Exception as e:
            print(f"An error occurred during execution {i + 1}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <number_of_times> [finite | infinite]")
        sys.exit(1)

    if int(sys.argv[1]) >= 50:
        print("pls less simulations")
        sys.exit(1)

    if sys.argv[2] == "finite":
        try:
            n = int(sys.argv[1])
            # finite horizon STOP: terminal time (close the door)      */
            stop = 2000.0
            main(n, stop)

            response_time_monitor_interval = confidence_interval(ALPHA, n, RESPONSE_TIME_MONITOR)
            waiting_time_monitor_interval = confidence_interval(ALPHA, n, WAITING_TIME_MONITOR)
            response_time_plan_interval = confidence_interval(ALPHA, n, RESPONSE_TIME_PLAN)
            waiting_time_plan_interval = confidence_interval(ALPHA, n, WAITING_TIME_PLAN)
            rho_man1_interval = confidence_interval(ALPHA, n, RHO_MONITOR_1)
            rho_man2_interval = confidence_interval(ALPHA, n, RHO_MONITOR_2)
            rho_man3_interval = confidence_interval(ALPHA, n, RHO_MONITOR_3)
            rho_pla_interval = confidence_interval(ALPHA, n, RHO_PLAN)

            print("Monitor Centre")
            print(f"E[Tq] = {np.mean(WAITING_TIME_MONITOR)}", f"+/- {waiting_time_monitor_interval}")
            print(f"E[Ts] = {np.mean(RESPONSE_TIME_MONITOR)}", f"+/- {response_time_monitor_interval}")
            print(f"rho1 = {np.mean(RHO_MONITOR_1)}", f"+/- {rho_man1_interval}")
            print(f"rho2 = {np.mean(RHO_MONITOR_2)}", f"+/- {rho_man2_interval}")
            print(f"rho3 = {np.mean(RHO_MONITOR_3)}", f"+/- {rho_man3_interval}")

            print("Plan Centre")
            print(f"E[Tq] = {np.mean(WAITING_TIME_PLAN)}", f"+/- {waiting_time_plan_interval}")
            print(f"E[Ts] = {np.mean(RESPONSE_TIME_PLAN)}", f"+/- {response_time_plan_interval}")
            print(f"rho = {np.mean(RHO_PLAN)}", f"+/- {rho_pla_interval}")

        except ValueError:
            print("The argument must be an integer.")
            sys.exit(1)

    elif sys.argv[2] == "infinite":
        # infinite horizon STOP:
        stop = sys.float_info.max

        batch_size = 156
        main(1, stop)
    else:
        print("Usage: python main.py <number_of_times> [finite | infinite]")
        sys.exit(1)
