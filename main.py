from flask import Flask, render_template, request, jsonify
from script import script1
import csv
import time
from script2 import script2
import threading
from flask import Response

app = Flask(__name__)

def run_script2():
    script2()

def read_csv_data(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        csv_data = list(reader)
    return csv_data

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

monitoring = True

# Define a function to monitor data changes
def monitor_data():
    while monitoring:
        time.sleep(10)
        prod_csv_data = read_csv_data('./product-data.csv')
        link_csv_data = read_csv_data('./link.csv')
        
        prod_count = len(prod_csv_data)
        link_count = len(link_csv_data)
        
        # Check if there are new products added
        if prod_count >= link_count:
            # Render the template with the updated CSV data
            csv_data = read_csv_data('./product-data.csv')
            print("we are returning")
            return render_template('results.html', csv_data=csv_data)
        else:
            return monitor_data()

# Route for handling search request
@app.route('/search', methods=['POST'])
def search():
    
    def clear_csv_data(csv_file_path):
        with open(csv_file_path, 'w', newline=''):
            pass
    clear_csv_data('./product-data.csv')
    
    form_data = request.form['search_query']
    script1(form_data)
    script2_thread = threading.Thread(target=run_script2)
    script2_thread.start()
    
    csv_data = read_csv_data('./product-data.csv')
    return render_template('results.html', csv_data=csv_data)

@app.route('/get_more_data')
def get_data():
    csv_data = read_csv_data('./product-data.csv')
    return jsonify(csv_data)


if __name__ == '__main__':
    app.run(debug=True)
