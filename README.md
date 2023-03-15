# manifold optimisation
Implementation of the following examples of manifold optimisation using the python package pymanopt:
- find largest Eigenvalue of a matrix, manifold is a sphere
- compute the PCA of dataset, manifold is the Stiefel manifold
- compute the comass of a differential form, manifold is the Grassmannian
 
## Background and How to use

### largest eigenvalue
This is the toy problem in manifold optimisation. Run the file `largest_eigenvalue/raleigh_quotient.py`. The function returns the eigenvector for the largest eigenvalue of a random matrix using pymanopt and a classical linear algebra algrorithm.

### PCA
The key function is `pca(data,dim_subspace)` in `pca/pca.py`, which computes the pca of any dataset. To visualize the eigenvector with the largest eigenvalue`for a random 2D dataset, run `pca/visualization_2D.py`

### Differential forms
Differential forms are used to generalise the fundamental theorem of calculus to higher dimensions. In $\mathbb{R}^n$, they can be expressed in a particular basis. The co-mass is important in the field of calibrated geometry. It returns to any differential form a real number in a non-linear way. In general it is hard to compute the comass analytically, The point of this module is to give numerical assistance for proving general statements about the comass. To experiment, run the function `compute_comass(manifold, form)`in `comass_differentialforms/compute_comass.py`.
