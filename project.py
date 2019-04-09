# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:36:16 2019

@author: Kunal
"""

import numpy as np
import pandas
from sqlalchemy import create_engine

# to keep track of the column corresponding to a number in signature
signature = {1: 6, 2: 7, 3: 8, 4: 9, 5: 10}
    
def notRedundant(lean_database, tuples):
    for rows in lean_database:
        # check if the plot types are same.
        if tuples[3] == rows[3]:
            # Plot types are same, check signatures
            rowsSignature = [int(x) for x in str(int(rows[2]))] if not np.isnan(rows[2]) else []
            tupleSignature = [int(x) for x in str(int(tuples[2]))] if not np.isnan(tuples[2]) else []
            
            if set(tupleSignature).issuperset(set(rowsSignature)):
                # tuple signature is a superset, now check if they 
                # agree on the variables in the row signature.
                if len(tupleSignature) != 0:
                    flag = 0
                    for letter in rowsSignature:
                        if rows[signature[letter]] != tuples[signature[letter]]:
                            flag = 1
                            break
                    # flag = 1 means that the variables in the signature don't agree. 
                    # So, tuple cannot be an extension of the current row. Check next row.
                    if flag == 1:
                        continue
                if tuples[11] < rows[11] + 0.05:
                    return False, None
            # If the signatures are same and the new tuple is not an extension 
            # of the earlier one, check if the previous one is an extension of the new tuple.
            if rows[2] == tuples[2] and rows[11] < tuples[11] + 0.05:
                return False, rows
    return True, None

def saveToDatabase(data_frame):
    selectQuery = ("SELECT * FROM test_database.wine_charts_lean")
    engine = create_engine("mysql://kmokashi:Amazon123@mysqlkunal.cwef3mafxix3.us-east-2.rds.amazonaws.com/test_database")
    connection = engine.connect()
    data_frame.to_sql(name='wine_charts_lean', con=connection, if_exists='replace')
    connection.execute(selectQuery).fetchall()
    connection.close()
    
if __name__ == '__main__':
    wine_charts = pandas.read_csv('wine_charts2.csv')
    lean_database = []
    redundant_tuples = 0
    for tuples in wine_charts.itertuples():
        nonRedundant, removeRow = notRedundant(lean_database, tuples)
        if nonRedundant:
            lean_database.append(tuples)
        elif not nonRedundant and removeRow is not None:
            lean_database.remove(removeRow)
            lean_database.append(tuples)
            redundant_tuples+=1
        else:
            redundant_tuples+=1
    data_frame = pandas.DataFrame(lean_database)
    data_frame = data_frame.drop(data_frame.columns[[0]], axis = 1)
    data_frame = data_frame.set_index('id')
    data_frame.to_csv('wine_charts_lean.csv')
    saveToDatabase(data_frame)
    
    print("Number of redundant tuples - ", redundant_tuples)
    
