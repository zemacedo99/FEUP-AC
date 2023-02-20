import sys


from load_data.prepocessing.data_cleaning import fill_final_na, correct_types
from load_data.prepocessing.data_cleaning import handle_categorical_OH, parse_dates

from load_data.prepocessing.feature_engineering import *

from load_data.constants import *


def load_score_ds():
    """Import and preprocesses dataset to score, accordingly to ds_type

    :param ds_type: defines how we want to import. Can be s (only the loan), au (all but without preprocessing) or ap (all w/preprocessing)


    :return: DataFrame containing the dataset to score
    """
    data = pd.read_csv("ds/preprocessed/all_preproc_score.csv")
    return data


def load_simple(to_score=False):
    data = pd.read_csv(LOAN_SCORE_PATH) if to_score else pd.read_csv(LOAN_PATH)
    data.pop('date')
    if to_score:
        data.pop('status')
    return data


def load_all_unproc():
    data = [load_loan(preprocess=False), load_account(preprocess=False),
            load_card(preprocess=False), load_client(preprocess=False),
            load_disp(preprocess=False), load_district(preprocess=False),
            load_trans(preprocess=False)]

    return join_data(data)


def load_all_preproc(to_score: bool):
    """Import and preprocesses datasets

    :return: DataFrame containing the dataset
    """

    data = load_all(to_score)

    joined_data = join_data(data)

    filled_data = fill_final_na(joined_data)

    final_data = final_fe(filled_data)

    if to_score:
        final_data.drop(['status'], axis=1, inplace=True)

    return final_data


def load_all(to_score):
    data = [load_loan(to_score=to_score), load_account(),
            load_card(to_score=to_score), load_client(),
            load_disp(), load_district(),
            load_trans(to_score=to_score)]
    return data


def join_data(data):
    """Joins all the DataFrames present in the list data

    :param data: a list of DataFrames
    :return: a DataFrame with all data merged
    """
    temp = pd.merge(data[LOAN_IDX], data[ACC_IDX], on='account_id', how='left')
    temp = pd.merge(temp, data[DISP_IDX], on='account_id', how='left')
    temp = pd.merge(temp, data[CARD_IDX], on='disp_id', how='left')
    temp = pd.merge(temp, data[CLIENT_IDX], on='client_id', how='left')
    temp = pd.merge(temp, data[DISTRICT_IDX], left_on='district_id', right_on='code', how='left')
    temp = pd.merge(temp, data[TRANS_IDX], left_on='account_id', right_on='account_id', how='left')
    return temp


def load_loan(to_score=False, preprocess=True):
    """Imports and preprocess loan

    :return: DataFrame loan
    """
    loan = pd.read_csv(LOAN_SCORE_PATH) if to_score else pd.read_csv(LOAN_PATH)
    if not preprocess:
        return loan

    loan = fe_loan(loan)

    loan = parse_dates(loan, ['loan_date'])

    return loan


def load_account(preprocess=True):
    """Imports and preprocess account

    :return: DataFrame loan
    """
    account = pd.read_csv(ACCOUNT_PATH)
    if not preprocess:
        return account

    account = fe_account(account)

    account = handle_categorical_OH(account, ['frequency'])

    account = parse_dates(account, ['account_date'])

    return account


def load_card(to_score=False, preprocess=True):
    """Imports and preprocess card

    :return: DataFrame loan
    """
    card = pd.read_csv(CARD_SCORE_PATH) if to_score else pd.read_csv(CARD_PATH)
    if not preprocess:
        return card

    card = fe_card(card)

    card = handle_categorical_OH(card, ['cc_type'])
    card = parse_dates(card, ['cc_issued_date'])

    return card


def load_client(preprocess=True):
    """Imports and preprocess client

    :return: DataFrame loan
    """
    client = pd.read_csv(CLIENT_PATH)
    if not preprocess:
        return client

    client = fe_client(client)

    client = parse_dates(client, ['birth_number'])

    return client


def load_disp(preprocess=True):
    """Imports and preprocess disp

    :return: DataFrame loan
    """
    disp = pd.read_csv(DISP_PATH)
    if not preprocess:
        return disp

    disp = fe_disp(disp)
    return disp


def load_district(preprocess=True):
    """Imports and preprocess district

    :return: DataFrame loan
    """
    district = pd.read_csv(DISTRICT_PATH)
    if not preprocess:
        return district

    # TODO: Make this a function
    district["unemploymant rate '95"].fillna(value=district["unemploymant rate '95"].mean(), inplace=True)
    district["no. of commited crimes '95"].fillna(value=district["no. of commited crimes '95"].mean(), inplace=True)

    district = fe_district(district)
    return district


def load_trans(to_score=False, preprocess=True):
    """Imports and preprocess trans

    :return: DataFrame loan
    """
    try:
        trans = pd.read_csv(TRANS_PREPROC_SCORE_PATH) if to_score else pd.read_csv(TRANS_PREPROC_PATH)
        return trans
    except FileNotFoundError:
        print("Redoing trans")

    trans = pd.read_csv(TRANS_SCORE_PATH) if to_score else pd.read_csv(TRANS_PATH)
    if not preprocess:
        return trans

    # TODO: Maybe we can extract more knowledge from Trans table
    trans = fe_trans(trans)

    if to_score:
        trans.to_csv(TRANS_PREPROC_SCORE_PATH, index=False)
    else:
        trans.to_csv(TRANS_PREPROC_PATH, index=False)
    return trans
