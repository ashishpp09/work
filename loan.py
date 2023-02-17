from flask import Flask , jsonify , request
import pickle
import pandas as pd
import numpy as np 
import mysql.connector as  sql

app=Flask(__name__)

mydb = sql.connect(host = 'localhost',
                  user = 'root',
                  passwd = '14920151',
                  use_pure = True,
                  database = 'loan_data')

print(mydb)

mycursor = mydb.cursor()


log_model = pickle.load(open('log_model.pickle','rb'))

@app.route('/')
def main():
    return jsonify({'Message' : 'Model Activated'})



@app.route('/loan_approval_system',methods = ['POST','GET'])
def loan_approval_prediction():
    global data 
    data = request.get_json()
    Gender = data['Gender']
    Married = data['Married']
    Dependents = data['Dependents']
    Education = data['Education']
    Self_Employed = data['Self_Employed']
    ApplicantIncome = data['ApplicantIncome']
    CoapplicantIncome = data['CoapplicantIncome']
    LoanAmount = data['LoanAmount']
    Loan_Amount_Term = data['Loan_Amount_Term']
    Credit_History = data['Credit_History']
    Property_Area = data['Property_Area']
    
    
    d = {'Gender':[Gender],
         'Married':[Married],
         'Dependents':[Dependents],
         'Education':[Education],
         'Self_Employed':[Self_Employed],
         'ApplicantIncome':[ApplicantIncome],
         'CoapplicantIncome':[CoapplicantIncome],
         'LoanAmount':[LoanAmount],
         'Loan_Amount_Term':[Loan_Amount_Term],
         'Credit_History':[Credit_History],
         'Property_Area':[Property_Area],   
         }
    input = pd.DataFrame(d)
    
    prediction = log_model.predict(input)
    
    insert_query = ("""INSERT INTO loan_data.new_loan_data (Gender,
    Married,
    Dependents,
    Education,
    Self_Employed,
    ApplicantIncome,
    CoapplicantIncome,
    LoanAmount,
    Loan_Amount_Term,
    Credit_History,
    Property_Area
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""") 

    data = (data['Gender'],data['Married'],data['Dependents'],data['Education']
            ,data['Self_Employed'],data['ApplicantIncome'],data['CoapplicantIncome'],data['LoanAmount'],
            data['Loan_Amount_Term'],data['Credit_History'],data['Property_Area'])
    
    print(data)
    try:
        mycursor.execute(insert_query,data)
        mydb.commit()
        print('We are in try block')
    except:
        mydb.rollback()
        print('We are in except block')
    
    return jsonify({'Approval Status': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
    
    
"""
(Gender,
Married,
Dependents,
Education,
Self_Employed,
ApplicantIncome,
CoapplicantIncome,
LoanAmount,
Loan_Amount_Term,
Credit_History,
Property_Area"""




    
    
    


app = Flask(__name__)
