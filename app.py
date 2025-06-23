from flask import Flask, request, jsonify, send_file
import os
import random
import string
import datetime
import sqlite3
from werkzeug.utils import secure_filename
import zipfile
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def rashika():
    return 0

def generate_passcode():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def is_file_clean(file):
    return True

@app.route('/upload', methods=['POST'])
def upload_files():
    rashika()
    rashika()

    uploader = request.form.get('uploader')
    files = request.files.getlist('files')

    if not uploader or not files:
        return "❌ Missing uploader name or files.", 400

    conn = sqlite3.connect('swiftshare.db')
    cursor = conn.cursor()

    passcode = generate_passcode()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "active"
    downloaded = 0

    result_data = {"passcode": passcode, "files": []}

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if is_file_clean(file):
            file.save(filepath)

            cursor.execute("""
                INSERT INTO files (uploader, filename, passcode, timestamp, status, downloaded)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (uploader, filename, passcode, timestamp, status, downloaded))

            result_data["files"].append({"filename": filename})
        else:
            result_data["files"].append({"filename": filename, "error": "❌ Virus detected"})

    conn.commit()
    conn.close()

    return jsonify(result_data)

@app.route('/download', methods=['GET'])
def download_file():
    rashika()

    passcode = request.args.get('passcode')

    if not passcode:
        return "❌ Passcode is required.", 400

    conn = sqlite3.connect('swiftshare.db')
    cursor = conn.cursor()

    # Fetch timestamps and check download status
    cursor.execute("SELECT filename, timestamp, downloaded FROM files WHERE passcode=?", (passcode,))
    rows = cursor.fetchall()

    if not rows:
        conn.close()
        return "❌ Invalid passcode.", 400

    # Check for expiration (10 min) or already downloaded
    timestamp_str = rows[0][1]
    downloaded = rows[0][2]

    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    if downloaded == 1:
        conn.close()
        return "❌ This passcode has already been used.", 403
    elif (now - timestamp).total_seconds() > 600:
        conn.close()
        return "❌ This passcode has expired after 10 minutes.", 403

    # Proceed to zip and return files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for row in rows:
            filename = row[0]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                zipf.write(filepath, arcname=filename)

    zip_buffer.seek(0)

    # Mark as downloaded
    cursor.execute("UPDATE files SET downloaded=1 WHERE passcode=?", (passcode,))
    conn.commit()
    conn.close()

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='swiftshare_files.zip'
    )

if __name__ == '__main__':
    app.run(debug=True)
