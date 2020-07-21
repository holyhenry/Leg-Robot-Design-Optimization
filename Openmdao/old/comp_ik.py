import numpy as np
import sympy as sp
from sympy.utilities.lambdify import lambdify
from scipy.optimize import minimize
from scipy.optimize import fsolve
from openmdao.api import ExplicitComponent

class IkComp(ExplicitComponent):

     def setup(self):

          self.add_input('x')
          self.add_input('y')
          self.add_input('l1')
          self.add_input('l2')
          self.add_output('thetaL')
          self.add_output('thetaR')

     def compute(self, inputs, outputs):

          x = inputs['x']
          y = inputs['y']
          l1 = inputs['l1']
          l2 = inputs['l2']

          def IK_5_link(x, y, l1, l2, w = 0.07):
          
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

          outputs['thetaL'] = IK_5_link(x, y, l1, l2).x[0]
          outputs['thetaR'] = IK_5_link(x, y, l1, l2).x[1]

if __name__ == '__main__':

     from openmdao.api import Problem, Group, IndepVarComp

     group = Group()

     comp = IndepVarComp()
     comp.add_output('x', val=-0.024021708847354217)
     comp.add_output('y', val=0.12411037295149752)  
     comp.add_output('l1', val=0.09) 
     comp.add_output('l2', val=0.16) 
     group.add_subsystem('comp1', comp, promotes=['*'])

     comp = IkComp()
     group.add_subsystem('comp2', comp, promotes=['*'])

     prob = Problem()
     prob.model = group

     prob.setup()
     prob.run_model()
     prob.model.list_outputs()
     print('theta should be: [0.5, np.pi]')
