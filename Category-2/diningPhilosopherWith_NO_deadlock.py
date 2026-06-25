import threading
import time


class Philosopher(threading.Thread):
    """Philosopher thread using Resource Hierarchy to prevent deadlock.

    The last philosopher picks right fork first, others pick left first.
    This breaks the circular wait condition and prevents deadlock.
    """
    def __init__(self, pid, left_fork, right_fork, is_last):
        threading.Thread.__init__(self)

        self.pid = pid
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.is_last = is_last
    
    def think(self):
        print(f"{self.pid} is thinking.")
        time.sleep(1)

    def eat(self):
        print(f"{self.pid} is eating.")
        time.sleep(1)
    
    def run(self):
        self.think()

        if self.is_last:
            # Last philosopher picks right fork first to break circular wait
            print(f"{self.pid} picking right fork first")
            self.right_fork.acquire()

            print(f"{self.pid} picking left fork")
            self.left_fork.acquire()

        else:
            # Other philosophers pick left fork first
            print(f"{self.pid} picking left fork")
            self.left_fork.acquire()

            print(f"{self.pid} picking right fork")
            self.right_fork.acquire()
            
        self.eat()

        self.right_fork.release()
        self.left_fork.release()
        print(f"{self.pid} released both forks")
        

# Main function

forks = [threading.Semaphore(1) for i in range(5)]

philosophers = [
    Philosopher(f"p{i+1}", forks[i], forks[(i+1)%5], is_last=(i==4))  # only last philosopher picks right first
    for i in range(5)
]

for p in philosophers:
    p.start()

for p in philosophers:
    p.join()

print("Execution completed - No deadlock!")
    