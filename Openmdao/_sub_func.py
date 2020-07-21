import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import fsolve

def SineTrajectory(DownAMP = 0.01, UpperAMP = 0.05, StanceHeight = 0.18, StepLength = 0.12):

     CurrentPercent = np.array([a/100+0.01 for a in range(100)])
     StancePercent = 0.6
     SwingPercent = 1 - StancePercent

     x = np.zeros(len(CurrentPercent), dtype=float)
     y = np.zeros(len(CurrentPercent), dtype=float)

     for i in range(len(CurrentPercent)):
          if (CurrentPercent[i] <= StancePercent):
               x[i] = -(StepLength / 2) + (CurrentPercent[i] / StancePercent) * StepLength
               y[i] =  DownAMP * np.sin(np.pi * CurrentPercent[i] / StancePercent) + StanceHeight
          else:
               x[i] = (StepLength / 2) - ((CurrentPercent[i] - StancePercent) / SwingPercent) * StepLength
               y[i] = -UpperAMP * np.sin(np.pi * (CurrentPercent[i] - StancePercent) / SwingPercent) + StanceHeight

     return x, y



def Ik_5_link(x, y, l1 = 0.09, l2 = 0.16, w = 0.07):
    
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

def FkGetPosition(thetaL, thetaR, l1 = 0.09, l2 = 0.16):

     w       = 0.07
     a       = np.sqrt(w ** 2 + l1 ** 2 - 2 * w * l1 * np.cos(thetaR))
     alpha   = np.arcsin(l1 * np.sin(thetaR) / a)
     L       = np.sqrt(l1 ** 2 + a ** 2 - 2 * l1 * a * np.cos(np.pi - alpha - thetaL))
     beta    = np.arcsin(a * np.sin(np.pi - alpha - thetaL) / L)
     thetaL2 = np.pi - beta

     '''
     Transmission Matrix
     '''
     def T(theta, x, y): 
          return np.array([[np.cos(theta), -np.sin(theta), x], 
                           [np.sin(theta), np.cos(theta),  y],
                           [0,             0,              1]])

     # Fk = T(thetaL, w/2, 0).dot( T(thetaL2, l1, 0) ).dot(np.array( [L/2, -np.sqrt(l2 ** 2 - (L/2) ** 2), 1]) )
     # Fk = multi_dot([T(thetaL, w/2, 0), T(thetaL2, l1, 0), np.array( [L/2, -np.sqrt(l2 ** 2 - (L/2) ** 2), 1])])
     Fk = T(thetaL, w/2, 0) @ T(thetaL2, l1, 0) @ np.array( [L/2, -np.sqrt(l2 ** 2 - (L/2) ** 2), 1])
     Fk = Fk[:2]
     
     x = Fk[0]
     y = Fk[1]

     return x, y


if __name__ == '__main__':
     
     x = SineTrajectory()[0]
     y = SineTrajectory()[1]

     thetaL = np.zeros(len(x),dtype=float)
     thetaR = np.zeros(len(x),dtype=float)

     for i in range(len(x)):
          theta = Ik_5_link(x[i], y[i])
          # print(theta.x[0], theta.x[1])
          thetaL[i] = theta.x[0]
          thetaR[i] = theta.x[1]

     x_ = FkGetPosition(thetaL, thetaR)[0]
     y_ = FkGetPosition(thetaL, thetaR)[1]

     plt.plot(x_, y_, x, y, marker='*')
     plt.show()

     j = np.min(y_)
     print(j)

     p = FkGetPosition(0, np.pi)
     q = FkGetPosition(0.25*np.pi, 0.75*np.pi)
     r = FkGetPosition(0.5*np.pi, 0.5*np.pi)
     print(p, q, r)