import numpy as np

from openmdao.api import ExplicitComponent


g = 9.81

class TComp(ExplicitComponent):

    def setup(self):
        self.add_input('vy_m_s')
        self.add_output('tf')
        self.declare_partials('tf', 'vy_m_s', val=2/g)

    def compute(self, inputs, outputs):
        vy_m_s = inputs['vy_m_s']
        outputs['tf'] = 2 * vy_m_s / g