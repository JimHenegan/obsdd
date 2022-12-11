import re

def string_series_is_series_of_blsa_dates(series):

    no_missing = series.dropna()
    num_in_series = no_missing.shape[0]    
    num_matching_blsa_date_pattern = no_missing.apply(lambda x: string_is_blsa_date(x)).sum()
    
    return num_matching_blsa_date_pattern == num_in_series

def string_series_is_series_of_extended_blsa_dates(series):

    no_missing = series.dropna()
    num_in_series = no_missing.shape[0]    
    num_matching_blsa_date_pattern = no_missing.apply(lambda x: string_is_extended_blsa_date(x)).sum()
    
    return num_matching_blsa_date_pattern == num_in_series



def string_series_is_series_of_td_dates(series):

    no_missing = series.dropna()
    num_in_series = no_missing.shape[0]    
    num_matching_td_date_pattern = no_missing.apply(lambda x: string_is_stata_td_date(x)).sum()
    
    return num_matching_td_date_pattern == num_in_series


def string_is_blsa_date(string):
    string = str(string)
    blsa_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    if blsa_date_pattern.match(string):
        return True
    
    else:
        return False
    
def string_is_extended_blsa_date(string):
    string = str(string)
    blsa_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    
    if blsa_date_pattern.match(string):
        return True
    
    else:
        return False
    
    

def string_is_stata_td_date(string):
    string = str(string)
    
    list_of_months = ['mar',                      
     'jan',
     'may',
     'nov',
     'dec',
     'aug',
     'oct',
     'sep',
     'jun',
     'jul',
     'feb',
     'apr'
    ]
    
    string_is_td_date = True
    
    # string is 9 characters long
    if (len(string) != 9):
        return False

    # First two characters are digits
    if not re.compile(r'\d{2}\b').match(string[:2]):
        return False
    
    # Last four characters are digits    
    if not re.compile(r'\d{4}\b').match(string[-4:]):
        return False
    
    # middle three characters are in list_of_months
    if not string[2:5] in list_of_months:
        return False
    
    return True
