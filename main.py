if __name__=="__main__":
    import sys
    sys.path.append('./aima-python/')
    import os

from probability import *
from itertools import product

class Problem:

    def __init__(self, fh):
        lines = fh.read().splitlines()
        r = [li for li in lines if li.find("R") == 0][0]
        c = [li for li in lines if li.find("C") == 0][0]
        s = [li for li in lines if li.find("S") == 0][0]
        p = [li for li in lines if li.find("P") == 0][0]
        m = [li for li in lines if li.find("M") == 0]

        # g is undirected simple graph
        self.graph = {i: list() for i in r.split()[1:]}
        pairs = c[1:].replace(",", " ").split()
        for a, b in zip(pairs[::2], pairs[1::2]):
            self.graph[a].append(b)
            self.graph[b].append(a)

        self.sensors = {}
        for li in s.split()[1:]:
            sn, r, tpr, fpr = li.split(":")
            self.sensors[sn] = {'room':r, 'tpr':float(tpr), 'fpr':float(fpr)}

        self.P = float(p.split()[1])
        self.time_stamps = [ {w.split(":")[0]: w.split(":")[1] for w in li.split()[1:]} for li in m ]

    def construct_net(self):

        self.bn = BayesNet()

        for t, ts in enumerate(self.time_stamps):
            if t == 0:
                for room in self.graph:
                    print((room + '_' + str(t), '', 0.5))
                    self.bn.add((room+'_'+str(t), '', 0.5))
            else:
                for room, adjacent in self.graph.items():
                    first_half = {i:1.0 for j,i in enumerate(product((True,False),repeat=len(adjacent)+1)) if j < 2**len(adjacent) }
                    second_half = {i: self.P for j,i in enumerate(product((True,False),repeat=len(adjacent)+1)) if j >= 2**len(adjacent) }
                    second_half[(F,)*(len(adjacent)+1)] = 0
                    print((room+'_'+str(t), str('_'+str(t-1)+' ').join([room]+adjacent)+'_'+str(t-1), {**first_half, **second_half} ))
                    self.bn.add((room+'_'+str(t), str('_'+str(t-1)+' ').join([room]+adjacent)+'_'+str(t-1), {**first_half, **second_half} ))

            for s in ts:
                print((s+'_'+str(t), self.sensors[s]['room']+'_'+str(t), {T:self.sensors[s]['tpr'], F: self.sensors[s]['fpr']}))
                self.bn.add((s+'_'+str(t), self.sensors[s]['room']+'_'+str(t), {T:self.sensors[s]['tpr'], F: self.sensors[s]['fpr']}))

    def construct_ev(self):
        to_bool = lambda  x: T if x=='T' else F
        self.ev = {s+'_'+str(t):to_bool(val) for t,ts in enumerate(self.time_stamps) for s,val in ts.items()}
        print(self.ev)

    def solve(self):
        self.construct_net()
        self.construct_ev()
        results = ( (room, elimination_ask(room+'_'+str(len(self.time_stamps)-1),self.ev,self.bn)[True]) for room in self.graph )
        print(list(results))
        return max(results, key=lambda i: i[1])
        #return (room, likelihood)

def solver(input_file):
    return Problem(input_file).solve()

if __name__=="__main__":
    fp = open("examples2/P2.txt")
    # solved files should finish with *_solved.txt
    print(solver(fp))
