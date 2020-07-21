import numpy as np 
import sympy as sp
import pprint
from sympy.utilities.lambdify import lambdify 

thetaL = sp.symbols('thetaL')
thetaR = sp.symbols('thetaR')
l1 = sp.symbols('l1')
l2 = sp.symbols('l2')
w = 0.07

a       = sp.sqrt(w ** 2 + l1 ** 2 - 2 * w * l1 * sp.cos(thetaR))
alpha   = sp.asin(l1 * sp.sin(thetaR) / a)
L       = sp.sqrt(l1 ** 2 + a ** 2 - 2 * l1 * a * sp.cos(sp.pi - alpha - thetaL))
beta    = sp.asin(a * sp.sin(sp.pi - alpha - thetaL) / L)
thetaL2 = sp.pi - beta

def T(theta, x, y): 
    return sp.Matrix([[sp.cos(theta), -sp.sin(theta), x], 
                    [sp.sin(theta), sp.cos(theta),  y],
                    [0,             0,              1]])

Fk = T(thetaL, w/2, 0) @ T(thetaL2, l1, 0) @ sp.Matrix([L/2, -sp.sqrt(l2 ** 2 - (L/2) ** 2), 1])
Fk = Fk[:2,:]

'''
px_pl1 px_pl2
py_pl1 py_pl2
'''
px_pl = Fk.jacobian([l1,l2]).evalf()
# np.array(px_pl.tolist()).astype(np.float64)
# px_pl1 = px_pl[0,0]
# px_pl2 = px_pl[0,1]
# py_pl1 = px_pl[1,0]
# py_pl2 = px_pl[1,1]

print('shape of px_pl:',np.shape(px_pl))
# pprint.pprint(px_pl[1,1])

'''
px_pthetaL px_pthetaR
py_pthetaL py_pthetaR
'''
px_ptheta = Fk.jacobian([thetaL,thetaR]).evalf()
# np.array(px_ptheta).astype(np.float64)
# px_pthetaL = px_ptheta[0,0]
# px_pthetaR = px_ptheta[0,1]
# py_pthetaL = px_ptheta[1,0]
# py_pthetaR = px_ptheta[1,1]

print('shape of px_pθ:',np.shape(px_ptheta))
# pprint.pprint(px_ptheta[1,1])
