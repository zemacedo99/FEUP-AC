import sys
from load_data.load_ds import load_all_preproc, load_simple
from models import dtc, knn, gbm, bayes, svm, rfc, nn
from parsers import cmd_args
import warnings

warnings.filterwarnings("ignore")

if not cmd_args.parse(sys.argv[1:]):
    exit(1)

model_type = sys.argv[1]
ds = sys.argv[2]

data = None
if ds == "s":
    data = load_simple(False)
elif ds == "ap":
    data = load_all_preproc(False)

model = None
try:
    if model_type == 'knn':
        model = knn.explore(data)
    elif model_type == 'bys':
        model = bayes.explore(data)
    elif model_type == 'svm':
        model = svm.explore(data)
    elif model_type == 'rfc':
        model = rfc.explore(data)
    elif model_type == 'nn':
        model = nn.explore(data)
except AttributeError:
    print("Model doesn't have fine-tuning implemented. Please try another one.")
    exit(1)
