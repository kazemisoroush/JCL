import sys
import math
import random
from Solver import Solver


class Jcl():

    # initialize the object
    def __init__(self, datacenter):
        # number of servers in data-center
        self.m = len(datacenter.servers)
        self.datacenter = datacenter

        # converts delay to monetary
        self.teta = 0.01
        # converts power to monetary
        self.alpha = 0.01
        # tunable smoothing parameter
        self.delta = 10
        # stopping criteria
        self.epsilon = 0.01

        # best answer
        self.c = sys.maxint - 1
        # next step's best answer
        self.c_prime = sys.maxint

        # number of iterations that algorithm iterates
        self.iterations = 10

        # these variables used for percentage of servers that should be active
        self.initial_percentage = 0
        self.percentage_step = 0.001

    # main body of JCL algorithm
    def optimize(self):
        iterations = self.iterations

        while (abs(self.c - self.c_prime) > self.epsilon) and iterations != 0:
            # 1. choose m_prime randomly
            percentage = self.initial_percentage

            while True:
                self.random_activate_servers(self.datacenter.servers, percentage)

                if self.feasible(self.datacenter):
                    break
                else:
                    percentage += self.percentage_step

            # 2. find lambda_i for minimum c_prime
            solver = Solver(self.datacenter.servers, self.alpha, self.teta, self.datacenter.lamb)
            lambs = solver.solve(False)

            # print(lambs)
            # print("C = " + str(solver.c_prime))
            # print(lambs)

            iterations -= 1

            # 3. if we don't have a better answer, stay in current state
            if solver.c_prime > self.c or solver.c_prime < 0:
                continue

            # 4. with probability 1-p stay in current state
            if random.uniform(0, 1) < 1 - self.transition_probability():
                continue

            # 5. with probability p go to next step
            self.c_prime = self.c
            self.c = solver.c_prime

            for index, server in enumerate(self.datacenter.servers):
                server.lamb = lambs[index]

    # find random subset of servers and make them active
    # make others inactive
    def random_activate_servers(self, servers, percentage):
        for server in servers:
            if random.uniform(0, 1) < percentage:
                server.activate()
            else:
                server.de_active()

    # probability that JCL algorithm moves to next step (p)
    def transition_probability(self):
        delta = self.delta

        try:
            return math.exp(delta * self.c_prime) / (math.exp(delta * self.c_prime) + math.exp(delta * self.c))
        except:
            return 1

    # check if with this set of activated servers
    # all input traffic can be processed
    def feasible(self, datacenter):
        total_capacity = 0

        for server in datacenter.servers:
            if server.active == 1:
                total_capacity += server.mu * server.k

        return datacenter.lamb <= total_capacity