import pandas as pd
import pandasql as ps

def gen_values(program_cd, earn_sql):
    
    df3_ = df3[df3['txn_id'] == 29] # used in sql

    # Run SQL
    query = f"""
        SELECT *, {earn_sql} as earn_rule_outcome
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

    return df_dl

df_dl = df_dl(1565159)