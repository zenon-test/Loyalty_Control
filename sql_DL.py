import sqlparse
import pandas as pd
import re
import pandasql as ps

# 1. Helpers
class MyStmts:
    def __init__(self):
        self.tokens = []
        self.ttype = None
        self.value = ''

def gen_pl(query):
    df_q = pd.DataFrame(columns=['QUERY_TEXT'], dtype='object')
    df_q.at[0, 'QUERY_TEXT'] = query
    pl = MyStmts()
    for index, row in df_q.iterrows():
        sql = row['QUERY_TEXT']
        sql = re.sub(r'--.*', '', sql)
        parsed = sqlparse.parse(sql) 
        root = parsed[0]
        pl.tokens.append(root)
        pl.value += row['QUERY_TEXT'] + "\n"
    return pl

def sql2tree(node, pnode_id='', local_node_id=0):
    if node is None:
        return []

    node_id = 'N0' if pnode_id == '' else f'{pnode_id}.{local_node_id}'
    ntype = str(node.ttype)
    Lines = len(str(node).splitlines())
    value = sqlparse.format(str(node.value), reindent=False)
    value = '  ' * node_id.count('.') + value
    Value_Len = len(value)
    results = [{'Node_ID': node_id, 'Type': ntype, 'Lines': Lines, 'Value': value, 'Value_Len': Value_Len}]
    
    if node.ttype is None:
        for i, child in enumerate(node.tokens):
            results.extend(sql2tree(child, node_id, i))
    return results

def gen_DL(query):
    pl = gen_pl(query)
    df_list = sql2tree(pl)
    df = pd.DataFrame(df_list)
    dff = df[~df['Type'].isin([
        'Token.Text.Whitespace.Newline',
        'Token.Punctuation',
        'Token.Text.Whitespace'])] #.set_index('Node_ID')
    return dff

def process_dff(dff):
    # Filter rows based on conditions
    df2 = dff[(dff['Node_ID'] == 'N0') | (dff['Type'] == 'Token.Name')].copy()

    # Create 'Variable' column based on conditions using loc
    df2['Variable'] = ''
    df2.loc[df2['Node_ID'] == 'N0', 'Variable'] = 'earn_rule_outcome'
    df2.loc[df2['Type'] == 'Token.Name', 'Variable'] = df2['Value']

    # Copy 'Value' column to 'Formula'
    df2['Formula'] = df2['Value']

    # Keep only the desired columns
    df2 = df2[['Node_ID', 'Variable', 'Formula']]

    return df2

def get_formula(program_cd):
    # 2. Get Formula
    df4 = pd.read_excel('data/params.xlsx')
    #print(df4)
    
    df4_ = df4[df4['PROGRAM_CD'] == program_cd]

    # Get the value of earn_sql for that row
    earn_sql = df4_['earn_sql'].values[0]
    #print(earn_sql)
    return earn_sql

def gen_values(program_cd, earn_sql):
    df3 = pd.read_excel('data/tran_prog.xlsx')
    df3_ = df3[df3['txn_id'] == 29] # used in sql

    # Run SQL
    query = f"""
        SELECT *, {earn_sql} as earn_rule_outcome_{program_cd}
        FROM df3_
        WHERE program_name = {str(program_cd)}
    """

    df3c = ps.sqldf(query, locals())

    value_columns = [col for col in df3c.columns if col != 'txn_id']

    dfm = df3c.melt(id_vars=['txn_id'], value_vars=value_columns, 
                    var_name='col_name', value_name='col_value')
    return dfm

def df_dl(program_cd):
    earn_sql = get_formula(program_cd)
    dff = gen_DL(earn_sql)
    df2 = process_dff(dff)
    dfm = gen_values(program_cd, earn_sql)
    q = f"""
        SELECT df2.Node_ID, df2.Variable, dfm.col_value, df2.Formula
        FROM df2 
        LEFT JOIN dfm on dfm.col_name = TRIM(df2.Variable)
    """
    df_dl = ps.sqldf(q, locals())
    df_dl.to_excel(f'data/df_dl_{str(program_cd)}.xlsx', index=False, engine='openpyxl')
    return df_dl

# 2. Create SQL DL
#df_dl = df_dl(1565159)
df_dl = df_dl(1565160)
print(df_dl)





#query1 = '''
# (merchantSystemIdentifier = '0010') AND 
# (merchantPrincipalIdentifier = '0000') AND 
# (merchantAgentIdentifier = '0000') AND 
# (transactionCode in ('253','255')) AND 
# (merchantCategoryCode  not in ('4899','5462','5541','5542','5733','5735','5811','5812','5813','5814','5815','5816','5971','7032','7033','7829','7832','7841','7911','7922','7929','7932','7933','7941','7991','7992','7993','7994','7996','7997','7998','7999')) AND 
# (associatedMerchantSystemNumber != '6846') AND 
# (associatedMerchantPrinNumber != '4660')
# '''



