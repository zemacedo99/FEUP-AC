import configparser

import pandas as pd
from sklearn.model_selection import KFold, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTENC
from sklearn import neural_network
from load_data.load_ds import load_all_preproc, load_loan
from sklearn import metrics


def score_model(model):
    """Scores a model, with the score dataset wit type ds_type

    :param model: sklearn model to score
    :param ds_type: defines how we want to import. Can be s (only the loan), au (all but without preprocessing) or ap (all w/preprocessing)
    :return:
    """

    score_data = load_all_preproc(True)
    loan = load_loan(True)

    score_predictions = pd.DataFrame(model.predict_proba(score_data)[:, 0])
    score_predictions = score_predictions.rename(columns={"loan_id": "Id", 0: "Predicted"})

    # print(score_predictions)
    # print(loan["loan_id"])

    # score_predictions['Id'] = loan["loan_id"]

    final = pd.DataFrame()
    final["Id"] = loan["loan_id"]
    final['Predicted'] = score_predictions['Predicted']

    # print(final)

    final.to_csv('scores/dtc_res.csv', index=False)


def train_model(data: pd.DataFrame, model_type):
    """Trains a model of model_type using SMOTE and Cross-Validation, with the data provided

    :param data: data to train the model with
    :param model_type: type of the model (dtc, rfc, etc...)
    :return: best model o
    """

    kf = KFold(n_splits=5)
    X = data.copy()

    y = X.pop('status')
    models = {}
    cat_cols = ['frequency_issuance_after_transaction', 'frequency_monthly_issuance',
                'frequency_weekly_issuance', 'cc_type_classic', 'cc_type_gold',
                'cc_type_junior', 'sex', 'Cluster']
    cat_idx = [X.columns.get_loc(col) for col in cat_cols]

    for fold, (train_index, test_index) in enumerate(kf.split(X)):
        X_train = X.iloc[train_index, :]
        y_train = y.iloc[train_index]
        X_test = X.iloc[test_index, :]
        y_test = y.iloc[test_index]

        sm = SMOTENC(categorical_features=cat_idx, random_state=10)
        X_train_oversampled, y_train_oversampled = sm.fit_resample(X_train, y_train)

        model = create_model(model_type)
        model.fit(X_train_oversampled, y_train_oversampled)

        y_pred = model.predict_proba(X_test)[:, 1]
        score = metrics.roc_auc_score(y_test, y_pred)
        models[score] = model

    max_val = sorted(models, reverse=True)[0]
    print(f"Max value: {max_val}")

    return models[max_val]


def create_model(model_type):
    """Creates the model of type model_type accordingly to the configurations of config.ini

    :param model_type: type of the model (dtc, rfc, etc...)
    :return:
    """

    config = configparser.ConfigParser()
    config.read('configurations/config.ini')

    if model_type == "dtc":
        return DecisionTreeClassifier()

    elif model_type == "knn":
        weights = config['KNN']['weights']
        p = config['KNN']['p']
        n_neighbors = config['KNN']['n_neighbors']
        metric = config['KNN']['metric']
        leaf_size = config['KNN']['leaf_size']

        return KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights,
                                    p=p, metric=metric, leaf_size=leaf_size)

    elif model_type == "gbm":
        return GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)

    elif model_type == "bys":
        return GaussianNB()

    elif model_type == "svm":
        C = float(config['SVM']['C'])
        coef0 = float(config['SVM']['coef0'])
        gamma = config['SVM']['gamma']
        kernel = config['SVM']['kernel']
        return svm.SVC(C=C, coef0=coef0, gamma=gamma, kernel=kernel)

    elif model_type == "rfc":
        return RandomForestClassifier(random_state=11,
                                      n_estimators=1600,
                                      min_samples_split=2,
                                      min_samples_leaf=2,
                                      max_features='sqrt',
                                      max_depth=100,
                                      criterion='entropy',
                                      class_weight='balanced_subsample',
                                      bootstrap=False)

    elif model_type == "nn":
        activation = config['NN']['activation']
        alpha = float(config['NN']['alpha'])
        hidden_layer_sizes = tuple([int(n) for n in config['NN']['hidden_layer_sizes'][1:-1].split(',')])
        learning_rate_init = float(config['NN']['learning_rate_init'])
        solver = config['NN']['solver']
        model = neural_network.MLPClassifier(alpha=alpha, hidden_layer_sizes=hidden_layer_sizes,
                                             solver=solver, random_state=10, activation=activation,
                                             learning_rate_init=learning_rate_init)
        return model


def fine_tuning(model, params, data):
    X = data.copy()
    y = X.pop('status')

    rs = RandomizedSearchCV(estimator=model, param_distributions=params, cv=10, scoring='roc_auc', n_jobs=-1,
                            random_state=10)

    result = rs.fit(X, y)

    print("Best parameters: ")
    print(result.best_params_)
    print(f"Best score: {result.best_score_}")
