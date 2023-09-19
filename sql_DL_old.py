import sqlparse
import pandas as pd
print(pd.__version__)
import re

#------------
# 1. Helpers
#------------
class MyStmts:
    def __init__(self):
        self.tokens = []
        self.ttype = None
        self.value = ''

def gen_pl(query):
    '''
    pl: parsed list
    query: sql query text
    '''

    # initialize df_q
    df_q = pd.DataFrame()
    df_q.at[0, 'QUERY_TEXT'] = query # assign sql text to df cell
    
    # initialize pl, to handle multiple statements
    pl = MyStmts()

    # process pl
    for index, row in df_q.iterrows(): #multiple queries in SF
        sql = row['QUERY_TEXT']
        sql = re.sub(r'--.*', '', sql) # remove comment
        #sql = sql.replace(",", ",\n") # break commas, Why need this?
        parsed = sqlparse.parse(sql) 
        root = parsed[0]
        pl.tokens.append(root)
        pl.value += row['QUERY_TEXT'] + "\n" # all sub query text are added to root
    
    return pl

def sql2tree(node, pnode_id='', local_node_id = 0, df = pd.DataFrame()):
    '''
    node is pl (parsed list of sqlparse objects)
    '''
    if node is None:
        return
    
    node_id = 'N0' if pnode_id=='' else f'{pnode_id}.{local_node_id}'
    ntype = str(node.ttype)
    Lines = len(str(node).splitlines())
    value = sqlparse.format(str(node.value), reindent=False) # format node value, NO Re-indent for long list
    value = '  ' * node_id.count('.') + value # add indentation
    Value_Len = len(value)
    
    new_row = pd.Series({'Node_ID': node_id, 'Type': ntype, 'Lines': Lines, 'Value': value, 'Value_Len': Value_Len})
    
    df = df.append(new_row, ignore_index=True)
    
    if node.ttype is None :
        for i, child in enumerate(node.tokens):
            df = sql2tree(child, node_id, i, df) # index start from 0
            
    return df

def gen_DL(query):
    pl = gen_pl(query)
    df = sql2tree(pl)
    dff = df[~df['Type'].isin([
        'Token.Text.Whitespace.Newline',
        'Token.Punctuation',
        'Token.Text.Whitespace'])].set_index('Node_ID')
    print(dff)
    return dff

#-------------
# 2. Create SQL DL
#-------------
query1 = '''
(merchantSystemIdentifier = '0010') AND 
(merchantPrincipalIdentifier = '0000') AND 
(merchantAgentIdentifier = '0000') AND 
(transactionCode in ('253','255')) AND 
(merchantCategoryCode  not in ('4899','5462','5541','5542','5733','5735','5811','5812','5813','5814','5815','5816','5971','7032','7033','7829','7832','7841','7911','7922','7929','7932','7933','7941','7991','7992','7993','7994','7996','7997','7998','7999')) AND 
(associatedMerchantSystemNumber != '6846') AND 
(associatedMerchantPrinNumber != '4660')
'''
gen_DL(query1) 