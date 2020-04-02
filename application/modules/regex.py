separator = "|"

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
startmat = '(?<=<span class="ColoredIcon__label___j9bHRXy">)'
startamount = ('(?<=<div class="MaterialIcon__indicator___2QhPuFO'
               ' MaterialIcon__type-very-small___kE8NFjh">)')

## BLCK & SHPT items in inventory

# Filter by BLCK or SHPT #number

startnum = '(?<=<div><div class="GridItemView__container___2w6wM6r" draggable="true"><div class="GridItemView__image___qBVipu1"><div class="ColoredIcon__container___1H-MG70" title=")'
lookup = '(Shipment #\d+)|(Blocked Materials #\d+)'
endnum = '(?=" style=")'

num = startnum+lookup+endnum

startblsh = '(?<=<div><div class="GridItemView__container___2w6wM6r" draggable="true"><div class="GridItemView__image___qBVipu1"><div class="ColoredIcon__container___1H-MG70" title="'

#endblsh = '(?=#\d+</span></div></div>)'
#blck = startblck+'.*'+endblck

def cleaner(num, start=startblsh):
    startblsh = start+num+')'
    endblsh = '(?='+num+')'
    lookup = '.*'

    return startblsh+lookup+endblsh

# Inventory

mat = ""
for i in matches_mat:
    # generate the regex string with correct syntax for every match
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
# also matches the --
regex_prun_numbers = r'((\d{1,3}(,\d{3})*(\.\d{2})?)|(\-{2}))'
rpn = regex_prun_numbers

commodity_data = {
    'ticker': r'(?<=MAT )(H2O|HE3|NV1|NV2|[A-Z]{1,3})(?=\nCXPC)',
    'cx': r'(?<=CX )([A-Z]{2}\d)(?=\nMAT)',
    'last_trade': ''.join([r'(?<=\d\n)', rpn]),
    'average': ''.join([r'(?<= Exchange\n)', rpn, r'(?=\n)']),
    'high': ''.join([r'(?<= Average\n)', rpn, r'(?=\n)']),
    'all_time_high': ''.join([r'(?<=\nHigh\n)', rpn, r'(?=\n)']),
    'low': ''.join([r'(?<=\nAll-time High\n)', rpn, r'(?=\n)']),
    'all_time_low': ''.join([r'(?<=\nLow\n)', rpn, r'(?=\n)']),
    'ask': ''.join([r'(?<=All-time Low\n)', rpn, r'(?=\nAsk\n)']),
    'ask_amount': ''.join([r'(?<=\nAsk\n)', rpn, r'(?=\n)']),
    'bid': ''.join([r'(?<=\nAsk Amount\n)', rpn, r'(?=\n)']),
    'bid_amount': ''.join([r'(?<=\nBid\n)', rpn, r'(?=\n)']),
    'traded': ''.join([r'(?<=\nBid Amount\n)', rpn, r'(?=\n)']),
    'volume': ''.join([r'(?<=\nTraded\n)', rpn, r'(?=\n)'])}
