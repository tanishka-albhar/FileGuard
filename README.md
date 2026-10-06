# FileGuard — File Integrity Monitoring Tool

FileGuard is a beginner-friendly cybersecurity tool built with Python that monitors files and detects security-relevant changes.

## 🔐 What FileGuard Does

FileGuard creates a baseline of files using SHA-256 hashes and compares the current state of the files with the saved baseline.

It can detect:

- New files
- Modified files
- Deleted files
- Unchanged files

## ⚙️ Features

- SHA-256 file hashing
- File integrity monitoring
- Baseline creation
- Change detection
- JSON-based baseline storage
- Command-line interface

## 🛠️ Technologies Used

- Python
- SHA-256
- JSON
- File System
- Cybersecurity / File Integrity Monitoring

## 📂 Project Structure

```text
FileGuard/
│
├── data/
│   └── baseline.json
│
├── src/
│   ├── fileguard.py
│   └── test_folder/
│       ├── config.txt
│       ├── hello.txt
│       └── old.txt
│
└── README.md