import numpy as np
import sympy as sp
from sympy.utilities.lambdify import lambdify
from scipy.optimize import minimize
from scipy.optimize import fsolve

def IK_5_link(x, y, l1 = 0.09, l2 = 0.16, w = 0.07):
    
    def leg_wide(var):
        return np.linalg.norm([var[0], var[1] - np.pi])

    def x_constraint_equation(var):
        # should be equal to zero when the 
        return l1**2 - l2**2 + (x - w/2)**2 + y**2 - 2*l1*(y*np.sin(var[0]) + (x - w/2)*np.cos(var[0]))

    def y_constraint_equation(var):
        return l1**2 - l2**2 + (x + w/2)**2 + y**2 - 2*l1*(y*np.sin(var[1]) + (x + w/2)*np.cos(var[1]))

    
    res = minimize(leg_wide, (0.1, 9*np.pi/10), method="SLSQP", constraints= ({"type": "eq", "fun": x_constraint_equation}, 
                                                                               {"type": "eq", "fun": y_constraint_equation}))
    
    return (res)


# Test, the following theta's correspond to the x-y below
thetaR = .5
thetaL = np.pi
    
x = -0.024021708847354217
y = 0.12411037295149752

res = IK_5_link(x, y)


# print("""Compare the FK position (top) and the IK solution (bottom) method: 
#           \r\n theta_R = {:.4f} \t theta_L = {:.4f} \r\n theta_R = {:.4f} \t theta_L = {:.4f}""".format(thetaR, thetaL, res[0].x[0], res[0].x[1]))

print(res.x)