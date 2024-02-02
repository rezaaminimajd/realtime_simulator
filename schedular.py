from dag_genrator import generate


class Processor:
    processors = []

    def __init__(self, index: int):
        self.index = index
        self.scheduled_time = 0
        Processor.processors.append(self)

    @staticmethod
    def get_free_processors(time):
        free_processors = []
        for p in Processor.processors:
            if p.scheduled_time < time:
                free_processors.append(p)
        return free_processors


class Dag:
    dags = []
    sign = 0

    def __init__(
            self,
            tasks: list,
            criticality: float,
            deadline: int,
            arrival_time: int
    ):
        self.tasks = tasks
        self.criticality = criticality
        self.deadline = deadline
        self.arrival_time = arrival_time
        Dag.dags.append(self)


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
    for d in dags_dict.values():
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
        Dag(tasks, d['criticality'], d['lower_bound'])


def schedule(algorithm):
    timer = 0

    while True:
        available_processors = Processor.get_free_processors()
        for p in available_processors:
            pass


if __name__ == '__main__':
    p = int(input("input the number of processors(4,8,16,32): "))
    lf = float(input("input the factor of lower bound(1.1,1.2,1.5): "))
    a = input("input the scheduling algorithm(w: FDWS, f: FDS_MIMF, a: ADS_MIMF): ")
    dags = generate(processors_count=p, lower_bound_factor=lf)
    create_processors(p)
    create_dags(dags)
    schedule(a)
