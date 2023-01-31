import autograd.numpy as np
import pymanopt

def pca(data,dim_subspace):
    '''Computes the pca of a dataset using optimisation on a Stiefel manifold.
    :param data a numpy array, whose columns represent the datapoints
    :param dim_subspace the number of orthogonal vectors for which the variance is optmised
    :return numpy array whose columns span the subspace of maximal variance along the dataset
    Taken from example 2.4 from the book https://www.nicolasboumal.net/book/IntroOptimManifolds_Boumal_2022.pdf

    '''
    amb_dim, n_datapoints = np.shape(data)
    # the stiefel manifold parametrises orthonormal sets of vectors, along we wish to optimise
    manifold = pymanopt.manifolds.stiefel.Stiefel(amb_dim, dim_subspace)

    @pymanopt.function.autograd(manifold)
    def cost(u):
        '''The cost function <u data data^T,u D > in numpy. The matrix D is a diagonal matrix representing weights for the functional.'''
        D = np.zeros((dim_subspace, dim_subspace))
        for i in range(dim_subspace):
            D[i, i] = dim_subspace-i
        matrix1 = np.dot(data, np.dot(np.transpose(data), u))
        matrix2 = np.dot(u, D)
        # The cost function is the inner product of the matrices. We need to turn them into vectors to efficiently compute it in numpy
        matrix1_flat = matrix1.reshape(-1, )
        matrix2_flat = matrix2.reshape(-1, )
        return np.dot(matrix1_flat, matrix2_flat)

    #the standard pymanopt syntax
    problem = pymanopt.Problem(manifold, cost)
    optimizer = pymanopt.optimizers.SteepestDescent()
    result = optimizer.run(problem)
    return np.transpose(result.point)

if __name__ == '__main__':
    dim_subspace = 2
    dim_amb = 4
    data_points = 3
    data = np.random.rand(dim_amb,data_points)
    x,y = pca(data,dim_subspace)
    print(np.dot(x,y))
