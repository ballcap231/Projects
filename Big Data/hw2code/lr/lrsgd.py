# Do not use anything outside of the standard distribution of python
# when implementing this class
import math 

class LogisticRegressionSGD:
    """
    Logistic regression with stochastic gradient descent
    """

    def __init__(self, eta, mu, n_feature):
        """
        Initialization of model parameters
        """
        self.eta = eta
        self.weight = [0.0] * n_feature
        self.mu = mu
    def Update_W(self, X,y,qq, exist_ok = 0):
        w_t_1 = self.weight[qq]
        if exist_ok == 0:
            x_t = dict(X)[qq]
            change = self.eta*((y - self.predict_prob(X))*x_t - 2*self.mu*self.weight[qq])
        elif exist_ok == 1:
            change =  -2*self.eta*self.mu*self.weight[qq]#weights regularized even if not used?
        w_t = w_t_1 + change
        return w_t

    def fit(self, X, y):
        """
        Update model using a pair of training sample
        """
        feat_ls = list(dict(X).keys())
        self.weight = [self.Update_W(X, y,qq) if qq in feat_ls else self.Update_W(X, y,qq, 1) for qq in range(len(self.weight))]

    def predict(self, X):
        """
        Predict 0 or 1 given X and the current weights in the model
        """
        return 1 if self.predict_prob(X) > 0.5 else 0

    def predict_prob(self, X):
        """
        Sigmoid function
        """
        return 1.0 / (1.0 + math.exp(-math.fsum((self.weight[f]*v for f, v in X))))
