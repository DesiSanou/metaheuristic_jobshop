from typing import List
from Instance import Instance
from Task import Task


class Schedule:

    def __init__(self, pb: Instance, times):
        self.pb = pb
        self.times = [[] for _ in range(pb.numJobs)]

        for i in range(pb.numJobs):
            self.times[i] = times[i]
            if len(times[i]) - pb.numTasks > 0:
                siz = [0 for i in range(len(times[i]) - pb.numTasks)]
                self.times[i] += siz

    def startTime(self, job, task=None):
        if task is None:
            task_instance = job
            return self.startTime(task_instance.job, task_instance.task)
        else:
            job_index = job
            return self.times[job_index][task]

    def isValid(self) -> bool:

        for j in range(self.pb.numJobs):
            for t in range(1, self.pb.numTasks):
                if self.startTime(j, t - 1) + self.pb.duration(j, t - 1) > self.startTime(j, t):
                    return False

            for t in range(self.pb.numTasks):
                if self.startTime(j, t) < 0:
                    return False

        for machine in range(self.pb.numMachines):
            for j1 in range(self.pb.numJobs):
                t1 = self.pb.task_with_machine(j1, machine)
                for j2 in range(j1 + 1, self.pb.numJobs):
                    t2 = self.pb.task_with_machine(j2, machine)

                    t1_first: bool = self.startTime(j1, t1) + self.pb.duration(j1, t1) <= self.startTime(j2, t2)
                    t2_first: bool = self.startTime(j2, t2) + self.pb.duration(j2, t2) <= self.startTime(j1, t1)

                    if t1_first is False and t2_first is False:
                        return False

        return True

    def makespan(self) -> int:
        m= -1
        for j in range(self.pb.numJobs):

            m = max(m, self.startTime(job=j, task=self.pb.numTasks - 1) + self.pb.duration(j, self.pb.numTasks - 1))
        return m

    def endTime(self, task: Task) -> int:
        return self.startTime(task) + self.pb.duration(task.job, task.task)

    def isCriticalPath(self, path: List[Task]) -> bool:
        if self.startTime(path[0]) != 0:
            return False
        elif self.endTime(path[len(path) - 1]) != self.makespan():
            return False
        for i in range(len(path) - 1):
            if self.endTime(path[i]) != self.startTime(path[i + 1]):
                return False
        return True

    def criticalPath(self) -> List[Task]:
        ldd: Task
        tmp = [Task(j, self.pb.numTasks - 1) for j in range(self.pb.numJobs)]
        ldd = sorted(tmp, key=lambda x: self.endTime(x), reverse=True)[0]
        assert self.endTime(ldd) == self.makespan()
        path = list()
        path.insert(0, ldd)

        while self.startTime(path[0]) != 0:
            cur: Task = path[0]
            machine: int = self.pb.machine(cur.job, cur.task)
            latestPredecessor = None

            if cur.task > 0:
                predOnJob: Task = Task(cur.job, cur.task - 1)

                if self.endTime(predOnJob) == self.startTime(cur):
                    latestPredecessor = predOnJob
            if (latestPredecessor is None):
                latestPredecessor = [Task(j, self.pb.task_with_machine(j, machine)) for j in range(self.pb.numJobs)]
                latestPredecessor = list(
                    filter(lambda elem: self.endTime(elem) == self.startTime(cur), latestPredecessor))
                latestPredecessor = latestPredecessor[0]

            assert latestPredecessor is not None and self.endTime(latestPredecessor) == self.startTime(cur)

            path.insert(0, latestPredecessor)
        assert self.isCriticalPath(path)
        return path
