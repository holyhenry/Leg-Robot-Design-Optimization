import numpy as np
import matplotlib.pyplot as plt
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from ozone.api import ODEIntegrator
from projectile_function import ProjectileFunction


ode_function = ProjectileFunction()

t0 = 0.
t1 = 1.
initial_conditions = {
    'x': 0.,
    'y': 0.,
    # 'vx': 1.,
    # 'vy': 1.,
}

num = 100
method_name = 'ForwardEuler'
formulation = 'time-marching'

initial_time = 0.
normalized_times = np.linspace(0., 1, num)

integrator = ODEIntegrator(
    ode_function, formulation, method_name,
    initial_time=initial_time, normalized_times=normalized_times,
    initial_conditions=initial_conditions,
)

group = Group()
group.add_subsystem('final_time_comp', IndepVarComp('final_time', val=1.0))
group.add_subsystem('theta_comp', IndepVarComp('theta', val=np.pi/3.))
group.add_subsystem('v_comp', IndepVarComp('v', val=1.))
group.add_subsystem('vx_comp', ExecComp('vx = v * cos(theta)'))
group.add_subsystem('vy_comp', ExecComp('vy = v * sin(theta)'))
group.add_subsystem('integrator_group', integrator)

group.connect('final_time_comp.final_time', 'integrator_group.final_time')
group.connect('theta_comp.theta', 'vx_comp.theta')
group.connect('theta_comp.theta', 'vy_comp.theta')
group.connect('v_comp.v', 'vx_comp.v')
group.connect('v_comp.v', 'vy_comp.v')

group.connect('vx_comp.vx', 'integrator_group.initial_condition:vx')
group.connect('vy_comp.vy', 'integrator_group.initial_condition:vy')

group.add_design_var('final_time_comp.final_time', lower=1e-3)
group.add_design_var('theta_comp.theta', lower=0., upper=np.pi/2.)
group.add_constraint('integrator_group.state:y', indices=[-1], equals=0.)
group.add_objective('integrator_group.state:x', index=-1, scaler=-1.)

prob = Problem()
prob.model = group

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
# from openmdao.api import pyOptSparseDriver
# prob.driver = driver = pyOptSparseDriver()
# driver.options['optimizer'] = 'SNOPT'
# driver.opt_settings['Verify level'] = 0
# driver.opt_settings['Major iterations limit'] = 200 #1000
# driver.opt_settings['Minor iterations limit'] = 1000
# driver.opt_settings['Iterations limit'] = 100000
# driver.opt_settings['Major step limit'] = 2.0
# driver.opt_settings['Major feasibility tolerance'] = 1.0e-6
# driver.opt_settings['Major optimality tolerance'] = 1.0e-6
# driver.opt_settings['Minor feasibility tolerance'] = 1.0e-6

prob.setup()
prob.run_model()
# prob.check_partials(compact_print=True); exit()
prob.run_driver()

print(prob['theta_comp.theta'])

plt.plot(prob['integrator_group.state:x'], prob['integrator_group.state:y'])
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.show()
