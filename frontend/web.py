from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB connection (replace <your-db-url> with your actual MongoDB connection string)
client = MongoClient('mongodb://localhost:27017')  # Change this to your MongoDB URI if necessary
db = client['mysql']  # Replace 'mysql' with your actual database name

# Collections
users_collection = db['users']
studentdetail_collection = db['studentdetail']
company_collection = db['company']

app.template_folder = 'templates'


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/studentdetail.html')
def studentdetail():
    return render_template('studentdetail.html')


@app.route('/jobportal.html')
def jobportal():
    return render_template('jobportal.html')


# User login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.data
        json_data = json.loads(data)

        email = json_data['email']
        password = json_data['password']

        user = users_collection.find_one({'email': email})
        student = studentdetail_collection.find_one({'Email_id': email})

        if user and check_password_hash(user['password_hash'], password):
            if student:
                return {'message': 'success', 'studentDataFilled': 'true'}
            else:
                return {'message': 'success', 'studentDataFilled': 'false'}
        else:
            return {'message': 'ERROR: Invalid email or password'}


# User registration route
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.data
        json_data = json.loads(data)

        username = json_data['username']
        email = json_data['email']
        password = json_data['password']

        password_hash = generate_password_hash(password)

        users_collection.insert_one({
            'username': username,
            'email': email,
            'password_hash': password_hash
        })

        return {'message': 'success'}


# Route to handle form submission for student details
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.data
            form_data = json.loads(data)

            # Validate incoming data
            required_fields = ['first_name', 'last_name', 'birthday_day', 'birthday_month', 'birthday_year', 'email', 'mobile_number', 'gender', 'address']
            for field in required_fields:
                if field not in form_data:
                    return f"Missing field: {field}", 400  # Bad request if any field is missing

            # Construct the DOB string
            dob_string = '-'.join([form_data['birthday_year'], form_data['birthday_month'].zfill(2), form_data['birthday_day'].zfill(2)])
            # Convert to datetime object
            dob = datetime.strptime(dob_string, '%Y-%m-%d')

            studentdetail_collection.insert_one({
                'First_name': form_data['first_name'],
                'Last_name': form_data['last_name'],
                'DOB': dob,
                'Email_id': form_data['email'],
                'Mobile_No': form_data['mobile_number'],
                'Gender': form_data['gender'],
                'Address': form_data['address']
            })

            return 'Form submitted successfully', 200
        except Exception as e:
            print(f"Error: {e}")  # Log the error to the console
            return str(e), 500


# Serialization function for MongoDB documents
def company_serializer(obj):
    return {
        'name': obj['company_name'],
        'location': obj['location'],
        'company_type': obj['company_type'],
        'skill': obj['skill'],  # No need to convert to string if skill is a list
        'salary': obj['salary'],  # Let salary remain as an integer
        'cgpa': obj['cgpa']  # Keep CGPA as a float
    }


# Function to get filtered companies
def get_filtered_companies(filters):
    query = {}

    if filters.get('cgpa', 0) > 0:
        query['cgpa'] = {"$gte": filters['cgpa']}
    if filters.get('location'):
        query['location'] = {'$regex': filters['location'], '$options': 'i'}
    if filters.get('salary', 0) > 0:
        query['salary'] = {"$gte": filters['salary']}
    if filters.get('company-type'):
        query['company_type'] = {'$regex': filters['company-type'], '$options': 'i'}
    if filters.get('skill'):
        query['skill'] = {'$all': filters['skill']}

    # DEBUG: Print the query to see if it's formed correctly
    print("MongoDB Query:", query)

    filtered_companies = company_collection.find(query)
    
    serialized_companies = [company_serializer(company) for company in filtered_companies]

    # DEBUG: Print filtered companies before returning
    print("Filtered Companies: ", serialized_companies)

    return serialized_companies



# Filtered companies route
@app.route('/filtered-companies', methods=['POST'])
def filter():
    if request.method == 'POST':
        data = request.data
        json_data = json.loads(data)

        filters = {
            'cgpa': float(json_data.get('cgpa', 0)),
            'location': json_data.get('location', ''),
            'salary': int(json_data.get('salary', 0)),
            'company-type': json_data.get('company-type', ''),
            'skill': json_data.get('skill', [])
        }

        # DEBUG: Print received filters
        print("Received filters:", filters)

        companies = get_filtered_companies(filters)

        # DEBUG: Print companies returned from the filter function
        print("Filtered companies:", companies)

        return jsonify(companies)  # Return list of companies as JSON
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
