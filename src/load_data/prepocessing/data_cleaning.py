# importing module
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
import datetime

from load_data.constants import COLS_TO_CATEGORY


def fix_date(x):
    if x.year > 2000:

        year = x.year - 100

    else:

        year = x.year

    return datetime.date(year, x.month, x.day)


def handle_categorical_OE(data, cols):
    """handle categorical variables with ordinal encoder
        :param data: DataFrame to handle
        :param cols: List of columns names of the DataFrama to handle
    """
    # print("Categorical variables:")
    # print(cols)

    # # Make copy to avoid changing original data 
    label_data = data.copy()

    # # Apply ordinal encoder to each column with categorical data
    ordinal_encoder = OrdinalEncoder()
    label_data[cols] = ordinal_encoder.fit_transform(data[cols])

    # print(label_data)

    return label_data


def handle_categorical_OH(data, cols):
    """handle categorical variables with ordinal encoder
        :param data: DataFrame to handle
        :param cols: List of columns names of the DataFrama to handle
    """

    # Apply one-hot encoder to each column with categorical data
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    OH_cols = pd.DataFrame(OH_encoder.fit_transform(data[cols])).astype(int)

    new_cols = [col.replace(' ', '_') for col in OH_encoder.get_feature_names(cols)]

    OH_cols.columns = new_cols

    # One-hot encoding removed index; put it back
    OH_cols.index = data.index

    # Remove categorical columns (will replace with one-hot encoding)
    num_data = data.drop(cols, axis=1)

    # Add one-hot encoded columns to numerical features
    OH_data = pd.concat([num_data, OH_cols], axis=1)

    return OH_data


def handle_na_values(data):
    """handle categorical variables with ordinal econder
        :param data: DataFrame to handle
    """

    # get the number of missing data points per column
    missing_values_count = data.isnull().sum()

    # how many total missing values do we have?
    total_cells = np.product(data.shape)
    total_missing = missing_values_count.sum()

    # percent of data that is missing
    percent_missing = (total_missing / total_cells) * 100
    print(percent_missing)

    return data


def fill_na(data, col):
    """fill na values with "other"
        :param data: DataFrame to handle
        :param col: Column name of the DataFrama to fill, (column operation on the trans table )
    """

    # get the number of missing data points per column
    # missing_values_count = data.isnull().sum()
    # print(missing_values_count)

    data[col].fillna("Other", inplace=True)

    # missing_values_count = data.isnull().sum()
    # print(missing_values_count)     

    return data


def parse_dates(data, cols, date_format="%y%m%d"):
    """handle categorical variables with ordinal encoder
        :param data: DataFrame to handle
        :param cols: Date column name to handle
        :param date_format:
    """
    for col in cols:
        data[col] = pd.to_datetime(data[col], format=date_format)
        data[col] = data[col].apply(fix_date)

    return data


def fill_final_na(data: pd.DataFrame):
    return data.fillna(value=0, axis=1)


def correct_types(data: pd.DataFrame):
    for col in COLS_TO_CATEGORY:
        data[col].astype('category', copy=False)
