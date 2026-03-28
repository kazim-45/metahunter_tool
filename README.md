# MetaHunter 🔍
**Metadata Extraction & Sanitization Tool for Kali Linux**

> Built for cybersecurity professionals, OSINT analysts, and privacy-conscious users.

---

## What It Does

MetaHunter extracts and removes hidden metadata from files — the kind of data that can silently expose GPS locations, author identities, device models, software names, and timestamps.

**Supported file types:** Images (JPG, PNG, TIFF, RAW, HEIC...) · Audio (MP3, FLAC, WAV, OGG...) · Video (MP4, MKV, MOV...) · Documents (PDF, DOCX, XLSX, PPTX...)

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/MetaHunter.git
cd MetaHunter

# 2. Run the installer (handles all dependencies)
chmod +x install.sh
./install.sh

# 3. Launch
python3 metahunter.py
```

---

## Manual Install (if needed)

```bash
# Install system dependency (core engine)
sudo apt install libimage-exiftool-perl

# Install optional stripper
sudo apt install mat2

# Install Python UI library
pip install rich
```

---

## Features

| Feature | Description |
|---|---|
| **Extract Metadata** | Pull all embedded metadata from any supported file |
| **Batch Extract** | Process an entire folder at once |
| **Strip Metadata** | Remove all metadata — creates a clean copy, never modifies originals |
| **Batch Strip** | Sanitize an entire folder |
| **Export Reports** | Save findings as JSON, CSV, or plain TXT |
| **Privacy Risk Flags** | GPS coordinates and PII fields are highlighted automatically |

---

## Use Cases

- **OSINT / Reconnaissance** — Extract metadata from collected files to identify devices, authors, and locations
- **Digital Forensics** — Batch-analyze evidence folders for timestamp and device trails
- **Privacy Hardening** — Strip metadata before sharing sensitive files publicly
- **CTF Challenges** — Quickly inspect challenge files for hidden metadata clues

---

## Safety

MetaHunter **never modifies your original files**. When stripping metadata, a clean copy is created in `MetaHunter_Reports/`. Your originals are always preserved.

---

## Requirements

- Kali Linux (or any Debian-based distro)
- Python 3.8+
- exiftool (`sudo apt install libimage-exiftool-perl`)
- rich (`pip install rich`)

---

## Legal

This tool is intended for legal security research, digital forensics, and personal privacy protection. Only use it on files you own or have explicit authorization to analyze.
