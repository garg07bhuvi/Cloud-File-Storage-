# ☁️ Cloud File Storage

A simple cloud-style file storage web app built with Flask. Upload files, view them in a dashboard, download them, or delete them.

## Features

- Upload, download, and delete files
- Dashboard showing file name, size, and upload time
- Flash messages for success and error feedback
- Delete confirmation prompt
- Responsive, custom-styled interface

## Security

- Filenames sanitized with `secure_filename` to prevent path traversal
- Delete is POST-only, so links and browser prefetching can't remove files
- Extension whitelist for allowed file types
- 16 MB upload size limit
- Duplicate filenames handled automatically (`report.pdf` becomes `report_1.pdf`)
- Debug mode off by default

## Tech Stack

Python, Flask, HTML, CSS, JavaScript

## Getting Started

```bash
git clone https://github.com/YOUR-USERNAME/cloud-file-storage.git
cd cloud-file-storage
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Project Structure

```
├── app.py
├── requirements.txt
└── templates/
    ├── index.html
    └── files.html
```

## Future Improvements

- User authentication so each user sees only their own files
- Database for file metadata
- Cloud storage backend (e.g., AWS S3)
- Deployment with Docker

## Screenshots

*(Add screenshots of the upload page and dashboard here.)*
