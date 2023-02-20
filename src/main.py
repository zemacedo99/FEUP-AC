import sys

import pandas as pd

from load_data.load_ds import load_all_preproc, load_simple
from models import dtc, knn, gbm, bayes, svm, nn, rfc
from parsers import cmd_args
from models.common import score_model

import warnings

warnings.filterwarnings("ignore")

if not cmd_args.parse(sys.argv[1:]):
    exit(1)

model_type = sys.argv[1]
ds = sys.argv[2]

data = None
data_score = None
if ds == "s":
    data = load_simple(False)
    data_score = load_simple(True)
elif ds == "ap":
    data = load_all_preproc(False)
    data_score = pd.read_csv("ds/preprocessed/all_preproc_score.csv")

model = None
if model_type == 'dtc':
    model = dtc.create(data)
    score_model(model)
elif model_type == 'knn':
    model = knn.create(data)
    score_model(model)
elif model_type == 'gbm':
    model = gbm.create(data)
    score_model(model)
elif model_type == 'bys':
    model = bayes.create(data)
    score_model(model)
elif model_type == 'svm':
    model = svm.create(data)
    score_model(model)
elif model_type == 'rfc':
    model = rfc.create(data)
    score_model(model)
    
elif model_type == 'nn':
    model = nn.create(data)
    score_model(model)



