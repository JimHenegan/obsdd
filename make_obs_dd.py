from obsdd.make_obs_dd_entry import make_obs_dd_entry
import pandas as pd

def make_obs_dd(df):

    all_records = []
    all_cols = df.columns

    for curr_var_name in all_cols:
        curr_col = df[curr_var_name]
        obs_dd_entry = make_obs_dd_entry(curr_col)
        all_records.append(obs_dd_entry)

    obs_dd = pd.DataFrame(all_records)

    return obs_dd
