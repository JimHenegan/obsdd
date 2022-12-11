from obsdd.guess_data_type import guess_data_type

def get_pv_pcts(curr_col, cat_col_cut):
    no_missing = curr_col.dropna()
    length = no_missing.shape[0]
    props = no_missing.value_counts()/length
    pcts = props.apply(lambda x: f'{round(100 * x , 2)}%')
    
    pcts = pcts.reset_index()
    pcts = pcts.rename(columns = {"index" : "value", curr_col.name : "pct"})
    if guess_data_type(curr_col, cat_col_cut) == "NumberList":
        pcts['value'] = pcts['value'].astype(int)
    pcts = pcts.to_dict(orient = "records")
    pcts = str(pcts)
    return pcts
