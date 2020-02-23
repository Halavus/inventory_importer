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
