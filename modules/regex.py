import re

separator="|"

regexcolor_chrome = (
        'background: linear-gradient\(135deg,'
        ' rgb\(\d+, \d+, \d+\),'
        ' rgb\(\d+, \d+, \d+\)\); color: rgb\(\d+, \d+, \d+\);'
        ' font-size: \d+.\d+px')
regexcolor_firefox = (
        'background: rgba\(\d+, \d+, \d+, \d+\)'
        ' linear-gradient\(135deg, rgb\(\d+, \d+, \d+\),'
        ' rgb\(\d+, \d+, \d+\)\) repeat scroll \d+\% \d+\%;'
        ' color: rgb\(\d+, \d+, \d+\); font-size: \d+.\d+px')

regexcolor2 = separator.join((regexcolor_chrome, regexcolor_firefox))
regexcolor = regexcolor_chrome+separator+regexcolor_firefox

matches_mat = ["H2O", "HE3", "NV1", "NV2", "[A-Z]+"]
startmat = '(?<=<span class="MaterialIcon__ticker___1qLDE5z">)'
startamount = ('(?<=<div class="MaterialIcon__indicator___2QhPuFO'
               ' MaterialIcon__type-very-small___kE8NFjh">)')

mat = ""
for i in matches_mat:
    # creates the regex string with correct syntax for every match
    mat = mat+startmat+i+separator

# TO IMPORT
inventory_importer = regexcolor+separator+mat+startamount+"\d+"

# Prodimporter

match_prodtime = '(?<=span><span>).*?(?=<\/span>)'
match_progress = '(?<="><span>)\d+(?=% done)'
units_prod = '(?<=p"><span>)\d+(?= unit)'

# TO IMPORT
prod_importer = {
        "mat": regexcolor+separator+mat+units_prod, 
        "prodtime": match_prodtime,
        "progress": match_progress}

# Screens

screen_name = '(?<=SCRN: )(?P<screen_name>.*)(?=nSCRNS)'



## Elements

# Matches 15,000,000,000,000,000.00, 45.00, 100, 5.00
# Watch out for the decimals !
#regex_prun_numbers = '(\d{1,3}(,\d{3})*(\.\d{2})?)'
regex_prun_numbers = r'((\d{1,3}(,\d{3})*(\.\d{2})?)|(\-{2}))'
rpn=regex_prun_numbers

commodity_data = {
    #ok
    'ticker': r'(?<=MAT )(H2O|HE3|NV1|NV2|[A-Z]{1,3})(?=\nCXPC)',
    #ok
    'cx': r'(?<=CX )([A-Z]{2}\d)(?=\nMAT)',
    #ok
    'last_trade': ''.join([r'(?<=\d\n)', rpn]),
    #ok
    'average': ''.join([r'(?<= Exchange\n)', rpn, r'(?=\n)']),
    #ok
    'high': ''.join([r'(?<= Average\n)', rpn, r'(?=\n)']),
    #ok
    'all_time_high': ''.join([r'(?<=\nHigh\n)', rpn, r'(?=\n)']),
    #ok
    'low': ''.join([r'(?<=\nAll-time High\n)', rpn, r'(?=\n)']),
    #ok
    'all_time_low': ''.join([r'(?<=\nLow\n)', rpn, r'(?=\n)']),
    #ok
    'ask': ''.join([r'(?<=All-time Low\n)', rpn, r'(?=\nAsk\n)']),
    #ok
    'ask_amount': ''.join([r'(?<=\nAsk\n)', rpn, r'(?=\n)']),
    #ok
    'bid': ''.join([r'(?<=\nAsk Amount\n)', rpn, r'(?=\n)']),
    #ok
    'bid_amount': ''.join([r'(?<=\nBid\n)', rpn, r'(?=\n)']),
    #ok
    'traded': ''.join([r'(?<=\nBid Amount\n)', rpn, r'(?=\n)']),
    #ok
    'volume': ''.join([r'(?<=\nTraded\n)', rpn, r'(?=\n)'])}

'''
# Old variant - Not matching every 1,000,000 ...
commodity_data = {
    #ok
    'ticker': '(?<=MAT )(H2O|HE3|NV1|NV2|[A-Z]{1,3})(?=\\nCXPC)',
    #ok
    'cx': '(?<=CX )([A-Z]{2}\d)(?=\nMAT)',
    #ok
    'last_trade': '(?<=\d\\n)(\d+\.\d{2})(?=\s[A-Z]{3}[+-]\d)',
    #ok
    'average': '(?<= Exchange\n)(\d+\.\d{2})(?=\n)',
    #ok
    'high': '(?<= Average\n)(\d+\.\d{2})(?=\n)',
    #ok
    'all_time_high': '(?<=\\nHigh\\n)(\d+\.\d{2})(?=\\n)',
    #ok
    'low': '(?<=\\nAll-time High\\n)(\d+\.\d{2})(?=\\n)',
    #ok
    'all_time_low': '(?<=\\nLow\\n)(\d+\.\d{2})(?=\\n)',
    #ok
    'ask': '(?<=All-time Low\n)(\d+\.\d{2})(?=\\n)',
    #ok
    'ask_amount': '(?<=\\nAsk\\n)(\d+\,?\d*)(?=\\n)',
    #ok
    'bid': '(?<=\\nAsk Amount\\n)(\d+\.\d{2})(?=\\n)',
    #ok
    'bid_amount': '(?<=\\nBid\\n)(\d+\,?\d*)(?=\\n)',
    #ok
    'traded': '(?<=\\nBid Amount\\n)(\d*,?\d+)(?=\\n)',
    #ok
    'volume': '(?<=\\nTraded\\n)(\d*,?\d+)(?=\\n)'}
'''
