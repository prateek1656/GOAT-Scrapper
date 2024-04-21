from flask import Flask, render_template, request, redirect, url_for
from script import script1
import csv
from script2 import script2

app = Flask(__name__)

def read_csv_data(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        csv_data = list(reader)
    return csv_data

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/search', methods=['POST'])
def search():
    form_data = request.form['search_query']
    script1(form_data)
    script2()
    
    csv_data = read_csv_data('./product-data.csv')
    return render_template('results.html', csv_data=csv_data)
    

if __name__ == '__main__':
    app.run(debug=True)
