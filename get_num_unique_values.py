def get_num_unique_values(curr_col):
    return curr_col.dropna().nunique()
