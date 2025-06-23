import os
import sqlite3
import zipfile
from flask import request, send_file, current_app

def download_file():
    passcode = request.args.get('passcode')

    if not passcode:
        return "❌ Passcode is required.", 400

    conn = sqlite3.connect('swiftshare.db')
    cursor = conn.cursor()

    cursor.execute("SELECT filename FROM files WHERE passcode=?", (passcode,))
    files = cursor.fetchall()
    conn.close()

    if not files:
        return "❌ Invalid passcode.", 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    zip_filename = f"{passcode}_files.zip"
    zip_path = os.path.join(upload_folder, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for (filename,) in files:
            file_path = os.path.join(upload_folder, filename)
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=filename)

    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    else:
        return "❌ Something went wrong while creating ZIP.", 500
