import numpy as np
import numpy.linalg as LA
from matplotlib import pyplot as plt
from matplotlib import animation

nx = 150
ny = 150

class car:
    def __init__(self):
        self.wheelbase = 4
        self.width = 2
        self.wheel = 0.5
        self.drawing = np.zeros((14, 2))
        self.alpha = 0
        self.psi = 0
        self.x = 0
        self.y = 0
        self.sz = 0.5
        self.dt = 10
        self.v = 0

    def draw_init(self, ax, center, psi):
        self.x = center[0]
        self.y = center[1]
        self.psi = psi
        line = []
        a, = ax.plot([-1 + center[0], 1 + center[0]], [2 + center[1], 2 + center[1]], 'b')
        line.append(a)
        a, = ax.plot([-1 + center[0], 1 + center[0]], [-2 + center[1], -2 + center[1]], 'b')
        line.append(a)
        a, = ax.plot([0 + center[0], 0 + center[0]], [-2 + center[1], 2 + center[1]], 'b')
        line.append(a)
        a, = ax.plot([1 + center[0], 1 + center[0]], [1.5 + center[1], 2.5 + center[1]], 'b')
        line.append(a)
        a, = ax.plot([-1 + center[0], -1 + center[0]], [1.5 + center[1], 2.5 + center[1]], 'b')
        line.append(a)
        a, = ax.plot([1 + center[0], 1 + center[0]], [-1.5 + center[1], -2.5 + center[1]], 'b')
        line.append(a)
        a, = ax.plot([-1 + center[0], -1 + center[0]], [-1.5 + center[1], -2.5 + center[1]], 'b')
        line.append(a)
        return line

    def gen_triangle(self, center, psi, alpha):
        x2 = -2 * self.sz * np.sin(psi) + center[0]
        y2 = +2 * self.sz * np.cos(psi) + center[1]
        x1 = -1 * self.sz * np.cos(psi) + x2
        y1 = -1 * self.sz * np.sin(psi) + y2
        x3 = +1 * self.sz * np.cos(psi) + x2
        y3 = +1 * self.sz * np.sin(psi) + y2

        x5 = +2 * self.sz * np.sin(psi) + center[0]
        y5 = -2 * self.sz * np.cos(psi) + center[1]
        x4 = -1 * self.sz * np.cos(psi) + x5
        y4 = -1 * self.sz * np.sin(psi) + y5
        x6 = +1 * self.sz * np.cos(psi) + x5
        y6 = +1 * self.sz * np.sin(psi) + y5

        x7 = x1 - 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        x8 = x1 + 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        x9 = x3 - 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        x10 = x3 + 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        y7 = y1 + 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)
        y8 = y1 - 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)
        y9 = y3 + 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)
        y10 = y3 - 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)

        x11 = x4 - 0.5 * self.sz * np.sin(psi)
        x12 = x4 + 0.5 * self.sz * np.sin(psi)
        x13 = x6 - 0.5 * self.sz * np.sin(psi)
        x14 = x6 + 0.5 * self.sz * np.sin(psi)
        y11 = y4 + 0.5 * self.sz * np.cos(psi)
        y12 = y4 - 0.5 * self.sz * np.cos(psi)
        y13 = y6 + 0.5 * self.sz * np.cos(psi)
        y14 = y6 - 0.5 * self.sz * np.cos(psi)
        mat_ = [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7], [x8, y8], [x9, y9], [x10, y10], [x11, y11], [x12, y12], [x13, y13], [x14, y14]]
        return mat_

    def move(self, goal):

        if np.cross([goal[0] - self.x, goal[1] - self.y, 0], [np.sin(self.psi), -np.cos(self.psi), 0])[2] > 0:
            self.alpha += 1
            self.alpha = min(self.alpha, 20)
        else:
            self.alpha -= 1
            self.alpha = max(self.alpha, -20)
        if LA.norm([goal[0] - self.x, goal[1] - self.y]) > 5:
            self.v += 0.1
            self.v = min(self.v, 0.1)
        else:
            self.v -= 0.1
            self.v = max(0, self.v)

        self.psi += self.v * np.sin(self.alpha * np.pi / 180) * self.dt / 4
        print(self.alpha, self.psi)
        if self.psi > np.pi:
            self.psi -= 2 * np.pi
        elif self.psi < -np.pi:
            self.psi += 2 * np.pi
        self.x += self.v * self.dt * np.sin(-self.psi)
        self.y += self.v * self.dt * np.cos(self.psi)
        mat = self.gen_triangle([self.x, self.y], self.psi, self.alpha)
        return mat


