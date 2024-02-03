from dag_genrator import generate
from scheduling_algorithm import FDWS, FDS_MIMF, ADS_MIMF


class Processor:
    processors = []

    def __init__(self, index: int):
        self.index = index
        self.scheduled_time = 0
        Processor.processors.append(self)

    @staticmethod
    def get_free_processors(timer):
        free_processors = []
        for p in Processor.processors:
            if p.scheduled_time < timer:
                free_processors.append(p)
        return free_processors

    @staticmethod
    def get_free_processor(timer):
        free_processor = None
        for p in Processor.processors:
            if p.scheduled_time < timer:
                free_processor = p
        return free_processor


class Dag:
    dags = []
    sign = 0

    def __init__(
            self,
            index: int,
            tasks: list,
            criticality: float,
            deadline: int,
            arrival_time: int
    ):
        self.index = index
        self.tasks = tasks
        self.criticality = criticality
        self.deadline = deadline
        self.arrival_time = arrival_time
        self.done_tasks = []
        Dag.dags.append(self)

    def update_start_time(self, start_time, task):
        for t in self.tasks:
            for dep in t.dependencies:
                if dep.index_from == task.index:
                    t.start_time = start_time

    def print_information(self):
        end_time = max([t.end_time for t in self.done_tasks])
        print(f"dag index: {self.index}, dag arrival time: {self.arrival_time}, dag end time: {end_time}, dag deadline: {self.deadline}")


class Task:

    def __init__(
            self,
            index: int,
            start_time: int,
            execution_time: list,
            dependencies: list,
    ):
        self.index = index
        self.start_time = start_time
        self.execution_time = execution_time
        self.dependencies = dependencies
        self.done = False
        self.end_time = None

    def get_execution_time(self, p_index):
        return self.execution_time[p_index]

    def turnaround_time(self, p_index):
        time = 0
        for dp in self.dependencies:
            time += dp.get_execution_time(p_index)
        time += self.get_execution_time(p_index)
        return time


class Edge:

    def __init__(self, index_from: int, index_to: int, execution_time: list):
        self.index_from = index_from
        self.index_to = index_to
        self.execution_time = execution_time
        self.done = False

    def get_execution_time(self, p_index):
        return self.execution_time[p_index]


def create_processors(processors_count: int):
    for i in range(processors_count):
        Processor(i)


def create_dags(dags_dict: dict):
    for d_index, d in dags_dict.items():
        tasks = []
        for n_index, task in d['nodes'].items():
            dependencies = []
            for e_index, edge in d['edges'].items():
                e = edge[0]
                if e[0] == n_index:
                    dependencies.append(
                        Edge(
                            e_index,
                            n_index,
                            e[1]
                        )
                    )
            tasks.append(
                Task(
                    n_index,
                    d['arrival_time'],
                    task,
                    dependencies
                )
            )
        Dag(d_index, tasks, d['criticality'], d['lower_bound'], d['arrival_time'])


def schedule(algorithm):
    timer = 0
    algorithm_class = find_algorithm_class(algorithm)

    while True:
        available_processors = Processor.get_free_processors(timer)
        queue, sign, done = algorithm_class.get_next_queue(
            Dag.dags,
            len(available_processors),
            Dag.sign,
            timer
        )
        if done:
            break
        if sign:
            Dag.sign = sign
        if not queue:
            timer += 1
        while queue:
            pr = Processor.get_free_processor(timer)
            if not pr:
                timer += 1
                continue
            t, d = queue.pop(0)
            pr.scheduled_time = max(t.start_time, timer) + t.get_execution_time(pr.index)
            t.end_time = pr.scheduled_time
            d.update_start_time(pr.scheduled_time, t)

        # print(f"timer: {timer}")
        timer += 1

    print("scheduling done!")
    for d in Dag.dags:
        d.print_information()


def find_algorithm_class(algorithm):
    algorithm_class = None
    if algorithm == 'w':
        algorithm_class = FDWS
    elif algorithm == 'f':
        algorithm_class = FDS_MIMF
    elif algorithm == 'a':
        algorithm_class = ADS_MIMF
    return algorithm_class


if __name__ == '__main__':
    p = int(input("input the number of processors(4,8,16,32): "))
    lf = float(input("input the factor of lower bound(1.1,1.2,1.5): "))
    a = input("input the scheduling algorithm(w: FDWS, f: FDS_MIMF, a: ADS_MIMF): ")
    dags = generate(processors_count=p, lower_bound_factor=lf)
    create_processors(p)
    create_dags(dags)
    schedule(a)
