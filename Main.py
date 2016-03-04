import random
from Jcl import Jcl
from Datacenter import Datacenter
from Server import Server
import time


start = time.time()
print("Algorithm started.")


m = 10
lamb = random.randint(50, 150)

datacenter = Datacenter(lamb)

# make some servers
for i in range(0, m):
    server = Server()
    # server.set_active(random.randint(0, 1))
    server.set_active(1)
    datacenter.add_server(server)

# turn on some of the servers
for server in datacenter.servers:
    if server.active:
        server.set_lambda(datacenter.lamb / len(datacenter.active_servers()))

jcl = Jcl(datacenter)

jcl.optimize()


end = time.time()

print("Algorithm ended. Time spent: " + str(end - start) + " (ms)")