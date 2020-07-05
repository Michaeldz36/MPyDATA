import numpy as np
from pynverse import inversefunc


default_dx = 0.05
default_dt = 0.01
default_gridsize = 16

class Setup:
    def __init__(self, dx = default_dx, dt = default_dt, gridsize = default_gridsize, nt = 500):
        self.dx = dx
        self.dt = dt
        self.nt = nt
        self.grid = np.linspace(-8, 8, int(gridsize/ dx))
        self.g = 1
        self.eps = 1e-8

        self.tt = lambda x: 1 / 2 * (np.sqrt(x * (x - 1)) + np.log(np.sqrt(x - 1) + np.sqrt(x)))
        self.lbd = inversefunc(self.tt)
        self.lbd_t = lambda t: 2 * np.sqrt(1 - 1/self.lbd(t))


    def H0(self, x):
        return np.where(abs(x) < 1, 1 - x**2, 0)

    def analytic_H(self, x, t, xc=0):
        H = (1/self.lbd(t)) * (1 - ((x-xc) / self.lbd(t)) ** 2)
        return np.where((x-xc)**2 < self.lbd(t)**2, H, 0)

    def analytic_u(self, x, t, xc=0):
        u = (x-xc) * (self.lbd_t(t) / self.lbd(t))
        return np.where((x-xc)**2 < self.lbd(t)**2, u, 0)

    def C(self, x):
        return 2* self.analytic_u(x, self.nt*self.dt) * self.dt/self.dx # TODO!!!!

class S2D:
    def __init__(self, dx = default_dx, dt = default_dt, gridsize = default_gridsize, nt = 500):
        self.dx = dx
        self.dy = dx # TODO
        self.dt = dt
        self.nt = nt
        self.x = np.linspace(-8, 8, int(gridsize/ dx))
        self.y = np.linspace(-8, 8, int(gridsize/ dx))
        self.xgrid, self.ygrid = np.meshgrid(self.x, self.y)



        self.lbd = lambda t: (2 * t ** 2 + 1) ** 1 / 2

    def H0(self, x, y):
        return np.where(abs(x)+abs(y) < 1, 1 - x**2 - y**2, 0)


    def analytic_H2(self, x, y, t):
        return np.where(x**2 + y**2 <= self.lbd(t)**2, self.lbd(t)**-2 * (1 - (x**2 + y**2)/ self.lbd(t)**2), 0)

