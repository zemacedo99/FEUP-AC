from models.common import train_model, fine_tuning
from scipy import stats
from sklearn.neighbors import KNeighborsClassifier

def create(data):
    """Creates the model and trains it

    :param data: data to feed the model
    """
    model = train_model(data, 'knn')
    return model

def explore(data):

    knn = KNeighborsClassifier(algorithm="auto")

    params = dict(n_neighbors = (5,10, 15, 20),
        leaf_size = (10,20,30, 40, 50),
        p = (1,2),
        weights = ('uniform', 'distance'),
        metric = ('minkowski', 'chebyshev')
    )

    fine_tuning(data=data, model=knn, params=params)

    
