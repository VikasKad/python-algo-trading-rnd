import pandas as pd
excel_loc = "sample_with_button.xlsm"
pd_excel = pd.read_excel(excel_loc)
pd_excel_required = pd_excel[['ID', 'Symbol', 'Decrement',
                              'CurrentValue', 'Increment']]
print(pd_excel_required)
