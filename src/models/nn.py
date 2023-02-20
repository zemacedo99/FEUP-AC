from sklearn.neural_network import MLPClassifier
from scipy import stats
from models.common import train_model, fine_tuning


def create(data):
    """Creates the model and trains it

    :param data: data to feed the model
    """
    model = train_model(data, 'nn')
    return model


def explore(data):
    nn = MLPClassifier(max_iter=100, random_state=10)
    print(nn.get_params().keys())
    params = dict(hidden_layer_sizes=[(100,), (100, 50), (100, 50, 20), (100, 50, 20, 10), (100, 50, 20, 10, 5)],
                  activation=['logistic', 'tanh', 'relu'],
                  solver=['lbfgs', 'adam'],
                  alpha=stats.uniform(loc=0.0001, scale=0.001),
                  learning_rate_init=stats.uniform(loc=0, scale=0.01))
    print("Fine tunning NN...")
    fine_tuning(data=data, model=nn, params=params)
