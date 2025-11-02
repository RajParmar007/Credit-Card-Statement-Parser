# Credit Card Statement Parser

This project is a web application that parses PDF credit card statements from various banks (HDFC, IDFC, Axis, ICICI) and extracts key information.

It consists of two parts:

- **Python (Flask) Backend**: An API that handles the PDF parsing.
- **Next.js (Node.js) Frontend**: A local web interface to upload files and view the JSON output.

## Sample PDFs

**Note:** Due to copyright, sample PDF statements are not included in this repository.

To run this project, you must provide your own sample PDFs. Please create the following folders in the project root and add your statements to them:

- `/hdfc_statements/`
- `/idfc_statements/`
- `/axis_statements/`
- `/icici_statements/`

## How to Run This Project

You must run both the backend and frontend simultaneously in two separate terminals.

### 1. Backend (Python)

1.  Navigate to the root project folder.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  Install dependencies:
    ```bash
    pip install flask flask-cors pdfplumber
    ```
4.  Run the Flask server:
    ```bash
    python app.py
    ```
    _Your backend will be running at `http://localhost:5001`._

### 2. Frontend (Next.js)

1.  Navigate into the frontend folder:
    ```bash
    cd pdf-parser-frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:

    ```bash
    npm run dev
    ```

    _Your frontend will be running at `http://localhost:3000`._

4.  Open `http://localhost:3000` in your browser to use the app.
