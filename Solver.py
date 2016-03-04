from scipy.optimize import minimize


class Solver(object):
    # initialize the object
    def __init__(self, servers, alpha, teta, lambda_s):
        self.c_prime = 0

        self.teta = teta
        self.alpha = alpha
        self.lambda_s = lambda_s

        # fill servers specification in arrays for solver use
        self.k = []
        self.a = []
        self.mu = []
        self.lambs = []
        self.bound = []
        self.active = []

        for server in servers:
            self.a.append((server.e_p - server.e_i) / server.mu * server.k)
            self.k.append(server.k)
            self.mu.append(server.mu)
            self.lambs.append(server.lamb)
            self.active.append(server.active)

    # solve sub-problem
    def solve(self, linear):
        if linear:
            return self.linear_solver()
        else:
            return self.non_linear_solver()

    # implementation of linear solver
    # this method uses cvxopt solver
    # visit http://cvxopt.org for more information
    def linear_solver(self):
        print("Initiating linear solver")

    # implementation of non-linear solver
    # this method uses scipy solver
    # visit http://docs.scipy.org for more information
    def non_linear_solver(self):
        print("Initiating non-linear solver")

        for active in self.active:
            print(active)

        cons = [{'type': 'eq', 'fun': self.workload_preserving_constraint}]
        cons += self.inactive_server_constraint(self.lambs)
        cons += self.positive_variables(self.lambs)

        res = minimize(self.objective_function, self.lambs, method='SLSQP', bounds=None, constraints=tuple(cons))

        print(res.x)

        self.c_prime = res.fun

        return res.x

    # definition of objective function
    def objective_function(self, x):
        objective = 0

        for index, lamb in enumerate(x):
            if lamb == 0:
                continue
            objective += self.teta * (lamb / (self.mu[index] - lamb / self.k[index])) + self.alpha * (
                self.a[index] * lamb)

        return objective

    # definition of workload preserving constraint
    def workload_preserving_constraint(self, x):
        constraint = 0

        for index, lamb in enumerate(x):
            constraint += lamb

        constraint -= self.lambda_s

        return constraint

    # definition of inactive server constraint using "Big M" method
    def inactive_server_constraint(self, x):
        constraints = []

        for index, lamb in enumerate(x):
            if self.active[index] == 0:
                continue
            constraints.append({'type': 'ineq', 'fun': lambda x: self.lambda_s - x[index]})

        return constraints

    # all variables must be positive
    def positive_variables(self, x):
        constraints = []

        for index, lamb in enumerate(x):
            if self.active[index] == 0:
                constraints.append({'type': 'eq', 'fun': lambda x: x[index]})
            else:
                constraints.append({'type': 'ineq', 'fun': lambda x: x[index]})

        return constraints
