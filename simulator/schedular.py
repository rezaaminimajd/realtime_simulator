from generator.dag_genrator import generate
from models import Processor, Dag, Task, Edge
from scheduling_algorithm import FDWS, FDS_MIMF, ADS_MIMF


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
        if timer % 500 == 0:
            print(f'time: {timer}')
        available_processors = Processor.get_free_processors(timer)
        if not available_processors:
            timer += 1
            continue
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
        while queue:
            pr = Processor.get_free_processor(timer)
            if not pr:
                timer += 1
                continue
            t, d = queue.pop(0)
            pr.scheduled_time = max(t.start_time, timer) + t.get_execution_time(pr.index)
            t.end_time = pr.scheduled_time
            d.update_start_time(pr.scheduled_time, t)
        timer += 1

    print("scheduling done!")
    Dag.print_information()


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
    print("processor created!")
    create_dags(dags)
    print("dags created!")
    print("start scheduling...")
    schedule(a)
