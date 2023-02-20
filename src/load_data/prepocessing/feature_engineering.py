import pandas as pd
from scipy.stats import stats
from sklearn.cluster import KMeans

from load_data.constants import COLS_TO_NORMALIZE, STATS
from load_data.prepocessing.data_cleaning import correct_types, handle_categorical_OH
import numpy as np

DISTR_PATH = '../../ds/district.csv'

LOAN_COLS_TO_RM = ['payments']
CARD_COLS_TO_RM = ['']
CLIENT_COLS_TO_RM = ['district_id']
DISTRICT_COLS_TO_RM = ['region', 'no. of municipalities with inhabitants < 499',
                       'no. of municipalities with inhabitants 500-1999',
                       'no. of municipalities with inhabitants 2000-9999',
                       'no. of municipalities with inhabitants >10000', 'no. of cities']
TRANS_COLS_TO_RM = ['type', 'operation', 'amount', 'k_symbol', 'bank', 'account']


def final_fe(data: pd.DataFrame):
    data_temp = remove_ids(data)

    # Extracting Age when client asked for the loan
    data_temp['Age'] = np.floor((data_temp['loan_date'] - data_temp['birth_number']) / np.timedelta64(1, 'Y'))
    data_temp['Age'] = data_temp['Age'].astype(int)

    data_temp.drop(['loan_date', 'account_date', 'birth_number', 'date', 'cc_issued_date'], axis=1, inplace=True)

    data_temp.drop(["n_kF", "p_kF"], axis=1, inplace=True)

    # Normalize data using zscore
    data_temp[COLS_TO_NORMALIZE] = data_temp[COLS_TO_NORMALIZE].apply(stats.zscore)

    correct_types(data_temp)

    return data_temp


def fe_loan(loan: pd.DataFrame):
    loan.drop(LOAN_COLS_TO_RM, axis=1, inplace=True)
    loan.rename(columns={'date': 'loan_date'}, inplace=True)
    loan.astype({'loan_id': 'Int64'}, copy=False)
    loan['duration'].astype('category')

    return loan


def fe_account(account: pd.DataFrame):
    account.rename(columns={'date': 'account_date'}, inplace=True)
    return account


def fe_card(card: pd.DataFrame):
    # card.drop(CARD_COLS_TO_RM, axis=1)
    card.rename(columns={'type': 'cc_type', 'issued': 'cc_issued_date'}, inplace=True)
    return card


def fe_client(client: pd.DataFrame):
    client['sex'] = client.apply(lambda row: extract_sex(row), axis=1)
    client['birth_number'] = client.apply(lambda row: rm_sex_from_date(row), axis=1)
    client.drop(CLIENT_COLS_TO_RM, axis=1, inplace=True)
    return client


def extract_sex(row):
    birth = str(row['birth_number'])
    return 0 if int(birth[2:4]) > 50 else 1


def rm_sex_from_date(row):
    return row['birth_number'] - 5000 if str(row['birth_number'])[2:4] > '50' else row['birth_number']


def fe_disp(disp: pd.DataFrame):
    disp["NumberOfPeople"] = (
        disp.groupby("account_id")
        ["type"]
            .transform("count")
    )
    disp = disp[disp.type != 'DISPONENT']
    disp.drop(['type'], axis=1, inplace=True)
    return disp


def fe_district(district: pd.DataFrame):
    cluster = k_clustering(district)
    district['Cluster'] = cluster
    district = district[['code', 'Cluster']]

    return district


def fe_trans(trans: pd.DataFrame):
    trans["NumberOfTrans"] = (
        trans.groupby("account_id")
        ["account_id"]
        .transform("count")
    )
    # Withdrawal in cash is the same has withdrawal
    trans.loc[trans["type"] == "withdrawal in cash", "type"] = "withdrawal"

    # Withdrawal amount must be negative
    trans.loc[trans["type"] == "withdrawal", "amount"] *= -1

    for stat in STATS:
        trans[f"amount_{stat}"] = (
            trans.groupby("account_id")
            ["amount"]
            .transform(stat)
        )
    for stat in STATS:
        trans[f"balance_{stat}"] = (
            trans.groupby("account_id")
            ["balance"]
            .transform(stat)
        )

    trans.sort_values(by=['account_id', 'date'], inplace=True)

    new_rows = []
    for i in range(1, 11383):
        rows = trans[trans.account_id == i]
        if rows.empty:
            continue

        create_summary_features(rows)

        new_rows.append(rows.iloc[-1, :])

    new_trans = pd.DataFrame(new_rows)
    new_trans.drop(TRANS_COLS_TO_RM, axis=1, inplace=True)
    return new_trans


def remove_ids(df: pd.DataFrame):
    cols = [c for c in df.columns if not "id" in c.lower()]
    cols.remove("code")
    return df[cols]


def k_clustering(data: pd.DataFrame):
    kmeans = KMeans(n_clusters=2)
    cpy_data = data.copy()
    cpy_data = handle_categorical_OH(cpy_data, ["name", "region"])
    cpy_data["Cluster"] = kmeans.fit_predict(cpy_data)
    cpy_data["Cluster"] = cpy_data["Cluster"].astype("category")
    return cpy_data["Cluster"]


def create_summary_features(rows):
    n_A = sum(rows.operation == 'credit in cash')
    n_B = sum(rows.operation == "collection from another bank")
    n_C = sum(rows.operation == 'withdrawal in cash')
    n_D = sum(rows.operation == 'remittance to another bank')
    n_E = sum(rows.operation == 'credit card withdrawal')
    n_F = rows.operation.isna().sum()

    n_kA = sum(rows.k_symbol == 'interest credited')
    n_kB = sum(rows.k_symbol == 'household')
    n_kC = sum(rows.k_symbol == 'payment for statement')
    n_kD = sum(rows.k_symbol == 'insurrance payment')
    n_kE = sum(rows.k_symbol == 'sanction interest if negative balance')
    n_kF = sum(rows.k_symbol == 'old-age pension')
    n_kG = rows.k_symbol.isna().sum()

    n_credit = sum(rows.type == 'credit')
    n_withdraw = sum(rows.type == 'withdrawal')

    total_op = n_A + n_B + n_C + n_D + n_E + n_F

    rows['n_A'] = n_A
    rows['n_B'] = n_B
    rows['n_C'] = n_C
    rows['n_D'] = n_D
    rows['n_E'] = n_E
    rows['n_F'] = n_F

    rows['p_A'] = n_A / total_op
    rows['p_B'] = n_B / total_op
    rows['p_C'] = n_C / total_op
    rows['p_D'] = n_D / total_op
    rows['p_E'] = n_E / total_op
    rows['p_F'] = n_F / total_op

    rows['n_credit'] = n_credit
    rows['n_withdraw'] = n_withdraw

    rows['p_credit'] = n_credit / (n_credit + n_withdraw)
    rows['p_withdraw'] = n_withdraw / (n_credit + n_withdraw)

    rows['n_kA'] = n_kA
    rows['n_kB'] = n_kB
    rows['n_kC'] = n_kC
    rows['n_kD'] = n_kD
    rows['n_kE'] = n_kE
    rows['n_kF'] = n_kF
    rows['n_kG'] = n_kG

    total_op = n_kA + n_kB + n_kC + n_kD + n_kE + n_kF + n_kG

    rows['p_kA'] = n_kA / total_op
    rows['p_kB'] = n_kB / total_op
    rows['p_kC'] = n_kC / total_op
    rows['p_kD'] = n_kD / total_op
    rows['p_kE'] = n_kE / total_op
    rows['p_kF'] = n_kF / total_op
    rows['p_kG'] = n_kG / total_op

