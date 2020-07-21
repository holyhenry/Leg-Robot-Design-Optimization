import numpy as np

from openmdao.api import ExplicitComponent


class VyComp(ExplicitComponent):

    def setup(self):
        self.add_input('v_m_s')
        self.add_input('theta_rad')

        self.add_output('vy_m_s')

        self.declare_partials('vy_m_s', 'v_m_s')
        self.declare_partials('vy_m_s', 'theta_rad')

    def compute(self, inputs, outputs):
        v_m_s = inputs['v_m_s']
        theta_rad = inputs['theta_rad']
        outputs['vy_m_s'] = v_m_s * np.sin(theta_rad)

    def compute_partials(self, inputs, partials):
        v_m_s = inputs['v_m_s']
        theta_rad = inputs['theta_rad']

        partials['vy_m_s', 'v_m_s'] = np.sin(theta_rad)
        partials['vy_m_s', 'theta_rad'] = v_m_s * np.cos(theta_rad)


if __name__ == '__main__':
    from openmdao.api import Problem, Group, IndepVarComp
    group = Group()

    comp = IndepVarComp()
    comp.add_output('v_m_s')
    comp.add_output('theta_rad')
    group.add_subsystem('comp1', comp)

    comp = VyComp()
    group.add_subsystem('comp2', comp)

    group.connect('comp1.v_m_s', 'comp2.v_m_s') 
    group.connect('comp1.theta_rad', 'comp2.theta_rad') 

    prob = Problem()
    prob.model = group

    prob.setup()
    prob.run_model()
    prob.model.list_outputs()
    prob.check_partials(compact_print=True)