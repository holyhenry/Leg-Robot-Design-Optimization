import numpy as np
from openmdao.api import ExplicitComponent

from comp_fk import FkComp

class StancePointCon(ExplicitComponent):

    def setup(self):
          
        self.add_input('x')
        self.add_input('y')
        self.add_output('stance_dist')

    def compute(self, inputs, outputs):

        x = inputs['x']
        y = inputs['y']

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

        TestPoint_x = trajectory_x[29]
        TestPoint_y = trajectory_y[29]

        outputs['stance_dist'] = np.linalg.norm([x - TestPoint_x, y - TestPoint_y])

if __name__ == '__main__':

    from openmdao.api import Problem, Group, IndepVarComp

    group = Group()

    comp = IndepVarComp()
    comp.add_output('l1') 
    comp.add_output('l2') 
    group.add_subsystem('i_comp', comp, promotes=['*'])

    comp = FkComp()
    group.add_subsystem('fk_comp', comp, promotes=['*'])

    comp = StancePointCon()
    group.add_subsystem('stance_con', comp, promotes=['*'])

    prob = Problem()
    prob.model = group

    prob.setup()
    prob.run_model()
    prob.model.list_outputs()