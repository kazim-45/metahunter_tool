#!/bin/bash
# ============================================================
#   MetaHunter — Installer for Kali Linux
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
DIM='\033[2m'
NC='\033[0m'

echo ""
echo -e "${CYAN}  MetaHunter — Installer${NC}"
echo -e "${DIM}  Cybersecurity Metadata Tool for Kali Linux${NC}"
echo ""

# ── Check Python ────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[✗] Python 3 not found. Install it with: sudo apt install python3${NC}"
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}[✓] Python ${PY_VERSION} found${NC}"

# ── Install exiftool ─────────────────────────────────────────
if command -v exiftool &>/dev/null; then
    echo -e "${GREEN}[✓] exiftool already installed${NC}"
else
    echo -e "${YELLOW}[→] Installing exiftool...${NC}"
    sudo apt-get install -y libimage-exiftool-perl -q
    if command -v exiftool &>/dev/null; then
        echo -e "${GREEN}[✓] exiftool installed${NC}"
    else
        echo -e "${RED}[✗] exiftool install failed. Try manually: sudo apt install libimage-exiftool-perl${NC}"
    fi
fi

# ── Install mat2 (optional) ──────────────────────────────────
if command -v mat2 &>/dev/null; then
    echo -e "${GREEN}[✓] mat2 already installed (optional)${NC}"
else
    echo -e "${YELLOW}[→] Installing mat2 (optional metadata stripper)...${NC}"
    sudo apt-get install -y mat2 -q 2>/dev/null
    if command -v mat2 &>/dev/null; then
        echo -e "${GREEN}[✓] mat2 installed${NC}"
    else
        echo -e "${DIM}[○] mat2 not available — skipping (tool will still work)${NC}"
    fi
fi

# ── Install Python deps ──────────────────────────────────────
echo -e "${YELLOW}[→] Installing Python dependencies...${NC}"
pip install -r requirements.txt -q --break-system-packages 2>/dev/null || pip install -r requirements.txt -q
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[✓] Python packages installed${NC}"
else
    echo -e "${RED}[✗] pip install failed. Try: pip install rich${NC}"
fi

# ── Make executable ──────────────────────────────────────────
chmod +x metahunter.py
echo -e "${GREEN}[✓] metahunter.py is now executable${NC}"

# ── Optional: Add to PATH ────────────────────────────────────
echo ""
echo -e "${YELLOW}[?] Add 'metahunter' command globally? (y/n)${NC}"
read -r ADD_PATH
if [[ "$ADD_PATH" =~ ^[Yy]$ ]]; then
    INSTALL_DIR="/usr/local/bin"
    sudo cp metahunter.py "$INSTALL_DIR/metahunter"
    sudo chmod +x "$INSTALL_DIR/metahunter"
    echo -e "${GREEN}[✓] Installed globally — you can now run: metahunter${NC}"
else
    echo -e "${DIM}[○] Skipped global install — run with: python3 metahunter.py${NC}"
fi

echo ""
echo -e "${GREEN}  ✓ Installation complete!${NC}"
echo ""
echo -e "  Run with: ${CYAN}python3 metahunter.py${NC}"
if [[ "$ADD_PATH" =~ ^[Yy]$ ]]; then
    echo -e "  Or:        ${CYAN}metahunter${NC}"
fi
echo ""
