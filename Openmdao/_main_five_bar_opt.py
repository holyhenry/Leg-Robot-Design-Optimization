import numpy as np
import sympy as sp 
'''
setting up initial values to feed-------------------------
'''
from _sub_func import SineTrajectory, Ik_5_link

x = SineTrajectory()[0]
y = SineTrajectory()[1]

thetaL = np.zeros(len(x),dtype=float)
thetaR = np.zeros(len(x),dtype=float)

for i in range(len(x)):
    theta = Ik_5_link(x[i], y[i])
    thetaL[i] = theta.x[0]
    thetaR[i] = theta.x[1]

'''
model building---------------------------------------------
'''
import openmdao.api as om
from openmdao.api import IndepVarComp
from _sub_comp_fk             import FkComp
from _sub_obj_bar_length      import BarLengthObj

prob = om.Problem() 

# during one iteration, l1, l2 would be scalar, while thetaL, R would be vector of number of point 
comp = IndepVarComp()
comp.add_output('l1', val=0.09) 
comp.add_output('l2', val=0.16) 
comp.add_output('thetaL', val=np.array(thetaL))
comp.add_output('thetaR', val=thetaR)
prob.model.add_subsystem('comp_i', comp)

comp = FkComp()
prob.model.add_subsystem('comp_fk', comp)

comp = BarLengthObj()
prob.model.add_subsystem('obj_bar', comp)

prob.model.connect('comp_i.l1',['comp_fk.l1','obj_bar.l1'])
prob.model.connect('comp_i.l2',['comp_fk.l2','obj_bar.l2'])
prob.model.connect('comp_i.thetaL','comp_fk.thetaL')
prob.model.connect('comp_i.thetaR','comp_fk.thetaR')

'''
setting up model----------------------------------------------
'''
from openmdao.api import Problem, ScipyOptimizeDriver

prob.driver = om.ScipyOptimizeDriver() 
prob.driver.options['optimizer'] = 'SLSQP'

prob.model.add_design_var('comp_i.l1',lower=0)
prob.model.add_design_var('comp_i.l2',lower=0)
prob.model.add_design_var('comp_i.thetaL', lower=-0.2*np.pi, upper=0.2*np.pi)
prob.model.add_design_var('comp_i.thetaR', lower=0.7*np.pi, upper=1.2*np.pi)

prob.model.add_objective('obj_bar.length')

prob.model.add_constraint('comp_fk.x',equals=x)
prob.model.add_constraint('comp_fk.y',equals=y)

prob.setup()
prob.run_model()
prob.model.list_outputs()

prob.run_driver()
print('L1=   ',prob['comp_i.l1'])
print('L2=   ',prob['comp_i.l2'])
print('Total=',prob['obj_bar.length'])
