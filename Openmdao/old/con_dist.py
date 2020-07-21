import numpy as np
from openmdao.api import ExplicitComponent

from fk_comp import FkComp
from sin_trajectory_comp import SineTrajectoryComp

class DistCon(ExplicitComponent):

     def setup(self):
          
          self.add_input('x')
          self.add_input('y')
          self.add_input('TestPoint_x')
          self.add_input('TestPoint_y')
          self.add_output('dist')

     def compute(self, inputs, outputs):

          x = inputs['x']
          y = inputs['y']
          TestPoint_x = inputs['TestPoint_x']
          TestPoint_y = inputs['TestPoint_y']
          outputs['dist'] = np.linalg.norm([x - TestPoint_x, y - TestPoint_y])

if __name__ == '__main__':

     from openmdao.api import Problem, Group, IndepVarComp

     group = Group()

     comp = IndepVarComp()
     comp.add_output('thetaL')
     comp.add_output('thetaR')  
     comp.add_output('l1') 
     comp.add_output('l2') 
     group.add_subsystem('i_comp', comp, promotes=['*'])

     comp = FkComp()
     group.add_subsystem('fk_comp', comp, promotes=['*'])

     comp = SineTrajectoryComp()
     group.add_subsystem('sin_trajectory_comp', comp, promotes=['*'])

     comp = DistCon()
     group.add_subsystem('dist_comp', comp, promotes=['*'])

     prob = Problem()
     prob.model = group

     prob.setup()
     prob.run_model()
     prob.model.list_outputs()