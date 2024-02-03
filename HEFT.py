def calculate_heft(dag):
    # Extract information from the DAG
    nodes = dag['nodes']
    edges = dag['edges']
    processors_count = len(nodes[0])

    # Calculate the rank for each task
    ranks = {}
    for node in nodes:
        rank_value = calculate_rank(node, ranks, edges, processors_count)
        ranks[node] = rank_value

    # Sort tasks based on rank in descending order
    sorted_tasks = sorted(ranks.keys(), key=lambda x: ranks[x], reverse=True)

    # Schedule tasks based on EFT policy
    schedule = {}
    for task in sorted_tasks:
        schedule[task] = schedule_task(task, schedule, ranks, edges, processors_count)

    return schedule


def calculate_rank(task, ranks, edges, processors_count):
    if task in ranks:
        return ranks[task]

    if not edges[task]:
        return nodes[task][0]

    max_rank = 0
    for child in edges[task]:
        communication_cost = edges[task][child]
        child_rank = calculate_rank(child, ranks, edges, processors_count)
        total_cost = nodes[task][0] + communication_cost + child_rank
        max_rank = max(max_rank, total_cost)

    return max_rank


def schedule_task(task, schedule, ranks, edges, processors_count):
    if task in schedule:
        return schedule[task]

    if not edges[task]:
        return 0

    earliest_start_time = 0
    for parent in edges[task]:
        communication_cost = edges[parent][task]
        parent_finish_time = schedule_task(parent, schedule, ranks, edges, processors_count)
        earliest_start_time = max(earliest_start_time, parent_finish_time + communication_cost)

    # Find the processor with the earliest finish time
    best_processor = min(range(processors_count), key=lambda p: earliest_start_time + ranks[task][p])

    # Update schedule with task's start time on the selected processor
    schedule[task] = earliest_start_time
    return earliest_start_time

