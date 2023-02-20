TRANS_PREPROC_PATH = 'ds/preprocessed/trans_preproc.csv'
TRANS_PREPROC_SCORE_PATH = 'ds/preprocessed/trans_preproc_score.csv'
TRANS_PATH = 'ds/trans.csv'
TRANS_SCORE_PATH = 'ds/trans_to_score.csv'
ACCOUNT_PATH = 'ds/account.csv'
CARD_PATH = 'ds/card.csv'
CARD_SCORE_PATH = 'ds/card_to_score.csv'
CLIENT_PATH = 'ds/client.csv'
DISP_PATH = 'ds/disp.csv'
DISTRICT_PATH = 'ds/district.csv'
LOAN_PATH = 'ds/loan.csv'
LOAN_SCORE_PATH = 'ds/loan_to_score.csv'

TABLE_NAMES = [TRANS_PATH, ACCOUNT_PATH, CARD_PATH, CLIENT_PATH, DISP_PATH, DISTRICT_PATH, LOAN_PATH]

LOAN_IDX = 0
ACC_IDX = 1
CARD_IDX = 2
CLIENT_IDX = 3
DISP_IDX = 4
DISTRICT_IDX = 5
TRANS_IDX = 6

PREPROC_DATA_PATH = "ds/preprocessed/all_data.csv"

COLS_TO_NORMALIZE = ['amount', 'NumberOfTrans', 'balance', 'Age',
                    "amount_min", "amount_max", "amount_mean", "amount_std",
                    "balance_min", "balance_max", "balance_mean", "balance_std",
                    "n_A", "n_B", "n_C", "n_D", "n_E", "n_F", "n_credit", "n_withdraw",
                     "n_kA","n_kB","n_kC","n_kD","n_kE","n_kG"]

COLS_TO_CATEGORY = ['cc_type_classic', 'cc_type_gold', 'cc_type_junior', 'sex',
                    'status', 'frequency_issuance_after_transaction',
                    'frequency_monthly_issuance', 'frequency_weekly_issuance']

STATS = ['min', 'max', 'mean', 'std']
