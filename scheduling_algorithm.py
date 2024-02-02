class FDWS:
    all_queues = []
    generated = False

    @staticmethod
    def get_next_queue(dags):
        if FDWS.generated:
            if FDWS.all_queues:
                return FDWS.all_queues.pop(0)
            return None
        FDWS.generate_queue(dags)
        return FDWS.get_next_queue(dags)

    @staticmethod
    def generate_queue(dags):
        while True:
            queue = []
            for d in dags:
                if d.tasks:
                    queue.append(d.tasks.pop(0))
            if not queue:
                break
            FDWS.all_queues.append(queue)
        FDWS.generated = True


class FDS_MIMF:

    @staticmethod
    def get_next_queue(dags, processors_count, sign, timer):
        queue = []
        for i in range(processors_count):
            index = (sign + i) % len(dags)
            if dags[index].tasks:
                if dags[index].tasks[0].start_time <= timer:
                    queue.append(dags[index].tasks.pop(0))
            if i - 1 == processors_count:
                sign = index
        return queue, sign


class ADS_MIMF:

    @staticmethod
    def get_next_dags(dags, processors, timer):
        pass
