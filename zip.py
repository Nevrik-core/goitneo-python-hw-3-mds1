import zipfile
import os

def zip_files(zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk('.'):
            for file in files:
                if file != zip_filename and file != 'zip.py':
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), '.'))

if __name__ == "__main__":
    zip_files('goitneo-python-hw-2-mds1.zip')
