import configparser

HELP = """
This script runs a given model with a given dataset
    Usage:
        python main.py <model> <ds>

    model:
        - dtc: Decision Tree Classifier
        - rfc: Random Forest Classifier
        - knn: K Nearest Neighbor
        - gbm: Gradient Boosting Classifier
        - bys: Naive Bayes
        - svm: Support Vector Machine
        - nn: Neural Networks

    ds:
        - s: simple dataset (only loan)
        - ap: all dataset, preprocessed with the configuration of config.ini

"""

config = configparser.ConfigParser()
config.read("configurations/config.ini")
VALID_MODELS = [string.lower() for string in config]
VALID_DS = ["s", "ap"]

MODEL = 0
DS = 1


def parse(args):
    if len(args) == 0:
        print("Wrong usage. Run help for more info")
        return False

    if args[MODEL] == "help":
        print(HELP)
        return False

    if len(args) != 2:
        print("Wrong usage. Run help for more info")
        return False

    if args[MODEL] in VALID_MODELS and args[DS] in VALID_DS:
        return True
    else:
        print("Wrong usage. Run help for more info")
        return False
