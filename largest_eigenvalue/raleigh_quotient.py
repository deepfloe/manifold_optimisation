import autograd.numpy as np
import pymanopt
import pymanopt.manifolds
import pymanopt.optimizers
# this is a minimally modified version of the example https://pymanopt.org/docs/stable/quickstart.html#installation

def compute_largest_ev(dim = 3):
    np.random.seed(42)
    manifold = pymanopt.manifolds.Sphere(dim)

    matrix = np.random.normal(size=(dim, dim))
    matrix = 0.5 * (matrix + matrix.T)

    @pymanopt.function.autograd(manifold)
    def cost(point):
        return -np.dot(point,(np.dot(matrix,point)))


    problem = pymanopt.Problem(manifold, cost)
    optimizer = pymanopt.optimizers.SteepestDescent()
    result = optimizer.run(problem)

    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    dominant_eigenvector = eigenvectors[:, eigenvalues.argmax()]
    return dominant_eigenvector, result.point

if __name__ == "__main__":
    linalg_sol, pyman_sol = compute_largest_ev(dim=3)
    print("Dominant eigenvector:", linalg_sol)
    print("Pymanopt solution:", pyman_sol)