import numpy as np
import openmdao.api as om
from openmdao.api import Group, IndepVarComp

from comp_fk             import FkComp
from obj_bar_length      import BarLengthObj

class FiveBarOptGroup(Group):

     def setup(self):

          comp = IndepVarComp()
          comp.add_output('l1') 
          comp.add_output('l2') 
          comp.add_output('thetaL')
          comp.add_output('thetaR')
          self.add_subsystem('i_comp', comp, promotes=['*'])

          comp = FkComp()
          self.add_subsystem('comp_fk', comp, promotes=['*']) 

          comp = BarLengthObj()
          self.add_subsystem('bar_length_obj', comp, promotes=['*'])


from openmdao.api import Problem, ScipyOptimizeDriver

prob = Problem()
prob.model = FiveBarOptGroup()

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['tol'] = 1e-8

from func import SineTrajectory
x = SineTrajectory()[0]
y = SineTrajectory()[1]

prob.model.add_design_var('l1',lower=0, upper=0.09)
prob.model.add_design_var('l2',lower=0, upper=0.16)
prob.model.add_design_var('thetaL', lower=0, upper=np.pi)
prob.model.add_design_var('thetaR', lower=0, upper=np.pi)
prob.model.add_objective('length')
prob.model.add_constraint('x', equals=x)
prob.model.add_constraint('y', equals=y)

prob.setup()
prob.run_model()
prob.model.list_outputs()

prob.run_driver()
print(prob['l1'])
print(prob['l2'])
print(prob['length'])


