# 🔍 MetaHunter

**Professional Metadata Extraction & Sanitization Tool for Security Professionals**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Debian-red.svg)](https://kali.org)

MetaHunter is a comprehensive metadata analysis tool designed for cybersecurity professionals, OSINT investigators, and digital forensics experts. Extract hidden metadata or strip it entirely to protect privacy—all from a clean, professional CLI interface.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **📸 Multi-Format Support** | Images (JPG, PNG, TIFF, HEIC, RAW), Audio (MP3, FLAC, WAV), Video (MP4, MKV, MOV), Documents (PDF, DOCX, XLSX, PPTX) |
| **🔎 Deep Metadata Extraction** | GPS coordinates, author names, device models, software versions, timestamps, camera settings, edit history |
| **⚠️ Privacy Risk Detection** | Automatically flags GPS locations, emails, phone numbers, and author identities |
| **🧹 Safe Metadata Stripping** | Creates clean copies—never modifies original files |
| **📊 Export Reports** | Save findings as JSON, CSV, or plain text for documentation |
| **⚡ Batch Processing** | Analyze or sanitize entire folders recursively |

---

## 🚀 Quick Installation

```bash
# Clone the repository
git clone https://github.com/kazim-45/metahunter_tool.git
cd metahunter_tool

# Run the automated installer
chmod +x install.sh
./install.sh

# Launch MetaHunter
python3 metahunter.py
```

**Manual Installation:**
```bash
# Install core dependencies
sudo apt install libimage-exiftool-perl mat2
pip install rich
```

---

## 🎯 Use Cases

### 🔍 OSINT Investigations
Extract metadata from publicly available files to identify device types, authors, and even GPS coordinates.

### 🛡️ Digital Forensics
Batch-analyze evidence folders for timestamp inconsistencies, device trails, and document authorship.

### 🔒 Privacy Hardening
Strip metadata before sharing sensitive files online—perfect for journalists, activists, and privacy-conscious users.

### 🏆 CTF Challenges
Quickly inspect challenge files for hidden metadata clues during capture-the-flag competitions.

---

## 📖 Usage Examples

```bash
# Extract metadata from a single file
python3 metahunter.py -i image.jpg

# Batch extract from entire folder
python3 metahunter.py -d /path/to/folder

# Strip metadata (creates clean copy)
python3 metahunter.py -s image.jpg

# Batch strip folder contents
python3 metahunter.py -d /path/to/folder -s

# Export report in JSON format
python3 metahunter.py -i image.jpg -o report.json
```

---

## 🖥️ Output Example

```
╭─────────────────────────────────────────────╮
│           M E T A H U N T E R               │
│         Metadata Analysis Tool              │
╰─────────────────────────────────────────────╯

📁 File: vacation_photo.jpg
────────────────────────────────────────────────
📍 GPS Coordinates: 40.7128° N, 74.0060° W
👤 Author: John Doe
📱 Device: iPhone 14 Pro
🕒 Timestamp: 2024-07-15 14:23:45
⚠️ Camera: Apple iPhone 14 Pro back camera

[!] PRIVACY RISK DETECTED: Location data found
[!] PRIVACY RISK DETECTED: Author name found

Report saved to: MetaHunter_Reports/vacation_photo_metadata.json
```

---

## 📁 Project Structure

```
metahunter_tool/
├── metahunter.py          # Main application
├── install.sh             # Automated dependency installer
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── MetaHunter_Reports/    # Output directory (created on first run)
└── LICENSE                # MIT License
```

---

## 🔧 Requirements

- **OS:** Kali Linux / Debian-based distributions
- **Python:** 3.8 or higher
- **Dependencies:** exiftool, mat2, rich

---

## ⚠️ Legal Disclaimer

MetaHunter is designed for **legitimate security research, authorized penetration testing, and personal privacy protection**. Users are responsible for ensuring they have proper authorization before analyzing files. The author assumes no liability for misuse of this tool.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Kazim Khan**
- GitHub: [@kazim-45](https://github.com/kazim-45)
- Portfolio [kazimportfolio](https://kazimportfolio.vercel.app)

---

## 🙏 Acknowledgments

- Built with [exiftool](https://exiftool.org/) by Phil Harvey
- Icons and inspiration from the OSINT community

---

**⭐ If this tool helped you, consider giving it a star!**
