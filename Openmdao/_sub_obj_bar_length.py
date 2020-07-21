import numpy as np
from openmdao.api import ExplicitComponent

class BarLengthObj(ExplicitComponent):

     def setup(self):
          self.add_input('l1')
          self.add_input('l2')

          self.add_output('length')

          self.declare_partials('length', 'l1', val=1)
          self.declare_partials('length', 'l2', val=1)

     def compute(self, inputs, outputs):
          l1 = inputs['l1']
          l2 = inputs['l2']
          outputs['length'] = l1 + l2

if __name__ == '__main__':
     from openmdao.api import Group, Problem, IndepVarComp
     group = Group()

     comp = IndepVarComp()
     comp.add_output('l1', val=0.09) 
     comp.add_output('l2', val=0.16) 
     group.add_subsystem('comp1', comp)

     comp = BarLengthObj()
     group.add_subsystem('comp2', comp)

     group.connect('comp1.l1', 'comp2.l1')
     group.connect('comp1.l2', 'comp2.l2')

     prob = Problem()
     prob.model = group

     prob.setup()
     prob.run_model()
     prob.model.list_outputs()
     prob.check_partials(compact_print=True)