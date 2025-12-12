class Vertex:
    def __init__(self, id, rank_val, specific_set):
        self.id = id
        self.rank_val = rank_val
        self.specific_set = specific_set

        self.curr_msgs = []
        self.next_msgs = []
        self.neighbours = []
        self.halt = False
    
    def compute(self, superstep, maxstep, beta):
        if superstep >= 1:
            s = sum(self.curr_msgs)
            self.curr_msgs = self.next_msgs
            self.next_msgs = []
            self._update_rank_val(beta * s + (1 - beta) / len(self.specific_set))
        
        if superstep < maxstep:
            m = len(self.neighbours)
            for nb in self.neighbours:
                self.send_message(nb, self.rank_val / m)
        else:
            self.vote_to_halt()
    
    def _update_rank_val(self, val):
        self.rank_val = val

    def vote_to_halt(self):
        self.halt = True
    
    def get_state(self):
        return self.halt

    def send_message(self, nb, msg):
        nb.next_msgs.append(msg)

class FakePregel:
    def __init__(self, graph: list[list[int]]):
        self.graph = self._nodeify(graph)

    def _nodeify(self, graph):
        n = len(graph)
        res = [Vertex(i, 1 / n, list(range(n))) for i in range(n)]
        for i in range(n):
            for nb in graph[i]:
                res[i].neighbours.append(res[nb])
        return res
    
    def run(self, total_supersteps=30, beta=0.85):
        for superstep in range(total_supersteps):
            for node in self.graph:
                node.compute(superstep, total_supersteps, beta)
        return [node.rank_val for node in self.graph]

if __name__ == '__main__':
    # graph = [[1,2],[2],[0]]
    # graph = [[1,2], [2], [2]]
    graph = [[1,2], [0], [3], [2]]
    print(FakePregel(graph).run(total_supersteps=1000, beta=0.7))