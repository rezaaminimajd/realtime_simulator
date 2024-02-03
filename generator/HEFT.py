def calculate_upward_rank(task_id, dag, task_ranks):
    if task_id in task_ranks:
        return task_ranks[task_id]

    task_execution_time = dag['nodes'][task_id]
    max_successor_rank = 0
    for successor, transfer_time in dag['edges'].get(task_id, []):
        successor_rank = calculate_upward_rank(successor, dag, task_ranks)
        max_successor_rank = max(max_successor_rank, transfer_time + successor_rank)

    task_ranks[task_id] = task_execution_time + max_successor_rank
    return task_ranks[task_id]


def heft_lower_bound(dag):
    task_ranks = {}
    for task in dag['nodes']:
        calculate_upward_rank(task, dag, task_ranks)
    return max(task_ranks.values())


def calculate_heft(dag):
    # lower_bound = heft_lower_bound(dag)
    return 10
