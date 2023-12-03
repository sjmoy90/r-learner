from sklearn.model_selection import cross_val_predict, GridSearchCV, KFold


class RLearner:
    """
    Define R-Learner class.
    """
    def __init__(
        self,
        outcome_model,
        propensity_model,
        tau_model
    ):
        self.outcome_model = outcome_model
        self.propensity_model = propensity_model
        self.tau_model = tau_model
        self.k_fold = KFold(n_splits=5, shuffle=False)

    def fit(self, X, Y, T):
        """
        Fit R-learner.
        """
        # step 1
        Y_tilde, T_tilde = self._fit_step1(X, Y, T)
        
        # step 2
        self._fit_step2(X, Y_tilde, T_tilde)
        return
    
    def predict(self, X):
        """
        Make predictions using fitted treatment effect model.
        """
        te = self.tau_model.predict(X)
        return te
    
    def tune(
        self, X, Y, T,
        param_grid_outcome_model=None,
        param_grid_propensity_model=None,
        param_grid_tau_model=None
    ):
        """
        Tune R-Learner outcome model, propensity model, and treatment effect model.
        """
        if param_grid_outcome_model:
            self.outcome_model = self._tune(self.outcome_model, 'outcome_model', param_grid_outcome_model, X, Y)
        if param_grid_propensity_model:
            self.propensity_model = self._tune(self.propensity_model, 'propensity_model', param_grid_propensity_model, X, T)
        if param_grid_tau_model:
            Y_tilde, T_tilde = self._fit_step1(X, Y, T)
            pseudo_outcome = Y_tilde / T_tilde
            weights = T_tilde ** 2
            self.tau_model = self._tune(self.tau_model, 'tau_model', param_grid_tau_model, X, pseudo_outcome, weights)
        return

    def _fit_step1(self, X, Y, T):
        """
        Residualize outcome, Y, and treatment, T.
        """
        Y_tilde = self._residualize(self.outcome_model, X, Y)
        T_tilde = self._residualize(self.propensity_model, X, T)
        return Y_tilde, T_tilde

    def _fit_step2(self, X, Y_tilde, T_tilde):
        """
        Define pseudo-outcome and sample weights, then fit CATE model.
        """
        pseudo_outcome = Y_tilde / T_tilde
        weights = T_tilde ** 2

        self.tau_model.fit(X, pseudo_outcome, sample_weight=weights)
        return

    def _residualize(self, model, X, Y):
        """
        Train model and residualize using cross-fitted predictions.
        """
        Y_hat = cross_val_predict(model, X, Y, cv=self.k_fold)
        Y_tilde = Y - Y_hat
        return Y_tilde
    
    def _tune(self, model, model_name, param_grid, X, Y, weights=None):
        """
        Tune a model using grid search over hyperparameter grid.
        """
        print('Tuning {}...'.format(model_name))
        model_cv = GridSearchCV(estimator=model, param_grid=param_grid, cv=self.k_fold)
        model_cv.fit(X, Y, sample_weight=weights)
        print('Best hyperparameters for {}:'.format(model_name))
        print(model_cv.best_params_, '\n')
        self._update(model, model_cv.best_params_)
        return model
    
    def _update(self, obj, params):
        """
        Update attributes of an object.
        """
        for key, value in params.items():
            setattr(obj, key, value)
        return 