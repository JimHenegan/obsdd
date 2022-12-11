from obsdd.get_num_unique_values import get_num_unique_values
from obsdd.guess_data_type import guess_data_type
from obsdd.num_expected_obs import num_expected_obs
from obsdd.num_missing_obs import num_missing_obs
from obsdd.get_permissible_values import get_permissible_values
from obsdd.get_possible_anomalies import get_possible_anomalies
from obsdd.get_pv_proportions import get_pv_proportions
from obsdd.get_pv_pcts import get_pv_pcts

import pandas as pd

from obsdd.date_helpers import (
    string_series_is_series_of_blsa_dates, 
    string_series_is_series_of_td_dates,
    string_series_is_series_of_extended_blsa_dates
)
    


def make_obs_dd_entry(curr_col):

    curr_obj = {}

    cat_col_cut = 15

    curr_obj['obs_var_name'] = curr_col.name
    # print(f'Working on {curr_col.name}...')

    obs_data_type = guess_data_type(curr_col, cat_col_cut)
    # print(curr_col.name, obs_data_type)
    
    curr_obj['obs_numobs'] = curr_col.dropna().shape[0]
    curr_obj['obs_distinct'] = get_num_unique_values(curr_col)
    curr_obj['obs_data_type'] = obs_data_type
    num_exp_obs = num_expected_obs(curr_col)
    num_mis_obs = num_missing_obs(curr_col)
    curr_obj['obs_prop_missing'] = num_mis_obs/num_exp_obs

    num_missing = curr_col[curr_col.isna()].shape[0]
    prop_missing = num_missing / curr_col.shape[0]
    pct_missing = f'{round(100 * prop_missing, 2)}%'
    num_pct_missing = f'{num_missing} ({pct_missing})'
    curr_obj['obs_missing'] = num_pct_missing

    
    if obs_data_type == "DateTime":
        print("Looking, trying...")
        if string_series_is_series_of_blsa_dates(curr_col):
            curr_obj['obs_date_format'] = "YYYY-MM-DD"
        if string_series_is_series_of_td_dates(curr_col):
            curr_obj['obs_date_format'] = "%td"        
        if string_series_is_series_of_extended_blsa_dates(curr_col):
            curr_obj['obs_date_format'] = "YYYY-MM-DD HH:MM:SS"        

    if obs_data_type in ["Decimal",  "Integer"]:
    
        curr_obj['obs_max'] = curr_col.max()
        curr_obj['obs_min'] = curr_col.min()

        if curr_col.shape[0] < 100000:
            print(f'Getting potential anomalies...')
            curr_obj['obs_anomalies'] = get_possible_anomalies(curr_col)
        
        curr_obj['obs_mean'] = curr_col.mean()
        curr_obj['obs_median'] = curr_col.median()

        no_missing = curr_col.dropna()
        description = no_missing.describe()

        curr_obj['obs_std_dev'] = description['std']

        quantiles = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]
        
        for q in quantiles:
            curr_obj[f'obs_p_{round(100*q)}'] = round(no_missing.quantile(q = q), 2)
        

        summary_stats = {}

        summary_stats['mean'] = description['mean']
        summary_stats['std'] = description['std']



        below_two_sd = no_missing[no_missing < summary_stats['mean'] - 2 * summary_stats['std']]
        above_two_sd = no_missing[no_missing > summary_stats['mean'] + 2 * summary_stats['std']]
        obs_outside_two_sd_from_mean = list(pd.concat([below_two_sd, above_two_sd]))
        obs_outside_two_sd_from_mean.sort()
        curr_obj['obs_outside_two_sd_from_mean'] = obs_outside_two_sd_from_mean



    
        

    if obs_data_type in ['NumberList', 'StringList']:
        curr_obj['obs_permissible_values'] = get_permissible_values(curr_col, cat_col_cut)
        curr_obj['obs_pv_proportions'] = get_pv_proportions(curr_col, cat_col_cut)
        curr_obj['obs_pv_pcts'] = get_pv_pcts(curr_col, cat_col_cut)

    return curr_obj
