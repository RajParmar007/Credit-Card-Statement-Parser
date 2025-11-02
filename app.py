# app.py

import pdfplumber
import io
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import all your parser classes from parsers.py
from parsers import HDFCParser, IDFCParser, AxisParser, ICICIParser

app = Flask(__name__)
# Allow requests from your Next.js app (which runs on http://localhost:3000)
CORS(app, resources={r"/parse": {"origins": "http://localhost:3000"}})

# A dictionary to map bank names to their parser classes
PARSER_MAP = {
    "hdfc": HDFCParser,
    "idfc": IDFCParser,
    "axis": AxisParser,
    "icici": ICICIParser,
}

def parse_pdf(file_storage, bank_name):
    """
    The main parsing logic.
    """
    parser_class = PARSER_MAP.get(bank_name)
    if not parser_class:
        raise ValueError("Invalid bank name provided")

    full_text = ""
    # Use io.BytesIO to read the file from memory
    with io.BytesIO(file_storage.read()) as pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    
    # Initialize and run the correct parser
    parser = parser_class(full_text)
    
    data = {
        "issuer": bank_name.upper(),
        "last_4_digits": parser.get_last_4_digits(),
        "due_date": parser.get_due_date(),
        "total_balance": parser.get_total_balance(),
        "transactions": parser.get_transactions()
    }
    return data

@app.route("/parse", methods=["POST"])
def handle_parse():
    """
    This is the API endpoint your Next.js app will call.
    """
    try:
        # 1. Get the bank name from the form data
        bank_name = request.form.get("bank")
        if not bank_name:
            return jsonify({"error": "No bank name provided"}), 400

        # 2. Get the uploaded file
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["file"]
        
        # 3. Run the parsing logic
        parsed_data = parse_pdf(file, bank_name.lower())
        
        # 4. Return the data as JSON
        return jsonify(parsed_data)

    except Exception as e:
        # Return a generic error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app on port 5001
    # (Next.js will run on 3000, so we use a different port)
    print("Starting Python backend server on http://localhost:5001")
    app.run(port=5001, debug=True)