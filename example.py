import sys


from RVO import RVO_update, reach, compute_V_des, reach
from vis import visualize_traj_dynamic, get_cmap
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#------------------------------
#define workspace model
ws_model = dict()
#robot radius
ws_model['robot_radius'] = 0.2
#circular obstacles, format [x,y,rad]
# no obstacles
# ws_model['circular_obstacles'] = []
# with obstacles
ws_model['circular_obstacles'] = [[-0.3, 2.5, 0.3], [1.5, 2.5, 0.3], [3.3, 2.5, 0.3], [5.1, 2.5, 0.3]]
#rectangular boundary, format [x,y,width/2,heigth/2]
ws_model['boundary'] = []

#------------------------------
#initialization for robot
# position of [x,y]
X = [[-0.5+1.0*i, 0.0] for i in range(7)] + [[-0.5+1.0*i, 5.0] for i in range(7)]
# velocity of [vx,vy]
V = [[0,0] for i in range(len(X))]
# maximal velocity norm
V_max = [1.0 for i in range(len(X))]
# goal of [x,y]
goal = [[5.5-1.0*i, 5.0] for i in range(7)] + [[5.5-1.0*i, 0.0] for i in range(7)]

#------------------------------
#simulation setup
# total simulation time (s)
total_time = 15
# simulation step
step = 0.01

#------------------------------
#simulation starts
t = 0

figure = plt.figure()
ax = figure.add_subplot(1,1,1)

tp = []
cmap = get_cmap(len(X))
for i in range(len(X)):
    a, = ax.plot(X[i][0], X[i][1], 'o', color=cmap(i))
    tp.append(a)

for hole in ws_model['circular_obstacles']:
    print(hole)
    ax.add_patch(
       patches.Circle(
           (hole[0], hole[1]),      # (x, y) coordinates of center point
           radius = hole[2],     # radius
           edgecolor = 'black',
           linestyle = 'dotted',
           fill = True,
           facecolor = 'lightgray',
       ))
# plt.show()
while t*step < total_time:
    # compute desired vel to goal
    V_des = compute_V_des(X, goal, V_max)
    # compute the optimal vel to avoid collision
    V = RVO_update(X, V_des, V, ws_model)
    # update position

    for i in range(len(X)):
        X[i][0] += V[i][0]*step
        X[i][1] += V[i][1]*step

        tp[i].set_xdata(X[i][0])
        tp[i].set_ydata(X[i][1])
    plt.pause(0.01)

    #----------------------------------------
    # visualization

    #if t%10 == 0:
        #visualize_traj_dynamic(ws_model, X, V, goal, time=t*step, name='data/snap%s.png'%str(t/10))
        #visualize_traj_dynamic(ws_model, X, V, goal, time=t*step, name='data/snap%s.png'%str(t/10))
    t += 1