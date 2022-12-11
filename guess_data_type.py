from obsdd.num_expected_obs import num_expected_obs
from obsdd.num_missing_obs import num_missing_obs

from obsdd.date_helpers import string_series_is_series_of_blsa_dates, string_series_is_series_of_td_dates

def guess_data_type(curr_col, cat_col_cut):
    dt = pd_dt(curr_col)
    if dt == "object":
        return handle_object(curr_col, cat_col_cut)
    elif str(curr_col.dtype) == "datetime64[ns]":
        return "DateTime"    
    else:
        return handle_numeric(curr_col, cat_col_cut)

def pd_dt(curr_col):
    # what is the data type, as classified by pandas?
    series_type = curr_col.dtype
    return str(series_type)

def handle_object(curr_col, cat_col_cut):
    if is_date_like(curr_col):
        return "DateTime"
    else:
        return handle_non_date_object(curr_col, cat_col_cut)

def is_date_like(curr_col):
    if str(curr_col.dtype) == "datetime64[ns]":
        return True

    if string_series_is_series_of_blsa_dates(curr_col):
        return True
    
    if string_series_is_series_of_td_dates(curr_col):
        return True
    
    return False   
    

def handle_non_date_object(curr_col, cat_col_cut):    
    nunique = curr_col.nunique()    
    if nunique <= cat_col_cut:
        return "StringList"
    else:
        return "String"

def handle_numeric(curr_col, cat_col_cut):
    nunique = curr_col.nunique()
    if nunique <= cat_col_cut:
        return check_number_list(curr_col)
    else:
        return handle_non_number_list(curr_col)
    
def check_number_list(curr_col):
    if all_integers(curr_col):
        return "NumberList"
    else:
        return "StringList"

def handle_non_number_list(curr_col):
    if all_integers(curr_col):
        return "Integer"
    else:
        return "Decimal"
    
def all_integers(curr_col):
    """
    Are all entries of a numeric column integers? If so, return True.
    Returns False if there are some decimals.
    Works by comparing the "int" version of a number to its "decimal" form.    
    """


    all_integers = False
    temp_1 = curr_col.dropna().apply(lambda x: int(x))
    temp_2 = curr_col.dropna()
    difference = temp_1 - temp_2
    squared_difference = difference.apply(lambda x: x*x)
    sum_squared_difference = squared_difference.sum()
    if sum_squared_difference == 0:
        all_integers = True
    return all_integers


    
