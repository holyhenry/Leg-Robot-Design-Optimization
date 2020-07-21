import numpy as np

from openmdao.api import ExplicitComponent


# Dynamics---original, 2nd order:
# x''=0
# y''=-g
# Dynamics---modified, 1st order:
# (x )' = x'
# (y )' = y'
# (x')' = 0
# (y')' = -g
# Initial conditions:
# (x )_0 = 0
# (y )_0 = 0
# (x')_0 = v * cos(theta)
# (y')_0 = v * sin(theta)
# Constraints:
# (y )_f = 0 
# Objective:
# (x )_f  [maximize!]

class ProjectileSystem(ExplicitComponent):

    def initialize(self):
        self.options.declare('num_nodes', default=1, types=int)

        self.g = -9.81

    def setup(self):
        num = self.options['num_nodes']

        self.add_input('vx', shape=(num, 1))
        self.add_input('vy', shape=(num, 1))

        self.add_output('dx_dt', shape=(num, 1))
        self.add_output('dy_dt', shape=(num, 1))
        self.add_output('dvx_dt', shape=(num, 1))
        self.add_output('dvy_dt', shape=(num, 1))

        self.declare_partials('*', '*', dependent=False)

        self.declare_partials('dx_dt', 'vx', val=1., rows=np.arange(num), cols=np.arange(num))
        self.declare_partials('dy_dt', 'vy', val=1., rows=np.arange(num), cols=np.arange(num))

    def compute(self, inputs, outputs):
        outputs['dx_dt'] = inputs['vx']
        outputs['dy_dt'] = inputs['vy']
        outputs['dvx_dt'] = 0.
        outputs['dvy_dt'] = self.g
