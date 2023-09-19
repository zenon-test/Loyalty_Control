import pandas as pd
import pandasql as ps

# 1. Get Txn Data
df3 = pd.read_excel('data/tran_prog.xlsx')
df3_ = df3[df3['txn_id'] == 29]

# 2. Get Formula
df4 = pd.read_excel('data/params.xlsx')
#print(df4)
program_cd = 1565159
df4_ = df4[df4['PROGRAM_CD'] == program_cd]

# Get the value of earn_sql for that row
earn_sql = df4_['earn_sql'].values[0]
#print(earn_sql)

# Run SQL
query = f"""
    SELECT *, {earn_sql} as earn_rule_outcome
    FROM df3_
    WHERE program_name = {str(program_cd)}
"""

df3c = ps.sqldf(query, locals())
#df3c.to_excel(f'data/df3c_{str(program_cd)}.xlsx', index=False, engine='openpyxl')
#print(df3c)

value_columns = [col for col in df3c.columns if col != 'txn_id']

dfm = df3c.melt(id_vars=['txn_id'], value_vars=value_columns, 
                var_name='col_name', value_name='col_value')
dfm.to_excel(f'data/dfm_{str(program_cd)}.xlsx', index=False, engine='openpyxl')
#print(dfm)
