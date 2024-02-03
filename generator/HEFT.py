from queue import PriorityQueue


def calculate_heft(dag):
    rank = {}
    for task in dag['object'].nodes:
        rank[task] = 0
    averages = [sum(times) / len(times) for node, times in dag['nodes'].items()]
    node_sum = sum(averages)
    averages = [sum(times[0][1]) / len(times[0][1]) for node, times in dag['edges'].items()]
    edge_sum = sum(averages)
    makespann = (edge_sum + node_sum) / 2
    for task in dag['object'].nodes:
        rank[task] = calculate_rankk(task, dag['object'], rank)

    return makespann


def calculate_rank(task, graph, rank):
    if rank[task] > 0:
        return rank[task]

    max_rank = 0
    for successor in graph.successors(task):
        successor_rank = calculate_rank(successor, graph, rank)
        communication_cost = 0
        rank_value = graph.nodes[successor]['execution_time'] + communication_cost + successor_rank
        if rank_value > max_rank:
            max_rank = rank_value

    rank[task] = max_rank
    return max_rank
def calculate_rankk(task, graph, rank):
    return 0


def schedule_heft(dag):
    ready_tasks = set()
    scheduled_tasks = set()
    task_start_time = {}
    processor_finish_time = {}

    for task in dag['object'].nodes:
        ready_tasks.add(task)

    while ready_tasks:
        task = select_task(ready_tasks, dag['object'], task_start_time, processor_finish_time)
        processor = select_processor(task, processor_finish_time)
        start_time = max(task_start_time[task], processor_finish_time[processor])
        finish_time = start_time + dag['object'].nodes[task]['execution_time']
        task_start_time[task] = start_time
        processor_finish_time[processor] = finish_time
        ready_tasks.remove(task)
        scheduled_tasks.add(task)

        for successor in dag['object'].successors(task):
            ready = True
            for predecessor in dag['object'].predecessors(successor):
                if predecessor not in scheduled_tasks:
                    ready = False
                    break
            if ready:
                ready_tasks.add(successor)


def select_task(ready_tasks, graph, task_start_time, processor_finish_time):
    max_rank = -1
    selected_task = None

    for task in ready_tasks:
        rank = calculate_rank(task, graph, task_start_time)
        if rank > max_rank:
            max_rank = rank
            selected_task = task

    return selected_task


def select_processor(task, processor_finish_time):
    min_finish_time = float('inf')
    selected_processor = None

    for processor, finish_time in processor_finish_time.items():
        if finish_time < min_finish_time:
            min_finish_time = finish_time
            selected_processor = processor

    return selected_processor


def calculate_lowerbound(dags):
    for dag in dags.values():
        lower_bound = calculate_heft(dag)
        dag['lower_bound'] = lower_bound
        print(f"DAG {dag['index']} lowerbound: {lower_bound}")
