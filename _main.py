import numpy as np 
import sympy as sp 
import matplotlib.pyplot as plt
from sympy.utilities.lambdify import lambdify

from _function import five_bar, trajectory

# Set up geomytry--------------------------------------------------------
thetaL_s = sp.symbols('thetaL_s')
thetaR_s = sp.symbols('thetaR_s')

opt = five_bar(thetaL_s, thetaR_s, l1=0.09, l2=0.16, w=0.07)

# Computing Forward Kinematics--------------------------------------------
FK_s = opt.get_FK_s()

# Forward Kinematics Test-------------------------------------------------
s_top    = opt.FK_get_position(0, np.pi)
s_bottom = opt.FK_get_position(np.pi/2, np.pi/2)
s_test   = opt.FK_get_position(0.2 * np.pi, 0.7 * np.pi)
print('\nStarting:', s_top, '\nFurthest:', s_bottom, '\nTest:    ', s_test)

# Converge test-----------------------------------------------------------
theta = opt.PIK_get_theta(-5.80000000e-02, 0.19075104)

# Computing Jacobian------------------------------------------------------
J_s = opt.pre_J_s()

# Generating Sine Trajectory----------------------------------------------
par = [0.12, 0.03, 0.05, 0.18]
ideal_tar = trajectory(par)
[x, y] = ideal_tar.SineTrajectory(num_point = 100)
x_ = np.zeros(len(x), dtype=float)
y_ = np.zeros(len(x), dtype=float)

for i in range(len(x)):
     print(i)
     # [thetaL, thetaR] = opt.PIK_get_theta(x[i], y[i])
     [thetaL, thetaR] = opt.IK_5_link(x[i], y[i])
     # thetaL_[i] = thetaL
     # thetaR_[i] = thetaR
     g = opt.FK_get_position(thetaL, thetaR)
     [x_[i], y_[i]] = g
     # x_[i] = g[0]
     # y_[i] = g[1]

plt.plot(x, y, x_, y_, marker = '*')
plt.title('SineTrajectory')
plt.grid()
plt.show()
