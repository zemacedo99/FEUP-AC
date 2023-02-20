from models.common import train_model, fine_tuning
from sklearn.naive_bayes import GaussianNB


def create(data):
    """Creates the model and trains it

    :param data: data to feed the model
    """
    model = train_model(data, 'bayes')
    return model

def explore(data):

    knn = GaussianNB()

    params = dict()

    fine_tuning(data=data, model=knn, params=params)
