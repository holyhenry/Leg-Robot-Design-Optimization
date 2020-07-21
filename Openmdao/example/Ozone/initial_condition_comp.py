import numpy as np

from openmdao.api import ExplicitComponent


class InitialConditionComp(ExplicitComponent):

    def setup(self):
        self.add_input('theta')
        self.add_input('v')

        self.add_output('vx')
        self.add_output('vy')

        self.declare_partials('*', '*')

    def compute(self, inputs, outputs):
        v = inputs['v']
        theta = inputs['theta']

        outputs['vx'] = v * np.cos(theta)
        outputs['vy'] = v * np.sin(theta)
        
    def compute_partials(self, inputs, partials):
        v = inputs['v']
        theta = inputs['theta']

        partials['vx', 'theta'] = -v * np.sin(theta)
        partials['vy', 'theta'] =  v * np.cos(theta)

        partials['vx', 'v'] = np.cos(theta)
        partials['vy', 'v'] = np.sin(theta)


if __name__ == '__main__':
    from openmdao.api import Problem, Group, IndepVarComp


    prob = Problem()

    group = Group()

    comp = IndepVarComp()
    comp.add_output('v', val=np.random.rand())
    comp.add_output('theta', val=np.random.rand())
    group.add_subsystem('ivc', comp, promotes=['*'])

    comp = InitialConditionComp()
    group.add_subsystem('comp', comp, promotes=['*'])

    prob.model = group

    prob.setup()
    prob.run_model()
    prob.check_partials(compact_print=True)