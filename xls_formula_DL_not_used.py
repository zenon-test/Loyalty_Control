from copy import copy
from textwrap import indent
import pandas as pd
import numpy as np
from pycel.excelformula import ExcelFormula, FunctionNode
import re
from bs4 import BeautifulSoup
import js2py
import openpyxl
from openpyxl.worksheet.table import Table


def beautify(formula_val, result, tempfile):
    # download https://github.com/joshbtn/excelFormulaUtilitiesJS/blob/main/dist/excel-formula.js
    result= tempfile.excelFormulaUtilities.formatFormulaHTML(formula_val)
    r2 = result.replace('<br />', '\n') #.replace('&nbsp;',' ')
    soup = BeautifulSoup(r2)
    bf = soup.get_text() # beautified formula
    bf = bf.replace(u'\xa0', u' ')
    return bf

def break_colon(formula):
    """
    Function which return full formula after breaking colon
    
    Arguments:
    arg {str}  : Formula text with colon
    
    Return: 
    A new formula string
    
    """

    sheetname = str(formula[:formula.find('[')]).strip()
    funcname = str(sheetname[sheetname.rfind('(')+1:]).strip()
    
    var_1 = str(formula[formula.find('@')+1:formula.find(':')]).strip()
    var_2 = str(formula[formula.find(':')+1:][:formula[formula.find(':')+1:].find(']')+1]).strip()

    tail = str(formula[formula.find(':')+1:][formula[formula.find(':')+1:].find(']')+2:]).strip()


    formula_new = str(sheetname + '[@' + var_1 + '], ' + funcname + '[@' + var_2 + ']' + tail)

    return formula_new

def intermediary_column(arg1,arg2, var_ls):
    """
    Function which return intermediary column names
    
    Arguments:
    arg1 {str}  : First argument of formula
    arg2 {str}  : Last argument of formula
    var_ls {list}  : List of all variable as per the excel order 
    
    Return: 
    A List with elements as arg1, all intermediary columns and arg2
    
    """
    c = []
    for i, s in enumerate(var_ls):
        if arg1 == s:
            c.append(i)
        if arg2 == s:
            c.append(i+1)
    return (var_ls[c[0]:c[1]])

def formula_preprocess(input_formula, df):
    """
    Function which return formatted formula adding all hidden columns from functions
    
    Arguments:
    formula {str} : input formula with hidden columns 
    df {DataFrame} : Dataframe generated from excel with all relevant columns 
    
    Return: 
    Formuatted formula with all hidden columns 
    
    """
    var_ls = df['FORMULA COLUMN NAME'].unique().tolist()    
    val_clean = input_formula.split(",")
    out_new = ''
    for val in val_clean:
        if val.find(":") !=-1:
    #         formula = ExcelFormula(val)
            l = []
            for i in [x.split("@") for x in break_colon(val).split(",")]:
                l.append(str(re.search('(?<=\[).*?(?=\])',str(i[1])).group()))
            all_vars = intermediary_column(l[0],l[1], var_ls)

            s = []
            for i in range(1, len(all_vars)-1):
                s.append("RedressCalc[@[" + all_vars[i] + "]]")
    #         print("\n")
            new_ls = break_colon(val).split(",")
            new = ','.join([new_ls[0]] + s + [new_ls[1]])
    #         print(new)
            out_new = out_new + ',' + new
#             out_new =  out_new + "," +new 
        else:
            out_new = out_new + ","+ val

    return out_new[1:]

def get_varname(formula):
    var = formula[formula.find('@'):formula.find(']')][formula[formula.find('@'):formula.find(']')].find('[')+1:]
    return var

