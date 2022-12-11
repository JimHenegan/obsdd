from obsdd.guess_data_type import guess_data_type

def get_permissible_values(curr_col, cat_col_cut):
    permissible_values = list(curr_col.dropna().unique())
    # permissible_values.sort()
    if guess_data_type(curr_col, cat_col_cut) == "NumberList":
        permissible_values = [int(pv) for pv in permissible_values]
        permissible_values.sort()
    return permissible_values
