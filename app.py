from flask import Flask, render_template, request
from scraper.court_scraper import fetch_case_data
import os
import sqlite3

app = Flask(__name__)
DB_PATH = "database/court_data.db"

# Ensure database exists
if not os.path.exists(DB_PATH):
    from database.db_setup import init_db
    init_db()
    
@app.route('/')
def home():
    case_types = [
        "ARB.A.", "BAIL APPLN.", "C.M.", "CRL.M.C.", "W.P.(C)", "W.P.(CRL)", "FAO", "RSA",
        "CS(OS)", "CS(COMM)", "TEST.CAS.", "CRL.A.", "CRL.REV.P.", "LPA", "MAC.APP.", "RC.REV.",
        "CM(M)", "RFA", "CRL.M.A.", "ARB.P.", "O.M.P.", "CRL.W.P."
    ]
    return render_template('index.html')

@app.route('/fetch',methods=['POST'])
def fetch():
    case_type = request.form['case_type']
    case_number = request.form['case_number']
    filling_year = request.form['filling_year']
    
    try:
        result, raw = fetch_case_data(case_type,case_number,filling_year,use_mock=True)
        
        # save to db
        conn =  sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO queries (case_type, case_number , filling_year, response)
                       VALUES (?,?,?,?)""",
                       (case_type, case_number, filling_year, raw))
        conn.commit()
        conn.close()
        
        return render_template('result.html',result=result,
                                            case_type=case_type,
                                            case_number=case_number,
                                            filling_year=filling_year)
    
    except Exception as e:
        return render_template("result.html", error=str(e))
    
if __name__ == '__main__':
    app.run(debug=True)