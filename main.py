from flask import Flask, request, jsonify

from database import Database
from file_parser import FileParser
from dotenv import load_dotenv
from algolia_server import AlgoliaServer
from web_crawler import WebCrawler
from flask_cors import CORS

import bcrypt

load_dotenv()

app = Flask(__name__)
CORS(app)
fileparser = FileParser()
webcrawler = WebCrawler()
algoliaserver = AlgoliaServer()
db = Database()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        #Validation
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        # # Check if user exists
        exists = db.get_user_account(email, password)
        if not exists:
            #create
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            payload = {
                "email": email,
                "password": hashed_password
            }
            id = db.insert_data("users",payload)
            return jsonify({
                'message': 'User created successfully',
                'user_id': id
            }), 201
        else:
            return jsonify({
                'message': 'User already exists'
            }), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        #Validation
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        # # Check if user exists
        id = db.get_user_account(email, password)
        if id is not None:
            #create
            return jsonify({
                'user_id': id
            }), 201
        else:
            return jsonify({
                'message': "User doesn't exists",
            }), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload-files', methods=['POST'])
def upload_files():
    files = request.files
    id = request.form["id"]
    file_list = []
    for each_file in files.keys():
        file_list = files.getlist(each_file)
    if len(file_list) > 0:
        fileparser.read_files(file_list, id)
        for each_record in fileparser.processed_files:
            algoliaserver.save_record_to_server(each_record)
        return jsonify({
            'message': 'File uploaded successfully'
        }), 200
    else:
        return jsonify({
            'message': 'No files uploaded'
        }), 403


@app.route('/add-links', methods=['POST'])
def add_links():
    body = request.get_json()
    webcrawler.parse_link(body["link"], body["id"])
    response = webcrawler.extracted_content
    if len(response) > 0:
        algoliaserver.save_record_to_server(webcrawler.extracted_content)
        return jsonify({
            'message': 'Link crawled successfully'
        }), 200
    else:
        return jsonify({
            'message': 'Unable to crawl the link'
        }), 403

if __name__ == "__main__":
    print("Starting Study Enhancement Server...")
    print()

    # Keep your existing HTTP endpoints
    app.run(debug=True, host='0.0.0.0', port=9000)


