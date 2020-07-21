import numpy as np
import matplotlib.pyplot as plt
from openmdao.api import Problem
from ozone.api import ODEIntegrator
from projectile_function import ProjectileFunction


ode_function = ProjectileFunction()

t0 = 0.
t1 = 1.
initial_conditions = {
    'x': 0.,
    'y': 0.,
    'vx': 1.,
    'vy': 1.,
}

num = 100

times = np.linspace(t0, t1, num)

method_name = 'RK4'
formulation = 'solver-based'

integrator = ODEIntegrator(ode_function, formulation, method_name,
    times=times, initial_conditions=initial_conditions,
)

prob = Problem(integrator)
prob.setup()
prob.run_model()

plt.plot(prob['state:x'], prob['state:y'])
plt.xlabel('x')
plt.ylabel('y')
plt.show()
