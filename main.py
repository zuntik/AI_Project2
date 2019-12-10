if __name__=="__main__":
    import sys
    sys.path.append('./aima-python/')
    import os

from probability import *
from itertools import product

class Problem:

    def __init__(self, fh):
        lines = fh.read().splitlines()
        # extract lines beggining in R,...,M
        r = [li for li in lines if li.find("R") == 0][0]
        c = [li for li in lines if li.find("C") == 0][0]
        s = [li for li in lines if li.find("S") == 0][0]
        p = [li for li in lines if li.find("P") == 0][0]
        m = [li for li in lines if li.find("M") == 0]

        # g is undirected simple graph to store rooms and their adjacent
        self.graph = {i: list() for i in r.split()[1:]}
        pairs = c[1:].replace(",", " ").split()
        for a, b in zip(pairs[::2], pairs[1::2]):
            self.graph[a].append(b)
            self.graph[b].append(a)

        # a sensor in sensores stors the room it's in and the conditional prob table
        self.sensors = {}
        for li in s.split()[1:]:
            sn, r, tpr, fpr = li.split(":")
            self.sensors[sn] = {'room':r, 'tpr':float(tpr), 'fpr':float(fpr)}

        # P is the propagation probability which is the same for every room
        self.P = float(p.split()[1])

        # the a time_stamp is a dictionary whose keys are the sensors and the item is the sensor's value
        self.time_stamps = [ {w.split(":")[0]: w.split(":")[1]=='T' for w in li.split()[1:]} for li in m ]

    def construct_net(self):
        # The Baesyan network for this problem contains a node for each room for each timestamp and a node for each sensor
        # for each timestamp if the measurement is available
        self.bn = BayesNet()

        for t, ts in enumerate(self.time_stamps):

            if t == 0:
                # on the first time stamp the rooms have no parents
                for room in self.graph:
                    self.bn.add((room+'_0', '', 0.5))
            else:
                for room, adjacent in self.graph.items():
                    # The first half of the conditional joint probability table is for when the room is already on fire
                    first_half = {i:1.0 for j,i in enumerate(product((True,False),repeat=len(adjacent)+1)) if j < 2**len(adjacent) }
                    # The second half is for when the room is not on fire and there is at least one adjacent room on fire
                    second_half = {i: self.P for j,i in enumerate(product((True,False),repeat=len(adjacent)+1)) if j >= 2**len(adjacent) }
                    # When no adjacent room is on fire nor it self is on fire, the chance of catching fire is 0
                    second_half[(F,)*(len(adjacent)+1)] = 0
                    # for the following timestamps the rooms have as parents the adjacent and itself for the previous timestep
                    self.bn.add((room+'_'+str(t), str('_'+str(t-1)+' ').join([room]+adjacent)+'_'+str(t-1), {**first_half, **second_half} ))

            for s in ts:
                # the sensors only depend on the current timestamp
                self.bn.add((s+'_'+str(t), self.sensors[s]['room']+'_'+str(t), {T:self.sensors[s]['tpr'], F: self.sensors[s]['fpr']}))

    def construct_ev(self):
        # the evidence is a list of measurements from the sensors for each timestop
        self.ev = {s+'_'+str(t): val for t,ts in enumerate(self.time_stamps) for s,val in ts.items()}

    def solve(self):
        self.construct_net()
        self.construct_ev()
        # we want to return the tuple (room, likelihood) of the room most likely to be on fire
        return max(((room, elimination_ask(room+'_'+str(len(self.time_stamps)-1),self.ev,self.bn)[True]) for room in self.graph), key=lambda i: i[1])

def solver(input_file):
    return Problem(input_file).solve()

if __name__=="__main__":
    for l in open("public_tests/solutions.txt"):
        print(l)
        l = l.split()
        sol = solver(open("public_tests/"+l[0]))
        print(l[0] +' '+ sol[0]+ ' ' + str(sol[1]) + ' mine' +'\n')
