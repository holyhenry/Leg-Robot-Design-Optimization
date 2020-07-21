import numpy as np
from openmdao.api import ExplicitComponent

class SineTrajectoryComp(ExplicitComponent):

     def setup(self):

          self.add_output('TestPoint_x')
          self.add_output('TestPoint_y')

     def compute(self, inputs, outputs):

          DownAMP      = 0.01
          UpperAMP     = 0.05
          StanceHeight = 0.18
          StepLength   = 0.12

          CurrentPercent = np.array([a/100+0.01 for a in range(100)])
          StancePercent = 0.6
          SwingPercent = 1 - StancePercent

          trajectory_x = np.zeros(len(CurrentPercent), dtype=float)
          trajectory_y = np.zeros(len(CurrentPercent), dtype=float)

          for i in range(len(CurrentPercent)):
               if (CurrentPercent[i] <= StancePercent):
                    trajectory_x[i] = -(StepLength / 2) + (CurrentPercent[i] / StancePercent) * StepLength
                    trajectory_y[i] =  DownAMP * np.sin(np.pi * CurrentPercent[i] / StancePercent) + StanceHeight
               else:
                    trajectory_x[i] = (StepLength / 2) - ((CurrentPercent[i] - StancePercent) / SwingPercent) * StepLength
                    trajectory_y[i] = -UpperAMP * np.sin(np.pi * (CurrentPercent[i] - StancePercent) / SwingPercent) + StanceHeight

          # return the furthest points
          print(trajectory_x[59], trajectory_y[59])
          
          outputs['TestPoint_x'] = trajectory_x[59]
          outputs['TestPoint_y'] = trajectory_y[59]

if __name__ == '__main__':

     from openmdao.api import Problem, Group, IndepVarComp

     group = Group()

     comp = SineTrajectoryComp()
     group.add_subsystem('comp1', comp)

     prob = Problem()
     prob.model = group

     prob.setup()
     prob.run_model()
     prob.model.list_outputs()