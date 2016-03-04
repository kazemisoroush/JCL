

class Datacenter():

    # initialize the object
    def __init__(self, lamb):
        # array of servers in the data-center
        self.servers = []
        # input request rate of data-center
        self.lamb = lamb

    # add a server to the data-center
    def add_server(self, server):
        self.servers.append(server)

    # get array of active servers in the data-center
    def active_servers(self):
        active_servers = []

        for server in self.servers:
            if server.active == 1:
                active_servers.append(server)

        return active_servers

    # number of servers in data-center
    def size(self):
        return len(self.servers)

    # TODO: calculate cost of data-center
    def cost(self):
        return self.power() + self.delay()

    # TODO: calculate power consumption of data-center
    def power(self):
        power = 0

        for server in self.servers:
            if server.active == 1:
                power += server.e_i + (server.e_p - server.e_i) * server.utilization()

        return self.alpha * power

    # TODO: calculate delay of data-center
    def delay(self):
        delay = 0

        for server in self.servers:
            if server.active == 1:
                delay += server.lamb / (server.mu - (server.lamb / server.k))

        return self.teta * delay