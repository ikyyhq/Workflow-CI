import os
import sys
import json
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

GDRIVE_FOLDER_ID = "1B1BMP7JN-Oh14bpQ1Do_dNdJ-QpcTdV0"

def main():
    # 1. Mengambil argumen path folder dari GitHub Actions 
    if len(sys.argv) < 2:
        print("Error: Path folder model tidak diberikan.")
        sys.exit(1)
        
    model_dir = sys.argv[1]
    
    # 2. Membaca kredensial Service Account dari GitHub Secrets
    creds_json_str = os.environ.get("GDRIVE_CREDENTIALS")
    if not creds_json_str:
        print("Error: Secret GDRIVE_CREDENTIALS tidak ditemukan di environment.")
        sys.exit(1)

    print("Membaca kredensial dan melakukan autentikasi...")
    creds_dict = json.loads(creds_json_str)
    credentials = service_account.Credentials.from_service_account_info(creds_dict)

    # 3. Membangun koneksi ke Google Drive API
    drive_service = build('drive', 'v3', credentials=credentials)

    # 4. Melakukan kompresi folder model menjadi file .zip
    print(f"Mengompres folder {model_dir} menjadi zip...")
    zip_filename = "heart_failure_model_artifact"
    shutil.make_archive(zip_filename, 'zip', model_dir)
    zip_filepath = f"{zip_filename}.zip"

    # 5. Mengatur metadata untuk Google Drive
    file_metadata = {
        'name': 'model_advance_terbaru.zip',
        'parents': [GDRIVE_FOLDER_ID]
    }
    
    # 6. Mengunggah file
    media = MediaFileUpload(zip_filepath, mimetype='application/zip', resumable=True)
    
    print(f"Mengunggah {zip_filepath} ke Google Drive (Folder ID: {GDRIVE_FOLDER_ID})...")
    request = drive_service.files().create(body=file_metadata, media_body=media, fields='id')
    response = request.execute()

    print(f"Upload berhasil dengan sukses! File ID di GDrive: {response.get('id')}")

if __name__ == '__main__':
    main()