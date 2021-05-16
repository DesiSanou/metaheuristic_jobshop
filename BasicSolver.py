from Instance import Instance
from Result import Result, ExitCause
from JobNumbers import JobNumbers


class BasicSolver():
    def __init__(self):
        pass

    def solve(self, instance, deadline=None):
        sol = JobNumbers(instance)
        for t in range(instance.numTasks):
            for j in range(instance.numJobs):
                sol.jobs[sol.nextToSet]= j
                sol.nextToSet += 1
        return Result(instance, sol.toSchedule(), ExitCause.Blocked), sol

