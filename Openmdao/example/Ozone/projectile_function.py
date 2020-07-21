import numpy as np
import time

from ozone.api import ODEFunction
from projectile_system import ProjectileSystem


class ProjectileFunction(ODEFunction):

    def initialize(self, system_init_kwargs=None):
        self.set_system(ProjectileSystem, system_init_kwargs)

        self.declare_state('x', 'dx_dt', shape=1)
        self.declare_state('y', 'dy_dt', shape=1)
        self.declare_state('vx', 'dvx_dt', shape=1, targets=['vx'])
        self.declare_state('vy', 'dvy_dt', shape=1, targets=['vy'])