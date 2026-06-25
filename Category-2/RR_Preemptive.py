'''
Round Robin is a scheduling algorithm where every process 
gets a fixed amount of CPU time called Time Quantum (or Time Slice).

Simple Rule:
Each process runs for maximum = time quantum units

If the process is not done in that time, 
it goes back to the end of the queue

If the process finishes before the quantum ends, 
CPU moves to next process immediately
'''
from collections import deque

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid     = pid
        self.arrival = arrival
        self.burst   = burst
        self.rem     = burst
        self.ct      = 0  # completion time
        self.tt      = 0  # turnaround time
        self.wt      = 0  # waiting time


class RoundRobin:
    def __init__(self):
        self.processes = []
        self.quantum   = 0

    # input
    def input(self):
        print("Round Robin Scheduling Algorithm:")
        n = int(input("Enter the Number of Process: "))

        for i in range(n):
            print(f"\nProcess {i+1}")
            arrival = int(input("Arrival Time : "))
            burst   = int(input("Burst Time   : "))
            self.processes.append(Process(f"P{i+1}", arrival, burst))

        self.quantum = int(input("\nTime Quantum : "))

    # run
    def run(self):
        queue        = deque()
        current_time = 0  # CPU clock
        completed    = 0
        index        = 0  # tracks which process to add next
        n            = len(self.processes)

        self.processes.sort(key=lambda p: p.arrival)

        print(f"\nExecution Timeline.....")

        while completed < n:

            # add all arrived processes to queue
            while index < n and self.processes[index].arrival <= current_time:
                queue.append(self.processes[index])
                index += 1

            # if queue is empty cpu is idle
            if not queue:
                current_time = self.processes[index].arrival
                continue

            p = queue.popleft()  # pop from the front

            run_time      = min(self.quantum, p.rem)
            start_time    = current_time
            current_time += run_time
            p.rem        -= run_time

            print(f"t={start_time} -> t={current_time} : running {p.pid} | remaining {p.rem}")

            # add newly arrived processes after this run
            while index < n and self.processes[index].arrival <= current_time:
                queue.append(self.processes[index])
                index += 1

            # current process status
            if p.rem == 0:
                completed += 1
                p.ct       = current_time
                p.tt       = current_time - p.arrival
                p.wt       = p.tt - p.burst
            else:
                queue.append(p)

    # print result
    def print_result(self):
        print("\nFinal Result...")
        print(f"\n{'PID':<6} {'Arrival':<10} {'Burst':<8} {'Completion':<13} {'TT':<6} {'WT':<6}")
        print("-" * 50)

        total_TT = total_WT = 0

        for p in self.processes:
            print(f"{p.pid:<6} {p.arrival:<10} {p.burst:<8} {p.ct:<13} {p.tt:<6} {p.wt:<6}")
            total_TT += p.tt
            total_WT += p.wt

        n = len(self.processes)
        print("-" * 50)
        print(f"Average Turnaround Time : {total_TT / n:.2f}")
        print(f"Average Waiting Time    : {total_WT / n:.2f}")


# Main
schedular = RoundRobin()
schedular.input()
schedular.run()
schedular.print_result()