from sklearn.ensemble import RandomForestClassifier
from scipy import stats
from models.common import train_model, fine_tuning


def create(data):
    """Creates the model and trains it

    :param data: data to feed the model
    """
    model = train_model(data, 'rfc')
    return model


def explore(data):
    # TODO: Add here the code to explore the model (using RandomSearch or Bayesian, dont know whats best)
    # TODO: Explore parameters should be imported from explore.ini

    rfc = RandomForestClassifier(random_state=10)
    
    print("keys:")
    print(rfc.get_params().keys())
    
    params = dict(
                  n_estimators = [ 10, 100,200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000], 
                  criterion = ['gini', 'entropy'],
                  max_depth = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
                  min_samples_split =  [2, 5, 10],
                  min_samples_leaf = [1, 2, 4],
                  max_features =  ['auto', 'sqrt', 'log2'],
                  bootstrap=[True,False],
                  class_weight = ['balanced', 'balanced_subsample']
                  )
    
    print("Fine tunning rfc...")
    fine_tuning(data=data, model=rfc, params=params)
    pass