def init_tree(formula_df, variable, output_path):
    # initialize tree with formula sheet, root variable and node_id for root variable
    df = formula_df
    start_node = variable

    # Find the index of the starting node in the setup sheet
    row_index = formula_df.index[formula_df['FORMULA COLUMN NAME'] == start_node].tolist()

    # Get the formula for starting node
    val = formula_df.at[row_index[0], 'FORMULA VALUES']

    # Pass the formula of starting node into ExcelFormula parser
    formula = ExcelFormula(val)

    # Get the Abstract syntax tree for the formula
    my_node = formula.ast

    # Initialize id for the starting node
    my_node_id = '1'
        
    smallfile = open(output_path, "w")
    smallfile.write('Node_ID,Variable,Formula\n')

    # Writing the first line to the csv
    smallfile.write(my_node_id + ',' + start_node + '\n')

    build_tree(my_node, my_node_id, df, smallfile)

def build_tree(node, node_id, formula_df, smallfile):

    """This function create a tree with node id from the start node using the formula list and outputs a csv representation of the tree
    Args:
        node (ast): the abstract syntax tree of the root formula
        node_id (str): node_id of the root node
        formula_df (pandas dataframe): a pandas dataframe that contains all the formulas and variable names to be created
        smallfile (file.csv): the output file to which the tree is written to
    
    Outputs:
        A csv representation of the tree
    
    """

    # Keep unique and meaningful child only; include numbers if necessary
    res = []
    
    # DEDUP DESCENDANTS
    for i in range(0, len(node.descendants)):
        dup_flg = False
        if node.descendants[i][0].subtype == 'RANGE':
            for j in range(0, i - 1):
                if node.descendants[i][0].value == node.descendants[j][0].value: dup_flg = True                  
            if not dup_flg: res.append(node.descendants[i])          

    data = []

    for i, child in enumerate(res):       
        if child[0].type == 'OPERAND':
            child_id = node_id + "." + str(i+1) 
                       
            if str(child[0]).count('@') == 0:  
                child_nodename = str(child[0])
            else:
                child_nodename = get_varname(str(child[0]))


            smallfile.write(child_id + ',' + child_nodename + '\n')
            # print(child_id, child_nodename)
           
            if child_nodename in formula_df['FORMULA COLUMN NAME'].unique().tolist(): # chech whole formula var list
                row_index = formula_df.index[formula_df['FORMULA COLUMN NAME'] == child_nodename].tolist()
                val = formula_df.at[row_index[0], 'FORMULA VALUES']

                if ':' in val and child_nodename != 'Redress_Method':
                    print(row_index, " ", val, child_nodename)
                    new_val = formula_preprocess(val, formula_df)
                    val = val.replace(val,new_val) 

                # print(row_index, " ", val, child_nodename)
                formula = ExcelFormula(val)
                # print(type(formula))
                mynode = formula.ast
                build_tree(mynode, child_id, formula_df, smallfile=smallfile)

def add_formula_to_tree(formula_df, tree_df):
    formula_df = formula_df[['FORMULA COLUMN NAME','FORMULA VALUES']]
    tree_df = tree_df.merge(formula_df, how='left', left_on='Variable', right_on='FORMULA COLUMN NAME')
    tree_df = tree_df[['Node_ID', 'Variable', 'FORMULA VALUES']].rename(columns={'FORMULA VALUES':'Formula'}).reset_index(drop=True)
    result, tempfile = js2py.run_file("Darish_E2E_Calculator/src/excel-formula.js")
    tree_df.Formula = tree_df.Formula.astype(str).apply(lambda row: beautify(row, result, tempfile))
    tree_df.Formula = "'" + tree_df.Formula

    return tree_df


def main():

    formula_df = pd.read_excel('Darish_E2E_Calculator/data/MDO/MDO_1.0_Decision_Lineage.xlsm'
    , sheet_name='Setup_Sheet'
    , skiprows=1
    , nrows= 64
    , usecols='EM:ER'
    , names = ['BT SCRUB COLUMN NAMES', 'FORMULA COLUMN NAME', 'FORMULA VALUES', 'FORMAT', 'Display BT Scrub in Calc', 'Is column Displayed in Calc']
    )

    init_tree(formula_df=formula_df, variable='Redress_Amt', output_path='Darish_E2E_Calculator/data/out.csv')



