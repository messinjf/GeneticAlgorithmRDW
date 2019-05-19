# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 08:55:30 2019

@author: messinjf
"""

import numpy as np
import matplotlib.pyplot as plt

n = 10
bounds = [np.array([0,0]), np.array([n,0]), np.array([n,2*n]), np.array([0.5 * n, 2 * n]), np.array([0, n])]
#bounds = [np.array([0,0]), np.array([n,0]), np.array([n,n]), np.array([0,n])]
for i in range(4):
    subdivide_bounds = []
    for i in range(-1,len(bounds)-1):
        bound_center = (bounds[i] + bounds[i+1]) / 2
        
        subdivide_bounds.append(bounds[i])
        subdivide_bounds.append(bound_center)
        subdivide_bounds.append(bounds[i+1])
    bounds = subdivide_bounds


def control(X,Y):
    R = X * 0 + Y * 0
    U, V = R * np.cos(T), R * np.sin(T)
    return U, V

def centroid(bounds):
    C_x = 0
    C_y = 0
    A = 0
    for i in range(-1,len(bounds)-1):
        x_0 = bounds[i][0]
        x_1 = bounds[i+1][0]
        y_0 = bounds[i][1]
        y_1 = bounds[i+1][1]
        C_x += (x_0 + x_1) * (x_0*y_1-x_1*y_0)
        C_y += (y_0 + y_1) * (x_0*y_1-x_1*y_0)
        A += 0.5 * (x_0*y_1-x_1*y_0)
    C_x /= 6 * A
    C_y /= 6 * A
    
    return np.array([C_x, C_y])
        
        

def STC(X,Y):
    U = np.zeros(X.shape)
    V = np.zeros(Y.shape)
    center = centroid(bounds)
    for x_i in range(len(X)):
        for y_i in range(len(X[0])):
            p = np.array([X[x_i][y_i],Y[x_i][y_i]])
            force = (center - p) / np.linalg.norm(center - p)
            U[x_i, y_i] = force[0]
            V[x_i, y_i] = force[1]
    return U, V

def APFForceOnPoint(p, C=0.00897, lambda_const=2.656):
    force = np.zeros(p.shape)
    #print("p = {}".format(p))
    #print("force = {}".format(force))
    for i in range(-1,len(bounds)-1):
        bound_center = (bounds[i] + bounds[i+1]) / 2
        #print(bound_center)
        wall_length = np.linalg.norm(bounds[i] - bounds[i+1])
        d = p - bound_center
        force += d * C * wall_length / (np.linalg.norm(d) ** lambda_const)
    return force
        

def APF(X,Y):
    U = np.zeros(X.shape)
    V = np.zeros(Y.shape)
    for x_i in range(len(X)):
        for y_i in range(len(X[0])):
            p = np.array([X[x_i][y_i],Y[x_i][y_i]])
            force = APFForceOnPoint(p)
            R = np.linalg.norm(force)
            U[x_i, y_i] = force[0] / R ** 0.5
            V[x_i, y_i] = force[1] / R ** 0.5
    return U, V

def plot_polygon(bounds):
    xs, ys = zip(*bounds)
    xs = list(xs)
    ys = list(ys)
    xs.append(xs[0])
    ys.append(ys[0])
    plt.plot(xs, ys)
            


X, Y = np.mgrid[1:n, 1:2*n:2]

#R = 10 + np.sqrt((Y - n / 2.0) ** 2 + (X - n / 2.0) ** 2)
#U, V = R * np.cos(T), R * np.sin(T)
#U,V = STC(X,Y)


plt.figure(figsize=(10,5))
plt.xlim(0, n)
plt.xticks(())
plt.ylim(0, 2*n)
plt.yticks(())
plt.axis('equal')
plt.suptitle("Direction Users are Steered")

#plt.axes([0.025, 0.025, 0.95, 0.95])
#plt.quiver(X, Y, U, V, R, alpha=.5)
plt.subplot(1,2,1)
plt.xticks(())
plt.yticks(())
plt.title("STC")
plot_polygon(bounds)
U,V = STC(X,Y)
plt.quiver(X, Y, U, V, edgecolor='k', facecolor='None', linewidth=.5)
plt.subplot(1,2,2)
plt.xticks(())
plt.yticks(())
plt.title("APF")
plot_polygon(bounds)
U,V = APF(X,Y)
plt.quiver(X, Y, U, V, edgecolor='k', facecolor='None', linewidth=.5)

plt.show()