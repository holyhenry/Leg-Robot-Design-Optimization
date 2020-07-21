import numpy as np

from openmdao.api import ExplicitComponent


class DComp(ExplicitComponent):

    def setup(self):
        self.add_input('v_m_s')
        self.add_input('theta_rad')
        self.add_input('tf')
        self.add_output('d')
        self.declare_partials('d', 'v_m_s')
        self.declare_partials('d', 'theta_rad')
        self.declare_partials('d', 'tf')

    def compute(self, inputs, outputs):
        v_m_s = inputs['v_m_s']
        theta_rad = inputs['theta_rad']
        tf = inputs['tf']

        d = v_m_s * np.cos(theta_rad) * tf
        outputs['d'] = d
        print(theta_rad, d)

    def compute_partials(self, inputs, partials):
        v_m_s = inputs['v_m_s']
        theta_rad = inputs['theta_rad']
        tf = inputs['tf']
        partials['d', 'v_m_s'] = np.cos(theta_rad) * tf
        partials['d', 'theta_rad'] = -v_m_s * np.sin(theta_rad) * tf
        partials['d', 'tf'] = v_m_s * np.cos(theta_rad)


if __name__ == '__main__':
    from openmdao.api import Problem, Group, IndepVarComp

    group = Group()

    comp = IndepVarComp()
    comp.add_output('v_m_s')
    comp.add_output('theta_rad')
    comp.add_output('tf')
    group.add_subsystem('comp1', comp)

    comp = DComp()
    group.add_subsystem('comp2', comp) 

    prob = Problem()
    prob.model = group

    prob.setup()
    prob.run_model()
    prob.model.list_outputs()
    prob.check_partials(compact_print=True)