class rvo_:
    def __init__(self):
        self.fig = plt.figure()
        plt.axis([-nx, nx, -ny, ny])
        self.ax = plt.gca()
        self.ax.set_aspect(1)
        self.alpha = 0
        self.v = 0
        self.dt = 1
        self.x = 0
        self.y = 0
        self.psi = 0
        self.sz = 0.5

        self.cc = []
        self.pos = []
        self.psi = []
        self.goal = []
        r = 100
        for i in range(50):
            self.cc.append(car())
            self.pos.append([r * np.cos(i/100 * np.pi * 2), r * np.sin(i/100 * np.pi * 2)])
            self.psi.append(i/100 * np.pi * 2)
            self.goal.append([r * np.cos(i/100 * np.pi * 2 + np.pi), r * np.sin(i/100 * np.pi * 2 + np.pi)])

        # self.pos = [[0,0], [20, 0], [40, 0], [60, 0], [80, 0], [0,20], [20, 20], [40, 20], [60, 20], [80, 20]]
        # self.goal = [[80,20], [60, 20], [40, 20], [20, 20], [0, 20], [80,0], [60, 0], [40, 0], [20, 0], [0, 0]]
        # self.psi = [0, 0, 0, 0, 0, np.pi, np.pi, np.pi, np.pi, np.pi]
        self.line = []
        for i in range(len(self.cc)):
            tp = self.cc[i].draw_init(self.ax, self.pos[i], self.psi[i])
            for j in range(7):
                self.line.append(tp[j])

    def gen_triangle(self, center, psi, alpha):
        x2 = -2 * self.sz * np.sin(psi) + center[0]
        y2 = +2 * self.sz * np.cos(psi) + center[1]
        x1 = -1 * self.sz * np.cos(psi) + x2
        y1 = -1 * self.sz * np.sin(psi) + y2
        x3 = +1 * self.sz * np.cos(psi) + x2
        y3 = +1 * self.sz * np.sin(psi) + y2

        x5 = +2 * self.sz * np.sin(psi) + center[0]
        y5 = -2 * self.sz * np.cos(psi) + center[1]
        x4 = -1 * self.sz * np.cos(psi) + x5
        y4 = -1 * self.sz * np.sin(psi) + y5
        x6 = +1 * self.sz * np.cos(psi) + x5
        y6 = +1 * self.sz * np.sin(psi) + y5

        x7 = x1 - 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        x8 = x1 + 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        x9 = x3 - 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        x10 = x3 + 0.5 * self.sz * np.sin(psi+alpha*np.pi/180)
        y7 = y1 + 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)
        y8 = y1 - 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)
        y9 = y3 + 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)
        y10 = y3 - 0.5 * self.sz * np.cos(psi+alpha*np.pi/180)

        x11 = x4 - 0.5 * self.sz * np.sin(psi)
        x12 = x4 + 0.5 * self.sz * np.sin(psi)
        x13 = x6 - 0.5 * self.sz * np.sin(psi)
        x14 = x6 + 0.5 * self.sz * np.sin(psi)
        y11 = y4 + 0.5 * self.sz * np.cos(psi)
        y12 = y4 - 0.5 * self.sz * np.cos(psi)
        y13 = y6 + 0.5 * self.sz * np.cos(psi)
        y14 = y6 - 0.5 * self.sz * np.cos(psi)
        mat_ = [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7], [x8, y8], [x9, y9], [x10, y10], [x11, y11], [x12, y12], [x13, y13], [x14, y14]]
        return mat_

    def ani_init(self):
        # initialize an empty list of cirlces
        return self.line

    def car_update(self, start, mat):
        self.line[0+start].set_xdata([mat[0][0], mat[2][0]])
        self.line[0+start].set_ydata([mat[0][1], mat[2][1]])
        self.line[1+start].set_xdata([mat[3][0], mat[5][0]])
        self.line[1+start].set_ydata([mat[3][1], mat[5][1]])
        self.line[2+start].set_xdata([mat[1][0], mat[4][0]])
        self.line[2+start].set_ydata([mat[1][1], mat[4][1]])

        self.line[3+start].set_xdata([mat[6][0], mat[7][0]])
        self.line[3+start].set_ydata([mat[6][1], mat[7][1]])
        self.line[4+start].set_xdata([mat[8][0], mat[9][0]])
        self.line[4+start].set_ydata([mat[8][1], mat[9][1]])

        self.line[5+start].set_xdata([mat[10][0], mat[11][0]])
        self.line[5+start].set_ydata([mat[10][1], mat[11][1]])
        self.line[6+start].set_xdata([mat[12][0], mat[13][0]])
        self.line[6+start].set_ydata([mat[12][1], mat[13][1]])

    def ani_update(self, i):
        # draw circles, select to color for the circles based on the input argument i.
        for j in range(len(self.cc)):
            mat = self.cc[j].move(self.goal[j])
            self.car_update(7*j, mat)

        return self.line

    def animate(self):
        self.anim = animation.FuncAnimation(self.ax.figure, self.ani_update, init_func=self.ani_init, frames=50, interval=50,
                                            blit=False)
    def run(self):
        self.animate()

vv = rvo_()
vv.run()
plt.show()
