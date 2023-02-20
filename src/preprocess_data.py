import sys
import warnings
from load_data.load_ds import load_simple, load_all_unproc, load_all_preproc
warnings.filterwarnings("ignore")

HELP = """This script does the preprocessing of the data
    Usage:
        python preprocess_data.py <mode>

    mode:
        - s: simple dataset (only loan)
        - ap: all dataset, preprocessed with the configuration of config.ini
"""

COMMON = "Run python preprocess_data.py help to get possible usage"

if len(sys.argv) != 2:
    print(f"Wrong number of arguments: expected 1, provided {len(sys.argv) - 1}.\n{COMMON}")
    exit(1)

if sys.argv[1] == "help":
    print(HELP)
    exit(0)

preprocess_type = sys.argv[1]

if preprocess_type == "s":
    data = load_simple(False)
    data_score = load_simple(True)
    data.to_csv("ds/preprocessed/simple.csv", index=False)
    data_score.to_csv("ds/preprocessed/simple_score.csv", index=False)
elif preprocess_type == "ap":
    data = load_all_preproc(False)
    data_score = load_all_preproc(True)
    data_score.to_csv("ds/preprocessed/all_preproc_score.csv", index=False)
else:
    print(f"Unrecognized argument.\n{COMMON}")
    exit(1)


