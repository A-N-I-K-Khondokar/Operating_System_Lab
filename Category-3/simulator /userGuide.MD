# MOSS Deadlock Simulator

A Java-based simulator that shows processes competing for resources and demonstrates how deadlock happens step by step.

---

## Buttons

| Button | What it does |
|---|---|
| `run` | runs simulation automatically to the end |
| `stop` | stops the auto run |
| `step` | runs ONE step at a time |
| `reset` | starts over from beginning |
| `options` | change number of processes and resources |
| `processes` | change which .dat file each process uses |
| `resources` | change how many instances each resource has |
| `exit` | close the simulator |

---

## Process States

| State | Meaning |
|---|---|
| `U` | Unknown — just started |
| `C` | Computable — currently running |
| `W` | Waiting — blocked waiting for a resource |
| `H` | Halted — finished |

> When ALL processes show `W` — that is **DEADLOCK**

---

## .dat Command Files

Each process gets a `.dat` file with 4 commands:

| Command | Meaning |
|---|---|
| `C 10` | Compute for 10 milliseconds |
| `R 0` | Request resource 0 |
| `F 0` | Free resource 0 |
| `H` | Halt — process ends |

Comments in .dat files use `//`

---

## Terminal Commands for .dat Files

```bash
notepad b0.dat   # open or create a .dat file
type b0.dat      # read file content in terminal
dir *.dat        # check all .dat files exist
del b0.dat       # delete a .dat file
```

---

## Example 1 — DEADLOCK

### Setup
```
2 processes  → P0 and P1
2 resources  → Resource 0 and Resource 1
Each resource has 1 instance
```

### b0.dat
```
C 5    // P0 computes for 5 milliseconds
R 0    // P0 requests Resource 0
C 5    // P0 computes for 5 milliseconds
R 1    // P0 requests Resource 1
C 5    // P0 computes for 5 milliseconds
F 0    // P0 frees Resource 0
F 1    // P0 frees Resource 1
H      // P0 halts
```

### b1.dat
```
C 5    // P1 computes for 5 milliseconds
R 1    // P1 requests Resource 1
C 5    // P1 computes for 5 milliseconds
R 0    // P1 requests Resource 0
C 5    // P1 computes for 5 milliseconds
F 1    // P1 frees Resource 1
F 0    // P1 frees Resource 0
H      // P1 halts
```

### Run Command
```bash
java deadlock b 2 1 1
```

| Part | Meaning |
|---|---|
| `java` | run using java |
| `deadlock` | the simulator program |
| `b` | use files b0.dat and b1.dat |
| `2` | create 2 processes P0 and P1 |
| `1` | Resource 0 has 1 instance |
| `1` | Resource 1 has 1 instance |

### Simulator Screen
```
Processes              Resources
Id  State  Resource    Id  Available
0   W      R1          0   0
1   W      R0          1   0

All processes = W → DEADLOCK
```

### Why Deadlock Happens
```
P0 holds R0 → wants R1 → held by P1 → WAIT
P1 holds R1 → wants R0 → held by P0 → WAIT
Circular wait → nobody moves → DEADLOCK
```

---

## Example 2 — NO DEADLOCK

### Setup
```
2 processes  → P0 and P1
2 resources  → Resource 0 and Resource 1
Resource 0 has 1 instance
Resource 1 has 2 instances  ← only change
```

### Same b0.dat and b1.dat — no change needed

### Run Command
```bash
java deadlock b 2 1 2
```

| Part | Meaning |
|---|---|
| `java` | run using java |
| `deadlock` | the simulator program |
| `b` | use files b0.dat and b1.dat |
| `2` | create 2 processes P0 and P1 |
| `1` | Resource 0 has 1 instance |
| `2` | Resource 1 has 2 instances ← only change |

### Simulator Screen
```
Processes              Resources
Id  State  Resource    Id  Available
0   H                  0   1
1   H                  1   2

All processes = H → NO DEADLOCK
```

### Why No Deadlock Happens
```
Resource 1 has 2 instances
P0 gets Resource 1 without waiting
P0 finishes and releases Resource 0
P1 can now get Resource 0
No circular wait → NO DEADLOCK
```

---

## Key Difference

```
java deadlock b 2 1 1  →  R1 = 1 instance  →  DEADLOCK
java deadlock b 2 1 2  →  R1 = 2 instances →  NO DEADLOCK
```

Changing the last number from `1` to `2` gives Resource 1 one extra instance. This breaks the circular wait and prevents deadlock.