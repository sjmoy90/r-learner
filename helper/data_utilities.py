# base packages
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# import packages
import numpy as np
from numpy.random import binomial, multivariate_normal, normal, uniform

# user-defined packages
from data.dgps import ihdp_surface_B


def generate_data_example1(d, n, n_test, seed=12345):
    np.random.seed(seed)
    controls_outcome = generate_controls_outcome(d)
    X_test = multivariate_normal(np.zeros(d), np.diag(np.ones(d)), n_test)
    delta = 6/n_test
    X_test[:, 1] = np.arange(-3, 3, delta)
    Y, T, X = generate_data(n, d, controls_outcome, treatment_effect, propensity)
    return Y, T, X, X_test, treatment_effect


def generate_data_example2(seed=123456):
    Y, T, X, expected_te = ihdp_surface_B(random_state=seed)
    return Y, T, X, expected_te


# controls outcome, treatment effect, propensity definitions
def generate_controls_outcome(d):
    beta = uniform(-3, 3, d)
    return lambda x: np.dot(x, beta) + normal(0, 1)

treatment_effect = lambda x: (1 if x[1] > 0.1 else 0)*8

propensity = lambda x: (0.8 if (x[2]>-0.5 and x[2]<0.5) else 0.2)


# Define DGP
def generate_data(n, d, controls_outcome, treatment_effect, propensity, seed=1234):
    """Generates population data for given untreated_outcome, treatment_effect and propensity functions.
    
    Parameters
    ----------
        n (int): population size
        d (int): number of covariates
        controls_outcome (func): untreated outcome conditional on covariates
        treatment_effect (func): treatment effect conditional on covariates
        propensity (func): probability of treatment conditional on covariates
        seed (int): random seed to ensure reproducibility
    """
    np.random.seed(seed)
    # Generate covariates
    X = multivariate_normal(np.zeros(d), np.diag(np.ones(d)), n)
    # Generate treatment
    T = np.apply_along_axis(lambda x: binomial(1, propensity(x), 1)[0], 1, X)
    # Calculate outcome
    Y0 = np.apply_along_axis(lambda x: controls_outcome(x), 1, X)
    treat_effect = np.apply_along_axis(lambda x: treatment_effect(x), 1, X)
    Y = Y0 + treat_effect * T
    return (Y, T, X)

