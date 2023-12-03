import numpy as np


class SLearner:
    """
    Define S-Learner class.
    """
    def __init__(
        self,
        overall_model
    ):
        self.overall_model = overall_model

    def fit(self, X, Y, T):
        """
        Fit S-learner.
        """
        # augment feature matrix
        X_aug = self._augment_features(T, X)
        # fit model
        self.overall_model.fit(X_aug, Y)
        return

    def predict(self, X):
        """
        Make predictions using fitted treatment effect model.
        """
        X_1 = self._augment_features(np.ones(X.shape[0]), X)
        X_0 = self._augment_features(np.zeros(X.shape[0]), X)
        
        # predict mu_1(X) and mu_0(X)
        mu1_hat = self.overall_model.predict(X_1)
        mu0_hat = self.overall_model.predict(X_0)
        
        # predict treatment effect
        te = mu1_hat - mu0_hat
        return te
    
    def _augment_features(self, T, X):
        X_aug = np.concatenate([np.reshape(T, [-1, 1]), X], axis=1)
        return X_aug
