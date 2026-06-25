class Process:
    def __init__(self, pid, arrival, burst):
        self.pid     = pid
        self.arrival = arrival
        self.burst   = burst
        self.rem     = burst  # remaining burst
        self.ct      = 0      # completion time
        self.tt      = 0      # turnaround time
        self.wt      = 0      # waiting time


class SJF_Preemptive:
    def __init__(self):
        self.processes = []

    # Take input
    def takeInput(self):
        n = int(input("Enter Number of process: "))

        for i in range(n):
            print(f"\nProcess : {i + 1}")
            arrival = int(input("Arrival Time: "))
            burst   = int(input("Burst Time: "))
            self.processes.append(Process(f"P{i+1}", arrival, burst))

    # Algorithm
    def run(self):
        completed    = 0               # processes that are finished
        current_time = 0               # CPU clock, increments by 1
        n            = len(self.processes)  # total number of processes
        prev         = None            # avoid printing the same process

        print("\nExecution Timeline")
        while completed < n:           # stop when completed == n
            # list comprehension to filter available processes
            available = [
                p for p in self.processes
                if p.arrival <= current_time and p.rem > 0  # rem = remaining burst
            ]
            if not available:          # if available is empty, increment CPU clock
                current_time += 1
                continue

            # find the process with lowest remaining burst
            shortest = min(available, key=lambda p: p.rem)

            if shortest.pid != prev:
                print(f"t={current_time} -> Running {shortest.pid} | remBurst {shortest.rem}")
                prev = shortest.pid    # only print when process changes

            shortest.rem   -= 1
            current_time   += 1

            if shortest.rem == 0:
                completed      += 1
                shortest.ct     = current_time
                shortest.tt     = current_time - shortest.arrival
                shortest.wt     = shortest.tt - shortest.burst
                prev            = None

    def print_result(self):
        print("\n----- Result ------")
        print(f"{'PID':<6} {'Arrival':<10} {'Burst':<6} {'Completion':<13} {'Turnaround':<10} {'Waiting':<6}")
        total_tt = total_wt = 0

        for p in self.processes:
            print(f"{p.pid:<7}{p.arrival:<11}{p.burst:<7}{p.ct:<14}{p.tt:<11}{p.wt:<7}")
            total_tt += p.tt
            total_wt += p.wt

        n = len(self.processes)
        print(f"\nAverage Turnaround Time: {total_tt / n:.2f}")
        print(f"Average Waiting Time   : {total_wt / n:.2f}")


# Main Section
scheduler = SJF_Preemptive()
scheduler.takeInput()
scheduler.run()
scheduler.print_result()