import random


class Server(object):

    # initialize the object
    def __init__(self):
        # number of virtual machines in server
        self.k = random.randint(4, 10)
        # service rate of server
        self.mu = random.randint(3, 10)
        # idle power of server
        self.e_i = random.randint(200, 250)
        # peak power of server
        self.e_p = random.randint(400, 500)
        # is server activated or not
        self.active = 0
        # input request rate of server
        self.lamb = 0

    # utilization of server
    def utilization(self):
        return self.lamb / (self.k * self.mu)

    # activate the server
    def activate(self):
        self.active = 1

    # de-activate the server
    def de_active(self):
        self.active = 0

    # activate the server
    def set_active(self, active):
        self.active = active

    # set input request rate of server
    def set_lambda(self, lamb):
        self.lamb = lamb