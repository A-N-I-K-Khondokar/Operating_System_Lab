import threading  # for Semaphore and Thread
import time

# barrier forces all 5 threads to start at exact same time
barrier = threading.Barrier(5)

class Philosopher(threading.Thread):  # inheriting the Thread class
    def __init__(self, pid, left_fork, right_fork):
        threading.Thread.__init__(self)  # initializing the parent
        self.pid = pid
        self.left_fork = left_fork
        self.right_fork = right_fork
        
    def think(self):
        print(f"{self.pid} is thinking.....")
        time.sleep(2)  # sleep for 2 sec to give time for all threads to run simultaneously
    
    def eat(self):
        print(f"{self.pid} is eating....")
        time.sleep(2)  # eating time
        
    def run(self):
        self.think()
        barrier.wait()  # force all threads to wait for each other

        print(f"{self.pid} pick up left fork")
        self.left_fork.acquire()  # acquire semaphore for left fork
        time.sleep(2)

        print(f"{self.pid} picked up the right fork")
        self.right_fork.acquire()  # acquire semaphore for right fork
        
        self.eat()
        
        self.right_fork.release()
        self.left_fork.release()
        
        print(f"{self.pid} releases both forks")


# Main function

forks = [threading.Semaphore(1) for i in range(5)]
"""
Creates 5 forks with indices 0, 1, 2, 3, 4
representing 5 forks all on the left side.
forks[(i+1)%5] represents the right forks
"""
philosophers = [
    Philosopher(f"p{i+1}", forks[i], forks[(i+1)%5]) for i in range(5)
]

for p in philosophers:
    p.start()  # start all philosophers; do not wait for run() to finish

for p in philosophers:
    p.join()  # wait for all philosophers to finish before continuing

print("Philosopher execution completed.")



        
        