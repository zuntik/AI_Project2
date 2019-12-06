if __name__=="__main__":
    import sys
    sys.path.append('./aima-python/')
    import os

from probability import *


class Problem:

    def __init__(self, fh):
        lines = fh.read().splitlines()
        r = [li for li in lines if li.find("R") == 0][0]
        c = [li for li in lines if li.find("C") == 0][0]
        s = [li for li in lines if li.find("S") == 0][0]
        p = [li for li in lines if li.find("P") == 0][0]
        m = [li for li in lines if li.find("M") == 0]

        # g is undirected simple graph
        g = {i: list() for i in r.split()[1:]}
        pairs = c[1:].replace(",", " ").split()
        for a, b in zip(pairs[::2], pairs[1::2]):
            g[a].append(b)
            g[b].append(a)

        sensors = []
        for li in s.split()[1:]:
            sn, r, tpr, fpr = li.split(":")
            sensors.append({'name': sn, 'room': r, 'tpr': tpr, 'fpr': fpr})

        propag_prob = float(p.split()[1])


        time_stamps = []
        for li in m:
            time_stamps.append({w.split(":")[0]: w.split(":") for w in li.split()[1:]})

        self.graph = g
        self.time_stamps = time_stamps
        self.sensors = sensors
        self.propag_prob = propag_prob



    # Place here your code to load problem from opened file object fh
    # and use probability.BayesNet() to create the Bayesian network

    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        return (room, likelihood)


def solver(input_file):
    return Problem(input_file).solve()


if __name__=="__main__":
    fp = open("examples2\P2.txt")
    # solved files should finish with *_solved.txt
    p = Problem(fp)
