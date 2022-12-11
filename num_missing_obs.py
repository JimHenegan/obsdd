def num_missing_obs(curr_col):
    # how many missing values are there?
    return curr_col.isna().sum()
