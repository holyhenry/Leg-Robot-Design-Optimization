import numpy as np

from openmdao.api import Group, IndepVarComp
from vy_comp import VyComp
from t_comp import TComp
from d_comp import DComp


class DistGroup(Group):

    def setup(self):
        comp = IndepVarComp()
        comp.add_output('v_m_s')
        comp.add_output('theta_rad')
        self.add_subsystem('i_comp', comp, promotes=['*'])

        comp = VyComp()
        self.add_subsystem('vy_comp', comp, promotes=['*'])

        comp = TComp()
        self.add_subsystem('t_comp', comp, promotes=['*'])

        comp = DComp()
        self.add_subsystem('d_comp', comp, promotes=['*'])


if __name__ == '__main__':
    from openmdao.api import Problem, ScipyOptimizeDriver

    prob = Problem()
    prob.model = DistGroup()

    prob.model.add_design_var('theta_rad', lower=0, upper=np.pi/2.)
    prob.model.add_objective('d', scaler=-1.)

    prob.driver = ScipyOptimizeDriver()
    prob.driver.options['optimizer'] = 'SLSQP'

    prob.setup()
    prob.run_model()
    prob.model.list_outputs()
    # prob.check_partials(compact_print=True)

    prob.run_driver()
    print(prob['i_comp.v_m_s'])
