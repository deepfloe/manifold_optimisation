import autograd.numpy as np
import pymanopt
from differential_forms_class import Form

manifold = pymanopt.manifolds.grassmann.Grassmann(7,3)

phi = Form({(0,1,2): 1,(0,3,4): -1,(0,5,6):-1,(1,3,5):-1,(1,4,6):1,(2,3,6):-1,(2,4,5):-1})
# the G2 form
@pymanopt.function.autograd(manifold)
def cost(X):
    return -abs(phi.contract(np.transpose(X)).numpy_float())


problem = pymanopt.Problem(manifold, cost)
optimizer = pymanopt.optimizers.SteepestDescent()
result = optimizer.run(problem)
print('The comass is ~: {}'.format(-result.cost))