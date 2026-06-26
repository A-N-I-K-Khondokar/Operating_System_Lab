class BankersAlgorithm:
    def __init__(self):
        self.n          = 0  # number of process
        self.m          = 0  # number of resources
        self.allocation = []
        self.maximum    = []
        self.available  = []
        self.need       = []

    def take_input(self):
        self.n = int(input("Enter the number of Process   : "))
        self.m = int(input("Enter the number of Resources : "))

        print("\nAllocation Matrix ?")
        for i in range(self.n):
            row = list(map(int, input(f"  p{i} : ").split()))
            self.allocation.append(row)

        print("\nMaximum Matrix ?")
        for i in range(self.n):
            row = list(map(int, input(f"  p{i} : ").split()))
            self.maximum.append(row)

        print("\nAvailable ?")
        self.available = list(map(int, input("  Enter : ").split()))

    def calNeed(self):
        for i in range(self.n):       # loop for process
            row = []                   # empty row for each process
            for j in range(self.m):   # loop through every resource
                row.append(self.maximum[i][j] - self.allocation[i][j])
            self.need.append(row)

    def printNeed(self):
        print("\n---- Need Matrix ----")
        print(f"{'process':<8}", end="")
        for i in range(self.m):
            print(f"r{i:<4}", end="")
        print()
        for i in range(self.n):
            print(f"p{i:<8}", end="")
            for j in range(self.m):
                print(f"{self.need[i][j]:<5}", end="")
            print()

    def print_safety_row(self, process, need, work, finish):
        print(f"  p{process:<6}", end="")
        print(f"{str(need):<25}", end="")  # need list as string
        print(f"{str(work):<25}", end="")  # work list as string
        print(finish)

    def safety_algorithm(self, work, finish):
        sequence = []
        count    = 0

        # print header
        print(f"\n  {'process':<8} {'need':<25} {'work':<25} {'finish'}")
        print("  " + "-" * 60)

        while count < self.n:
            found = False

            for i in range(self.n):
                if not finish[i]:  # check process is not finished

                    # check need <= work for all resources
                    all_satisfied = True
                    for j in range(self.m):
                        if self.need[i][j] > work[j]:
                            all_satisfied = False
                            break

                    # process can execute
                    if all_satisfied:
                        # add allocation back to work
                        for k in range(self.m):
                            work[k] += self.allocation[i][k]

                        finish[i] = True
                        sequence.append(f"p{i}")
                        count += 1
                        found  = True

                        self.print_safety_row(i, self.need[i], work, finish[i])

            # no process could execute in this pass
            if not found:
                break

        return count == self.n, sequence

    def check_safe_state(self):
        print("\n--- Safety Algorithm ---")

        work   = self.available[:]   # copy of available
        finish = [False] * self.n    # all processes unfinished

        is_safe, sequence = self.safety_algorithm(work, finish)

        if is_safe:
            print(f"\nSAFE STATE")
            print(f"Sequence : {' -> '.join(sequence)}")
        else:
            print(f"\nUNSAFE STATE")

        return is_safe

    def resource_request(self):
        print("\n--- Resource Request ---")

        pid     = int(input("Requesting process? (number only) : "))
        request = list(map(int, input(f"p{pid} request : ").split()))  # space separated

        # check 1 — request <= need
        for i in range(self.m):
            if request[i] > self.need[pid][i]:
                print("DENIED — request exceeds need")
                return

        print("Check 1 passed — request <= need")

        # check 2 — request <= available
        for i in range(self.m):
            if request[i] > self.available[i]:
                print("DENIED — request exceeds available")
                return

        print("Check 2 passed — request <= available")

        # pretend allocate
        for i in range(self.m):
            self.available[i]       -= request[i]
            self.allocation[pid][i] += request[i]
            self.need[pid][i]       -= request[i]

        print(f"\nNew available : {self.available}")

        work   = self.available[:]   # copy of new available
        finish = [False] * self.n    # all processes unfinished

        is_safe, sequence = self.safety_algorithm(work, finish)

        if is_safe:
            print("\nREQUEST GRANTED")
            print(f"Sequence : {' -> '.join(sequence)}")
        else:
            # rollback to previous state
            for i in range(self.m):
                self.available[i]       += request[i]
                self.allocation[pid][i] -= request[i]
                self.need[pid][i]       += request[i]
            print("\nREQUEST DENIED — unsafe state")
            print("Rolled back to previous state")


# Main
bank = BankersAlgorithm()
bank.take_input()
bank.calNeed()
bank.printNeed()
bank.check_safe_state()

while True:
    choice = input("\nDo you want to make a resource request? (yes/no) : ").strip().lower()
    if choice == "yes":
        bank.resource_request()
    else:
        print("\nProgram ended.")
        break
