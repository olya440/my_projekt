class PageRank:

    def __init__(self, damping=0.85, iterations=20):

        self.damping = damping
        self.iterations = iterations
        self.ranks = {}

    def calculate(self, edges):

        nodes = set()
        graph = {}

        for source, target, weight in edges:
            nodes.add(source)
            nodes.add(target)
            if source not in graph:
                graph[source] = []
            graph[source].append((target, weight))

        num_nodes = len(nodes)
        if num_nodes == 0:
            return {}

        current_ranks = {node: 1.0/num_nodes for node in nodes}

        for _ in range(self.iterations):
            new_ranks = {}
            for node in nodes:
                rank_sum = 0.0
                for source, targets in graph.items():
                    for target, weight in targets:
                        if target == node:
                            out_weight_sum = sum(w for _, w in targets)
                            if out_weight_sum > 0:
                                rank_sum += current_ranks[source] * (weight / out_weight_sum)

                new_ranks[node] = (1-self.damping) / num_nodes + self.damping * rank_sum

            current_ranks = new_ranks

        self.ranks = current_ranks
        return current_ranks