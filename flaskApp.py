from flask import Flask, render_template, request
import sqlalchemy
from sqlalchemy.sql import text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def getDetailsFromDatabase():
    result = []
    name = request.args.get('name')
    engine = sqlalchemy.create_engine("mysql://kmokashi:Amazon123@mysqlkunal.cwef3mafxix3.us-east-2.rds.amazonaws.com/test_database")
    connection = engine.connect()
    if name == '':
        selectQuery = "select * from wine_charts_lean"
    else:
        name = [x.strip() for x in name.split(',')]
        whereClause = []
        for val in name:
            keys = [x.strip() for x in val.split('=')]
            if len(keys) == 2:
                if keys[0] == 'month':
                    whereClause.append(keys[0] + "=" + keys[1])
                else:
                    whereClause.append(keys[0] + "=" + "'" + keys[1] + "'")
        if len(whereClause) == 0:
            return render_template('search.html', results = [])
        whereClause = " and ".join(whereClause)
        selectQuery = text("select * from wine_charts_lean where " + whereClause)
    resultset = connection.execute(selectQuery).fetchall()
    i = 1
    for row in resultset:
        innerResult = []
        innerResult.append(i)
        innerResult.append(row['id'])
        innerResult.append(" " if row['signature'] is None else int(row['signature']))
        innerResult.append(row['plot_type'])
        innerResult.append(" " if row['variable_1'] is None else row['variable_1'])
        innerResult.append(" " if row['variable_2'] is None else row['variable_2'])
        innerResult.append(" " if row['day'] is None else row['day'])
        innerResult.append(" " if row['gender'] is None else row['gender'])
        innerResult.append(" " if row['location'] is None else row['location'])
        innerResult.append(" " if row['month'] is None else int(row['month']))
        innerResult.append(" " if row['source'] is None else row['source'])
        innerResult.append(" " if row['score'] is None else row['score'])
        innerResult.append(" " if row['support'] is None else row['support'])
        innerResult.append(" " if row['dataset'] is None else row['dataset'])
        result.append(innerResult)
        i+=1
    return render_template('search.html', results = result)