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
    base_system_criticality = -1
    system_criticality = -1
    under_danger_dag = None

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
        if Dag.system_criticality < 0 or criticality < Dag.system_criticality:
            Dag.system_criticality = criticality
            Dag.base_system_criticality = criticality
        Dag.dags.append(self)

    def update_start_time(self, start_time, task):
        for t in self.tasks:
            for dep in t.dependencies:
                if dep.index_from == task.index:
                    t.start_time = start_time

    def distance_to_deadline(self):
        execution_time = 0
        for t in self.tasks:
            et = []
            for i in range(len(t.execution_time)):
                et.append(t.get_execution_time(i))
            execution_time += sum(et) // len(et)
        return execution_time, self.deadline

    @staticmethod
    def get_all_critical_dags():
        c = []
        for d in Dag.dags:
            if d.criticality >= Dag.system_criticality:
                c.append(d)
        if not c:
            if Dag.dags:
                return Dag.dags
            return None
        return c

    @staticmethod
    def check_under_danger_dag(timer):
        if Dag.under_danger_dag and not Dag.under_danger_dag.tasks:
            Dag.system_criticality = Dag.base_system_criticality
            Dag.under_danger_dag = None
        under_danger = None
        pc = len(Processor.processors)
        for d in Dag.dags:
            et, dt = d.distance_to_deadline()
            if et == 0:
                continue
            if timer + et // pc > dt:
                if not under_danger:
                    under_danger = d.criticality
                elif under_danger < d.criticality:
                    under_danger = d.criticality
        if under_danger:
            Dag.system_criticality = under_danger

    @staticmethod
    def print_information():
        miss_deadline = 0
        for d in Dag.dags:
            end_time = max([t.end_time for t in d.done_tasks])
            if end_time > d.deadline:
                miss_deadline += 1
            print(
                f"dag index: {d.index}, dag arrival time: {d.arrival_time}, dag end time: {end_time}, dag deadline: {d.deadline}")
        print(f"{(miss_deadline / len(Dag.dags)) * 100}% of dags missed deadline")


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
