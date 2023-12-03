class TLearner:
    """
    Define T-Learner class.
    """
    def __init__(
        self,
        mu1_model,
        mu0_model
    ):
        self.mu1_model = mu1_model
        self.mu0_model = mu0_model

    def fit(self, X, Y, T):
        """
        Fit T-learner.
        """
        X_1 = X[T==1,:]
        Y_1 = Y[T==1]
        # fit mu_1
        self.mu1_model.fit(X_1, Y_1)
        
        X_0 = X[T==0,:]
        Y_0 = Y[T==0]
        # fit mu_0
        self.mu0_model.fit(X_0, Y_0)
        return

    def predict(self, X):
        """
        Make predictions using fitted treatment effect model.
        """
        te = self.mu1_model.predict(X) - self.mu0_model.predict(X)
        return te
