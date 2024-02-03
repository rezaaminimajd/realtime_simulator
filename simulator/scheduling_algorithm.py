from models import Dag

class FDWS:
    all_queues = []
    generated = False

    @staticmethod
    def get_next_queue(dags, processors_count, sign, timer):
        if FDWS.generated:
            if FDWS.all_queues:
                return FDWS.all_queues.pop(0), None, False
            return None, None, True
        FDWS.generate_queue(dags)
        return FDWS.get_next_queue(dags, processors_count, sign, timer)

    @staticmethod
    def generate_queue(dags):
        while True:
            queue = []
            for d in dags:
                if d.tasks:
                    t = d.tasks.pop(0)
                    queue.append((t, d))
                    d.done_tasks.append(t)
            if not queue:
                break
            FDWS.all_queues.append(queue)
        FDWS.generated = True


class FDS_MIMF:

    @staticmethod
    def get_next_queue(dags, processors_count, sign, timer):
        done = True
        for d in dags:
            if d.tasks:
                done = False
        queue = []
        for i in range(processors_count):
            index = (sign + i) % len(dags)
            if dags[index].tasks:
                if dags[index].tasks[0].start_time <= timer:
                    t = dags[index].tasks.pop(0)
                    dags[index].done_tasks.append(t)
                    queue.append((t, dags[index]))
            if i - 1 == processors_count:
                sign = index
        return queue, sign, done


class ADS_MIMF:

    @staticmethod
    def get_next_queue(dags, processors_count, sign, timer):
        Dag.check_under_danger_dag(timer)
        dags = Dag.get_all_critical_dags()
        done = True
        for d in Dag.dags:
            if d.tasks:
                done = False
                break
        queue = []
        for i in range(processors_count):
            index = (sign + i) % len(dags)
            if dags[index].tasks:
                if dags[index].tasks[0].start_time <= timer:
                    t = dags[index].tasks.pop(0)
                    dags[index].done_tasks.append(t)
                    queue.append((t, dags[index]))
            if i - 1 == processors_count:
                sign = index
        return queue, sign, done
