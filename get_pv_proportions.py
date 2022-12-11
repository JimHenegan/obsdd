from obsdd.guess_data_type import guess_data_type

def get_pv_proportions(curr_col, cat_col_cut):
    no_missing = curr_col.dropna()
    length = no_missing.shape[0]
    props = no_missing.value_counts()/length
    props = props.reset_index()
    props = props.rename(columns = {"index" : "value", curr_col.name : "proportion"})
    if guess_data_type(curr_col, cat_col_cut) == "NumberList":
        props['value'] = props['value'].astype(int)
    props = props.to_dict(orient = "records")
    props = str(props)
    return props
