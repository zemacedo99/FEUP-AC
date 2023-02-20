from sklearn.svm import SVC
from scipy import stats
from models.common import train_model, fine_tuning


def create(data):
    """Creates the model and trains it

    :param data: data to feed the model
    """
    model = train_model(data, 'svm')
    return model


def explore(data):

    svc = SVC(random_state=10)

    params = dict(C=stats.uniform(loc=1, scale=6),
                  kernel=['rbf', 'sigmoid'],
                  gamma=['scale', 'auto'],
                   coef0=stats.uniform(loc=0, scale=6))

    fine_tuning(data=data, model=svc, params=params)


